# User Acceptance Tests (UATs)

User acceptance tests (UATs) describe end-user-facing scenarios that customers or relevant stakeholders can execute to inspect whether the product supports intended user goals.

---

## UAT-001: Verify Web Interface Displays Live Traffic Statistics

| Field | Detail |
|-------|--------|
| **ID** | UAT-001 |
| **Status** | Active |
| **User Goal** | As a network administrator, I want to view live traffic statistics through a web interface so that I can monitor network activity without accessing the container directly. |
| **Preconditions** | 1. Docker and Docker Compose are installed on the system.<br>2. The Traffic Processor repository is cloned locally.<br>3. Port 8080 is available on the host. |
| **Step-by-step Instructions** | 1. Navigate to the src folder: `cd src`<br>2. Start all services: `docker compose up --build -d`<br>3. Wait 10 seconds for services to initialise.<br>4. Open a web browser and navigate to `http://localhost:8080/static/index.html`<br>5. Observe the web interface loading.<br>6. Generate network traffic (e.g., `curl http://localhost:8080`).<br>7. Note the new values. |
| **Expected Outcome** | - The web interface loads without errors.<br>- The page displays traffic statistics (incoming/outgoing packets and bytes, rates, protocol breakdowns).<br>- Statistics update dynamically.<br>- The `/packets` API endpoint returns valid JSON data.<br>- Packet counts increase after traffic generation. |
| **Assignment-specific Execution Results** | - Sprint 2: All criteria passed <br>- Sprint 3: All criteria passed
| **Customer Comments or Observed Issues** | - Sprint 2: No observed issues <br>- Sprint 3: No observed issues|
| **Resulting PBIs or Issues** | - Sprint 2: No new PBIs <br>- Sprint 3: No new PBIs|

---

## UAT-002: Verify Traffic Processor Operation via Docker

| Field | Detail |
|-------|--------|
| **ID** | UAT-002 |
| **Status** | Active |
| **User Goal** | As a network administrator, I want to start the Traffic Processor using Docker Compose so that all required services (packet capture, data forwarding, web server, database) run together reliably. |
| **Preconditions** | 1. Docker and Docker Compose are installed.<br>2. The repository is cloned and the src folder is accessible. |
| **Step-by-step Instructions** | 1. Navigate to the src folder: `cd src`<br>2. Start all services: `docker compose up --build -d`<br>3. Verify all containers are running: `docker ps`<br>4. Check that the tproc container is capturing traffic:<br>&nbsp;&nbsp;&nbsp;`docker exec tproc cat /data/data.txt \| head -3`<br>5. Check that the cnss web server is responding:<br>&nbsp;&nbsp;&nbsp;`curl http://localhost:8080/root`  <br>6. verify the Gate servise is healthy: `curl http://localhost:8081/health` <br>7. Stop all services: `docker compose down` |
| **Expected Outcome** | - All containers (tproc, cn, cnss, postgres) start successfully.<br>- `docker ps` shows all containers with status `Up`.<br>- The `data.txt` file contains valid JSON statistics.<br>- The `/root` endpoint returns `{"message": "DEV_MODE is true"}`.<br>- `docker compose down` stops all containers cleanly. |
| **Assignment-specific Execution Results** | - Sprint 2: All criteria passed <br>- Sprint 3: All criteria passed|
| **Customer Comments or Observed Issues** | - Sprint 2: No observed issues <br>- Sprint 3: No observed issues|
| **Resulting PBIs or Issues** | - Sprint 2: No new PBIs <br>- Sprint 3: No new PBIs|

---

## UAT-003: Verify Directional Traffic Classification

