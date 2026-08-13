#!/usr/bin/env python3
"""Validate an imagegen-onepage render brief before ImageGen is authorized."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


WORK_STATES = {"completed_work", "next_step"}
COPY_STATES = WORK_STATES | {"editorial"}
METRIC_TYPES = {
    "absolute",
    "count",
    "count_share",
    "spend_share",
    "efficiency_rate",
    "uplift",
    "ranking",
    "cumulative",
    "qualitative",
}
IMAGE_ROLES = {
    "fact_source",
    "style_anchor",
    "layout_anchor",
    "brand_identity",
    "product_anchor",
    "proof_visual",
    "context_visual",
    "edit_target",
    "analysis_only",
}
ORIGINALITY_DIMENSIONS = {
    "narrative_order",
    "hero_focal_position",
    "region_boundaries",
    "kpi_anchor",
    "evidence_grammar",
    "module_shape",
    "conclusion_geometry",
}
COMPARISON_TERMS = ("提升", "增长", "降低", "同比", "环比", "高于", "低于", "倍")
STRONG_CLAIM_TERMS = ("高效", "稳定", "健康", "持续", "闭环", "底盘", "增长", "爆款", "高消耗")
GENERIC_AI_TERMS = (
    "glossy 3d icon",
    "ai icon",
    "generic icon",
    "circle icon",
    "circular icon",
    "graduation cap",
    "atom icon",
    "人物图标",
    "毕业帽",
    "原子图标",
    "通用图标",
)
GEOMETRY_AXES = (
    "region_pattern",
    "hero_focal_position",
    "kpi_anchor",
    "evidence_grammar",
    "conclusion_geometry",
)
CLAIM_BEARING_COPY_ROLES = {
    "headline",
    "subtitle",
    "conclusion",
    "metric_value",
    "metric_label",
    "evidence_caption",
    "caption",
}


def empty(value: Any) -> bool:
    return value in (None, "", [], {})


def need(mapping: dict[str, Any], key: str, prefix: str, errors: list[str]) -> None:
    if key not in mapping or empty(mapping[key]):
        errors.append(f"{prefix}.{key} is required")


def check_bbox(value: Any, prefix: str, errors: list[str]) -> None:
    if isinstance(value, dict):
        values = [value.get(key) for key in ("x", "y", "w", "h")]
    elif isinstance(value, list) and len(value) == 4:
        values = value
    else:
        errors.append(f"{prefix} must contain x, y, w, h")
        return
    if any(not isinstance(item, (int, float)) for item in values):
        errors.append(f"{prefix} values must be numbers")
        return
    x, y, width, height = values
    if x < 0 or y < 0 or width <= 0 or height <= 0:
        errors.append(f"{prefix} must use non-negative x/y and positive w/h")
    if x + width > 100 or y + height > 100:
        errors.append(f"{prefix} exceeds the normalized 0-100 canvas")


def unique_id(
    value: Any, prefix: str, seen: set[str], errors: list[str]
) -> str | None:
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{prefix} is required")
        return None
    if value in seen:
        errors.append(f"duplicate ID: {value}")
        return None
    seen.add(value)
    return value


def normalized_text(value: Any) -> str:
    return re.sub(r"[\s，。；：、,.!?！？|｜→+＋×xX()（）\[\]【】\-]", "", str(value)).lower()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("brief")
    args = parser.parse_args()

    path = Path(args.brief)
    data = json.loads(path.read_text(encoding="utf-8"))
    errors: list[str] = []
    warnings: list[str] = []

    required_top = (
        "case_id",
        "audience",
        "purpose",
        "canvas",
        "claims",
        "story",
        "copy_manifest",
        "reference_selection",
        "visual_construction_plan",
        "execution_budget",
        "constraints",
        "delivery",
    )
    for key in required_top:
        if key not in data or empty(data[key]):
            errors.append(f"missing required field: {key}")

    delivery = data.get("delivery", {})
    if delivery.get("final_pixel_source") != "imagegen":
        errors.append("delivery.final_pixel_source must equal 'imagegen'")
    if delivery.get("editable_source_required") is True:
        errors.append("editable_source_required conflicts with the pure ImageGen output contract")

    claim_ids: set[str] = set()
    claim_by_id: dict[str, dict[str, Any]] = {}
    claims = data.get("claims", [])
    for index, claim in enumerate(claims):
        prefix = f"claims[{index}]"
        if not isinstance(claim, dict):
            errors.append(f"{prefix} must be an object")
            continue
        fact_id = unique_id(claim.get("fact_id"), f"{prefix}.fact_id", claim_ids, errors)
        for key in (
            "label",
            "public_render_value",
            "metric_type",
            "source",
            "approval",
            "work_state",
            "wording_lock",
            "priority",
        ):
            need(claim, key, prefix, errors)
        for key in ("scope", "time_window", "comparison_base"):
            if key not in claim:
                errors.append(f"{prefix}.{key} key is required; use null only when inapplicable")
        if claim.get("work_state") not in WORK_STATES:
            errors.append(f"{prefix}.work_state must be completed_work or next_step")
        if claim.get("metric_type") not in METRIC_TYPES:
            errors.append(f"{prefix}.metric_type is unsupported")
        if claim.get("approval") != "LOCKED":
            warnings.append(f"{prefix} is not LOCKED and must not be referenced by visible copy")
        else:
            verification = claim.get("source_verification", {})
            if verification.get("result") != "PASS":
                errors.append(f"{prefix}.source_verification.result must be PASS before LOCKED rendering")
            if empty(verification.get("locator")) or empty(verification.get("rationale")):
                errors.append(f"{prefix}.source_verification requires locator and rationale")
        if fact_id:
            claim_by_id[fact_id] = claim

        metric_text = f"{claim.get('label', '')}{claim.get('wording_lock', '')}"
        numeric = bool(re.search(r"[0-9%％Xx万亿Ww+]", str(claim.get("public_render_value", ""))))
        if numeric:
            if empty(claim.get("scope")):
                errors.append(f"{prefix}.scope is required for a numeric claim")
            if empty(claim.get("time_window")):
                errors.append(f"{prefix}.time_window is required for a numeric claim")
        if claim.get("metric_type") in {"count_share", "spend_share"}:
            if empty(claim.get("numerator")) or empty(claim.get("denominator")):
                errors.append(f"{prefix} share metrics require numerator and denominator")
        if claim.get("metric_type") == "efficiency_rate" and empty(claim.get("formula")):
            errors.append(f"{prefix} efficiency_rate requires formula")
        if "有效" in metric_text and empty(claim.get("threshold")):
            errors.append(f"{prefix} uses 有效 and therefore requires threshold")
        if claim.get("metric_type") == "uplift" or any(term in metric_text for term in COMPARISON_TERMS):
            if empty(claim.get("comparison_base")):
                errors.append(f"{prefix} comparative wording requires comparison_base")
        if any(term in metric_text for term in STRONG_CLAIM_TERMS):
            if empty(claim.get("operational_definition")):
                errors.append(f"{prefix} strong claim wording requires operational_definition")
            if empty(claim.get("scope")) or empty(claim.get("time_window")):
                errors.append(f"{prefix} strong claim wording requires scope and time_window")

    story = data.get("story", {})
    if isinstance(story, dict):
        for key in ("primary_thesis", "business_problem", "completed_work", "evidence_summary", "validation"):
            need(story, key, "story", errors)
        if "next_steps" not in story:
            errors.append("story.next_steps key is required; use [] when none are approved")
        if not empty(story.get("method_steps")) or not empty(story.get("next_step")):
            errors.append("story uses legacy method_steps/next_step; migrate to completed_work/next_steps")
        thesis = story.get("primary_thesis", {})
        if not isinstance(thesis, dict):
            errors.append("story.primary_thesis must be an object")
        else:
            need(thesis, "text", "story.primary_thesis", errors)
            bindings = thesis.get("phrase_bindings", [])
            if empty(bindings):
                errors.append("story.primary_thesis.phrase_bindings is required")
            for index, binding in enumerate(bindings):
                prefix = f"story.primary_thesis.phrase_bindings[{index}]"
                if not isinstance(binding, dict):
                    errors.append(f"{prefix} must be an object")
                    continue
                need(binding, "phrase", prefix, errors)
                fact_id = binding.get("fact_id")
                if fact_id not in claim_by_id:
                    errors.append(f"{prefix}.fact_id references unknown claim {fact_id!r}")
                elif claim_by_id[fact_id].get("approval") != "LOCKED":
                    errors.append(f"{prefix}.fact_id must reference a LOCKED claim")
            thesis_text = normalized_text(thesis.get("text", ""))
            bound_text = "".join(normalized_text(item.get("phrase", "")) for item in bindings if isinstance(item, dict))
            if thesis_text and (not bound_text or not all(char in bound_text for char in thesis_text)):
                errors.append("story.primary_thesis.phrase_bindings must cover every material thesis character")
            if any(term in str(thesis.get("text", "")) for term in STRONG_CLAIM_TERMS):
                bound_claims = [claim_by_id.get(item.get("fact_id"), {}) for item in bindings if isinstance(item, dict)]
                if not bound_claims or any(empty(claim.get("operational_definition")) for claim in bound_claims):
                    errors.append("strong wording in story.primary_thesis requires operational_definition on every bound claim")

        completed = story.get("completed_work", [])
        if empty(completed):
            errors.append("story.completed_work must contain at least one item")
        for index, item in enumerate(completed):
            prefix = f"story.completed_work[{index}]"
            if not isinstance(item, dict):
                errors.append(f"{prefix} must be an object")
                continue
            for key in ("work_id", "text", "claim_ids"):
                need(item, key, prefix, errors)
            for fact_id in item.get("claim_ids", []):
                claim = claim_by_id.get(fact_id)
                if not claim:
                    errors.append(f"{prefix}.claim_ids references unknown claim {fact_id!r}")
                elif claim.get("work_state") != "completed_work":
                    errors.append(f"{prefix} may reference only completed_work claims")
        for index, item in enumerate(story.get("next_steps", [])):
            prefix = f"story.next_steps[{index}]"
            if not isinstance(item, dict):
                errors.append(f"{prefix} must be an object")
                continue
            for key in ("next_id", "text"):
                need(item, key, prefix, errors)
            for fact_id in item.get("claim_ids", []):
                claim = claim_by_id.get(fact_id)
                if not claim or claim.get("work_state") != "next_step":
                    errors.append(f"{prefix}.claim_ids may reference only next_step claims")

    copy_ids: set[str] = set()
    copy_by_id: dict[str, dict[str, Any]] = {}
    copy_manifest = data.get("copy_manifest", [])
    for index, item in enumerate(copy_manifest):
        prefix = f"copy_manifest[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{prefix} must be an object")
            continue
        copy_id = unique_id(item.get("copy_id"), f"{prefix}.copy_id", copy_ids, errors)
        for key in ("text", "priority", "role", "work_state"):
            need(item, key, prefix, errors)
        if "source_claim_ids" not in item:
            errors.append(f"{prefix}.source_claim_ids key is required")
        if item.get("work_state") not in COPY_STATES:
            errors.append(f"{prefix}.work_state is unsupported")
        source_claim_ids = item.get("source_claim_ids", [])
        if item.get("role") in CLAIM_BEARING_COPY_ROLES and empty(source_claim_ids):
            errors.append(f"{prefix} claim-bearing role requires source_claim_ids")
        expected_state = item.get("work_state") if item.get("work_state") in WORK_STATES else None
        for fact_id in source_claim_ids:
            claim = claim_by_id.get(fact_id)
            if not claim:
                errors.append(f"{prefix}.source_claim_ids references unknown claim {fact_id!r}")
            else:
                if claim.get("approval") != "LOCKED":
                    errors.append(f"{prefix} references non-LOCKED claim {fact_id!r}")
                if expected_state and claim.get("work_state") != expected_state:
                    errors.append(f"{prefix} mixes {item.get('work_state')} copy with {claim.get('work_state')} claim")
        if any(term in str(item.get("text", "")) for term in STRONG_CLAIM_TERMS):
            claims_for_copy = [claim_by_id.get(fact_id, {}) for fact_id in source_claim_ids]
            if not claims_for_copy or any(empty(claim.get("operational_definition")) for claim in claims_for_copy):
                errors.append(f"{prefix} strong wording requires operational_definition on every source claim")
        if item.get("work_state") == "next_step" and item.get("role") not in {
            "next_step",
            "next_step_note",
            "recommendation",
            "hypothesis",
        }:
            errors.append(f"{prefix} next_step copy must use an explicit future-facing role")
        if copy_id:
            copy_by_id[copy_id] = item
    if not any(item.get("priority") == "P0" for item in copy_manifest if isinstance(item, dict)):
        errors.append("copy_manifest must contain at least one P0 item")

    image_ids: set[str] = set()
    image_by_id: dict[str, dict[str, Any]] = {}
    for index, image in enumerate(data.get("input_images", [])):
        prefix = f"input_images[{index}]"
        if not isinstance(image, dict):
            errors.append(f"{prefix} must be an object")
            continue
        image_id = unique_id(image.get("image_id"), f"{prefix}.image_id", image_ids, errors)
        for key in (
            "path",
            "role",
            "generation_input",
            "allowed_influence",
            "forbidden_influence",
            "must_preserve",
            "priority",
        ):
            if key not in image or (key not in {"must_preserve"} and empty(image.get(key))):
                errors.append(f"{prefix}.{key} is required")
        if image.get("role") not in IMAGE_ROLES:
            errors.append(f"{prefix}.role is unsupported")
        if image.get("role") == "proof_visual":
            for key in (
                "supports_claim_ids",
                "selection_reason",
                "must_show",
                "frame_shape",
                "crop_anchor",
                "caption_copy_id",
                "forbidden_edits",
            ):
                need(image, key, prefix, errors)
            for fact_id in image.get("supports_claim_ids", []):
                claim = claim_by_id.get(fact_id)
                if not claim:
                    errors.append(f"{prefix}.supports_claim_ids references unknown claim {fact_id!r}")
                elif claim.get("approval") != "LOCKED" or claim.get("work_state") != "completed_work":
                    errors.append(f"{prefix} may support only LOCKED completed_work claims")
            if image.get("caption_copy_id") not in copy_by_id:
                errors.append(f"{prefix}.caption_copy_id references unknown copy")
        elif not empty(image.get("supports_claim_ids")):
            errors.append(f"{prefix}.supports_claim_ids is reserved for proof_visual")
        if image_id:
            image_by_id[image_id] = image

    generation_inputs = [
        image for image in image_by_id.values() if image.get("generation_input") is True
    ]
    if len(generation_inputs) > 5:
        errors.append("no more than five input images may be selected for one ImageGen call")
    if len(generation_inputs) > 3:
        warnings.append("four or five generation inputs require the high_risk tier")

    reference = data.get("reference_selection", {})
    if isinstance(reference, dict):
        for key in ("information_family", "closest_reference", "influence_ledger", "originality_transforms", "originality_tests"):
            need(reference, key, "reference_selection", errors)
        for index, entry in enumerate(reference.get("influence_ledger", [])):
            prefix = f"reference_selection.influence_ledger[{index}]"
            if not isinstance(entry, dict):
                errors.append(f"{prefix} must be an object")
                continue
            for key in ("reference_id", "learn", "do_not_copy", "generation_role"):
                need(entry, key, prefix, errors)
            if "controlled_features" not in entry:
                errors.append(f"{prefix}.controlled_features key is required")
            controlled = entry.get("controlled_features", [])
            if len(entry.get("learn", [])) > 2:
                errors.append(f"{prefix} extracts more than two atomic lessons")
            if len(controlled) > 2:
                errors.append(f"{prefix} controls more than two macro features")
        transforms = reference.get("originality_transforms", [])
        dimensions: set[str] = set()
        for index, transform in enumerate(transforms):
            prefix = f"reference_selection.originality_transforms[{index}]"
            if not isinstance(transform, dict):
                errors.append(f"{prefix} must be an object")
                continue
            for key in ("dimension", "anchor_trait", "transformed_trait", "factual_reason"):
                need(transform, key, prefix, errors)
            dimension = transform.get("dimension")
            if dimension not in ORIGINALITY_DIMENSIONS:
                errors.append(f"{prefix}.dimension is unsupported")
            else:
                dimensions.add(dimension)
        if len(dimensions) < 3:
            errors.append("reference_selection requires at least three distinct macro originality transforms")
        tests = reference.get("originality_tests", {})
        for name in ("feature_concentration", "brand_swap", "thumbnail_silhouette"):
            record = tests.get(name, {}) if isinstance(tests, dict) else {}
            if record.get("result") != "PASS" or empty(record.get("rationale")):
                errors.append(f"reference_selection.originality_tests.{name} requires PASS and rationale")
        closest_signature = reference.get("closest_reference_signature", {})
        for axis in GEOMETRY_AXES:
            need(closest_signature, axis, "reference_selection.closest_reference_signature", errors)

    plan = data.get("visual_construction_plan", {})
    region_ids: set[str] = set()
    element_ids: set[str] = set()
    referenced_copy: set[str] = set()
    referenced_images: set[str] = set()
    caption_elements: set[str] = set()
    if isinstance(plan, dict):
        need(plan, "text_wireframe", "visual_construction_plan", errors)
        geometry_signature = plan.get("geometry_signature", {})
        reference_signature = reference.get("closest_reference_signature", {}) if isinstance(reference, dict) else {}
        changed_axes = 0
        for axis in GEOMETRY_AXES:
            need(geometry_signature, axis, "visual_construction_plan.geometry_signature", errors)
            if not empty(geometry_signature.get(axis)) and not empty(reference_signature.get(axis)):
                if normalized_text(geometry_signature.get(axis)) != normalized_text(reference_signature.get(axis)):
                    changed_axes += 1
        if changed_axes < 3:
            errors.append("visual_construction_plan geometry signature must differ from the closest reference on at least three axes")
        canvas = plan.get("canvas", {})
        for key in ("aspect", "safe_margin_pct", "reading_path", "primary_focal_point"):
            need(canvas, key, "visual_construction_plan.canvas", errors)
        margin = canvas.get("safe_margin_pct")
        if isinstance(margin, (int, float)) and not 3 <= margin <= 6:
            warnings.append("visual_construction_plan.canvas.safe_margin_pct is normally 3-6")

        regions = plan.get("regions", [])
        if len(regions) < 2:
            errors.append("visual_construction_plan.regions must contain at least two regions")
        for index, region in enumerate(regions):
            prefix = f"visual_construction_plan.regions[{index}]"
            if not isinstance(region, dict):
                errors.append(f"{prefix} must be an object")
                continue
            unique_id(region.get("region_id"), f"{prefix}.region_id", region_ids, errors)
            for key in ("purpose", "bbox_pct", "visual_weight", "alignment_edges", "background"):
                need(region, key, prefix, errors)
            check_bbox(region.get("bbox_pct"), f"{prefix}.bbox_pct", errors)

        elements = plan.get("elements", [])
        if len(elements) < 6:
            errors.append("visual_construction_plan.elements must contain at least six elements")
        if len(elements) > 40:
            warnings.append("more than 40 elements increases ImageGen text and layout risk")
        for index, element in enumerate(elements):
            prefix = f"visual_construction_plan.elements[{index}]"
            if not isinstance(element, dict):
                errors.append(f"{prefix} must be an object")
                continue
            unique_id(element.get("element_id"), f"{prefix}.element_id", element_ids, errors)
            for key in (
                "region_id",
                "semantic_role",
                "content_ref",
                "bbox_pct",
                "layer",
                "primitive",
                "shape",
                "style",
                "alignment",
                "spacing",
                "reading_intent",
                "reference_lesson",
                "forbidden",
            ):
                need(element, key, prefix, errors)
            if element.get("region_id") not in region_ids:
                errors.append(f"{prefix}.region_id references unknown region")
            check_bbox(element.get("bbox_pct"), f"{prefix}.bbox_pct", errors)
            for subkey in ("container", "frame", "connector", "radius_px", "stroke", "shadow"):
                if subkey not in element.get("shape", {}):
                    errors.append(f"{prefix}.shape.{subkey} key is required")
            for subkey in ("fill", "text_role", "relative_scale", "color_role"):
                if subkey not in element.get("style", {}):
                    errors.append(f"{prefix}.style.{subkey} key is required")
            content_ref = element.get("content_ref", "")
            descriptor = " ".join(
                str(element.get(key, "")) for key in ("semantic_role", "primitive", "reading_intent")
            ).lower()
            descriptor += " " + json.dumps(element.get("shape", {}), ensure_ascii=False).lower()
            generic_icon = any(term in descriptor for term in GENERIC_AI_TERMS)
            if generic_icon:
                errors.append(f"{prefix} uses a forbidden generic AI icon primitive")
            if content_ref == "none" and element.get("semantic_role") not in {
                "divider",
                "background",
                "support_surface",
                "whitespace",
            }:
                errors.append(f"{prefix}.content_ref none is allowed only for non-semantic structure")
            if content_ref.startswith("copy:"):
                ref_id = content_ref.split(":", 1)[1]
                if ref_id not in copy_by_id:
                    errors.append(f"{prefix}.content_ref references unknown copy {ref_id!r}")
                referenced_copy.add(ref_id)
                if element.get("semantic_role") in {"caption", "image_caption"}:
                    caption_elements.add(ref_id)
            elif content_ref.startswith("claim:"):
                ref_id = content_ref.split(":", 1)[1]
                if ref_id not in claim_by_id:
                    errors.append(f"{prefix}.content_ref references unknown claim {ref_id!r}")
            elif content_ref.startswith("image:"):
                ref_id = content_ref.split(":", 1)[1]
                if ref_id not in image_by_id:
                    errors.append(f"{prefix}.content_ref references unknown image {ref_id!r}")
                referenced_images.add(ref_id)
            elif content_ref != "none":
                errors.append(f"{prefix}.content_ref must start with copy:, claim:, image:, or equal none")

        for copy_id, item in copy_by_id.items():
            if item.get("priority") in {"P0", "P1"} and copy_id not in referenced_copy:
                errors.append(f"copy {copy_id!r} has no visual element in the construction plan")

        image_slots = plan.get("image_slots", [])
        slot_images: set[str] = set()
        for index, slot in enumerate(image_slots):
            prefix = f"visual_construction_plan.image_slots[{index}]"
            if not isinstance(slot, dict):
                errors.append(f"{prefix} must be an object")
                continue
            for key in (
                "image_id",
                "region_id",
                "role",
                "selection_reason",
                "must_show",
                "frame",
                "crop",
                "min_legibility",
                "forbidden",
                "fallback",
            ):
                need(slot, key, prefix, errors)
            image_id = slot.get("image_id")
            slot_images.add(image_id)
            if image_id not in image_by_id:
                errors.append(f"{prefix}.image_id references unknown image")
            if slot.get("region_id") not in region_ids:
                errors.append(f"{prefix}.region_id references unknown region")
            if slot.get("role") == "proof_visual":
                need(slot, "caption_copy_id", prefix, errors)
                need(slot, "caption_logic", prefix, errors)
                review = slot.get("visual_fitness_review", {})
                if review.get("result") != "PASS" or empty(review.get("rationale")):
                    errors.append(f"{prefix}.visual_fitness_review requires PASS and rationale after direct inspection")
                claim_id = slot.get("claim_id")
                claim = claim_by_id.get(claim_id)
                if not claim or claim.get("approval") != "LOCKED" or claim.get("work_state") != "completed_work":
                    errors.append(f"{prefix}.claim_id must reference a LOCKED completed_work claim")
            frame = slot.get("frame", {})
            for key in ("shape", "aspect", "bbox_pct", "radius_px"):
                if key not in frame or empty(frame.get(key)) and key != "radius_px":
                    errors.append(f"{prefix}.frame.{key} is required")
            check_bbox(frame.get("bbox_pct"), f"{prefix}.frame.bbox_pct", errors)
            crop = slot.get("crop", {})
            for key in ("anchor", "preserve", "exclude"):
                if key not in crop or empty(crop.get(key)) and key != "exclude":
                    errors.append(f"{prefix}.crop.{key} is required")
            caption_id = slot.get("caption_copy_id")
            if slot.get("role") == "proof_visual":
                if caption_id not in copy_by_id:
                    errors.append(f"{prefix}.caption_copy_id references unknown copy")
                if caption_id not in caption_elements:
                    errors.append(f"{prefix} requires an adjacent caption element")
                claim_id = slot.get("claim_id")
                if claim_id not in copy_by_id.get(caption_id, {}).get("source_claim_ids", []):
                    errors.append(f"{prefix} caption must reference the same claim")
        for image_id, image in image_by_id.items():
            if image.get("generation_input") is True and image.get("role") in {
                "brand_identity",
                "product_anchor",
                "proof_visual",
                "context_visual",
            }:
                if image_id not in referenced_images:
                    errors.append(f"generation image {image_id!r} has no image element")
            if image.get("role") == "proof_visual" and image_id not in slot_images:
                errors.append(f"proof image {image_id!r} has no storyboard slot")
            if image.get("proof_required") is True and image_id not in slot_images:
                errors.append(f"required proof image {image_id!r} has no storyboard slot")

    budget = data.get("execution_budget", {})
    if isinstance(budget, dict):
        for key in ("tier", "max_clean_roots", "max_edits_per_lineage", "max_total_calls", "quick_reject_before_full_qa"):
            if key not in budget:
                errors.append(f"execution_budget.{key} is required")
        tier = budget.get("tier")
        ceilings = {
            "fast": (2, 2),
            "standard": (2, 3),
            "high_risk": (3, 4),
        }
        if tier not in ceilings:
            errors.append("execution_budget.tier must be fast, standard, or high_risk")
        else:
            roots_limit, calls_limit = ceilings[tier]
            roots = budget.get("max_clean_roots")
            calls = budget.get("max_total_calls")
            if not isinstance(roots, int) or not 1 <= roots <= roots_limit:
                errors.append(f"execution_budget.max_clean_roots exceeds {tier} limit {roots_limit}")
            if not isinstance(calls, int) or not 1 <= calls <= calls_limit:
                errors.append(f"execution_budget.max_total_calls exceeds {tier} limit {calls_limit}")
            if isinstance(roots, int) and isinstance(calls, int) and calls < roots:
                errors.append("execution_budget.max_total_calls cannot be less than max_clean_roots")
        if budget.get("max_edits_per_lineage") not in {0, 1}:
            errors.append("execution_budget.max_edits_per_lineage must be 0 or 1")
        if budget.get("quick_reject_before_full_qa") is not True:
            errors.append("execution_budget.quick_reject_before_full_qa must be true")
        if len(generation_inputs) > 3 and tier != "high_risk":
            errors.append("four or five generation inputs require execution_budget.tier high_risk")

    for fact_id, claim in claim_by_id.items():
        if claim.get("proof_required") is True:
            supported = any(
                fact_id in image.get("supports_claim_ids", [])
                for image in image_by_id.values()
                if image.get("role") == "proof_visual"
            )
            if not supported:
                errors.append(f"claim {fact_id!r} requires proof but no proof_visual supports it")

    visible_chars = sum(len(str(item.get("text", ""))) for item in copy_manifest if isinstance(item, dict))
    if visible_chars > 300:
        warnings.append(f"visible copy is {visible_chars} characters; simplify or use high_risk")
    elif visible_chars > 240 and budget.get("tier") != "high_risk":
        errors.append(f"visible copy is {visible_chars} characters and requires high_risk")
    elif visible_chars > 180 and budget.get("tier") == "fast":
        errors.append(f"visible copy is {visible_chars} characters and exceeds fast tier")

    result = {
        "status": "PASS" if not errors else "FAIL",
        "render_authorized": not errors,
        "errors": errors,
        "warnings": warnings,
        "generation_input_count": len(generation_inputs),
        "visible_copy_characters": visible_chars,
        "planned_element_count": len(plan.get("elements", [])) if isinstance(plan, dict) else 0,
        "planned_image_slot_count": len(plan.get("image_slots", [])) if isinstance(plan, dict) else 0,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
