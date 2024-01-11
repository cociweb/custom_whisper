FROM python:3.11-slim-bookworm


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
WORKDIR /usr/local/lib/python3.11/site-packages/wyoming_faster_whisper-1.0.1.dist-info/
RUN sed -i -e 's/==1.1.0/>=1.1.0/g' \
        -e 's/==0.13.3/>=0.13.3/g' \
        -e 's/Programming Language :: Python :: 3.10/Programming Language :: Python :: 3.11/g' \
        METADATA
WORKDIR /usr/src
RUN pip3 install --no-cache-dir -U --upgrade wyoming ctranslate2 tokenizers
RUN  apt-get purge -y --auto-remove \
        build-essential \
        python3-dev
RUN rm -rf /var/lib/apt/lists/*

WORKDIR /
COPY standalone_whisper/common/run.sh ./
WORKDIR /usr/local/lib/python3.11/site-packages/wyoming_faster_whisper/
COPY standalone_whisper/common/replacables ./


LABEL org.opencontainers.image.source https://github.com/cociweb/custom_whisper


EXPOSE 10300

ENTRYPOINT ["bash", "/run.sh"]

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=30s \
        CMD echo '{ "type": "describe" }' \
        | nc -w 1 localhost 10300 \
        | grep -q "faster-whisper" \
        || exit 1