| Field | Detail |
|-------|--------|
| **ID** | UAT-003 |
| **Status** | Active |
| **User Goal** | As a network administrator, I want to see separate counts for incoming and outgoing traffic in the web interface so that I can understand the direction of network flows. |
| **Preconditions** | 1. All Docker services are running (as per UAT-002).<br>2. The system has a known local IP address on the eth0 interface (or the interface specified in docker-compose.yml). |
| **Step‑by‑step Instructions** | 1. Ensure services are running: `docker compose up -d`<br>2. Open the web interface: `http://localhost:8080/static/index.html`<br>3. Note the current `incoming_packets` and `outgoing_packets` values.<br>4. Generate traffic by sending 10 ICMP Echo Requests to a reachable external host (e.g., `curl http://localhost:8080`).<br>5. Wait for the ping to finish and refresh the web interface.<br>6. Note the new values. |
| **Expected Outcome** | - The `outgoing_packets` counter increases by **at least** the number of requests sent (10, plus possible ARP/other overhead).<br>- The `incoming_packets` counter increases by **approximately** the number of replies received (should be 10 if the host is reachable).<br>- Both values are displayed clearly on the web interface.<br>- The `/packets` API endpoint returns the updated counts for both directions. |
| **Assignment-specific Execution Results** | - Sprint 2: All criteria passed <br>- Sprint 3: All criteria passed|
| **Customer Comments or Observed Issues** | - Sprint 2: No observed issues <br>- Sprint 3: No observed issues|
| **Resulting PBIs or Issues** | - Sprint 2: No new PBIs <br>- Sprint 3: No new PBIs|

---

### UAT‑004: Verify Gate Traffic Filtering and Forwarding

| Field | Detail |
|-------|--------|
| **ID** | UAT‑004 |
| **Status** | Active |
| **User Goal** | As a network administrator, I want to test that the Gate service correctly filters or forwards traffic according to configured rules so that I can enforce network policies. |
| **Preconditions** | 1. All services are running (as per UAT‑002).<br>2. The Gate is configured with a known rule set (e.g., allow ICMP, block UDP on port 53).<br>3. `curl` or `ping` tools are available on the host. |
| **Step‑by‑step Instructions** | 1. Ensure services are up: `docker compose up -d`<br>2. Generate traffic that should be **allowed** (e.g., `ping -c 5 8.8.8.8`).<br>3. Generate traffic that should be **blocked** (e.g., `dig @8.8.8.8 google.com` – if UDP/53 is blocked).<br>5. Verify that allowed traffic is counted/forwarded and blocked traffic is dropped (reflected in stats).<br>6. Check the web interface to confirm the numbers align. |
| **Expected Outcome** | – Allowed traffic results in successful pings and is recorded in the Gate’s stats (incoming/outgoing counters increment).<br>– Blocked traffic does not reach the target (timeout or no reply). <br>– The web interface reflects these statistics correctly. |
| **Assignment-specific Execution Results** | - Sprint 3: All criteria passed|
| **Customer Comments or Observed Issues** | - Sprint 3: No observed issues|
| **Resulting PBIs or Issues** | - Sprint 3: No new PBIs|

---

Based on the current state of the `dev` branch, the previously suggested UAT-005 (historical data persistence) is not applicable, as the database is not yet used to store packet or connection history. A more relevant test focuses on a feature that is actually implemented and distinct from the existing four UATs.

The **reset** functionality in the CNSS service allows administrators to set a baseline for traffic statistics, enabling them to measure traffic from a specific point in time. This is a simple, testable feature that is different from the web interface, Docker operation, directional classification, and gate filtering tests already defined.

---

## UAT-005: Verify Traffic Statistics Reset Functionality

| Field | Detail |
|-------|--------|
| **ID** | UAT-005 |
| **Status** | Active |
| **User Goal** | As a network administrator, I want to reset the traffic statistics baseline so that I can measure network activity from a specific point in time without restarting the entire system. |
| **Preconditions** | 1. All Docker services are running (as per UAT-002).<br>2. The CNSS service is accessible at `http://localhost:8080`.<br>3. `curl` or a similar HTTP client is available on the host. |
| **Step-by-step Instructions** | 1. Ensure services are running: `docker compose up -d`<br>2. Generate some initial traffic to populate statistics (e.g., `curl http://localhost:8080`).<br> 3.Record the `incoming_packets` and `outgoing_packets` values.<br>4. Reset the statistics baseline through the website <br>5. Record the values <br>6. Generate additional traffic (e.g., `curl http://localhost:8080`).<br>7. Observe the changes. |
| **Expected Outcome** | - Immediately after reset, the packet counts are **reduced to zero** .<br>- After generating new traffic, the counts increase from zero, reflecting only the traffic sent after the reset. |
| **Assignment-specific Execution Results** | - Sprint 3: All criteria passed|
| **Customer Comments or Observed Issues** | - Sprint 3: No observed issues|
| **Resulting PBIs or Issues** | - Sprint 3: No new PBIs|






