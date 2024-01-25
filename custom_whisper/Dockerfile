ARG BUILD_FROM
FROM ${BUILD_FROM}



# Install Whisper
WORKDIR /usr/src
ARG WYOMING_FASTER_WHISPER_VERSION

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

WORKDIR /
ADD https://github.com/rhasspy/wyoming-faster-whisper/archive/refs/tags/v${WYOMING_FASTER_WHISPER_VERSION}.tar.gz wyoming_faster_whisper-${WYOMING_FASTER_WHISPER_VERSION}.tar.gz
RUN ls -lah
RUN pip3 install --no-cache-dir wyoming_faster_whisper-${WYOMING_FASTER_WHISPER_VERSION}.tar.gz
#        "wyoming-faster-whisper==${WYOMING_FASTER_WHISPER_VERSION}"
WORKDIR /usr/local/lib/python3.11/dist-packages/wyoming_faster_whisper-${WYOMING_FASTER_WHISPER_VERSION}.dist-info/
RUN ls -lah
RUN sed -i -e 's/==1.2.0/>=1.5.2/g' \
        -e 's/==0.13.3/>=0.15.1/g' \
        METADATA
RUN pip3 install --no-cache-dir -U --upgrade wyoming ctranslate2 tokenizers

WORKDIR /usr/src
RUN apt-get purge -y --auto-remove \
        build-essential \
        python3-dev
RUN rm -rf /var/lib/apt/lists/*

WORKDIR /
COPY rootfs /
WORKDIR /usr/local/lib/python3.11/dist-packages/wyoming_faster_whisper/
COPY replacables/download.py ./
COPY replacables/__main__.py ./
COPY replacables/handler.py ./

LABEL org.opencontainers.image.source https://github.com/cociweb/custom_whisper


# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=30s \
        CMD echo '{ "type": "describe" }' \
        | nc -w 1 localhost 10300 \
        | grep -q "faster-whisper" \
        || exit 1
