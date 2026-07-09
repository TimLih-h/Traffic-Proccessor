# ADR-003: Scapy as Packet Capture Library

## Status

**Accepted**

## Date

2026-06-30

## Context

The Traffic Processor must capture live network packets, classify them by protocol, and determine their direction (incoming/outgoing). The choice of packet capture library affects performance, ease of use, and cross-platform compatibility.

### Quality Requirements Addressed

- **QR-002:** Traffic Processor startup time ≤500ms
- **QR-003:** Traffic Processor throughput capacity ≥1000 Kbps

### Alternatives Considered

1. **Scapy** — Feature-rich, pure Python, supports many protocols, easy to use.
2. **PyShark** — Wrapper around Wireshark/TShark, powerful but requires Wireshark installation.
3. **Raw socket with `socket` module** — Low-level, fast, but requires manual protocol parsing.
4. **libpcap via `pcap` or `pypcap`** — Fast and efficient, but lower-level and harder to use.
5. **NFQueue / Netfilter** — Linux-specific, powerful but complex.

## Decision

Use **Scapy** as the packet capture library.

- Scapy provides a high-level API for packet sniffing, protocol classification, and packet manipulation.
- The TP uses `scapy.all.sniff()` with a callback function (`prn=packet_handler`).
- Scapy automatically handles protocol dissections (TCP, UDP, ICMP, IP, Ethernet).
- The TP uses Scapy's `haslayer()` and field access (e.g., `packet[IP].src`) for classification and direction tracking.

## Consequences

### Positive

- **Ease of use:** Scapy's high-level API makes protocol classification and direction tracking trivial. The code is readable and maintainable.
- **Rapid development:** The team can quickly add support for new protocols or packet fields.
- **Cross-platform:** Scapy works on Linux, Windows, and macOS, supporting the product's target environments.
- **Rich feature set:** Scapy supports many protocols and can be extended for future needs (e.g., packet filtering, custom protocols).
- **Startup time:** Scapy imports quickly and `sniff()` starts capturing immediately, supporting QR-002 (≤500ms startup).

### Negative

- **Performance overhead:** Scapy is pure Python and may not handle very high packet rates (e.g., >1 Gbps) without dropping packets. However, it is sufficient for the target throughput of 1000 Kbps (QR-003).
- **Dependency:** Scapy is an external dependency that must be installed (`pip install scapy`). It is included in the Docker image.
- **Privileged access:** Packet capture typically requires root/administrator privileges. The Docker container must run with appropriate permissions (`--privileged` or `network_mode: host`).
- **Direction tracking limitations:** Direction tracking relies on the local IP/MAC. On the `any` interface, direction tracking is unreliable (documented in the code).

### Trade-offs

- **Performance vs. Developer Productivity:** We prioritized developer productivity and ease of use over raw performance. For the target throughput (1000 Kbps), Scapy's performance is adequate.
- **Simplicity vs. Control:** Scapy abstracts away low-level details, making the code simpler but giving less control over packet capture parameters.

## Related ADRs

- [ADR-001](ADR-001-async-http-communication.md) — The TP sends captured statistics via HTTP.
- [ADR-002](ADR-002-in-memory-storage.md) — The CNSS stores the statistics.

## References

- [docs/quality-requirements.md](../../quality-requirements.md) — QR-002, QR-003
- `src/Traffic_Processor/tproc.py` — Implementation of Scapy-based packet capture
- [Scapy Documentation](https://scapy.readthedocs.io/)
