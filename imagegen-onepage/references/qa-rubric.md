# Whole-image QA and failure routing

Read this before editing or delivering any candidate.

## Output states

- `PASS`: every hard gate passes.
- `REVISE`: a correctable defect remains and a passing ancestor exists.
- `BLOCKED`: facts are unresolved, required identity cannot be preserved, generation mode is unavailable, or retries are exhausted.

Do not use a weighted total to override a failed hard gate.

## Hard gates

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
- Confirm the selected layout family retains its approved asymmetry, region proportions, and distinct information forms; fail generic equal-column or repeated-card drift when the blueprint requires otherwise.

### G. Brand, product, and proof

- Check logo wording and geometry.
- Check packaging name, colors, silhouette, count, and hero-product relationship.
- Fail on invented product labels, fake UI, fake creator identities, or proof visuals that imply evidence not present in the source.
- If proof cannot be preserved, omit it with approval or use an intentional blank; never fabricate it.

### H. Reference contamination

- Confirm no reference brand, metric, date, PR number, watermark, footer, creator, or campaign name entered the candidate.

## Revision protocol

Create one defect ticket. The values below are synthetic placeholders:

```json
{
  "defect_id": "D-01",
  "category": "number",
  "exact_change": "Replace 18W+ with 12W+",
  "locked_invariants": ["all other copy", "layout", "brand", "product", "colors", "canvas"],
  "acceptance_criterion": "The page contains 12W+ exactly once and contains no 18W+"
}
```

Priority:

1. facts and numbers;
2. headline and core Chinese;
3. logo and product;
4. crop and readability;
5. layout;
6. decoration.

Change one category per ImageGen edit. Re-run every hard gate after each edit.

## Failure routing

- One localized defect: one targeted ImageGen edit.
- Same defect fails twice: return to the clean root prompt and regenerate with a simpler region.
- Three or more simultaneous defects or global drift: abandon the branch immediately.
- Mixed style: reduce references to one style anchor and one brand/product anchor.
- Persistent text errors: compress approved P2, then P1 copy; enlarge typography and reduce modules. Never patch text locally.
- Persistent logo/product/proof error: use a cleaner source anchor and fewer references. If still wrong, omit only with approval or return `BLOCKED`.
- Aspect or dimension error: regenerate. Never crop or upscale locally.
- Native 4K hard requirement: inspect the built-in output first. If it is not native 4K, ask for explicit CLI authorization and local API-key setup; never switch silently.
- Built-in ImageGen unavailable: state the CLI fallback and its API-key requirement; wait for explicit approval.
- Three clean full-image regenerations fail: report the exact failed gates and stop.
