import pytest
from unittest.mock import Mock, patch
import json
from urllib import error
import netifaces
import socket
from scapy.all import IP, TCP, UDP, ICMP, Ether

from tproc import TrafficProcessor


def test_initialization_with_interface():
    """Test that TrafficProcessor obtains IPs correctly using patched netifaces."""
    with patch("tproc.netifaces.ifaddresses") as mock_ifaddrs:
        mock_ifaddrs.return_value = {
            netifaces.AF_INET: [{"addr": "192.168.1.100"}],
            netifaces.AF_LINK: [{"addr": "aa:bb:cc:dd:ee:ff"}],
        }
        with patch("socket.gethostbyname") as mock_gethostbyname:
            def side_effect(hostname):
                if hostname == "cnss":
                    return "10.0.0.2"
                if hostname == "mock_target":
                    return "8.8.8.8"
                raise socket.gaierror("Unknown host")
            mock_gethostbyname.side_effect = side_effect

            tp = TrafficProcessor(interface="eth0", output_url="http://test", delay=0.5)

            assert tp.gate_ip == "192.168.1.100"
            assert tp.target_ip == "8.8.8.8"
            assert tp.cnss_ip == "10.0.0.2"
            assert tp.interface == "eth0"
            assert tp.output_url == "http://test"
            assert tp.delay == 0.5
            assert tp.packet_cnt == 0
            assert tp.incoming_packets == 0
            assert tp.outgoing_packets == 0
            assert tp.gate_ip in tp.ip_tracker.ignore_ips


def test_packet_handler_statistics():
    """Test packet_handler increments counters and directions correctly."""
    with patch("tproc.netifaces.ifaddresses") as mock_ifaddrs:
        mock_ifaddrs.return_value = {
            netifaces.AF_INET: [{"addr": "192.168.1.100"}],
        }
        with patch("socket.gethostbyname") as mock_gethostbyname:
            def side_effect(hostname):
                if hostname == "cnss":
                    return "10.0.0.2"
                if hostname == "mock_target":
                    return "8.8.8.8"
                raise socket.gaierror("Unknown host")
            mock_gethostbyname.side_effect = side_effect

            tp = TrafficProcessor(interface="eth0", output_url="http://test")

            # Override IPs to known test values; disable management filtering
            tp.gate_ip = "192.168.1.100"
            tp.target_ip = "8.8.8.8"
            tp.cnss_ip = None   # Disable management filter for test

            # Create packets
            # Incoming TCP (dst == gate_ip, non‑management port)
            pkt_in = Ether() / IP(src="10.0.0.1", dst="192.168.1.100") / TCP(sport=12345, dport=80)
            # Outgoing UDP (src == target_ip, non‑management port)
            pkt_out = Ether() / IP(src="8.8.8.8", dst="192.168.1.1") / UDP(sport=12345, dport=12345)
            # Incoming ICMP (dst == gate_ip)
            pkt_icmp = Ether() / IP(src="1.1.1.1", dst="192.168.1.100") / ICMP()

            # Process and check after each call to see which fails
            tp.packet_handler(pkt_in)
            assert tp.packet_cnt == 1, "First packet not counted"
            tp.packet_handler(pkt_out)
            assert tp.packet_cnt == 2, "Second packet not counted"
            tp.packet_handler(pkt_icmp)
            assert tp.packet_cnt == 3, "Third packet not counted"

            # Full assertions
            assert tp.bytes_cnt == len(pkt_in) + len(pkt_out) + len(pkt_icmp)
            assert tp.tcp_cnt == 1
            assert tp.udp_cnt == 1
            assert tp.icmp_cnt == 1
            assert tp.other_cnt == 0

            assert tp.incoming_packets == 2   # TCP and ICMP have dst==gate_ip
            assert tp.outgoing_packets == 1   # UDP has src==target_ip
            assert tp.incoming_bytes == len(pkt_in) + len(pkt_icmp)
            assert tp.outgoing_bytes == len(pkt_out)

            # Verify IP tracker was updated
            assert len(tp.ip_tracker.data) > 0


def test_post_json_success_and_failure():
    """Test post_json handles successful response and HTTP errors."""
    tp = TrafficProcessor(output_url="http://localhost:8000")
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
            # Success case
            mock_response = Mock()
            mock_response.getcode.return_value = 200
            mock_response.read.return_value = b'{"status":"ok"}'
            mock_urlopen.return_value.__enter__.return_value = mock_response

            status, body = tp.post_json()
            assert status == 200
            assert body == '{"status":"ok"}'

            args, kwargs = mock_urlopen.call_args
            request = args[0]
            assert request.get_method() == "POST"
            assert request.headers.get("Content-type") == "application/json"
            data = json.loads(request.data.decode())
            assert "timestamp" in data
            assert data["status"] == "online"

            # HTTP error case
            mock_urlopen.reset_mock()
            error_response = Mock()
            error_response.read.return_value = b'{"error":"bad request"}'
            mock_urlopen.side_effect = error.HTTPError(
                url="http://localhost:8000", code=400, msg="Bad Request",
                hdrs={}, fp=error_response
            )

            status, body = tp.post_json()
            assert status == 400
            assert body == '{"error":"bad request"}'

            # Non‑HTTP exception
            mock_urlopen.reset_mock()
            mock_urlopen.side_effect = ConnectionError("Network unreachable")
            with pytest.raises(ConnectionError):
                tp.post_json()
