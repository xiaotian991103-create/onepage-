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

## 4. Layout blueprint

Choose exactly one:

- result-led three-column closure;
- campaign timeline;
- formula matrix;
- model validation split;
- brand-color battlecard;
- product-led editorial three-act;
- dark event spectrum.

Describe top, body, proof, KPI, and footer regions. Require 3-4% safe margins and the complete canvas in frame.

For `product-led editorial three-act`, read [product-led-editorial.md](product-led-editorial.md) and reuse its composition contract and prompt block. Do not mix it with the five-stage operations topology.

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

Provide copy in reading order and quote every visible string. The values below are synthetic placeholders:

```text
Text (verbatim; render only these quoted strings):
P0 headline: "..."
P0 subtitle: "..."
P0 module 01: "..."
P0 metric 01 value: "12W+"
P0 metric 01 label: "单条素材消耗"
P1 evidence note 01: "..."
P0 footer: "数据来源：..."
```

State that field names such as `P0 headline` are instructions and must not appear in the image.

## 7. Evidence placement

Bind each proof visual to one claim or method step. Ask for fewer, larger proof frames. If proof is absent, request a clean blank well or omit the proof section; do not create fake backend UI or fake people as evidence.

## 8. Hard constraints

Always include:

```text
Generate the entire page as one raster artwork through ImageGen.
Render every quoted Chinese character, Latin acronym, digit, unit, plus sign, percent sign, and X exactly.
Do not add any unquoted word, digit, logo, brand, date, PR number, watermark, footnote, QR code, or filler.
Do not copy any text, brand, data, or watermark from style or layout references.
Keep the full 16:9 canvas visible with no cropped title, product, module, KPI, source line, or edge.
Use large readable typography; no microtext.
Preserve approved brand and product anchors faithfully.
```

## 9. Avoid list

```text
Avoid garbled Chinese, pseudo-characters, duplicated text, swapped CTR/CVR/ARPU, O/0 or l/1 confusion, fabricated metrics, crowded screenshots, random English, mixed visual families, equal columns when an unequal editorial layout is selected, repeated card systems, decorative props without category meaning, glossy 3D icons, excessive glow, generic dashboard UI, and PowerPoint-template stiffness.
```

## Complete compact skeleton

```text
Use case: productivity-visual
Asset type: one complete 16:9 Chinese marketing case-study OnePage raster image
Primary thesis: <one sentence>
Input images: <numbered role contracts>
Composition: <one layout blueprint, reading order, safe margins>
Style: <one visual family, brand-derived palette, surfaces, typography>
Text (verbatim; render only quoted strings): <ordered copy manifest>
Evidence: <proof-to-claim bindings>
Constraints: <whole-image, exact-copy, no-extra-content, brand, crop rules>
Avoid: <error and style exclusions>
```

## Edit prompt appendix

For an edit, add a defect contract at the end:

```text
Primary edit: change only <one exact defect>.
Acceptance criterion: <observable pass condition>.
Locked invariants: keep every other title, character, digit, metric, logo, product, proof image, layout boundary, color, background, crop, and canvas dimension unchanged.
```

Repeat all hard constraints. An ImageGen edit can drift outside the target region, so re-run the full QA rubric afterward.
