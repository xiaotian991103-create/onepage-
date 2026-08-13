# Visual construction plan and originality gate

Read this before the first ImageGen call. Do not render from a mood description alone. First produce a case-specific text wireframe and an element construction table detailed enough for another designer to rebuild the intended page.

## 1. Prove the thesis

- Write one primary thesis as `object + mechanism + result`.
- Bind every material phrase to one or more `LOCKED` claim IDs. Bind proof IDs when the phrase relies on visual evidence.
- Separate `completed_work` from `next_step`. Never draw a future test with the same visual grammar as a completed result.
- Treat words such as `高效`, `稳定`, `健康`, `持续`, `闭环`, `底盘`, `增长`, and `爆款` as strong claims. Remove them unless the ledger contains the scope, time basis, comparison, and evidence needed to support them.
- Do not infer an audience from the person depicted in a creative asset. A content-theme share proves a creative category, not the audience actually reached or converted.

## 2. Define page geometry

Use normalized coordinates from 0 to 100. Record:

- a compact text wireframe showing the page silhouette and reading sequence;
- canvas aspect ratio and safe margin;
- reading path and primary focal point;
- every main region as `x, y, w, h`;
- region purpose, visual weight, background treatment, and shared alignment lines;
- the intended whitespace bands between regions.

Descriptions such as `高级`, `简洁`, `三栏`, or `参考案例排版` are not a visual plan.

## 3. Specify every visible element

Register every P0/P1 text block, KPI, image frame, chart, icon, divider, connector, badge, and conclusion. Each row must state:

- `element_id`, `region_id`, semantic role, content reference, and `x, y, w, h`;
- exact primitive and shape: for example unframed type, flat rectangle, thin rule, two-panel comparison, capsule label, or timeline node;
- fill, stroke, corner radius, shadow, color role, typography role, and relative scale;
- alignment, spacing, layer, reading intent, and the fact or evidence it carries;
- one reference lesson being applied and the literal feature that must not carry over.

Do not allow unregistered filler. Replace vague `card` or `AI科技感图标` instructions with exact construction language.

## 4. Make shapes semantic

- Sequence: timeline, stepped path, or numbered progression only when the facts contain a real order.
- Comparison: split frame, paired bands, or before/after only when both sides are real and comparable.
- Share: bar, proportional strip, or 100-unit field only when the denominator is locked.
- Classification: matrix or grouped bands only when categories are mutually understandable.
- Mechanism: evidence-backed causal chain; never use arrows to imply causality that the facts do not prove.
- Case proof: readable filmstrip or evidence band with an adjacent explanation.

Do not use generic circles connected by arrows, graduation caps, atom icons, target icons, or glossy 3D symbols as substitutes for strategy or evidence. An icon may aid navigation; it may not carry a business claim by itself.

## 5. Build a proof-image storyboard

For every image slot, record:

- source image ID, role, supported claim ID, and why this exact frame is fit for the claim;
- what must be visibly present in the frame;
- frame shape, aspect ratio, normalized bounds, crop anchor, preserved area, and excluded clutter;
- an adjacent caption that states `what is visible + what it supports`;
- optional callout form, minimum legibility, forbidden edits, and a missing-image fallback.
- a `visual_fitness_review` recorded only after direct inspection, with PASS/BLOCKED and a concrete rationale.

A caption such as `案例展示` or `达人素材` is insufficient. A proof image without a supported claim, visible evidence subject, selection reason, and adjacent explanatory caption fails preflight. If an image is only atmospheric, mark it `context_visual` and keep it out of the evidence chain. Never AI-redraw a proof image to make it more convenient.

## 6. Learn from references without copying them

- During analysis, compare two to four relevant cases when available. Extract only one or two atomic lessons from each.
- Record the lesson and the literal features that must not be copied.
- Default a macro-layout reference to `analysis_only`. Prefer at most one style anchor in the generation call.
- A single reference may not control three or more of: page partition, KPI location, module grammar, proof treatment, and conclusion geometry.
- Rebuild the geometry from the current case's evidence volume, product role, thesis, and reading order.
- Record a five-axis geometry signature for both the closest reference and the new plan: region pattern, hero focal position, KPI anchor, evidence grammar, and conclusion geometry. At least three axes must differ.

Write at least three substantive originality transforms across different dimensions: narrative order, hero focal position, region boundaries, KPI anchor, evidence grammar, module shape, or conclusion geometry. Changing only brand, color, copy, numbers, or imagery does not count.

Run all three tests:

1. **Feature concentration:** fail if one reference determines three or more macro features.
2. **Brand-swap:** mentally replace the current brand, product, and copy with the reference's; fail if the page still looks like the same template.
3. **Thumbnail silhouette:** blur text and imagery; fail if region boundaries, focal weight, proof rhythm, and conclusion block match the reference on three of four axes.

## 7. Render authorization card

Before calling ImageGen, show the user a concise authorization card and save the full record. It must include:

- locked thesis and public claims;
- completed work and next steps as separate lists;
- selected visual family and the three originality transforms;
- a text wireframe, region geometry, and the element construction table;
- proof-image storyboard with captions;
- execution risk tier and call budget.

Mark `Data`, `Thesis`, `Copy`, `Image fitness`, `Visual construction`, and `Originality` as PASS or BLOCKED. Call ImageGen only when all six pass. If the user granted full autonomy, do not create six approval pauses: present the card, record the recommended choices, and continue.

Keep the user-visible card compact enough to review in one pass, normally about 600-1200 Chinese characters. Save the complete element table as the authoritative record and link it when it is longer; never omit the concrete element shapes, positions, or image explanations from that record.
