FROM python:3.12-slim

# Install dependencies for packet capture
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libpcap-dev \
        tcpdump \
        gcc \
        python3-dev && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir scapy netifaces

WORKDIR /app

COPY tproc.py .

# Use ENTRYPOINT so that command-line arguments can be passed
ENTRYPOINT ["python", "tproc.py"]

# Default command (can be overridden)
CMD ["-i", "eth0"]