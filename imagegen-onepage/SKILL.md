---
name: imagegen-onepage
description: Generate complete raster marketing case-study OnePage images through ImageGen only. Use when Codex needs to create, redesign, or iterate a Chinese marketing case OnePage, case-review poster, platform showcase infographic, campaign battlecard, 千川/星图案例长图, or any final bitmap whose pixels must come entirely from ImageGen rather than PPT, SVG, HTML, canvas, or local compositing. Handles evidence intake, two-layer data masking, story and copy locking, reference-case routing, prompt compilation, whole-image generation, ImageGen-only corrections, provenance checks, text/data QA, and final delivery.
---

# ImageGen OnePage

Create an evidence-led marketing case OnePage as one cohesive raster image. Treat ImageGen as the final layout and rendering engine, not as a background generator.

## Non-negotiable output contract

- Deliver an original whole-image output returned by ImageGen, or a whole-image edit returned by ImageGen.
- Permit only byte-preserving operations after generation: copy, move, rename, hash, catalog, inspect dimensions, OCR, and visual review.
- Never alter final pixels with PPT, SVG, HTML, canvas, PIL, ImageMagick, Photoshop, code overlays, local compositing, cropping, resizing, sharpening, or upscaling.
- Never generate a background and add text, numbers, logos, screenshots, charts, or decoration outside ImageGen.
- Never combine multiple generated panels into a final page outside ImageGen.
- Make every correction through an ImageGen whole-image edit or a fresh whole-image generation.
- Report the actual pixel dimensions and generation path. Call an output native 4K only when the ImageGen output itself is 3840x2160 or 2160x3840.
- Use the built-in ImageGen path by default. Enter CLI/API mode only after the user explicitly requests it and only when the required tool instructions are available.

## Read the relevant references

- For a new case or incomplete inputs, read [case-brief.md](references/case-brief.md).
- Before exposing any metric or claim, read [data-policy.md](references/data-policy.md).
- When choosing style or layout references, read [reference-library.md](references/reference-library.md).
- Before calling ImageGen, read [prompt-blueprint.md](references/prompt-blueprint.md).
- Before editing or delivering a candidate, read [qa-rubric.md](references/qa-rubric.md).

Resolve every bundled path relative to this skill's directory, not the caller's working directory.

## Workflow

### 1. Stabilize inputs

- Copy temporary attachments into a stable case work directory before analysis.
- Create a manifest with `<skill-directory>/scripts/image_manifest.py`; do not rely on expiring clipboard paths.
- Assign every input image one primary role:
  - `fact_source`: report or backend evidence; never a style source.
  - `style_anchor`: color, surface, spacing, and card language only.
  - `layout_anchor`: topology and hierarchy only.
  - `brand_identity`: logo, brand color, and identity cues.
  - `product_anchor`: packaging and product appearance.
  - `proof_visual`: real scene or material evidence.
  - `edit_target`: the current best whole image; exactly one during an edit.
  - `analysis_only`: style-pool item not sent to ImageGen.
- Record `allowed_influence`, `forbidden_influence`, `must_preserve`, and priority for each generation input.
- Treat missing brand, product, or proof assets as non-blocking only when the approved story can omit those visible elements. If visible identity or evidence is required, stop rather than invent it.

### 2. Build and lock the fact ledger

- Extract facts from reports and evidence before designing.
- Separate internal exact values from approved public render values.
- Record scope, time window, comparison base, source, wording, and approval state.
- Use only `LOCKED` public values in the visible copy. Never ask ImageGen to calculate, infer, rank, or mask data.
- Keep completed work and future recommendations in separate fields.
- Stop at the data gate when values conflict or lack approval. Ask one concise question that lists only the unresolved facts.

### 3. Lock the story and copy

