# ADR-001: Use Asynchronous HTTP Communication Between TP and CNSS

## Status

**Accepted**

## Date

2026-06-30

## Context

The Traffic Processor (TP) captures network packets, computes statistics, and sends them to the CNSS for storage and visualization. The communication between TP and CNSS must be reliable, fast, and non-blocking to ensure real-time dashboard updates.

### Quality Requirements Addressed

- **QR-001:** Dashboard metric update delay ≤1 second
- **QR-003:** Traffic Processor throughput capacity ≥1000 Kbps

### Alternatives Considered

1. **Synchronous blocking HTTP** — Simple to implement but could block packet capture if the CNSS is slow or unreachable.
2. **Message queue (e.g., RabbitMQ, Redis)** — More reliable and decoupled, but adds operational complexity.
3. **gRPC** — Faster and more efficient, but adds complexity and requires schema definitions.
4. **UDP datagrams** — Fast and lightweight, but lacks reliability and error handling.

## Decision

Use **asynchronous HTTP communication** with the following characteristics:

- TP sends statistics via HTTP POST using Python's `urllib` with a short timeout (0.5 seconds).
- TP runs the HTTP sender in a separate daemon thread, so packet capture continues even if the CNSS is unreachable.
- The CNSS responds with HTTP 200 OK upon successful receipt and validation.
- The TP logs failures but does not retry, to avoid blocking the capture loop.

## Consequences

### Positive

- **Non-blocking packet capture:** The sender thread runs independently, so packet capture is not delayed by network I/O.
- **Simple implementation:** Uses standard library (`urllib`) with no additional dependencies.
- **Low latency:** The 0.5-second timeout ensures the sender does not block for long, supporting QR-001.
- **Easy debugging:** HTTP is human-readable and can be inspected with tools like `curl` or browser dev tools.

### Negative

- **No guaranteed delivery:** If the CNSS is down, statistics are lost. The system is designed for real-time visibility, not historical accuracy.
- **No retry mechanism:** Failures are logged but not retried. This could lead to gaps in the dashboard during transient network issues.
- **Single endpoint:** All statistics are sent to a single URL. Future load balancing would require changes.

### Trade-offs

- **Simplicity vs. Reliability:** We prioritized simplicity and low latency over reliable delivery. For a real-time monitoring tool, missing a few batches is acceptable if the dashboard updates quickly.
- **Threading complexity:** The sender thread adds concurrency. Care must be taken to ensure thread-safe access to shared statistics (currently protected by the GIL, but future refactoring should consider locks).

## Related ADRs

- [ADR-002](ADR-002-in-memory-storage.md) — In-memory storage ensures the CNSS can respond quickly to POST requests.

## References

- [docs/quality-requirements.md](../../quality-requirements.md) — QR-001, QR-003
- `src/Traffic_Processor/tproc.py` — Implementation of HTTP sender
