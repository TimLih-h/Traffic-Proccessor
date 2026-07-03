from typing import List, Dict, Any
from pydantic import BaseModel, Field


# --- Nested models ---

class PortCount(BaseModel):
    """Represents traffic statistics for a single port."""
    port: int
    count: int

    def __add__(self, other: Any) -> 'PortCount':
        """Sum port counters. Ports must match."""
        if not isinstance(other, PortCount):
            return NotImplemented
        if self.port != other.port:
            raise ValueError("Cannot add ports with different numbers")
        return PortCount(port=self.port, count=self.count + other.count)

    def __sub__(self, other: Any) -> 'PortCount':
        """Subtract port counters. Ports must match."""
        if not isinstance(other, PortCount):
            return NotImplemented
        if self.port != other.port:
            raise ValueError("Cannot subtract ports with different numbers")
        return PortCount(port=self.port, count=self.count - other.count)


class IpStats(BaseModel):
    """Traffic statistics aggregated per IP address."""
    ip: str
    total_packets: int
    total_bytes: int
    incoming: int
    outgoing: int
    pps: float
    protocols: Dict[str, int]
    top_ports: List[PortCount]
    last_seen: int

    def _merge_ports(self, other_ports: List[PortCount], operation: str) -> List[PortCount]:
        """
        Helper to add or subtract port lists.
        Merges by port number and sorts descending by count to preserve 'top' semantics.
        """
        port_dict = {p.port: p.count for p in self.top_ports}

        for p in other_ports:
            if operation == 'add':
                port_dict[p.port] = port_dict.get(p.port, 0) + p.count
            else:
                port_dict[p.port] = port_dict.get(p.port, 0) - p.count

        # Sort descending by count to keep the "top-N" meaning
        sorted_ports = sorted(port_dict.items(), key=lambda x: x[1], reverse=True)
        return [PortCount(port=port, count=count) for port, count in sorted_ports]

    def __add__(self, other: Any) -> 'IpStats':
        """Combine stats for the same IP."""
        if not isinstance(other, IpStats):
            return NotImplemented
        if self.ip != other.ip:
            raise ValueError("Cannot add stats for different IPs")

        # Merge protocol dictionaries
        protocols = dict(self.protocols)
        for proto, count in other.protocols.items():
            protocols[proto] = protocols.get(proto, 0) + count

        return IpStats(
            ip=self.ip,
            total_packets=self.total_packets + other.total_packets,
            total_bytes=self.total_bytes + other.total_bytes,
            incoming=self.incoming + other.incoming,
            outgoing=self.outgoing + other.outgoing,
            pps=self.pps + other.pps,
            protocols=protocols,
            top_ports=self._merge_ports(other.top_ports, 'add'),
            last_seen=max(self.last_seen, other.last_seen)
        )

    def __sub__(self, other: Any) -> 'IpStats':
        """Compute delta between two IP stats snapshots."""
        if not isinstance(other, IpStats):
            return NotImplemented
        if self.ip != other.ip:
            raise ValueError("Cannot subtract stats for different IPs")

        protocols = dict(self.protocols)
        for proto, count in other.protocols.items():
            protocols[proto] = protocols.get(proto, 0) - count

        return IpStats(
            ip=self.ip,
            total_packets=self.total_packets - other.total_packets,
            total_bytes=self.total_bytes - other.total_bytes,
            incoming=self.incoming - other.incoming,
            outgoing=self.outgoing - other.outgoing,
            pps=self.pps - other.pps,
            protocols=protocols,
            top_ports=self._merge_ports(other.top_ports, 'sub'),
            last_seen=min(self.last_seen, other.last_seen)
        )


# --- Root model ---

