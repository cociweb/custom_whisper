ARG BUILD_FROM
FROM ${BUILD_FROM}

# Install Whisper
WORKDIR /usr/src
ARG WHISPER_VERSION

RUN apt-get update
RUN apt-get install -y --no-install-recommends \
        build-essential \
        netcat-traditional \
        python3 \
        python3-dev \
        python3-pip \
        python3-venv

RUN python3 -m venv myenv \
    && . ./myenv/bin/activate

RUN rm /usr/lib/python3.11/EXTERNALLY-MANAGED

RUN pip3 install --no-cache-dir -U  --upgrade pip
RUN pip3 install --no-cache-dir -U \
        setuptools \
        wheel
RUN pip3 install --no-cache-dir \
        "wyoming-faster-whisper==${WHISPER_VERSION}"
RUN apt-get purge -y --auto-remove \
        build-essential \
        python3-dev
RUN rm -rf /var/lib/apt/lists/*

WORKDIR /
COPY rootfs /
WORKDIR /usr/local/lib/python3.11/dist-packages/wyoming_faster_whisper/
COPY replacables/download.py ./
COPY replacables/__main__.py ./

LABEL org.opencontainers.image.source https://github.com/cociweb/custom_whisper


HEALTHCHECK --interval=5m --timeout=3s --start-period=2m \
   CMD echo '{ "type": "describe" }' | nc -w 1 localhost 10300 | grep -q "faster-whisper" || exit 1