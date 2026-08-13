# Case brief and input roles

Use this reference for a new OnePage case or whenever inputs are incomplete.

## Intake order

1. Identify the intended audience and use: platform showcase, client presentation, internal review, sales case, or campaign recap.
2. Locate the authoritative report and raw evidence.
3. Collect the current OnePage, if any.
4. Collect brand identity and product anchors.
5. Collect real proof visuals: creator frames, product scenes, backend screenshots, or charts.
6. Collect style and layout references.
7. Confirm aspect ratio, generation path, target resolution language, and deadline.

Do not stop for every missing optional item. Produce a missing-input list and ask only when the absence would change facts, brand identity, or the visual direction materially.

If no brand, product, or proof anchor exists, a method-only page may proceed only when the intended story does not require visible brand identity or evidence. Otherwise return `BLOCKED`; never substitute generated packaging, people, screenshots, or charts for missing proof.

## Image role schema

Record every image with:

```json
{
  "image_id": "IMG-01",
  "path": "/absolute/path/image.png",
  "role": "style_anchor",
  "generation_input": true,
  "allowed_influence": ["palette", "card surfaces", "spacing"],
  "forbidden_influence": ["brand", "logo", "copy", "metrics", "PR number"],
  "must_preserve": [],
  "priority": "P1"
}
```

Role definitions:

- `fact_source`: extract facts only; normally exclude from generation.
- `style_anchor`: visual system only.
- `layout_anchor`: hierarchy or information-grammar principle only; never literal topology.
- `brand_identity`: preserve identity cues.
- `product_anchor`: preserve packaging and product appearance.
- `proof_visual`: preserve the specified evidence meaning.
- `edit_target`: current complete image to edit.
- `analysis_only`: library item not used by the generation call.

## Case brief schema

Use `assets/case-brief-template.json` as the starting structure. Key fields:

- `case_id`, `audience`, `purpose`
- `canvas`
- `brand`, `product`
- `source_documents`
- `claims`
- `story`
- `copy_manifest`
- `input_images`
- `reference_selection`
- `visual_construction_plan`
- `execution_budget`
- `constraints`
- `delivery`

After completing the template, run:

```bash
python3 "<skill-directory>/scripts/validate_brief.py" /path/to/case-brief.json
```

Treat validation warnings as items to review, not as permission to invent missing content.

The validator computes `render_authorized`. Do not hand-write a PASS flag. Generation is permitted only when validation returns `render_authorized: true`.

## Required preflight records

- Every claim declares `work_state`, `metric_type`, scope, time window, comparison base, source, approval, and immutable public wording.
- Every proof image declares the claim it supports, selection reason, must-show content, crop anchor, adjacent caption, and forbidden edits.
- Every reference declares atomic lessons and forbidden literal carryover.
- The visual construction plan declares normalized page regions and every visible element's exact primitive, shape, position, treatment, content reference, and evidence role.
- The execution budget declares the risk tier, maximum roots, maximum calls, and one-edit-per-lineage rule.
- Every proof image includes a visual fitness review based on direct inspection; a non-empty caption or selection reason alone is not evidence of fitness.

Read [visual-construction-plan.md](visual-construction-plan.md) for the full preflight standard.

At delivery, validate the actual call history with `scripts/validate_run_log.py`; a declared budget does not prove that the run stayed within it.

## Copy priority

- `P0`: headline, primary result, method name, essential module labels, data source when required.
- `P1`: supporting metrics, short evidence explanations, next step.
- `P2`: long background paragraphs, service capability claims, decorative labels, repeated conclusions.

If the copy exceeds the budget, remove or compress P2 first, then P1 with user approval. Never remove P0 silently.
