# Dockerfile
FROM jenkins/jenkins:lts

USER root

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        qemu-system-arm \
        wget \
        git \
        python3 \
        python3-pip \
        python3-venv \
        chromium-driver \
        xvfb \
        ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Python-пакеты с обходом защиты (безопасно в Docker!)
RUN pip3 install --no-cache-dir --break-system-packages \
        pytest \
        requests \
        selenium \
        locust

USER jenkins