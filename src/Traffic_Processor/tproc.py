import time
import json
import argparse
import threading
import netifaces
import socket
import os
from datetime import datetime
from collections import defaultdict
from scapy.all import sniff, TCP, UDP, ICMP, IP, Ether
from urllib import request, error


class IPTracker:
    """Tracks per-IP statistics with a rolling window. Thread-safe with RLock."""

    def __init__(self, window_seconds=60, max_ips=1000, ignore_ips=None):
        self.window = window_seconds
        self.max_ips = max_ips
        self.data = {}
        self.lock = threading.RLock()
        self.ignore_ips = set(ignore_ips) if ignore_ips else set()

    def update(self, src_ip, dst_ip, size, proto, sport=None, dport=None):
        """Update statistics for a single packet."""
        now = time.time()
        with self.lock:
            self._update_single_ip(src_ip, size, "outgoing", proto, sport, dport, now)
            self._update_single_ip(dst_ip, size, "incoming", proto, sport, dport, now)

    def _update_single_ip(self, ip, size, direction, proto, sport, dport, now):
        """Update a single IP entry."""
        if ip in self.ignore_ips:
            return
        if ip not in self.data:
            self.data[ip] = {
                "total_packets": 0,
                "total_bytes": 0,
                "incoming": 0,
                "outgoing": 0,
                "protocols": defaultdict(int),
                "ports": defaultdict(int),
                "last_seen": now,
                "timeline": []  # (timestamp, count)
            }
        entry = self.data[ip]
        entry["total_packets"] += 1
        entry["total_bytes"] += size
        entry["last_seen"] = now
        entry[direction] += 1
        entry["protocols"][proto] += 1

        if proto in ("TCP", "UDP"):
            if direction == "incoming" and dport:
                entry["ports"][dport] += 1
            elif direction == "outgoing" and sport:
                entry["ports"][sport] += 1

        second_key = int(now)
        if entry["timeline"] and int(entry["timeline"][-1][0]) == second_key:
            entry["timeline"][-1] = (second_key, entry["timeline"][-1][1] + 1)
        else:
            entry["timeline"].append((second_key, 1))

        cutoff = int(now - self.window)
        entry["timeline"] = [(t, c) for t, c in entry["timeline"] if t >= cutoff]

    def clean_old_entries(self):
        """Remove IPs that have been inactive for more than window_seconds."""
        now = time.time()
        with self.lock:
            expired = [ip for ip, stats in self.data.items() if now - stats["last_seen"] > self.window]
            for ip in expired:
                del self.data[ip]

    def get_top_ips(self, limit=20):
        """Return the top N IPs by total_packets."""
        now = time.time()
        with self.lock:
            cutoff = int(now - self.window)
            for ip, stats in self.data.items():
                stats["timeline"] = [(t, c) for t, c in stats["timeline"] if t >= cutoff]

            sorted_ips = sorted(
                self.data.items(),
                key=lambda x: x[1]["total_packets"],
                reverse=True
            )[:limit]

            result = []
            for ip, stats in sorted_ips:
                total = sum(c for _, c in stats["timeline"])
                if stats["timeline"]:
                    first_time = stats["timeline"][0][0]
                    last_time = stats["timeline"][-1][0]
                    duration = max(last_time - first_time, 1)
                    pps = total / duration if duration > 0 else total
                else:
                    pps = 0

                top_ports = sorted(stats["ports"].items(), key=lambda x: x[1], reverse=True)[:5]
                result.append({
                    "ip": ip,
                    "total_packets": stats["total_packets"],
                    "total_bytes": stats["total_bytes"],
                    "incoming": stats["incoming"],
                    "outgoing": stats["outgoing"],
                    "pps": round(pps, 2),
                    "protocols": dict(stats["protocols"]),
                    "top_ports": [{"port": p, "count": c} for p, c in top_ports],
                    "last_seen": int(stats["last_seen"]),
                })
            return result



