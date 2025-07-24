FROM ubuntu:22.04 AS base

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-pip \
    python3-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

FROM base AS tools

RUN apt-get update && apt-get install -y --no-install-recommends \
    xvfb \
    x11vnc \
    xdotool \
    novnc \
    && rm -rf /var/lib/apt/lists/*

# Add user and set up VNC password
RUN useradd -m agent && \
    mkdir -p /home/agent/.vnc && \
    x11vnc -storepasswd novnc /home/agent/.vnc/passwd && \
    chown -R agent:agent /home/agent/.vnc

FROM tools AS jupyter

RUN pip3 install --no-cache-dir jupyterlab notebook
COPY requirements.txt /app/requirements.txt
RUN pip3 install --no-cache-dir -r /app/requirements.txt

COPY --chown=agent:agent . /app
WORKDIR /app

USER agent
EXPOSE 8888
EXPOSE 6080

CMD ["/app/start.sh"] 