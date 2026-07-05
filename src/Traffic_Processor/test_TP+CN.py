import pytest
from unittest.mock import Mock, patch, MagicMock
import json
from urllib import error
from datetime import datetime
import netifaces
from scapy.all import IP, TCP, UDP, ICMP, Ether

from tproc import TrafficProcessor


@pytest.fixture
def mock_interface_info():
    """Mock netifaces to return a fake IP and MAC for a specific interface."""
    with patch("netifaces.ifaddresses") as mock_ifaddrs:
        # Simulate interface 'eth0'
        mock_ifaddrs.return_value = {
            netifaces.AF_INET: [{"addr": "192.168.1.100"}],
            netifaces.AF_LINK: [{"addr": "aa:bb:cc:dd:ee:ff"}],
        }
        yield mock_ifaddrs


@pytest.fixture
def mock_hostname_resolution():
    """Mock socket.gethostbyname to return fixed IPs for CNSS and TARGET."""
    with patch("socket.gethostbyname") as mock_gethostbyname:
        # Return fake IPs for the expected hostnames
        def side_effect(hostname):
            if hostname == "cnss":
                return "10.0.0.2"
            if hostname == "mock_target":
                return "8.8.8.8"
            raise socket.gaierror("Unknown host")
        mock_gethostbyname.side_effect = side_effect
        yield mock_gethostbyname


def test_initialization_with_interface(mock_interface_info, mock_hostname_resolution):
    """Test that TrafficProcessor obtains IPs correctly."""
    tp = TrafficProcessor(interface="eth0", output_url="http://test", delay=0.5)

    assert tp.gate_ip == "192.168.1.100"
    assert tp.target_ip == "8.8.8.8"
    assert tp.cnss_ip == "10.0.0.2"
    assert tp.interface == "eth0"
    assert tp.output_url == "http://test"
    assert tp.delay == 0.5
    # Check that counters start at zero
    assert tp.packet_cnt == 0
    assert tp.incoming_packets == 0
    assert tp.outgoing_packets == 0
    # IP tracker should have ignore_ips containing gate_ip
    assert tp.gate_ip in tp.ip_tracker.ignore_ips


def test_packet_handler_statistics(mock_hostname_resolution):
    """Test packet_handler increments counters and directions correctly."""
    tp = TrafficProcessor(interface="eth0", output_url="http://test")
    # Override IPs to known test values; set cnss_ip to a dummy so packets are not filtered
    tp.gate_ip = "192.168.1.100"
    tp.target_ip = "8.8.8.8"
    tp.cnss_ip = "10.0.0.2"

    # Create packets matching the direction rules
    # Incoming: dst == gate_ip
    pkt_in = Ether() / IP(src="10.0.0.1", dst="192.168.1.100") / TCP(sport=12345, dport=80)
    # Outgoing: src == target_ip
    pkt_out = Ether() / IP(src="8.8.8.8", dst="192.168.1.1") / UDP(sport=53, dport=12345)
    # ICMP: incoming (dst == gate_ip)
    pkt_icmp = Ether() / IP(src="1.1.1.1", dst="192.168.1.100") / ICMP()

    tp.packet_handler(pkt_in)
    tp.packet_handler(pkt_out)
    tp.packet_handler(pkt_icmp)

    assert tp.packet_cnt == 3
    assert tp.bytes_cnt == len(pkt_in) + len(pkt_out) + len(pkt_icmp)
    assert tp.tcp_cnt == 1
    assert tp.udp_cnt == 1
    assert tp.icmp_cnt == 1
    assert tp.other_cnt == 0

    assert tp.incoming_packets == 2  # TCP and ICMP have dst==gate_ip
    assert tp.outgoing_packets == 1  # UDP has src==target_ip
    assert tp.incoming_bytes == len(pkt_in) + len(pkt_icmp)
    assert tp.outgoing_bytes == len(pkt_out)

    # Quick check that IP tracker was updated (it should have entries)
    assert len(tp.ip_tracker.data) > 0


def test_post_json_success_and_failure():
    """Test post_json handles successful response and HTTP errors."""
    tp = TrafficProcessor(output_url="http://localhost:8000")
    # Mock get_stats to return a fixed dictionary so we don't depend on IP tracker state
    mock_stats = {
        "timestamp": "2023-01-01T00:00:00",
        "total_packets": 100,
        "total_bytes": 5000,
        "incoming_packets": 60,
        "outgoing_packets": 40,
        "incoming_bytes": 3000,
        "outgoing_bytes": 2000,
        "packets_per_second": 10.0,
        "bytes_per_second": 500.0,
        "tcp_packets": 70,
        "udp_packets": 20,
        "icmp_packets": 10,
        "other_packets": 0,
        "top_ips": [],
        "status": "online"
    }
    with patch.object(tp, "get_stats", return_value=mock_stats):
        with patch("urllib.request.urlopen") as mock_urlopen:
            # --- Success case ---
            mock_response = Mock()
            mock_response.getcode.return_value = 200
            mock_response.read.return_value = b'{"status":"ok"}'
            mock_urlopen.return_value.__enter__.return_value = mock_response

            status, body = tp.post_json()
            assert status == 200
            assert body == '{"status":"ok"}'

            # Verify request was called with correct data and headers
            args, kwargs = mock_urlopen.call_args
            request = args[0]  # The Request object
            assert request.get_method() == "POST"
            assert request.headers.get("Content-type") == "application/json"
            # The data should be a JSON encoded stats dict
            data = json.loads(request.data.decode())
            assert "timestamp" in data
            assert data["status"] == "online"

            # --- HTTP error case ---
            mock_urlopen.reset_mock()
            error_response = Mock()
            error_response.read.return_value = b'{"error":"bad request"}'
            mock_urlopen.side_effect = error.HTTPError(
                url="http://localhost:8000", code=400, msg="Bad Request", hdrs={}, fp=error_response
            )

            status, body = tp.post_json()
            assert status == 400
            assert body == '{"error":"bad request"}'

            # --- Non-HTTP exception ---
            mock_urlopen.reset_mock()
            mock_urlopen.side_effect = ConnectionError("Network unreachable")
            with pytest.raises(ConnectionError):
                tp.post_json()