class TrafficProcessor:
    def __init__(self, interface=None, output_url=None, delay=None):
        # Read from environment if not provided explicitly
        self.interface = interface or os.environ.get("INTERFACE", "eth0")
        self.output_url = output_url or os.environ.get("CNSS_URL", "http://cnss:8080/load")
        self.delay = float(delay or os.environ.get("DELAY", "1"))

        # Global counters
        self.packet_cnt = 0
        self.bytes_cnt = 0
        self.tcp_cnt = 0
        self.udp_cnt = 0
        self.icmp_cnt = 0
        self.other_cnt = 0
        self.incoming_packets = 0
        self.outgoing_packets = 0
        self.incoming_bytes = 0
        self.outgoing_bytes = 0

        self.last_packet_cnt = 0
        self.last_bytes_cnt = 0
        self.last_update_time = time.time()

        # Resolve CNSS IP (for informational purposes)
        self.cnss_ip = None
        cnss_hostname = os.environ.get("CNSS_HOSTNAME", "cnss")
        try:
            self.cnss_ip = socket.gethostbyname(cnss_hostname)
            print(f"[TP] Resolved CNSS hostname '{cnss_hostname}' -> {self.cnss_ip}")
        except socket.gaierror:
            self.cnss_ip = os.environ.get("CNSS_IP")
            if self.cnss_ip:
                print(f"[TP] Using CNSS_IP from environment: {self.cnss_ip}")
            else:
                print("[TP] WARNING: CNSS IP not resolved – monitoring traffic may slip through.")

        # Resolve target IP (if any) – used for BPF filter
        self.target_ip = None
        target_hostname = os.environ.get("TARGET_HOSTNAME")
        if target_hostname:
            try:
                self.target_ip = socket.gethostbyname(target_hostname)
                print(f"[TP] Resolved target hostname '{target_hostname}' -> {self.target_ip}")
            except socket.gaierror:
                self.target_ip = os.environ.get("TARGET_IP")
                if self.target_ip:
                    print(f"[TP] Using TARGET_IP from environment: {self.target_ip}")
                else:
                    print("[TP] WARNING: target IP not resolved – outgoing counts will be incorrect.")

        self.ip_tracker = IPTracker(window_seconds=60, max_ips=1000)
        self.running = False
        self.sender_thread = None
        self.cleanup_thread = None

        print(f"[TP] Output url: {self.output_url}")
        print(f"[TP] Interface: {self.interface}")
        print(f"[TP] Delay: {self.delay}s")

    def packet_handler(self, packet):
        try:
            if not packet.haslayer(IP):
                return
            ip_layer = packet[IP]
            src_ip = ip_layer.src
            dst_ip = ip_layer.dst

            self.packet_cnt += 1
            self.bytes_cnt += len(packet)

            proto = "Other"
            sport = None
            dport = None
            if packet.haslayer(TCP):
                proto = "TCP"
                self.tcp_cnt += 1
                sport = packet[TCP].sport
                dport = packet[TCP].dport
            elif packet.haslayer(UDP):
                proto = "UDP"
                self.udp_cnt += 1
                sport = packet[UDP].sport
                dport = packet[UDP].dport
            elif packet.haslayer(ICMP):
                proto = "ICMP"
                self.icmp_cnt += 1
            else:
                self.other_cnt += 1

            if self.target_ip:
                if ip_layer.src == self.target_ip:
                    self.outgoing_packets += 1
                    self.outgoing_bytes += len(packet)
                elif ip_layer.dst == self.target_ip:
                    self.incoming_packets += 1
                    self.incoming_bytes += len(packet)

            self.ip_tracker.update(
                src_ip=src_ip,
                dst_ip=dst_ip,
                size=len(packet),
                proto=proto,
                sport=sport,
                dport=dport
            )
        except Exception as e:
            print(f"[TP] Error processing packet: {e}")

    def get_stats(self):
        current_time = time.time()
        elapsed = current_time - self.last_update_time
        pps = (self.packet_cnt - self.last_packet_cnt) / elapsed if elapsed > 0 else 0
        bps = (self.bytes_cnt - self.last_bytes_cnt) / elapsed if elapsed > 0 else 0

        self.last_packet_cnt = self.packet_cnt
        self.last_bytes_cnt = self.bytes_cnt
        self.last_update_time = current_time

        top_ips = self.ip_tracker.get_top_ips(limit=20)

        return {
            "timestamp": datetime.now().isoformat(),
            "total_packets": self.packet_cnt,
            "total_bytes": self.bytes_cnt,
            "incoming_packets": self.incoming_packets,
            "outgoing_packets": self.outgoing_packets,
            "incoming_bytes": self.incoming_bytes,
            "outgoing_bytes": self.outgoing_bytes,
            "packets_per_second": round(pps, 2),
            "bytes_per_second": round(bps, 2),
            "tcp_packets": self.tcp_cnt,
            "udp_packets": self.udp_cnt,
            "icmp_packets": self.icmp_cnt,
            "other_packets": self.other_cnt,
            "top_ips": top_ips,
            "status": "online"
        }

    def post_json(self) -> tuple[int, str]:
        stats = self.get_stats()
        data = json.dumps(stats).encode("utf-8")
        req = request.Request(
            self.output_url,
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        try:
            with request.urlopen(req, timeout=1) as resp:
                body = resp.read().decode("utf-8", errors="replace")
                return resp.getcode(), body
        except error.HTTPError as he:
            try:
                body = he.read().decode("utf-8", errors="replace")
            except Exception:
                body = ""
            return he.code, body
        except Exception:
            raise

    def send_stats(self):
        try:
            status, body = self.post_json()
        except Exception:
            status = None
        if status is not None and 200 <= status < 300:
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Sent batch (status {status})")
        else:
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Failed to send batch: status={status}")

    def cleanup_loop(self):
        while self.running:
            time.sleep(10)
            self.ip_tracker.clean_old_entries()

    def sender_loop(self):
        print("[TP] Sender thread started")
        while self.running:
            self.send_stats()
            time.sleep(self.delay)

    def start(self):
        if self.running:
            print("[TP] Already running")
            return
        self.running = True

        self.sender_thread = threading.Thread(target=self.sender_loop)
        self.sender_thread.daemon = True
        self.sender_thread.start()

        self.cleanup_thread = threading.Thread(target=self.cleanup_loop)
        self.cleanup_thread.daemon = True
        self.cleanup_thread.start()

        print(f"[TP] Starting packet capture on {self.interface}...")
        print("[TP] Press Ctrl+C to stop")

        bpf_filter = None
        if self.target_ip:
            bpf_filter = f"host {self.target_ip}"
            print(f"[TP] Using BPF filter: {bpf_filter}")
        else:
            bpf_filter = "not arp and not port 53 and not port 5353 and not port 8080"
            print(f"[TP] Warning: target IP unknown. Using generic noise filter: {bpf_filter}")

        try:
            sniff(iface=self.interface, prn=self.packet_handler, store=False, filter=bpf_filter)
        except KeyboardInterrupt:
            print("\n[TP] Stopping...")
        finally:
            self.stop()

    def stop(self):
        self.running = False
        if self.sender_thread and self.sender_thread.is_alive():
            self.sender_thread.join(timeout=2)
        if self.cleanup_thread and self.cleanup_thread.is_alive():
            self.cleanup_thread.join(timeout=2)
        self.send_stats()
        print("[TP] Stopped")


def main():
    parser = argparse.ArgumentParser(description="Traffic Processor – standalone packet sniffer")
    parser.add_argument(
        "-i", "--interface",
        type=str,
        help="Network interface to capture from (default: eth0, or INTERFACE env)"
    )
    parser.add_argument(
        "-u", "--url",
        type=str,
        help="HTTP endpoint URL to POST batches to (default: http://cnss:38080/load, or CNSS_URL env)"
    )
    parser.add_argument(
        "-d", "--delay",
        type=float,
        help="Delay in seconds between POST batches (default: 0.5, or DELAY env)"
    )
    args = parser.parse_args()

    tp = TrafficProcessor(
        interface=args.interface,
        output_url=args.url,
        delay=args.delay
    )
    tp.start()


if __name__ == "__main__":
    main()