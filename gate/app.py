from flask import Flask, request, Response
import requests

app = Flask(__name__)

MAIN_SERVER = "http://cnss:8080"
ERROR_SERVER = "http://error-server:5000"

# Blocked IP list.
# It is empty for now, so all IPs are allowed.
BLOCKED_IPS = {
    "172.19.0.1"
    "10.241.1.122"
}


def get_client_ip():
    """
    Get client IP address.
    request.remote_addr is the direct client IP.
    X-Forwarded-For need for if there is another proxy before this gate
    """
    forwarded_for = request.headers.get("X-Forwarded-For")

    if forwarded_for:
        return forwarded_for.split(",")[0].strip()

    return request.remote_addr


def proxy_request(target_server):
    """
    Forward request to the selected server:
    - cnss if the IP is allowed
    - error-server if the IP is blocked
    """

    url = target_server + request.full_path

    if url.endswith("?"):
        url = url[:-1]

    response = requests.request(
        method=request.method,
        url=url,
        headers={
            key: value
            for key, value in request.headers
            if key.lower() != "host"
        },
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False
    )

    excluded_headers = [
        "content-encoding",
        "content-length",
        "transfer-encoding",
        "connection"
    ]

    headers = [
        (name, value)
        for name, value in response.raw.headers.items()
        if name.lower() not in excluded_headers
    ]

    return Response(response.content, response.status_code, headers)


@app.route("/", defaults={"path": ""}, methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
@app.route("/<path:path>", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
def gate(path):
    client_ip = get_client_ip()

    print(f"[GATE] Request from IP: {client_ip}")

    if client_ip in BLOCKED_IPS:
        print(f"[GATE] DENY {client_ip} -> error-server")
        return proxy_request(ERROR_SERVER)

    print(f"[GATE] ALLOW {client_ip} -> cnss")
    return proxy_request(MAIN_SERVER)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
