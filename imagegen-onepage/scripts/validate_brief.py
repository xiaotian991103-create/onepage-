#!/usr/bin/env python3
"""Validate an imagegen-onepage case brief before generation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def require(data: dict, key: str, errors: list[str]) -> None:
    if key not in data or data[key] in (None, "", [], {}):
        errors.append(f"missing required field: {key}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("brief")
    args = parser.parse_args()

    path = Path(args.brief)
    data = json.loads(path.read_text(encoding="utf-8"))
    errors: list[str] = []
    warnings: list[str] = []

    for key in ("case_id", "audience", "purpose", "canvas", "claims", "story", "copy_manifest", "constraints", "delivery"):
        require(data, key, errors)

    delivery = data.get("delivery", {})
    if delivery.get("final_pixel_source") != "imagegen":
        errors.append("delivery.final_pixel_source must equal 'imagegen'")
    if delivery.get("editable_source_required") is True:
        errors.append("editable_source_required conflicts with the pure ImageGen output contract")

    claims = data.get("claims", [])
    for index, claim in enumerate(claims):
        prefix = f"claims[{index}]"
        for key in ("fact_id", "label", "public_render_value", "source", "approval"):
            if claim.get(key) in (None, ""):
                errors.append(f"{prefix}.{key} is required")
        if claim.get("approval") != "LOCKED":
            warnings.append(f"{prefix} is not LOCKED and must not be rendered")

    copy_manifest = data.get("copy_manifest", [])
    if not any(item.get("priority") == "P0" for item in copy_manifest if isinstance(item, dict)):
        errors.append("copy_manifest must contain at least one P0 item")

    generation_inputs = [
        image for image in data.get("input_images", [])
        if isinstance(image, dict) and image.get("generation_input") is True
    ]
    if len(generation_inputs) > 5:
        errors.append("no more than five input images may be selected for one ImageGen call")
    if len(generation_inputs) > 3:
        warnings.append("text-heavy OnePages usually perform better with three or fewer input images")

    visible_chars = sum(
        len(str(item.get("text", "")))
        for item in copy_manifest if isinstance(item, dict)
    )
    if visible_chars > 300:
        warnings.append(f"visible copy is {visible_chars} characters; compress toward 180-260")

    result = {
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "warnings": warnings,
        "generation_input_count": len(generation_inputs),
        "visible_copy_characters": visible_chars,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
