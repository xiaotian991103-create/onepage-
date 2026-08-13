# Execution policy

Use this policy to reduce wasted ImageGen calls without weakening any delivery gate.

## Select one risk tier

Count every whole-image generation and whole-image edit as one call.

### Fast

Use only when facts and copy are locked, visible Chinese is at most 180 characters, generation inputs are at most three, one visual family is enough, and no difficult screenshot, logo, product, or multi-SKU fidelity is required.

- Budget: two ImageGen calls.
- Route: one clean root plus either one edit or one replacement clean root, never both.

### Standard

Use by default for one product group, three primary modules, at most three generation inputs by default, and no more than about 240 visible Chinese characters.

- Budget: three calls.
- Route: at most two clean roots and one targeted edit on the best root.
- A clear, front-facing single product anchor may stay Standard. Use High-risk when exact logo or packaging text is P0, the source is small, angled, reflective, occluded, or contains several SKUs.

### High-risk

Use when exact product or logo fidelity, several proof groups, 240-300 visible Chinese characters, four or five difficult inputs, dense screenshots, multiple SKUs, or a native-resolution requirement raises failure risk.

- Budget: four calls and at most three clean roots.
- Tell the user the tier and budget before generation.
- Do not exceed the budget without reporting failed gates and obtaining approval for simplification or more calls.

## One authorization pause

Combine data, thesis, copy, completed/next separation, reference choice, originality transforms, visual construction, proof bindings, and execution budget in the render authorization card. Ask only when a P0 fact is unresolved, a required identity or proof asset is missing, or evidence cannot resolve two materially different stories.

## Rapid QA before full QA

After every call, first check:

1. openable ImageGen raster, correct aspect, and complete canvas;
2. visible P0 headline and primary KPI strings without obvious corruption;
3. no global crop, widespread microtext, fake proof, wrong product, or reference contamination;
4. understandable thesis at fit-to-window;
5. no interchangeable copy of the reference topology;
6. relevant, readable proof images visibly bound to claims and captions;
7. broad conformance to the approved construction plan.

Reject immediately without deep QA when a global defect appears or two independent hard-gate categories fail. A copied topology, invented evidence, wrong identity, pervasive unreadability, or a lower half made of generic icons and repeated cards is a systemic failure. Correct the plan or prompt and create a clean root; do not try to rescue it with local edits.

Run full QA only when a rapid-pass candidate becomes the current best, and again after the final edit before delivery. Rapid QA changes inspection order; it does not replace final QA.

## Keep lineages shallow

Name clean roots `R1`, `R2`, and so on. A root may have at most one edited child such as `R1-E1`.

- Never create an edit of an edit.
- One edit may fix up to three linked symptoms only when they share one region, one root cause, and one acceptance criterion.
- Never mix unrelated fact, copy, identity, proof, and layout defects in one edit.
- Repeat all locked invariants in the edit prompt.
- If the edit fails or causes regression, return to a clean root.

## Record telemetry

Record risk tier, call budget, case start/end, and separate durations for intake, preflight, generation, rapid QA, full QA, tool wait, and user wait. For every call record:

- call ID, root/edit, parent, mode, prompt hash, input roles and count;
- visible-copy count, actual dimensions, elapsed time;
- rapid/full QA result, failed gates, disposition, and regeneration reason.

Before delivery, run `scripts/validate_run_log.py <run-log.json>`. Do not deliver when the actual call count, root count, parent graph, edit depth, required telemetry, or final full-QA status violates the budget.

Do not claim an exact bottleneck without timing records. After at least ten completed cases, calculate median and P90 duration by tier before changing the budgets.

## User updates

Update the user after preflight, after each ImageGen call, before changing locked content or mode, and before exceeding budget. If the budget ends without a pass, list the exact failed gates and the smallest viable simplification. Do not pause for routine QA or one in-budget edit.

Never remove provenance, dimensions, exact P0 text and number checks, claim support, brand/product/proof fidelity, crop/readability, reference contamination, originality, image fitness, thesis integrity, or construction-plan conformance to save time.
