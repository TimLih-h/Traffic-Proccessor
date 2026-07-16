import pytest
from fastapi.testclient import TestClient
from app.main import app
from datetime import datetime, timedelta
import app.main as main_module


@pytest.fixture
def client():
    # lifespan (startup/shutdown) запускается только при использовании
    # TestClient как контекстного менеджера — иначе init_pool() не вызовется
    # и любой запрос, трогающий БД, упадёт с RuntimeError -> 500.
    with TestClient(app) as c:
        yield c


@pytest.fixture(autouse=True)
def reset_globals():
    main_module.last_info = None
    main_module.reset_dump = None
    yield


def test_insert_packets_info(client):
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


def test_obtain_packet_info(client):
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

    response = client.get('/packets').json()
    assert response.get('total_packets') is not None
    assert response['total_packets'] == 15234
    assert response.get('total_bytes') is not None
    assert response['total_bytes'] == 15728640


def test_reset_functionality(client):
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

    reset_response = client.post("/reset")
    assert reset_response.status_code == 200
    assert reset_response.json()["status"] == "ok"

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

    response = client.get('/packets').json()
    assert response['total_packets'] == 2500  # 12500 - 10000
    assert response['total_bytes'] == 250000  # 1250000 - 1000000
    assert response['incoming_packets'] == 1250  # 6250 - 5000
    assert response['outgoing_packets'] == 1250  # 6250 - 5000


def test_history_records_snapshots(client):
    payload = {
        "timestamp": "2026-06-28T15:30:45.123456",
        "total_packets": 111,
        "total_bytes": 2222,
        "incoming_packets": 50,
        "outgoing_packets": 61,
        "incoming_bytes": 1000,
        "outgoing_bytes": 1222,
        "packets_per_second": 1.0,
        "bytes_per_second": 2.0,
        "tcp_packets": 90,
        "udp_packets": 15,
        "icmp_packets": 5,
        "other_packets": 1,
        "top_ips": [],
        "status": "online"
    }
    client.post("/load", json=payload)

    response = client.get("/history?limit=10")
    assert response.status_code == 200

    records = response.json()
    assert isinstance(records, list)
    assert len(records) >= 1
    assert "timestamp" in records[0]
    assert "data" in records[0]
    assert records[0]["data"]["total_packets"] == payload["total_packets"]


def test_history_filters_by_timestamp(client):
    payload = {
        "timestamp": "2026-06-28T15:30:45.123456",
        "total_packets": 1,
        "total_bytes": 1,
        "incoming_packets": 0,
        "outgoing_packets": 0,
        "incoming_bytes": 0,
        "outgoing_bytes": 0,
        "packets_per_second": 0.0,
        "bytes_per_second": 0.0,
        "tcp_packets": 0,
        "udp_packets": 0,
        "icmp_packets": 0,
        "other_packets": 0,
        "top_ips": [],
        "status": "online"
    }
    client.post("/load", json=payload)

    # окно точно захватывает запись, только что вставленную
    now = datetime.utcnow()
    date_from = (now - timedelta(minutes=1)).isoformat()
    date_to = (now + timedelta(minutes=1)).isoformat()

    response = client.get(f"/history?date_from={date_from}&date_to={date_to}")
    assert response.status_code == 200
    records = response.json()
    assert len(records) >= 1

    # окно заведомо в прошлом — ничего не должно найтись
    far_past_from = "2000-01-01T00:00:00"
    far_past_to = "2000-01-02T00:00:00"
    response = client.get(f"/history?date_from={far_past_from}&date_to={far_past_to}")
    assert response.status_code == 200
    assert response.json() == []