class NetworkStats(BaseModel):
    """
    Network traffic snapshot.
    Supports addition (merging stats from multiple sources)
    and subtraction (computing deltas between two snapshots).
    """
    timestamp: str
    total_packets: int
    total_bytes: int
    incoming_packets: int
    outgoing_packets: int
    incoming_bytes: int
    outgoing_bytes: int
    packets_per_second: float
    bytes_per_second: float
    tcp_packets: int
    udp_packets: int
    icmp_packets: int
    other_packets: int
    top_ips: List[IpStats]
    status: str

    def _merge_ips(self, other_ips: List[IpStats], operation: str) -> List[IpStats]:
        """
        Merge two lists of IP stats by IP address.
        - On addition: missing IPs are added as-is.
        - On subtraction: missing IPs produce negative deltas (treated as zero baseline).
        Result is sorted descending by total_packets (absolute value for subtraction).
        """
        ip_dict = {ip_stat.ip: ip_stat for ip_stat in self.top_ips}

        for other_ip_stat in other_ips:
            ip = other_ip_stat.ip
            if ip in ip_dict:
                if operation == 'add':
                    ip_dict[ip] = ip_dict[ip] + other_ip_stat
                else:
                    ip_dict[ip] = ip_dict[ip] - other_ip_stat
            else:
                # IP exists only in 'other'.
                # For addition: include it directly.
                # For subtraction: treat self-side as zeros and subtract.
                if operation == 'add':
                    ip_dict[ip] = other_ip_stat
                else:
                    # Build a zeroed-out copy with the same structure
                    zero_ip = other_ip_stat.model_copy(
                        update={k: 0 for k in other_ip_stat.model_fields
                                if k not in ['ip', 'protocols', 'top_ports']}
                    )
                    zero_ip.protocols = {k: 0 for k in other_ip_stat.protocols}
                    zero_ip.top_ports = [PortCount(port=p.port, count=0)
                                         for p in other_ip_stat.top_ports]
                    ip_dict[ip] = zero_ip - other_ip_stat

        # Sort descending. Use abs() for subtraction so largest deltas appear on top.
        sorted_ips = sorted(
            ip_dict.values(),
            key=lambda x: abs(x.total_packets) if operation == 'sub' else x.total_packets,
            reverse=True
        )
        return sorted_ips

    def __add__(self, other: Any) -> 'NetworkStats':
        """Merge two network snapshots (e.g., from two routers)."""
        if not isinstance(other, NetworkStats):
            return NotImplemented

        return NetworkStats(
            timestamp=max(self.timestamp, other.timestamp),  # Latest timestamp wins
            total_packets=self.total_packets + other.total_packets,
            total_bytes=self.total_bytes + other.total_bytes,
            incoming_packets=self.incoming_packets + other.incoming_packets,
            outgoing_packets=self.outgoing_packets + other.outgoing_packets,
            incoming_bytes=self.incoming_bytes + other.incoming_bytes,
            outgoing_bytes=self.outgoing_bytes + other.outgoing_bytes,
            packets_per_second=self.packets_per_second + other.packets_per_second,
            bytes_per_second=self.bytes_per_second + other.bytes_per_second,
            tcp_packets=self.tcp_packets + other.tcp_packets,
            udp_packets=self.udp_packets + other.udp_packets,
            icmp_packets=self.icmp_packets + other.icmp_packets,
            other_packets=self.other_packets + other.other_packets,
            top_ips=self._merge_ips(other.top_ips, 'add'),
            status="online" if self.status == "online" or other.status == "online" else self.status
        )

    def __sub__(self, other: Any) -> 'NetworkStats':
        """Compute delta between two snapshots (e.g., counters over a time interval)."""
        if not isinstance(other, NetworkStats):
            return NotImplemented

        return NetworkStats(
            timestamp=min(self.timestamp, other.timestamp),  # Earliest timestamp for the delta
            total_packets=self.total_packets - other.total_packets,
            total_bytes=self.total_bytes - other.total_bytes,
            incoming_packets=self.incoming_packets - other.incoming_packets,
            outgoing_packets=self.outgoing_packets - other.outgoing_packets,
            incoming_bytes=self.incoming_bytes - other.incoming_bytes,
            outgoing_bytes=self.outgoing_bytes - other.outgoing_bytes,
            packets_per_second=self.packets_per_second - other.packets_per_second,
            bytes_per_second=self.bytes_per_second - other.bytes_per_second,
            tcp_packets=self.tcp_packets - other.tcp_packets,
            udp_packets=self.udp_packets - other.udp_packets,
            icmp_packets=self.icmp_packets - other.icmp_packets,
            other_packets=self.other_packets - other.other_packets,
            top_ips=self._merge_ips(other.top_ips, 'sub'),
            status=self.status  # Keep status from the minuend
        )