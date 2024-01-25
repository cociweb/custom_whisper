"""Utility for downloading faster-whisper models."""
import logging
import shutil
import tarfile
import json
from enum import Enum
from pathlib import Path
from typing import Dict, Optional, Union
from urllib.request import urlopen

from .file_hash import get_file_hash

URL_FORMAT = "https://github.com/rhasspy/models/releases/download/v1.0/asr_faster-whisper-{model}.tar.gz"

_LOGGER = logging.getLogger(__name__)


class FasterWhisperModel(str, Enum):
    """Available faster-whisper models."""

    TINY = "tiny"
    TINY_INT8 = "tiny-int8"
    BASE = "base"
    BASE_INT8 = "base-int8"
    SMALL = "small"
    SMALL_INT8 = "small-int8"
    MEDIUM = "medium"
    MEDIUM_INT8 = "medium-int8"
    CUSTOM = "custom"


EXPECTED_HASHES = {
    FasterWhisperModel.TINY: {
        "config.json": "e5a2f85afc17f73960204cad2b002633",
        "model.bin": "c21f8eccfdc11978e9496dcb731c54e2",
        "vocabulary.txt": "c1120a13c94a8cbb132489655cdd1854",
    },
    FasterWhisperModel.TINY_INT8: {
        "config.json": "e5a2f85afc17f73960204cad2b002633",
        "model.bin": "9674f22b7dee7b4d321a46f235ea6c7f",
        "vocabulary.txt": "c1120a13c94a8cbb132489655cdd1854",
    },
    FasterWhisperModel.BASE: {
        "config.json": "e5a2f85afc17f73960204cad2b002633",
        "model.bin": "d2d25254f644c5f8c4cbfcb4f310cffc",
        "vocabulary.txt": "c1120a13c94a8cbb132489655cdd1854",
    },
    FasterWhisperModel.BASE_INT8: {
        "config.json": "e5a2f85afc17f73960204cad2b002633",
        "model.bin": "ecd0fd5e2eb9390a2b31b7dd8d871bd1",
        "vocabulary.txt": "c1120a13c94a8cbb132489655cdd1854",
    },
    FasterWhisperModel.SMALL: {
        "config.json": "e5a2f85afc17f73960204cad2b002633",
        "model.bin": "8b2c0a5013899c255e1f16edc237123b",
        "vocabulary.txt": "c1120a13c94a8cbb132489655cdd1854",
    },
    FasterWhisperModel.SMALL_INT8: {
        "config.json": "e5a2f85afc17f73960204cad2b002633",
        "model.bin": "128d569e7d783f92eb307daa8c58e019",
        "vocabulary.txt": "c1120a13c94a8cbb132489655cdd1854",
    },
    FasterWhisperModel.MEDIUM_INT8: {
        "config.json": "e5a2f85afc17f73960204cad2b002633",
        "model.bin": "99b6aca05c475cbdcc182db2b2aed363",
        "vocabulary.txt": "c1120a13c94a8cbb132489655cdd1854",
    },
}

def download_custom_model(model_url_prefix, dest_dir: Union[str, Path]) -> Path:
    """
    Downloads custom model files: model.bin, vocabulary.txt, config.json and hash.json directly to destination directory.

    Returns directory of downloaded custom model.
    """
    dest_dir = Path(dest_dir)
    model_dir = dest_dir / FasterWhisperModel.CUSTOM.value

    if model_dir.is_dir():
        # Remove model directory if it already exists
        shutil.rmtree(model_dir)

    dest_dir.mkdir(parents=True, exist_ok=True)
    model_dir.mkdir(parents=True, exist_ok=True)
    _LOGGER.debug("Dest_dir is %s and the model_dir is %s", dest_dir, model_dir )


    filelist = ["model.bin", "vocabulary.txt", "config.json", "hash.json"]

    for fname in filelist:
        model_url = model_url_prefix+fname
        try:
            with urlopen(model_url) as d, open(model_dir / fname, "wb") as savefile:
                data = d.read()
                savefile.write(data)
                savefile.close()
                _LOGGER.info("%s is downloaded into %s from url: %s", fname, model_dir, model_url )
        except Exception as e:
            _LOGGER.warning("Download failed on  %s from %s! Info: %s", fname, model_url, e)

    return model_dir


def download_model(model: FasterWhisperModel, dest_dir: Union[str, Path]) -> Path:
    """
    Downloads/extracts tar.gz model directly to destination directory.

    Returns directory of downloaded model.
    """
    dest_dir = Path(dest_dir)
    model_dir = dest_dir / FasterWhisperModel(model).value

    if model_dir.is_dir():
        # Remove model directory if it already exists
        shutil.rmtree(model_dir)

    dest_dir.mkdir(parents=True, exist_ok=True)

    model_url = URL_FORMAT.format(model=FasterWhisperModel(model).value)
    with urlopen(model_url) as response:
        with tarfile.open(mode="r|*", fileobj=response) as tar_gz:
            tar_gz.extractall(dest_dir)

    return model_dir


def find_model(model: FasterWhisperModel, dest_dir: Union[str, Path]) -> Optional[Path]:
    """Returns model directory if model exists."""
    dest_dir = Path(dest_dir)
    model_dir = dest_dir / FasterWhisperModel(model).value

    if FasterWhisperModel(model).value == FasterWhisperModel.CUSTOM.value:
        try:
            with open( model_dir / "hash.json", "r") as hash_file:
                custom_model_hash = json.load(hash_file)
                filtered_files = ["model.bin", "config.json", "vocabulary.txt"]

                expected_hash: Dict[str, str] = {}
                for elements in filtered_files:
                    expected_hash[elements] = custom_model_hash[elements]


        except Exception as e:
            _LOGGER.warning("Retreive of hash failed on custom model: %s", e)
            expected_hash = None
    else:
        expected_hash = EXPECTED_HASHES.get(model.value)

    if expected_hash is None:
        # No expected hash, fall back to checking for a non-empty model.bin file
        model_bin = model_dir / "model.bin"
        if model_bin.exists() and (model_bin.stat().st_size > 0):
            return model_dir

        return None

    model_hash = get_model_hash(model_dir)
    if model_hash == expected_hash:
        # Hashes match
        return model_dir

    # Hashes do not match
    _LOGGER.warning("Model hashes do not match")
    _LOGGER.warning("Expected: %s", expected_hash)
    _LOGGER.warning("Got: %s", model_hash)

    return None


def get_model_hash(model_dir: Union[str, Path]) -> Dict[str, str]:
    """Get hashes for relevant model files."""
    model_dir = Path(model_dir)
    files_to_hash = [
        model_dir / "model.bin",
        model_dir / "config.json",
        model_dir / "vocabulary.txt",
    ]

    model_hash: Dict[str, str] = {}
    for file_to_hash in files_to_hash:
        hash_key = str(file_to_hash.relative_to(model_dir))
        if file_to_hash.exists():
            model_hash[hash_key] = get_file_hash(file_to_hash)
        else:
            # File is missing
            model_hash[hash_key] = ""

    return model_hash
