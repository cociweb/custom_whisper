# Home Assistant Add-on: Custom Whisper

Customized Whisper add-on for Home Assistant.

The Addon re-uses the original (v1.0.0) [Whisper Add-on](https://github.com/home-assistant/addons/tree/master/whisper) of Nabu Casa / Rhasspy which is based on a [wyoming-whisper](https://github.com/rhasspy/wyoming-faster-whisper) (v1.1.0) and [wyoming](https://github.com/rhasspy/wyoming) (v1.5.2) libraries.


This add-on will be maintained only while the official addon will be able to handle custom models.

Supports [amd64 Architecture][amd64-shield] and [aarch64 Architecture][aarch64-shield] only. Other archs are not planned to be supported!!! See [CTranslate2 HW limitation](https://opennmt.net/CTranslate2/hardware_support.html)

[aarch64-shield]: https://img.shields.io/badge/aarch64-yes-green.svg
[amd64-shield]: https://img.shields.io/badge/amd64-yes-green.svg
[armhf-shield]: https://img.shields.io/badge/armhf-no-red.svg
[armv7-shield]: https://img.shields.io/badge/armv7-no-red.svg
[i386-shield]: https://img.shields.io/badge/i386-no-red.svg

## How to Install as an Add-on for Home-Assistant
1. In Supervisor of Home-Assistant go to the Add-on Store,
2. In the overflow menu click "Repositories"
3. Add `https://github.com/cociweb/custom_whisper/`
4. Wait for the Custom Whisper Add-on to show up or click reload in the same overflow menu
5. Install Custom Whisper Add-on.
6. Follow Documentation, Setup and Install of the Add-on

## How to Install as a Standalone Docker Container


Example [docker-compose.yml](https://raw.githubusercontent.com/cociweb/custom_whisper/main/standalone_whisper/cpu/docker-compose.yml) file.


## How to Install as a Standalone Docker Container with GPU (CUDA) support

Example [docker-compose.yml](https://raw.githubusercontent.com/cociweb/custom_whisper/main/standalone_whisper/cuda/docker-compose.yml) file.
