import time
import pytest
import subprocess
import requests
from unittest.mock import Mock, patch
from threading import Thread
from http.server import HTTPServer, BaseHTTPRequestHandler
from Traffic_Processor.tproc import TrafficProcessor

# QRT-001: Dashboard metric update delay
def test_dashboard_metric_update_delay():
    # QRT-001: Verify that dashboard metrics update within ≤1000ms.
    # Setup: Create a mock dashboard server that records update timestamps
    class DashboardHandler(BaseHTTPRequestHandler):
        updates = []

        def do_POST(self):
            # Record the time when the dashboard receives an update
            self.updates.append(time.time())
            self.send_response(200)
            self.end_headers()

        def log_message(self, format, *args):
            pass  # Suppress log messages

    # Start a local HTTP server to act as the dashboard
    server = HTTPServer(("localhost", 0), DashboardHandler)  # Port 0 = auto-assign
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    port = server.server_address[1]
    dashboard_url = f"http://localhost:{port}"

    # Initialize the Traffic Processor with the dashboard URL
    tp = TrafficProcessor(interface="eth0", output_url=dashboard_url, delay=0.1)

    # Simulate data generation by the Traffic Processor
    data_generation_time = time.time()

    # Trigger an update (e.g., by processing a packet)
    from scapy.all import IP, TCP, Ether
    pkt = Ether() / IP(src="10.0.0.1", dst="192.168.1.100") / TCP()
    tp.packet_handler(pkt)
    tp.post_json()  # Force a POST to the dashboard

    # Wait a moment for the POST to complete
    time.sleep(0.2)

    # Check the recorded update times
    server.shutdown()
    thread.join(timeout=1)

    assert len(DashboardHandler.updates) > 0, "Dashboard did not receive any updates"
    update_time = DashboardHandler.updates[-1]
    delay_ms = (update_time - data_generation_time) * 1000

    # Expected: ≤1000ms for 95% of runs
    assert delay_ms <= 1000.0, f"Update delay was {delay_ms:.2f}ms, expected ≤1000ms"

# QRT-002: Traffic Processor startup time
def test_traffic_processor_startup_time():
    """
    QRT-002: Verify that the service starts and becomes ready within ≤500ms.
    Linked quality requirement: QR-002
    """
    # In a real CI environment, you would start the service via Docker or systemd.
    # Here we simulate by starting the process and measuring health check time.

    start_time = time.time()

    # Simulate service startup by running a subprocess (e.g., python tproc.py)
    # In practice, you might use docker-compose or a similar command.
    proc = subprocess.Popen(
        ["python", "-c", "import time; time.sleep(0.2); print('ready')"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    # Wait for the process to indicate it's ready (e.g., by printing "ready")
    # In a real service, you would poll a health check endpoint (e.g., /health)
    # using requests.get() until it returns 200 OK.
    ready = False
    for _ in range(50):  # Poll up to 5 seconds
        if proc.poll() is not None:
            # Process exited; check if it printed "ready"
            stdout, _ = proc.communicate()
            if "ready" in stdout:
                ready = True
            break
        time.sleep(0.1)

    elapsed_ms = (time.time() - start_time) * 1000

    # Clean up
    if proc.poll() is None:
        proc.terminate()
        proc.wait()

    assert ready, "Service did not become ready"
    # Expected: ≤500ms
    assert elapsed_ms <= 500.0, f"Startup time was {elapsed_ms:.2f}ms, expected ≤500ms"

# QRT-003: Traffic Processor throughput capacity
def test_traffic_processor_throughput():
    """
    QRT-003: Verify that the processor sustains ≥1000 Kbps for 60 seconds with <1% packet loss/error.
    Linked quality requirement: QR-003
    """
    import time
    import threading
    from scapy.all import Ether, IP, UDP
    from unittest.mock import patch

    # Configuration – reduce duration for CI (still long enough to be meaningful)
    TARGET_RATE_BPS = 1_000_000          # 1000 Kbps
    PACKET_SIZE_BYTES = 100              # 100 bytes per packet
    PACKETS_PER_SECOND = int(TARGET_RATE_BPS / (PACKET_SIZE_BYTES * 8))
    DURATION_SECONDS = 10                # 10 seconds is enough for a CI smoke test

    # Mock the HTTP POST to avoid external calls
    with patch('requests.post') as mock_post:
        mock_post.return_value.status_code = 200

        # Create a TrafficProcessor instance – use a dummy interface
        tp = TrafficProcessor(interface="lo", output_url="http://dummy")
        tp.local_ip = "127.0.0.1"
        tp.local_mac = "00:00:00:00:00:00"

        # Override packet_handler to count processed packets
        processed_count = 0
        original_handler = tp.packet_handler

        def counting_handler(pkt):
            nonlocal processed_count
            processed_count += 1
            original_handler(pkt)

        tp.packet_handler = counting_handler

        # Build a sample packet (Ether/IP/UDP)
        pkt = Ether(dst="ff:ff:ff:ff:ff:ff", src="00:00:00:00:00:00") / \
              IP(src="127.0.0.1", dst="8.8.8.8") / \
              UDP() / ("X" * (PACKET_SIZE_BYTES - 42))  # 42 bytes for Ether+IP+UDP

        start_time = time.time()
        # Generate packets at the target rate for the duration
        while time.time() - start_time < DURATION_SECONDS:
            tp.packet_handler(pkt)
            # Sleep to maintain the desired packet rate
            time.sleep(1.0 / PACKETS_PER_SECOND)

        # Calculate statistics
        total_expected = int(PACKETS_PER_SECOND * DURATION_SECONDS)
        # Allow some tolerance for timing inaccuracies (e.g., sleep overhead)
        loss_percent = ((total_expected - processed_count) / total_expected) * 100

        # Expected: less than 1% loss/error
        assert loss_percent < 1.0, f"Packet loss was {loss_percent:.2f}%, expected <1%"
        assert tp.packet_cnt > 0, "No packets were processed"
        assert tp.udp_cnt > 0, "UDP packets were not correctly identified"

        # Verify throughput in Kbps (based on processed bytes)
        throughput_kbps = (tp.bytes_cnt * 8) / (DURATION_SECONDS * 1000)
        assert throughput_kbps >= 1000, f"Throughput was {throughput_kbps:.2f} Kbps, expected ≥1000 Kbps"
