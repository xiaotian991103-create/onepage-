#!/usr/bin/env python3
"""Catalog PNG/JPEG images without changing their bytes."""

from __future__ import annotations

import argparse
import hashlib
import json
import struct
from pathlib import Path


def png_size(data: bytes) -> tuple[int, int] | None:
    if data[:8] != b"\x89PNG\r\n\x1a\n" or len(data) < 24:
        return None
    return struct.unpack(">II", data[16:24])


def jpeg_size(data: bytes) -> tuple[int, int] | None:
    if data[:2] != b"\xff\xd8":
        return None
    pos = 2
    sof_markers = {
        0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7,
        0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF,
    }
    while pos + 4 <= len(data):
        if data[pos] != 0xFF:
            pos += 1
            continue
        while pos < len(data) and data[pos] == 0xFF:
            pos += 1
        if pos >= len(data):
            return None
        marker = data[pos]
        pos += 1
        if marker in {0xD8, 0xD9}:
            continue
        if pos + 2 > len(data):
            return None
        segment_length = struct.unpack(">H", data[pos:pos + 2])[0]
        if segment_length < 2 or pos + segment_length > len(data):
            return None
        if marker in sof_markers and segment_length >= 7:
            height, width = struct.unpack(">HH", data[pos + 3:pos + 7])
            return width, height
        pos += segment_length
    return None


def inspect(path: Path, relative_to: Path | None = None) -> dict[str, object]:
    data = path.read_bytes()
    size = png_size(data)
    image_format = "PNG" if size else None
    if size is None:
        size = jpeg_size(data)
        image_format = "JPEG" if size else "UNKNOWN"
    width, height = size if size else (None, None)
    resolved = path.resolve()
    display_path = resolved
    if relative_to is not None:
        display_path = resolved.relative_to(relative_to.resolve())
    return {
        "path": str(display_path),
        "filename": path.name,
        "format": image_format,
        "width": width,
        "height": height,
        "aspect_ratio": round(width / height, 6) if width and height else None,
        "bytes": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
    }


def collect(inputs: list[str]) -> list[Path]:
    found: list[Path] = []
    for raw in inputs:
        path = Path(raw)
        if path.is_dir():
            found.extend(
                p for p in sorted(path.rglob("*"))
                if p.is_file() and p.suffix.lower() in {".png", ".jpg", ".jpeg"}
            )
        elif path.is_file():
            found.append(path)
        else:
            raise FileNotFoundError(raw)
    return found


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("inputs", nargs="+", help="Image files or directories")
    parser.add_argument("--output", help="Optional JSON output path")
    parser.add_argument("--relative-to", help="Store paths relative to this directory")
    args = parser.parse_args()

    relative_to = Path(args.relative_to) if args.relative_to else None
    manifest = {"images": [inspect(path, relative_to) for path in collect(args.inputs)]}
    rendered = json.dumps(manifest, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        Path(args.output).write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
