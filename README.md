# Traffic Processor (TP)

[![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)](CHANGELOG.md)
[![Docker](https://img.shields.io/badge/docker-ready-2496ED?logo=docker)](https://www.docker.com/)
[![License](https://img.shields.io/github/license/SWP-Team-46/Traffic-Proccessor)](LICENSE)

**Traffic Processor** is a network visibility and control tool that captures live packet counters, per‑connection statistics, and traffic history, while supporting blocking, tunneling, and failover behaviours.

---

## Access the Product

The easiest way to try the current version is to run the fully containerised stack:

Install [docker desktop](https://www.docker.com/products/docker-desktop/)

```bash
git clone https://github.com/SWP-Team-46/Traffic-Proccessor
cd Traffic-Proccessor/src
```

From the `src` directory:

```bash
docker compose up --build
```

This starts CNSS and PostgreSQL. The dashboard is available at http://localhost:38080.

To run Traffic Proccessor:
```bash
make build
$resultId = docker ps --filter "name=???" --format "{{.ID}}" 
 >> docker run --rm `
 >>   --network container:$resultId `
 >>   --cap-add=NET_ADMIN `
 >>   --cap-add=NET_RAW `
 >>   -e CNSS_URL="http://host.docker.internal:38080/load" `
 >>   -e INTERFACE="???" `
 >>   -e TARGET_HOSTNAME="???" `
 >>   traffic-processor:latest
```

TProc can be configured via environment variables:
- `INTERFACE` – network interface to capture from (default: `eth0`)
- `CNSS_URL` – CNSS endpoint URL (default: `http://cnss:38080/load`)
- `DELAY` – interval between data pushes in seconds (default: `1`)

Once running, open the **web dashboard** at  
**[http://localhost:8080/static/index.html](http://localhost:8080/static/index.html)**

For programmatic access, use the CNSS API endpoints (`POST /load`, `GET /packets`, `POST /reset`).



---

## Documentation

All maintained documentation lives in the [`docs/`](docs) folder:

| Document | Purpose |
|----------|---------|
| **[Architecture Overview](docs/architecture)** | System components, static/dynamic/deployment views, and key architectural decisions (ADRs) |
| **[Testing & Quality](docs/testing.md)** | Test strategy, coverage expectations, and quality automation |
| **[Roadmap](docs/roadmap.md)** | Planned features and future direction |
| **[User Acceptance Tests](docs/user-acceptance-tests.md)** | UAT scenarios and sign‑off criteria |

---

## Handover Guidance

For the current product state, handover scope, and customer‑facing instructions, see the **[Customer Handover document](docs/customer-handover.md)**.

---

## Contributing & Agent Workflow

- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Practical steps for setting up, branching, opening PRs, and meeting review requirements.
- **[AGENTS.md](AGENTS.md)** - Actionable setup, build, test, and safety instructions for coding agents.

---

## Repository Structure

.\
├── src/               # Application source code (TProc, CNSS, Gate, Error Server)\
├── docs/              # Maintained documentation (architecture, testing, handover, etc.)\
├── reports/           # Project reports and status updates\
├── .github/           # CI workflows and issue/PR templates\
├── AGENTS.md          # Agent‑focused setup and workflow guide\
├── CONTRIBUTING.md    # Contribution process and review expectations\
├── CHANGELOG.md       # Version history\
└── LICENSE            # Project license

---

## License

This project is licensed under the terms in the [LICENSE](LICENSE) file.

---

*For any questions or handover‑related inquiries, please refer to the [Customer Handover document](docs/customer-handover.md) or open an issue in this repository.*
