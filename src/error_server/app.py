from flask import Flask, request

app = Flask(__name__)


@app.route("/", defaults={"path": ""}, methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
@app.route("/<path:path>", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
def error_page(path):
    return f"""
    <h1>Access denied</h1>
    <p>Your IP is blocked or suspicious.</p>
    <p>Your IP from error server view: {request.remote_addr}</p>
    <p>Path: /{path}</p>
    """, 403


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
