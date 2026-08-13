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
- When routing to a product-led editorial or three-act layout, read [product-led-editorial.md](references/product-led-editorial.md).
- Before approving any visual direction, read [visual-construction-plan.md](references/visual-construction-plan.md).
- Before setting generation and revision budgets, read [execution-policy.md](references/execution-policy.md).
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
  - `layout_anchor`: hierarchy or information-grammar principle only; never literal topology.
  - `brand_identity`: logo, brand color, and identity cues.
  - `product_anchor`: packaging and product appearance.
  - `proof_visual`: real scene or material evidence.
  - `context_visual`: atmosphere or category context only; never factual proof.
  - `edit_target`: the current best whole image; exactly one during an edit.
  - `analysis_only`: style-pool item not sent to ImageGen.
- Record `allowed_influence`, `forbidden_influence`, `must_preserve`, and priority for each generation input.
- Treat missing brand, product, or proof assets as non-blocking only when the approved story can omit those visible elements. If visible identity or evidence is required, stop rather than invent it.

### 2. Build and lock the fact ledger

- Extract facts from reports and evidence before designing.
- Separate internal exact values from approved public render values.
- Record metric type, numerator and denominator when relevant, scope, time window, comparison base, source, wording, work state, and approval state.
- Use only `LOCKED` public values in the visible copy. Never ask ImageGen to calculate, infer, rank, or mask data.
- Keep completed work and future recommendations in separate fields.
- Distinguish a depicted creative theme from a measured audience. Do not call a person shown in content an efficient audience without audience or conversion evidence.
- Stop at the data gate when values conflict or lack approval. Ask one concise question that lists only the unresolved facts.

### 3. Lock the story and copy

- Reduce the case to: result -> business problem -> method -> evidence -> validation -> next step.
- Write one thesis as `object + mechanism + result`, then bind every material phrase to locked claims and proof IDs.
- Remove unsupported summary words such as `高效`, `稳定`, `健康`, `持续`, `闭环`, `底盘`, `增长`, and `爆款`; these are conclusions, not decoration.
- Recommend one main story and at most two alternatives. Do not create visual variants before the story is chosen.
- Prefer one conclusion headline, three primary modules, three to five KPIs, and three to six proof visuals.
- For a 16:9 page, target 180-260 visible Chinese characters and do not exceed about 300 without explicit user approval.
- Prioritize copy as `P0` mandatory, `P1` useful, and `P2` removable. Never silently delete locked copy.
- Export a copy manifest in reading order. Only text in that manifest may appear in the image.

### 4. Select references by function

- Compare two to four relevant cases during analysis when available, but extract only one or two atomic lessons from each.
- Select one coherent visual family. Prefer one `style_anchor`, one brand/product anchor, and the proof visuals required by the story.
- Keep macro-layout references `analysis_only` by default. If a layout image is sent to ImageGen, allow only named hierarchy principles and explicitly forbid literal topology.
- Keep a single ImageGen call to no more than five input images; default to three or fewer when the page is text-heavy.
- Never feed the whole reference library into one call.
- Do not mix conflicting families such as pastel spring, black-gold premium, and dark-red event styles.
- Treat user-provided cases as learning evidence, not templates. Never copy their brands, logos, metrics, dates, watermarks, people, screenshots, page partitions, KPI placement pattern, module grammar, or conclusion geometry as a set.
- Record a reference influence ledger and at least three case-driven macro transforms. Pass feature-concentration, brand-swap, and thumbnail-silhouette tests before rendering.

### 5. Produce the detailed visual construction plan

- Follow [visual-construction-plan.md](references/visual-construction-plan.md).
- Draft a visible text wireframe plus normalized region coordinates, reading path, hierarchy, shared alignment lines, and whitespace bands.
- Specify every visible element: bounds, exact primitive and shape, fill, stroke, radius, shadow, typography role, relative size, alignment, spacing, content reference, evidence, and forbidden carryover.
- Build an image storyboard. Every proof image needs a claim, selection reason, must-show subject, frame and crop plan, adjacent explanatory caption, forbidden edits, and missing-image fallback.
- Give the lower half its own evidence grammar. Reject generic repeated cards, unrelated icons, or circles-and-arrows that do not encode real facts.
- Present a concise render authorization card to the user before generation. If autonomy is granted, present it without pausing; still save the full plan.
- Run `scripts/validate_brief.py`. Do not call ImageGen unless it returns `render_authorized: true`.

