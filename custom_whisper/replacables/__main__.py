#!/usr/bin/env python3
import argparse
import asyncio
import logging
from functools import partial
from pathlib import Path
from typing import Optional

from wyoming.info import AsrModel, AsrProgram, Attribution, Info
from wyoming.server import AsyncServer

from .const import WHISPER_LANGUAGES
from .download import FasterWhisperModel, download_model, download_custom_model, find_model
from .faster_whisper import WhisperModel
from .handler import FasterWhisperEventHandler

_LOGGER = logging.getLogger(__name__)


async def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--model",
        required=True,
        choices=list(v.value for v in FasterWhisperModel),
        help="Name of faster-whisper model to use",
    )
    parser.add_argument(
        "--custom_model_url",
        action="store_true",
        help="URL of HuggingFace repository. model.bin, vocabulary.txt, config.json, hash.json is required there!",
        default=False
    )
    parser.add_argument(
        "--custom_model_name",
        action="store_true",
        help="Name of the HuggingFace repository",
        default=False
    )
    parser.add_argument(
        "--uri",
        required=True,
        help="unix:// or tcp://"
    )
    parser.add_argument(
        "--data-dir",
        required=True,
        action="append",
        help="Data directory to check for downloaded models",
    )
    parser.add_argument(
        "--download-dir",
        help="Directory to download models into (default: first data dir)",
    )
    parser.add_argument(
        "--device",
        default="cpu",
        help="Device to use for inference (default: cpu)",
    )
    parser.add_argument(
        "--language",
        help="Default language to set for transcription",
    )
    parser.add_argument(
        "--compute-type",
        default="default",
        help="Compute type (float16, int8, etc.)",
    )
    parser.add_argument(
        "--beam-size",
        type=int,
        default=5,
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Log DEBUG messages"
    )
    args = parser.parse_args()

    if not args.download_dir:
        # Download to first data dir by default
        args.download_dir = args.data_dir[0]

    logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO)
    _LOGGER.debug(args)

    # Look for model
    model = FasterWhisperModel(args.model)
    if args.model.lower() == FasterWhisperModel.CUSTOM:
        asr_model_name = args.model
        asr_model_desc = args.custom_model_name
        asr_model_attr_name = args.custom_model_name
        asr_model_attr_url = args.custom_model_url
    else:
        asr_model_name = model.value
        asr_model_desc = model.value
        asr_model_attr_name = "rhasspy"
        asr_model_attr_url = "https://github.com/rhasspy/models/"

    model_dir: Optional[Path] = None
    for data_dir in args.data_dir:
        model_dir = find_model(model, data_dir)
        if model_dir is not None:
            break
    if model_dir is None:
        if args.model.lower() == FasterWhisperModel.CUSTOM:
            _LOGGER.info("Downloading custom model %s to %s", args.custom_model_name, args.download_dir)
            model_dir = download_custom_model(args.custom_model_url, args.download_dir)
        else:
            _LOGGER.info("Downloading %s to %s", model, args.download_dir)
            model_dir = download_model(model, args.download_dir)

    if args.language == "auto":
        # Whisper does not understand "auto"
        args.language = None

    wyoming_info = Info(
        asr=[
            AsrProgram(
                name="faster-whisper",
                description="Faster Whisper transcription with CTranslate2",
                attribution=Attribution(
                    name="Guillaume Klein",
                    url="https://github.com/guillaumekln/faster-whisper/",
                ),
                installed=True,
                models=[
                    AsrModel(
                        name = asr_model_name,
                        description = asr_model_desc,
                        attribution=Attribution(
                            name = asr_model_attr_name,
                            url = asr_model_attr_url,
                        ),
                        installed=True,
                        languages=WHISPER_LANGUAGES,
                    )
                ],
            )
        ],
    )

    # Load converted faster-whisper model
    _LOGGER.debug("Loading %s", model_dir)
    whisper_model = WhisperModel(
        str(model_dir),
        device=args.device,
        compute_type=args.compute_type,
    )

    server = AsyncServer.from_uri(args.uri)
    _LOGGER.info("Ready")
    model_lock = asyncio.Lock()
    await server.run(
        partial(
            FasterWhisperEventHandler,
            wyoming_info,
            args,
            whisper_model,
            model_lock,
        )
    )


# -----------------------------------------------------------------------------

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