- Reduce the case to: result -> business problem -> method -> evidence -> validation -> next step.
- Recommend one main story and at most two alternatives. Do not create visual variants before the story is chosen.
- Prefer one conclusion headline, three primary modules, three to five KPIs, and three to six proof visuals.
- For a 16:9 page, target 180-260 visible Chinese characters and do not exceed about 300 without explicit user approval.
- Prioritize copy as `P0` mandatory, `P1` useful, and `P2` removable. Never silently delete locked copy.
- Export a copy manifest in reading order. Only text in that manifest may appear in the image.

### 4. Select references by function

- Select one coherent visual family from the text-only routing catalog or user-provided cases.
- Prefer one `style_anchor`, optionally one `layout_anchor`, one brand/product anchor, and up to two proof visuals.
- Keep a single ImageGen call to no more than five input images; default to three or fewer when the page is text-heavy.
- Never feed a whole user-provided reference set into one call.
- Do not mix conflicting families such as pastel spring, black-gold premium, and dark-red event styles.
- Treat user-provided cases as style and layout evidence only. Never copy their brands, logos, PR numbers, watermarks, dates, text, or metrics.

### 5. Compile the prompt

- Use the fixed order in [prompt-blueprint.md](references/prompt-blueprint.md).
- Label every input image and state both allowed and forbidden influence.
- Use exactly one layout blueprint and one visual family.
- Quote all visible copy verbatim. State that no other words, digits, logos, footers, watermarks, or labels may appear.
- Repeat data values and units character-for-character in the prompt.
- Require full-canvas framing, 3-4% safe margins, large Chinese typography, high contrast, and no microtext.
- If real proof visuals are not available or cannot be preserved, use clean intentional blanks or omit the proof block with approval; never fabricate proof.

### 6. Generate candidates

- Use built-in ImageGen for normal generation and editing.
- Generate one strong candidate by default. Generate two candidates only when the user wants a direction choice; vary one visual axis while keeping facts and copy identical.
- Do not create a 2x2 board for a text-dense final unless the user explicitly requests a comparison sheet.
- Save every candidate non-destructively and record parent, prompt, input roles, actual dimensions, and QA status.
- Select one lineage root. Continue edits only from the current best passing ancestor.

### 7. Inspect and revise

- Run the full rubric in [qa-rubric.md](references/qa-rubric.md) after every generation and every edit.
- Use OCR as a detector and direct visual inspection as the final judge.
- Open the candidate at fit-to-window, 100%, and 200%.
- Create one defect ticket per revision: category, exact change, locked invariants, and acceptance criterion.
- Change one variable per ImageGen edit. Repeat all invariants even for a small correction.
- Re-run all hard gates after the edit because untouched regions may drift.
- After two failed edits of the same defect, return to the clean prompt and regenerate. After three or more simultaneous defects, abandon the branch immediately.
- Do not exceed three clean full-image regenerations without reporting the remaining blocker.

### 8. Deliver and learn

- Deliver only a candidate that passes provenance, fact, number, core Chinese text, crop, brand/product, and actual-dimension gates.
- Copy the untouched ImageGen output into the project's user-facing output directory with a versioned filename.
- Report the path, actual pixel dimensions, built-in or CLI mode, the final prompt, selected input roles, and any non-blocking caveat.
- Preserve the fact ledger, copy manifest, prompt, reference selection, defect tickets, and QA result as intermediate records.
- When the user corrects a recurring rule, update the appropriate reference or routing entry rather than appending a long exception to this file.

## Default decision rules

- Default canvas: landscape 16:9 Chinese marketing case OnePage.
- Default generation path: built-in ImageGen.
- Default structure: result-led headline, three primary modules, proof evidence, KPI validation, one conclusion.
- Default style: brand-derived light editorial system unless the brand or event clearly calls for a dark or high-impact family.
- Default human gates: data lock, story lock, visual direction lock.
- If the user requests full autonomy, use the recommended choices and still record all three gate decisions in the manifest.
- If exact Chinese, numbers, logo, product, or provenance cannot pass after the allowed retries, return `BLOCKED`; never deliver a known-bad image as complete.