### 6. Compile the prompt

- Use the fixed order in [prompt-blueprint.md](references/prompt-blueprint.md).
- Label every input image and state both allowed and forbidden influence.
- Use exactly one layout blueprint and one visual family.
- Compile the approved case-specific geometry and element table. Do not reuse a reference's fixed proportions or prompt block unchanged.
- Quote all visible copy verbatim. State that no other words, digits, logos, footers, watermarks, or labels may appear.
- Repeat data values and units character-for-character in the prompt.
- Require full-canvas framing, 3-4% safe margins, large Chinese typography, high contrast, and no microtext.
- If real proof visuals are not available or cannot be preserved, use clean intentional blanks or omit the proof block with approval; never fabricate proof.

### 7. Generate candidates

- Use built-in ImageGen for normal generation and editing.
- Select `fast`, `standard`, or `high_risk` and enforce the call budget in [execution-policy.md](references/execution-policy.md).
- Generate one strong candidate by default. Generate two candidates only when the user wants a direction choice; vary one visual axis while keeping facts and copy identical.
- Do not create a 2x2 board for a text-dense final unless the user explicitly requests a comparison sheet.
- Save every candidate non-destructively and record parent, prompt, input roles, actual dimensions, and QA status.
- Record phase durations and per-call telemetry so later speed estimates are evidence-based.
- Select one lineage root. Continue edits only from the current best passing ancestor.

### 8. Inspect and revise

- Run rapid QA first. Reject systemic failures or candidates that fail two independent hard-gate categories without spending time on deep QA.
- Run the full rubric only on a rapid-pass candidate promoted as current best, and again on the final candidate.
- Use OCR as a detector and direct visual inspection as the final judge.
- Open the candidate at fit-to-window, 100%, and 200%.
- Create one defect ticket per region and root cause. It may group up to three linked symptoms with one acceptance criterion.
- Permit at most one edit per clean root. Never create an edit of an edit.
- Re-run all hard gates after the edit because untouched regions may drift.
- If an edit fails or causes regression, return to a corrected clean prompt. Abandon a branch immediately for copied structure, fabricated proof, wrong identity, pervasive unreadability, or generic AI diagram drift.
- Do not exceed the selected call budget without reporting exact failed gates and obtaining approval.

### 9. Deliver and learn

- Deliver only a candidate that passes provenance, fact, number, core Chinese text, crop, brand/product, and actual-dimension gates.
- Validate the recorded call graph and actual budget with `scripts/validate_run_log.py`; a preflight budget declaration alone is insufficient.
- Copy the untouched ImageGen output into the project's user-facing output directory with a versioned filename.
- Report the path, actual pixel dimensions, built-in or CLI mode, the final prompt, selected input roles, and any non-blocking caveat.
- Preserve the fact ledger, copy manifest, reference influence ledger, detailed visual plan, authorization card, prompt, execution log, defect tickets, and QA result as intermediate records.
- When the user corrects a recurring rule, update the appropriate reference or routing entry rather than appending a long exception to this file.

## Default decision rules

- Default canvas: landscape 16:9 Chinese marketing case OnePage.
- Default generation path: built-in ImageGen.
- Default structure: one case-specific hierarchy derived from the thesis and evidence; three primary modules are a density limit, not a reusable topology.
- Default style: brand-derived light editorial system unless the brand or event clearly calls for a dark or high-impact family.
- Default human gate: one combined render authorization card covering data, thesis, copy, image fitness, visual construction, originality, and call budget.
- If the user requests full autonomy, use the recommended choices, show the card as a progress artifact, and continue unless a P0 fact or required asset is blocked.
- If exact Chinese, numbers, logo, product, or provenance cannot pass after the allowed retries, return `BLOCKED`; never deliver a known-bad image as complete.
