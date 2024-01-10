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
WORKDIR /usr/local/lib/python3.11/dist-packages/wyoming_faster_whisper-1.0.1.dist-info/
RUN sed -i -e 's/==1.1.0/>=1.1.0/g' \
        -e 's/==0.13.3/>=0.13.3/g' \
        -e 's/Programming Language :: Python :: 3.10/Programming Language :: Python :: 3.11/g' \
        METADATA
WORKDIR /usr/src
RUN pip3 install --no-cache-dir -U --upgrade wyoming ctranslate2 tokenizers
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


# Health check
HEALTHCHECK --interval=5m --timeout=3s --start-period=30s \
   CMD nc -z localhost 10300 || exit 1
