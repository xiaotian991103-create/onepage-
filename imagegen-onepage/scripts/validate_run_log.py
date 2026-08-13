#!/usr/bin/env python3
"""Validate actual ImageGen call lineage and budget before delivery."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


PHASES = ("intake", "preflight", "generation", "rapid_qa", "full_qa", "tool_wait", "user_wait")
CALL_FIELDS = (
    "call_id",
    "kind",
    "parent_id",
    "mode",
    "prompt_sha256",
    "input_count",
    "input_roles",
    "visible_copy_characters",
    "actual_dimensions",
    "elapsed_seconds",
    "rapid_qa",
    "full_qa",
    "disposition",
)


def missing(value: Any) -> bool:
    return value in (None, "", [], {})


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("run_log")
    args = parser.parse_args()

    path = Path(args.run_log)
    data = json.loads(path.read_text(encoding="utf-8"))
    errors: list[str] = []

    brief_path = Path(str(data.get("case_brief_path", "")))
    if not brief_path.is_absolute() or not brief_path.is_file():
        errors.append("case_brief_path must be an existing absolute file")
        budget: dict[str, Any] = {}
    else:
        brief = json.loads(brief_path.read_text(encoding="utf-8"))
        budget = brief.get("execution_budget", {})
        if data.get("case_id") != brief.get("case_id"):
            errors.append("run log case_id must match case brief")

    for key in ("case_id", "started_at", "ended_at", "phase_durations_minutes", "calls", "delivery_call_id"):
        if key not in data or missing(data.get(key)):
            errors.append(f"{key} is required")

    durations = data.get("phase_durations_minutes", {})
    for phase in PHASES:
        value = durations.get(phase)
        if not isinstance(value, (int, float)) or value < 0:
            errors.append(f"phase_durations_minutes.{phase} must be a non-negative number")

    calls = data.get("calls", [])
    call_by_id: dict[str, dict[str, Any]] = {}
    root_count = 0
    edits_per_root: dict[str, int] = {}
    for index, call in enumerate(calls):
        prefix = f"calls[{index}]"
        if not isinstance(call, dict):
            errors.append(f"{prefix} must be an object")
            continue
        for field in CALL_FIELDS:
            if field not in call or field != "parent_id" and missing(call.get(field)):
                errors.append(f"{prefix}.{field} is required")
        call_id = call.get("call_id")
        if call_id in call_by_id:
            errors.append(f"duplicate call_id {call_id!r}")
        elif isinstance(call_id, str) and call_id:
            call_by_id[call_id] = call
        kind = call.get("kind")
        if kind == "root":
            root_count += 1
            if call.get("parent_id") is not None:
                errors.append(f"{prefix} root must have null parent_id")
        elif kind == "edit":
            parent_id = call.get("parent_id")
            parent = call_by_id.get(parent_id)
            if not parent:
                errors.append(f"{prefix} edit parent must appear earlier in the log")
            elif parent.get("kind") != "root":
                errors.append(f"{prefix} edit parent must be a clean root; edit-of-edit is forbidden")
            else:
                edits_per_root[parent_id] = edits_per_root.get(parent_id, 0) + 1
        else:
            errors.append(f"{prefix}.kind must be root or edit")
        if not re.fullmatch(r"[0-9a-f]{64}", str(call.get("prompt_sha256", ""))):
            errors.append(f"{prefix}.prompt_sha256 must be 64 lowercase hex characters")
        dimensions = call.get("actual_dimensions", {})
        if not isinstance(dimensions.get("width"), int) or dimensions.get("width", 0) <= 0:
            errors.append(f"{prefix}.actual_dimensions.width must be a positive integer")
        if not isinstance(dimensions.get("height"), int) or dimensions.get("height", 0) <= 0:
            errors.append(f"{prefix}.actual_dimensions.height must be a positive integer")
        if not isinstance(call.get("elapsed_seconds"), (int, float)) or call.get("elapsed_seconds", 0) <= 0:
            errors.append(f"{prefix}.elapsed_seconds must be positive")
        if call.get("rapid_qa", {}).get("status") not in {"PASS", "FAIL"}:
            errors.append(f"{prefix}.rapid_qa.status must be PASS or FAIL")
        if call.get("full_qa", {}).get("status") not in {"PASS", "FAIL", "NOT_RUN"}:
            errors.append(f"{prefix}.full_qa.status must be PASS, FAIL, or NOT_RUN")

    if isinstance(budget.get("max_total_calls"), int) and len(calls) > budget["max_total_calls"]:
        errors.append("actual ImageGen calls exceed execution_budget.max_total_calls")
    if isinstance(budget.get("max_clean_roots"), int) and root_count > budget["max_clean_roots"]:
        errors.append("actual clean roots exceed execution_budget.max_clean_roots")
    max_edits = budget.get("max_edits_per_lineage")
    if isinstance(max_edits, int):
        for root_id, count in edits_per_root.items():
            if count > max_edits:
                errors.append(f"root {root_id!r} exceeds max_edits_per_lineage")

    delivery_id = data.get("delivery_call_id")
    delivery_call = call_by_id.get(delivery_id)
    if not delivery_call:
        errors.append("delivery_call_id must reference a recorded call")
    else:
        if delivery_call.get("rapid_qa", {}).get("status") != "PASS":
            errors.append("delivery call must pass rapid QA")
        if delivery_call.get("full_qa", {}).get("status") != "PASS":
            errors.append("delivery call must pass full QA")
        if delivery_call.get("disposition") != "delivered":
            errors.append("delivery call disposition must equal delivered")

    result = {
        "status": "PASS" if not errors else "FAIL",
        "delivery_authorized": not errors,
        "errors": errors,
        "actual_calls": len(calls),
        "actual_clean_roots": root_count,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
