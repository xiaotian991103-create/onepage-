# Whole-image QA and failure routing

Read this before editing or delivering any candidate.

## Output states

- `PASS`: every hard gate passes.
- `REVISE`: a correctable defect remains and a passing ancestor exists.
- `BLOCKED`: facts are unresolved, required identity cannot be preserved, generation mode is unavailable, or retries are exhausted.

Do not use a weighted total to override a failed hard gate.

## Hard gates

Before deep inspection, use the rapid rejection order in [execution-policy.md](execution-policy.md). Rapid rejection prevents wasting full-QA time on a dead branch; it never replaces final QA.

### A. Provenance

- Confirm the delivered file is the original ImageGen output byte stream copied or renamed without pixel changes.
- Record generation mode, source path, saved path, parent version, prompt, input roles, and SHA-256.
- Fail if any external pixel edit, composition, crop, resize, sharpen, or upscale occurred.

### B. Actual dimensions

- Read actual width and height with `<skill-directory>/scripts/image_manifest.py`.
- Confirm the requested aspect ratio and complete canvas.
- Call it native 4K only when the original output is 3840x2160 or 2160x3840.

### C. Number and acronym whitelist

- Extract every visible digit, percentage, unit, plus sign, `X`, and business acronym.
- Compare them with the copy manifest.
- Fail on extra, missing, swapped, reversed, or malformed strings.
- Explicitly check `CTR`, `CVR`, `ARPU`, `ROI`, CPM, GMV, `0/O`, and `1/l`.

### D. Chinese text

- Require P0 text to be 100% character-accurate.
- Compare P1 text with the copy manifest using OCR and direct visual inspection.
- Fail on pseudo-characters, missing strokes, duplicated strings, homophone substitution, semantic changes, or unquoted filler.
- Treat OCR as a detector, not the sole judge.

### E. Readability

- Fit-to-window: identify the thesis and three to five KPIs immediately.
- 100%: read all intended body copy without guessing.
- 200%: inspect strokes, antialiasing, borders, repeated characters, texture noise, and product edges.
- Fail if body copy is legible only at 200%.

### F. Composition

- Confirm 3-4% safe margins and no cropped edge, title, logo, product, module, KPI, conclusion, or source line.
- Confirm no more than three primary modules plus one KPI area unless the approved brief says otherwise.
- Confirm proof images are large enough to understand and bind visibly to the relevant claim.
- Confirm the candidate follows the approved case-specific region geometry, hierarchy, alignment, whitespace, and distinct information forms; fail generic equal-column or repeated-card drift.

### G. Brand, product, and proof

- Check logo wording and geometry.
- Check packaging name, colors, silhouette, count, and hero-product relationship.
- Fail on invented product labels, fake UI, fake creator identities, or proof visuals that imply evidence not present in the source.
- If proof cannot be preserved, omit it with approval or use an intentional blank; never fabricate it.

### H. Reference contamination

- Confirm no reference brand, metric, date, PR number, watermark, footer, creator, or campaign name entered the candidate.

### I. Thesis integrity

- Match every material thesis phrase to its locked claim and proof binding.
- Fail unsupported summary language such as `高效`, `稳定`, `健康`, `持续`, `闭环`, `底盘`, `增长`, or `爆款`.
- Fail when a creative theme or depicted person is presented as a measured audience without audience evidence.
- Fail when a future recommendation uses the visual grammar of completed work or results.

### J. Proof-image fitness

- Confirm every proof image has a visible evidence subject, one supported claim, a valid selection reason, and an adjacent caption explaining what is visible and what it supports.
- Confirm the frame shape, crop anchor, preserved area, and final legibility match the storyboard.
- Fail irrelevant images, decorative use of proof, tiny unexplained screenshots, mismatched claims, or captions such as `案例展示` that do not interpret the evidence.
- Fail when ImageGen altered a person, product, UI, stain, testimonial, or result while the page still presents it as factual proof.
- Evidence sufficiency is claim-specific, not a fixed thumbnail quota. One real proof may support one modest claim; it may not be duplicated to imply several independent validations.

### K. Visual-plan conformance

- Compare the candidate with every approved region, P0/P1 element, image slot, semantic shape, and conclusion treatment.
- Fail unregistered filler, unexplained ornaments, arbitrary arrows, and icons carrying claims without evidence.
- Fail a lower section made from generic circular icons, repeated cards, or abstract nouns when the facts call for comparisons, proportions, evidence bands, or another meaningful form.

### L. Structural originality

- Confirm at least three approved macro transforms remain visible.
- Re-run feature-concentration, brand-swap, and thumbnail-silhouette tests.
- Fail when changing only brand, palette, text, metrics, or imagery would reveal the same page partition, KPI arrangement, module syntax, proof rhythm, and conclusion geometry as the closest reference.

## Revision protocol

Create one defect ticket per region and root cause:

```json
{
  "defect_id": "D-01",
  "category": "hero-copy",
  "region": "hero KPI rail",
  "root_cause": "two linked KPI strings were transcribed incorrectly",
  "linked_changes": ["Replace 84W+ with 24W+", "Restore CTR to uppercase"],
  "locked_invariants": ["all other copy", "layout", "brand", "product", "colors", "canvas"],
  "acceptance_criterion": "The hero contains 24W+ and CTR exactly once, and contains neither 84W+ nor Ctr"
}
```

Priority:

1. facts and numbers;
2. headline and core Chinese;
3. logo and product;
4. crop and readability;
5. layout;
6. decoration.

Allow up to three linked symptoms only when they share the same region, root cause, and acceptance criterion. Permit one edited child per clean root and never edit an edit. Run rapid global regression after the edit, then full QA on the final candidate.

## Failure routing

- One localized root cause: one targeted ImageGen edit.
- Failed edit or any regression: return to a clean root prompt and regenerate with a corrected or simpler construction plan.
- Two independent hard-gate failures, copied structure, invented proof, generic AI diagram drift, or another global defect: abandon the branch immediately.
- Mixed style: reduce references to one style anchor and one brand/product anchor.
- Persistent text errors: compress approved P2, then P1 copy; enlarge typography and reduce modules. Never patch text locally.
- Persistent logo/product/proof error: use a cleaner source anchor and fewer references. If still wrong, omit only with approval or return `BLOCKED`.
- Aspect or dimension error: regenerate. Never crop or upscale locally.
- Native 4K hard requirement: inspect the built-in output first. If it is not native 4K, ask for explicit CLI authorization and local API-key setup; never switch silently.
- Built-in ImageGen unavailable: state the CLI fallback and its API-key requirement; wait for explicit approval.
- Selected execution budget ends without a pass: report the exact failed gates and smallest viable simplification, then stop.
