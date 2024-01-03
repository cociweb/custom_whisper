FROM python:3.11-slim-bookworm

# Install Whisper
WORKDIR /usr/src


RUN apt-get update
RUN apt-get install -y --no-install-recommends \
        build-essential \
        netcat-traditional
RUN pip3 install --no-cache-dir -U  --upgrade pip
RUN pip3 install --no-cache-dir -U \
        setuptools \
        wheel
RUN pip3 install --no-cache-dir \
        --extra-index-url https://www.piwheels.org/simple \
        "wyoming-faster-whisper==1.0.1"
RUN  apt-get purge -y --auto-remove \
        build-essential \
        python3-dev
RUN rm -rf /var/lib/apt/lists/*

WORKDIR /
COPY standalone_whisper/run.sh ./
WORKDIR /usr/local/lib/python3.11/site-packages/wyoming_faster_whisper/
COPY standalone_whisper/replacables ./
# COPY replacables/__main__.py ./

LABEL org.opencontainers.image.source https://github.com/cociweb/custom_whisper

#USER nobody
EXPOSE 10300

ENTRYPOINT ["bash", "/run.sh"]

HEALTHCHECK --interval=5m --timeout=3s --start-period=10m \
   CMD echo '{ "type": "describe" }' | nc -w 1 localhost 10300 | grep -q "faster-whisper" || exit 1