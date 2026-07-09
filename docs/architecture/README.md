# Traffic Processor Architecture

This document describes the architecture of the Traffic Processor (TP) system as implemented in the `dev` branch.

## Overview

Traffic Processor is a network visibility and control tool that captures live packet counters, per-connection statistics, and traffic history, and supports blocking, tunneling, and failover behaviors.

The system consists of six main components:

| Component | Description | Technology |
|-----------|-------------|------------|
| **TProc** | Packet sniffer that captures traffic, classifies packets, computes per-IP statistics, and sends data to CNSS. | Python, Scapy |
| **Gate** | Reverse proxy with IP-based filtering. Blocks suspicious IPs and forwards allowed requests to the mock target. | Python HTTP Server |
| **Mock Target** | A protected application served behind the gate. | Flask |
| **Error Server** | Serves a dedicated access-denied page for blocked IPs. | Flask |
| **CNSS** | Control and Status Server – receives statistics, serves the web dashboard, and supports reset functionality. | FastAPI, PostgreSQL |
| **PostgreSQL** | Persistent storage for CNSS data. | PostgreSQL 14.8 |

## Architecture Views

### Static View

The static view describes the system's component structure, interfaces, and relationships.

- **Diagram:** [component-diagram.puml](static-view/component-diagram.puml)
- **Rendered form:**
  ![component-diagram.svg](static-view/component-diagram.svg)

### Dynamic View

The dynamic view describes key runtime interactions and workflows, including packet capture, statistics transmission, dashboard refresh, and protected access via the gate.

- **Diagram:** [sequence-diagram.puml](dynamic-view/sequence-diagram.puml)
- **Rendered form:**
  ![sequence-diagram.svg](dynamic-view/sequence-diagram.svg)

### Deployment View

The deployment view describes the runtime deployment structure using Docker Compose with six containers.

- **Diagram:** [deployment-diagram.puml](deployment-view/deployment-diagram.puml)
- **Rendered form:**
  ![deployment-diagram.svg](deployment-view/deployment-diagram.svg)

## Key Architectural Decisions (ADRs)

| ADR | Title | Status |
|-----|-------|--------|
| ADR-001 | Asynchronous HTTP Communication Between TP and CNSS | Implemented |
| ADR-002 | PostgreSQL for Persistent Storage | Implemented |
| ADR-003 | Scapy as Packet Capture Library | Implemented |
| ADR-004 | Gate as Reverse Proxy with IP Filtering | Implemented |
| ADR-005 | Docker Compose for Multi-Service Orchestration | Implemented |

## Running the System

From the `src` directory:

```bash
docker compose up --build
```

This starts all six services. The dashboard is available at `http://localhost:8080`, and the protected target is accessible via the gate at `http://localhost:8000`.


---

## Summary of Upgrades of sprint-3

| Aspect | before | after |
|--------|--------------|-----|
| **Components** | TP + CNSS | TProc + Gate + Mock Target + Error Server + CNSS + PostgreSQL |
| **Storage** | In-memory (PostgreSQL planned) | PostgreSQL (active) |
| **IP Filtering** | None | Gate with `BLOCKED_IPS` |
| **Error Handling** | None | Dedicated Error Server for 403 responses |
| **Network Mode** | Separate containers | TProc shares gate's network namespace |
| **Endpoints** | POST `/`, GET `/packets` | POST `/load`, GET `/packets`, POST `/reset` |
| **Persistence** | Not implemented | Alembic migrations + PostgreSQL |
| **Dashboard** | Static files | Static files + CORS middleware |
