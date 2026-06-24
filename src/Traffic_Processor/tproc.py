import time
import json
import argparse
import threading
from datetime import datetime
from urllib import request, error
from scapy.all import sniff, TCP, UDP, ICMP

class TrafficProcessor:
    def __init__(self, interface="any", output_url="http://localhost:8080", delay=0.5, retries=3):
        self.interface = interface
        self.output_url = output_url
        self.delay = delay
        self.retries = retries
        
        #Statistics
        self.packet_cnt = 0
        self.bytes_cnt = 0
        self.tcp_cnt = 0
        self.udp_cnt = 0
        self.icmp_cnt = 0
        self.other_cnt = 0
        self.last_packet_cnt = 0
        self.last_bytes_cnt = 0
        self.last_update_time = time.time()
        
        #States
        self.running = False
        self.sender_thread = None
        
        print(f"[TP] Initialized on interface: {interface}")
        print(f"[TP] Output file: {output_url}")
    
    def packet_handler(self, packet):
        self.packet_cnt += 1
        self.bytes_cnt += len(packet)
        if packet.haslayer(TCP):
            self.tcp_cnt += 1
        elif packet.haslayer(UDP):
            self.udp_cnt += 1
        elif packet.haslayer(ICMP):
            self.icmp_cnt += 1
        else:
            self.other_cnt += 1
    
    def get_stats(self):
        current_time = time.time()
        elapsed = current_time - self.last_update_time
        pps = (self.packet_cnt - self.last_packet_cnt) / elapsed if elapsed > 0 else 0
        bps = (self.bytes_cnt - self.last_bytes_cnt) / elapsed if elapsed > 0 else 0
        self.last_packet_cnt = self.packet_cnt
        self.last_bytes_cnt = self.bytes_cnt
        self.last_update_time = current_time
        
        return {
            "timestamp": datetime.now().isoformat(),
            "total_packets": self.packet_cnt,
            "total_bytes": self.bytes_cnt,
            "packets_per_second": round(pps, 2),
            "bytes_per_second": round(bps, 2),
            "tcp_packets": self.tcp_cnt,
            "udp_packets": self.udp_cnt,
            "icmp_packets": self.icmp_cnt,
            "other_packets": self.other_cnt,
            "status": "online"
        }
    
    def post_json(self) -> tuple[int, str]:
        stats = self.get_stats()
        data = json.dumps(stats).encode("utf-8")
        req = request.Request(self.output_url, data=data, headers={"Content-Type": "application/json"}, method="POST")
        try:
            with request.urlopen(req, timeout=0.5) as resp:
                body = resp.read().decode("utf-8", errors="replace")
                return resp.getcode(), body
        except error.HTTPError as he:
            # HTTP error with response body
            try:
                body = he.read().decode("utf-8", errors="replace")
            except Exception:
                body = ""
            return he.code, body
        except Exception:
            raise
    
    def send_stats(self):
        try:
            self.post_json()
        except Exception:
            return
        return
        attempt = 0
        while True:
            attempt += 1
            try:
                status, body = self.post_json()
            except Exception:
                status = None

            if status is not None and 200 <= status < 300:
                print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Sent batch -> {self.output_url} (status {status})")
                return
            else:
                print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Failed to send batch (attempt {attempt}): status={status}")
                if attempt >= self.retries:
                    print(f"Giving up after {self.retries} attempts")
                    return
                wait = 0.5 * attempt
                print(f"Retrying in {wait} seconds...")
                time.sleep(wait)
    
    def writer_loop(self):
        print("[TP] Writer thread started")
        while self.running:
            self.send_stats()
            time.sleep(self.delay)  # Update every (delay) seconds
    
    def start(self):
        if self.running:
            print("[TP] Already running")
            return
    
        self.running = True
        self.sender_thread = threading.Thread(target=self.writer_loop)
        self.sender_thread.daemon = True
        self.sender_thread.start()
        
        print(f"[TP] Starting packet capture on {self.interface}...")
        print("[TP] Press Ctrl+C to stop")
        try:
            sniff(iface=self.interface, prn=self.packet_handler, store=False)
        except KeyboardInterrupt:
            print("\n[TP] Stopping...")
        finally:
            self.stop()
    
    def stop(self):
        self.running = False
        if self.sender_thread and self.sender_thread.is_alive():
            self.sender_thread.join(timeout=2)
        self.send_stats()
        print("[TP] Stopped")


def main():
    parser = argparse.ArgumentParser(description="Simple Traffic Processor - MVP V1")
    parser.add_argument("-i", "--interface", type=str, default="any", help="Network interface to capture from (default: any)")
    parser.add_argument("-u", "--url", type=str, default="http://localhost:8080", help="HTTP endpoint URL to POST batches to")
    parser.add_argument("-d", "--delay", type=float, default=0.5, help="Delay in seconds between loop iterations (default 0.5)")
    parser.add_argument("-r", "--retries", type=int, default=3, help="Retries per batch on failure (default 3)")
    args = parser.parse_args()
    
    tp = TrafficProcessor(interface=args.interface, output_url=args.url, delay=args.delay, retries=args.retries)
    tp.start()

if __name__ == "__main__":
    main()


