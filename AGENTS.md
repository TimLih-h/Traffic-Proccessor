# AGENTS.md – Traffic Processor (TP)

This file is the maintained public guide for coding agents working in the Traffic Processor repository. It focuses on actionable setup, workflow, and safety instructions. For human‑oriented onboarding, see [README.md](./README.md). For detailed team processes, see [docs/development-process.md](./docs/development-process.md).

---

## 1. Setup, Build, Test, and Verification Commands

All development is containerised with **Docker** and **Docker Compose**. No system‑wide dependencies beyond Docker are required.

### 1.1 Quick Start
```bash
# Clone the repository
git clone https://github.com/SWP-Team-46/Traffic-Proccessor.git
cd Traffic-Proccessor/src

# Build and start all services (TP, CNSS, PostgreSQL, etc.)
docker compose up --build
```

### 1.2 Verify That the Traffic Processor Is Running
```bash
docker exec tproc cat /data/data.txt | head -3
```

### 1.3 Run Linters and Tests (CI‑aligned)

The CI pipeline uses flake8 for syntax checking and pytest for unit tests. Run them locally to catch issues before opening a PR:
```bash
# Install Python dependencies (if not using Docker)
pip install netifaces scapy pytest pytest-cov requests flake8

# Lint (syntax‑only checks)
flake8 src/ --count --select=E9,F63,F7,F82 --show-source --statistics

# Run tests with coverage
pytest src/ --cov=src/ --cov-report=xml --cov-report=html --maxfail=1 --disable-warnings -v
```

### 1.4 Build and Smoke‑Test the Docker Images
```bash
cd src
docker compose build
docker compose up -d
# Wait a few seconds for services to initialise, then check that all expected containers are running
docker ps --filter "status=running" --format "table {{.Names}}" | grep -E "tproc|cnss|cn|postgres"
docker compose down
```

## 2. Repository Workflow and Review Expectations

We follow a **modified GitHub Flow** with a long‑lived `main` branch. All changes are submitted via Pull Requests (PRs). The canonical workflow is documented in [`docs/development-process.md`](./docs/development-process.md); the key points for agents are:

- **Branch naming**: `feature/<issue-id>-short-description`, `bugfix/...`, `hotfix/...`, `chore/...`, or `docs/...`.
- **Pull Requests**:
  - Must link to at least one GitHub Issue.
  - Must use the PR template (automatically provided).
  - Require **at least one approval** from a team member other than the author.
  - Must pass all CI checks (linting, tests, Docker build, smoke test).
- **Merging**: Use **“Squash and merge”** to keep history clean, unless the PR is a release or hotfix where preserving individual commits is justified.
- **Definition of Done**: An issue is done when all acceptance criteria are met, the PR is approved, CI is green, the PR is merged, and the issue is closed (see [`docs/definition-of-done.md`](./docs/definition-of-done.md)).

---

## 3. Sensitive Data, Credentials, Privacy, and Safety Cautions

This tool captures live network traffic and connection statistics. Handle it with care.

- **Never commit secrets** – credentials, tokens, or private keys must **never** appear in the repository.
- **Use `.env` files for local development** – they are listed in `.gitignore` and are not pushed.
- **GitHub Secrets** are used for CI/CD (e.g., access tokens, deployment keys). Do not expose them in logs or output.
- **Network traffic** – the Traffic Processor captures packet counters and per‑connection data. Be mindful of privacy regulations (e.g., GDPR) when processing real user traffic.
- **Permissions** – running the scanner may require elevated privileges (e.g., `sudo` or `CAP_NET_RAW`). Ensure you have the necessary authorisation before executing the tool in a production or shared environment.

---

## 4. Links to Deeper Maintained Documentation

The following documents provide additional context and are kept up‑to‑date by the team:

| Document | Description |
|----------|-------------|
| [README.md](./README.md) | Project overview, quick start, and basic usage. |
| [docs/development-process.md](./docs/development-process.md) | **Canonical** development workflow, branching strategy, PR process, CI/CD, and secrets management. |
| [docs/quality-requirements.md](./docs/quality-requirements.md) | Quality standards, coding guidelines, and non‑functional requirements. |
| [docs/quality-requirements-tests.md](./docs/quality-requirements-tests.md) | Testing strategy, coverage expectations, and test organisation. |
| [docs/definition-of-done.md](./docs/definition-of-done.md) | Detailed Definition of Done for issues and PRs. |
| [docs/roadmap.md](./docs/roadmap.md) | High‑level project roadmap and upcoming milestones. |
| [CHANGELOG.md](./CHANGELOG.md) | Release notes and version history. |

For any process‑related questions not covered here, refer first to [`docs/development-process.md`](./docs/development-process.md) – it is the source of truth for the team’s current workflow.

---

*This AGENTS.md is maintained alongside the repository and updated whenever the setup, workflow, or safety constraints change.*
