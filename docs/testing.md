# Testing and Quality Automation

## Scope

The product has two critical modules:

| Critical module | Responsibility | Automated evidence |
|---|---|---|
| [`src/Traffic_Processor/tproc.py`](../src/Traffic_Processor/tproc.py) | Packet classification, incoming/outgoing counters, rate calculation, and statistics delivery | [Unit tests](../src/Traffic_Processor/test_TP+CN.py) and [QRTs](../src/qr_test.py) |
| [`src/cnss/app/main.py`](../src/cnss/app/main.py) | Receiving, validating, storing, and returning Traffic Processor statistics through the FastAPI interface | [Integration tests](../src/cnss/tests/cnss_test.py) |

Each critical module must maintain at least **30% automated line coverage**. Global repository coverage may be lower because the repository also contains configuration, migrations, static frontend files, and deployment code.

## Automated tests

### Unit tests

[`src/Traffic_Processor/test_TP+CN.py`](../src/Traffic_Processor/test_TP+CN.py) verifies:

- Traffic Processor initialization and interface information
- TCP, UDP, and ICMP counting
- Incoming and outgoing packet classification
- Byte counters
- JSON creation and HTTP success/error handling

### Integration tests

[`src/cnss/tests/cnss_test.py`](../src/cnss/tests/cnss_test.py) verifies the CNSS HTTP interface by submitting packet statistics through `POST /` and retrieving them through `GET /packets`.

The test currently uses FastAPI `TestClient`. A future improvement is to make each CNSS test independent instead of relying on shared application state.

### Quality requirement tests

[`src/qr_test.py`](../src/qr_test.py) contains the automated QRTs linked from:

- [`docs/quality-requirements.md`](quality-requirements.md)
- [`docs/quality-requirements-tests.md`](quality-requirements-tests.md)

QRT evidence is kept separate from unit and integration evidence because QRTs verify measurable quality scenarios rather than individual code behaviour.

## Coverage

Coverage is generated in [`.github/workflows/main.yml`](../.github/workflows/main.yml) with `pytest-cov` in XML and HTML formats.

Required policy:

- `src/Traffic_Processor/tproc.py`: at least 30%
- `src/cnss/app/main.py`: at least 30%
- A pull request must not reduce either critical module below the threshold
- New or changed critical behaviour must include corresponding tests

The latest protected-branch CI evidence is available in [GitHub Actions](https://github.com/SWP-Team-46/Traffic-Proccessor/actions/runs/28334444093).

**Current limitation:** CI generates coverage reports but does not yet visibly enforce a separate 30% threshold for each critical module. Per-module threshold enforcement and a downloadable coverage artifact should be added before claiming full coverage-gate compliance.

## Additional automated QA check

The team considered:

- Python dependency vulnerability scanning with `pip-audit`
- Python security scanning with Bandit
- Docker and Compose configuration validation
- A Docker Compose deployment smoke test

The selected additional QA check is the **Docker Compose smoke test** in [`.github/workflows/main.yml`](../.github/workflows/main.yml).

Its objective is to detect deployment and integration failures that normal Python tests cannot find, including broken Docker builds, invalid service configuration, missing runtime dependencies, and containers that terminate during startup. This matters because the product depends on the Traffic Processor, CNSS, and PostgreSQL starting together in one Compose environment.

The CI job:

1. Builds the Docker images.
2. Starts the Compose stack.
3. Waits for initialization.
4. Verifies that the expected containers are running.
5. Shuts the stack down.

This check is distinct from linting, tests, coverage, QRTs, and link checking. The Lychee link checker is useful repository maintenance, but it is **not** counted as the Assignment 4 additional QA check.

Limitations and deferred work:

- The smoke test verifies running containers, not complete end-to-end packet delivery.
- It does not currently call a CNSS health endpoint.
- It does not verify database contents or frontend rendering.
- Dependency vulnerability scanning remains a suitable future addition.

## CI quality gates

The current CI pipeline performs:

- Flake8 syntax checking
- Unit, integration, and quality requirement tests with pytest
- Coverage report generation
- Docker image builds
- Docker Compose smoke testing

The separate link-checking workflow validates Markdown links but is not used as the additional QA check.

## Maintenance policy

Tests introduced for Assignment 4 are maintained product assets. Later changes must keep them passing. When behaviour is replaced, the related tests must be updated or replaced with equivalent or stronger automated evidence. New critical modules must be documented here and must meet the same coverage policy.

## Requirement status

| Requirement | Status |
|---|---|
| Critical product logic has automated unit tests | Implemented |
| Important CNSS interactions have automated integration tests | Implemented |
| Automated QRTs are stored separately and linked | Implemented |
| Tests use normal repository locations and are linked here | Implemented |
| Distinct additional QA check is selected and runs in CI | Implemented: Docker Compose smoke test |
| Link checking is excluded as the additional QA check | Confirmed |
| Critical modules are identified | Implemented |
| At least 30% coverage is enforced separately for every critical module | **Not yet fully enforced in CI** |
| Tests are maintained as long-term product assets | Documented |
