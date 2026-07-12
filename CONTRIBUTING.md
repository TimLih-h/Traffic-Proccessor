# Contributing to Traffic Processor (TP)

First off, thank you for considering contributing to the Traffic Processor! This document outlines the practical steps and expectations for working with the codebase.

It complements the [README.md](./README.md) (which covers project overview and quick start) and focuses specifically on the contribution process.

---

## 1. Setup and Verification Before Submitting

All development is containerised with Docker; you don't need to install Python or dependencies globally.

### 1.1 Prerequisites
- [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/)
- [Git](https://git-scm.com/)
- A GitHub account with access to the repository

### 1.2 Local Setup
```bash
git clone https://github.com/SWP-Team-46/Traffic-Proccessor.git
cd Traffic-Proccessor/src
docker compose up --build
```

### 1.3 Verify Your Changes

Before submitting anything, ensure your changes work and don't break existing functionality:

Run the linter (syntax checks only – aligns with CI):
```bash
docker compose exec tproc flake8 src/ --count --select=E9,F63,F7,F82 --show-source --statistics
```

(Alternatively, run natively if you have Python installed: pip install flake8 && flake8 src/)

Run the test suite with coverage:
```bash
docker compose exec tproc pytest src/ --cov=src/ --cov-report=xml --cov-report=html --maxfail=1 --disable-warnings -v
```

Smoke-test the full stack:
```bash
docker compose build
docker compose up -d
docker ps --filter "status=running" --format "table {{.Names}}" | grep -E "tproc|cnss|cn|postgres"
docker compose down
```

Quick functional check (if the Traffic Processor should be capturing data):
```bash
docker exec tproc cat /data/data.txt | head -3
```

## 2. Branch and PR Workflow

We follow a **modified GitHub Flow** with a permanent `main` branch. All contributions are submitted via Pull Requests (PRs).

### 2.1 Branch Naming
Create your branch from `main` using one of these prefixes:
- `feature/<issue-id>-short-description` – for new features
- `bugfix/<issue-id>-short-description` – for bug fixes
- `hotfix/<issue-id>-short-description` – for urgent production fixes
- `chore/<issue-id>-short-description` – for maintenance (dependencies, refactoring, etc.)
- `docs/<issue-id>-short-description` – for documentation updates

Example: `feature/42-add-udp-support`

### 2.2 Opening a Pull Request
1. Push your branch to GitHub.
2. Open a PR against the `main` branch.
3. **Always link at least one GitHub Issue** – use the "Development" section in the PR sidebar or write `Closes #42` in the description.
4. Fill out the PR template (it appears automatically when you open a PR).

### 2.3 Keeping Your PR Up-to-Date
If the `main` branch advances while your PR is open, rebase your branch onto the latest `main` (or merge `main` into your branch) and resolve any conflicts.

---

## 3. Review and Merge Requirements

Every PR must meet the following criteria before it can be merged:

- **CI must be green** – all automated checks (linting, tests, Docker build, smoke test) must pass.
- **At least one approval** from a team member other than the PR author.
- **No unresolved review comments** – address all feedback from reviewers.
- **Linked issue must be resolved** – the associated issue should have all acceptance criteria met.

### Merging Strategy
- Use **“Squash and merge”** for most PRs to keep the commit history clean and atomic.
- **Exception**: Release or hotfix PRs may be merged with **“Create a merge commit”** if preserving individual commits adds clarity (e.g., for rollback purposes).

---

## 4. Deeper Maintained Documentation

For more detailed information, refer to these documents (all kept current by the team):

| Document | What it covers |
|----------|----------------|
| [docs/development-process.md](./docs/development-process.md) | **Full workflow** – branching, PR process, CI/CD, secrets, and release management. |
| [docs/quality-requirements.md](./docs/quality-requirements.md) | Coding standards, architecture guidelines, and non‑functional requirements. |
| [docs/quality-requirements-tests.md](./docs/quality-requirements-tests.md) | Detailed testing strategy, coverage targets, and test organisation. |
| [docs/definition-of-done.md](./docs/definition-of-done.md) | Complete Definition of Done for issues and PRs. |
| [docs/roadmap.md](./docs/roadmap.md) | High-level project roadmap and upcoming milestones. |
| [CHANGELOG.md](./CHANGELOG.md) | Release notes and version history. |

If you have any questions that aren't covered here, please reach out in the team Slack/Teams channel or comment directly on your issue/PR.

---

*This CONTRIBUTING.md is maintained alongside the repository and updated whenever the contribution workflow, verification commands, or review expectations change.*
