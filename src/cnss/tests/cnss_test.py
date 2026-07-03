from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_insert_packets_info():
    payload = {
        "timestamp": "2026-06-28T15:30:45.123456",
        "total_packets": 15234,
        "total_bytes": 15728640,
        "incoming_packets": 8234,
        "outgoing_packets": 7000,
        "incoming_bytes": 8388608,
        "outgoing_bytes": 7340032,
        "packets_per_second": 125.5,
        "bytes_per_second": 131072.0,
        "tcp_packets": 10200,
        "udp_packets": 3500,
        "icmp_packets": 1200,
        "other_packets": 334,
        "top_ips": [],
        "status": "online"
    }
    response = client.post("/load", json=payload)
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_obtain_packet_info():
    # First insert data
    payload = {
        "timestamp": "2026-06-28T15:30:45.123456",
        "total_packets": 15234,
        "total_bytes": 15728640,
        "incoming_packets": 8234,
        "outgoing_packets": 7000,
        "incoming_bytes": 8388608,
        "outgoing_bytes": 7340032,
        "packets_per_second": 125.5,
        "bytes_per_second": 131072.0,
        "tcp_packets": 10200,
        "udp_packets": 3500,
        "icmp_packets": 1200,
        "other_packets": 334,
        "top_ips": [],
        "status": "online"
    }
    client.post("/load", json=payload)
    
    # Then obtain it
    response = client.get('/packets').json()
    assert response.get('total_packets') is not None
    assert response['total_packets'] == 15234
    assert response.get('total_bytes') is not None
    assert response['total_bytes'] == 15728640

def test_reset_functionality():
    # Insert first snapshot
    payload1 = {
        "timestamp": "2026-06-28T15:30:45.123456",
        "total_packets": 10000,
        "total_bytes": 1000000,
        "incoming_packets": 5000,
        "outgoing_packets": 5000,
        "incoming_bytes": 500000,
        "outgoing_bytes": 500000,
        "packets_per_second": 100.0,
        "bytes_per_second": 10000.0,
        "tcp_packets": 8000,
        "udp_packets": 1500,
        "icmp_packets": 400,
        "other_packets": 100,
        "top_ips": [],
        "status": "online"
    }
    client.post("/load", json=payload1)
    
    # Reset - save current state as baseline
    reset_response = client.post("/reset")
    assert reset_response.status_code == 200
    assert reset_response.json()["status"] == "ok"
    
    # Insert second snapshot with higher values
    payload2 = {
        "timestamp": "2026-06-28T15:31:45.123456",
        "total_packets": 12500,
        "total_bytes": 1250000,
        "incoming_packets": 6250,
        "outgoing_packets": 6250,
        "incoming_bytes": 625000,
        "outgoing_bytes": 625000,
        "packets_per_second": 125.0,
        "bytes_per_second": 12500.0,
        "tcp_packets": 10000,
        "udp_packets": 2000,
        "icmp_packets": 400,
        "other_packets": 100,
        "top_ips": [],
        "status": "online"
    }
    client.post("/load", json=payload2)
    
    # Check that we got the delta (difference)
    response = client.get('/packets').json()
    assert response['total_packets'] == 2500  # 12500 - 10000
    assert response['total_bytes'] == 250000  # 1250000 - 1000000
    assert response['incoming_packets'] == 1250  # 6250 - 5000
    assert response['outgoing_packets'] == 1250  # 6250 - 5000