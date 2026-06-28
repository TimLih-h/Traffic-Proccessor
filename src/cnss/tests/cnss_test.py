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
        "status": "normal"
    }
    response = client.post("/", json=payload)
    
    assert response.status_code == 200
    
    
def test_obtain_packet_info():
    response = client.get('/packets').json()
    
    assert response.get('total_packets') is not None
    assert response['total_packets'] == 15234
    
    assert response.get('total_bytes') is not None
    assert response['total_bytes'] == 15728640
