#!/usr/bin/env python3
"""Entry point for the news-image-20261120 make.fun entry.

The picture itself is drawn ahead of time by compose.py and stored in
this repository as entry.png. This program's one job is to deliver that
file, byte for byte, to the directory the grader names through the
MAKEFUN_OUTPUT_DIR environment variable.

It uses only the Python standard library, touches no network, and finds
its image relative to its own file, so it behaves identically whatever
working directory it is started from.
"""

import hashlib
import os
import struct
import sys
from pathlib import Path

IMAGE_NAME = "entry.png"
MAX_IMAGE_BYTES = 1_048_576
EXPECTED_DIMENSIONS = (1024, 1024)
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


class DeliveryError(Exception):
    """The bundled image cannot be delivered as the rules require."""


def bundled_image() -> Path:
    """The image committed beside this script."""
    return Path(__file__).resolve().parent / IMAGE_NAME


def check_image(path: Path) -> bytes:
    """Read the bundled image and confirm it is a whole, in-limits PNG."""
    if not path.is_file():
        raise DeliveryError(f"bundled image is missing: {path}")
    data = path.read_bytes()
    if not data.startswith(PNG_SIGNATURE):
        raise DeliveryError("bundled image is not a PNG file")
    if len(data) > MAX_IMAGE_BYTES:
        raise DeliveryError(
            f"bundled image is {len(data)} bytes, over the 1 MiB limit"
        )
    width, height = struct.unpack(">II", data[16:24])
    if (width, height) != EXPECTED_DIMENSIONS:
        raise DeliveryError(
            f"bundled image is {width}x{height}, expected 1024x1024"
        )
    return data


def output_directory() -> Path:
    """The directory the grader named for the delivered image."""
    raw = os.environ.get("MAKEFUN_OUTPUT_DIR", "").strip()
    if not raw:
        raise DeliveryError("MAKEFUN_OUTPUT_DIR is not set")
    return Path(raw)


def deliver(data: bytes, directory: Path) -> Path:
    """Write the image into the output directory and verify the copy."""
    directory.mkdir(parents=True, exist_ok=True)
    target = directory / IMAGE_NAME
    target.write_bytes(data)
    if hashlib.sha256(target.read_bytes()).digest() != hashlib.sha256(data).digest():
        raise DeliveryError("written image does not match the bundled image")
    return target


def main() -> int:
    try:
        data = check_image(bundled_image())
        deliver(data, output_directory())
    except DeliveryError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
