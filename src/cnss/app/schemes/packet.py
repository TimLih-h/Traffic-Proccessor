from pydantic import BaseModel


class Packet(BaseModel):
    timestamp: str
    total_packets: int
    total_bytes: int
    packets_per_second: int
    bytes_per_second: int
    tcp_packets: int
    upd_packets: int
    icmp_packets: int
    other_packets: int
    status: str
