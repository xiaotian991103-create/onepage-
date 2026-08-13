# Prompt compiler for a complete ImageGen OnePage

Compile prompts in this order. Omit unused fields instead of filling them with generic language.

## 1. Classification and asset

```text
Use case: productivity-visual
Asset type: one complete 16:9 Chinese marketing case-study OnePage infographic, generated as one cohesive raster image
```

## 2. Primary thesis

State one sentence describing what the page must prove. This controls hierarchy; it is not necessarily visible copy.

## 3. Input images

For every generation input, state:

```text
Image 1 = style_anchor. May influence: palette, card surfaces, spacing. Must not influence: brand, logo, copy, metrics, dates, watermark.
Image 2 = product_anchor. Preserve: packaging name, colors, silhouette, product count. Must not invent labels.
Image 3 = proof_visual. Use only as evidence for: <scene>. Do not read metrics from it.
```

Use no more than five inputs. Default to three or fewer for text-heavy pages.

## 4. Case-specific construction blueprint

Choose exactly one information family:

- result-led three-column closure;
- campaign timeline;
- formula matrix;
- model validation split;
- brand-color battlecard;
- product-led editorial three-act;
- dark event spectrum.

Compile the approved text wireframe and normalized region coordinates from [visual-construction-plan.md](visual-construction-plan.md). Name every visible element, its exact shape and treatment, content reference, and reading intent. Require 3-4% safe margins and the complete canvas in frame.

For `product-led editorial three-act`, read [product-led-editorial.md](product-led-editorial.md) and translate its principles into new case-specific geometry. Never reuse a fixed ratio or prompt block unchanged, and do not mix it with a five-stage operations topology.

State the three or more macro transforms from the closest reference. Forbid literal carryover of its page partition, KPI placement, proof treatment, module grammar, and conclusion geometry.

## 5. Visual system

Specify:

- background and brand-derived palette;
- one primary color, one supporting color, one result accent;
- title-bar and card surface treatment;
- typography character: modern Chinese sans serif by default, or one editorial serif plus one crisp sans serif when the selected layout family calls for it;
- proof-image framing and callout treatment;
- human-designed spacing and alignment.

Use one coherent family. Do not mix incompatible references.

## 6. Copy manifest

Provide copy in reading order and quote every visible string:

```text
Text (verbatim; render only these quoted strings):
P0 headline: "..."
P0 subtitle: "..."
P0 module 01: "..."
P0 metric 01 value: "24W+"
P0 metric 01 label: "单条素材消耗"
P1 evidence note 01: "..."
P0 footer: "数据来源：..."
```

State that field names such as `P0 headline` are instructions and must not appear in the image.

## 7. Evidence placement

Bind each proof visual to one claim or method step. For each image specify why it was selected, what must remain visible, its exact frame shape and crop anchor, and an adjacent caption stating what is seen and what it supports. Ask for fewer, larger proof frames. If proof is absent, request a clean blank well or omit the proof section; do not create fake backend UI or fake people as evidence.

## 8. Hard constraints

Always include:

```text
Generate the entire page as one raster artwork through ImageGen.
Render every quoted Chinese character, Latin acronym, digit, unit, plus sign, percent sign, and X exactly.
Do not add any unquoted word, digit, logo, brand, date, PR number, watermark, footnote, QR code, or filler.
Do not copy any text, brand, data, or watermark from style or layout references.
Do not reproduce a reference's topology. Follow only the atomic lessons and the approved originality transforms.
Keep the full 16:9 canvas visible with no cropped title, product, module, KPI, source line, or edge.
Use large readable typography; no microtext.
Preserve approved brand and product anchors faithfully.
```

## 9. Avoid list

```text
Avoid garbled Chinese, pseudo-characters, duplicated text, swapped CTR/CVR/ARPU, O/0 or l/1 confusion, fabricated metrics, crowded screenshots, random English, mixed visual families, copied reference topology, repeated card systems, unexplained images, decorative props without category meaning, glossy 3D icons, excessive glow, generic dashboard UI, circles-and-arrows AI flowcharts, and PowerPoint-template stiffness.
```

## Complete compact skeleton

```text
Use case: productivity-visual
Asset type: one complete 16:9 Chinese marketing case-study OnePage raster image
Primary thesis: <one sentence>
Input images: <numbered role contracts>
Construction: <case-specific regions, element table, semantic shapes, reading order, safe margins, originality transforms>
Style: <one visual family, brand-derived palette, surfaces, typography>
Text (verbatim; render only quoted strings): <ordered copy manifest>
Evidence: <proof-to-claim bindings>
Constraints: <whole-image, exact-copy, no-extra-content, brand, crop rules>
Avoid: <error and style exclusions>
```

## Edit prompt appendix

For an edit, add a defect contract at the end:

```text
Primary edit: correct <one region and one root cause; up to three linked symptoms>.
Acceptance criterion: <one observable pass condition covering the linked symptoms>.
Locked invariants: keep every other title, character, digit, metric, logo, product, proof image, layout boundary, color, background, crop, and canvas dimension unchanged.
```

Repeat all hard constraints. Permit only one edited child per clean root. An ImageGen edit can drift outside the target region, so run rapid global regression first and full QA on the final candidate.
