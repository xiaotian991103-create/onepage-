# Fact ledger and two-layer masking

Read this before placing any metric, date, percentage, comparison, or claim in a OnePage.

## Fact record

Store each claim as. The values below are synthetic placeholders:

```json
{
  "fact_id": "F-01",
  "label": "单条素材消耗",
  "internal_exact": "123456.78",
  "public_render_value": "12W+",
  "unit": "CNY",
  "comparison_base": null,
  "time_window": "2099-01-01/2099-01-08",
  "scope": "示例活动（虚构）",
  "source": "报告章节或证据路径",
  "source_verification": {
    "result": "PASS",
    "locator": "报告页码、表格或证据ID",
    "rationale": "已逐项核对口径与公开文字"
  },
  "approval": "LOCKED",
  "work_state": "completed_work",
  "metric_type": "absolute",
  "operational_definition": null,
  "wording_lock": "单条素材消耗12W+",
  "priority": "P0"
}
```

Approval states:

- `LOCKED`: approved for visible rendering.
- `PROVISIONAL`: useful internally but not renderable.
- `DO_NOT_RENDER`: confidential, conflicting, irrelevant, or rejected.

Only `LOCKED` facts may enter the prompt's visible copy.

User-provided data is not automatically `LOCKED`. Lock it only after the public wording, scope, time window, metric type, source, and any masking have been explicitly approved or reconciled with the authoritative evidence.

## Masking rules

- Keep the exact internal value for traceability; expose only `public_render_value` to ImageGen.
- Treat capitalization, symbols, units, plus signs, `X`, and comparison wording as immutable characters.
- Synthetic examples: `123456.78 -> 12W+`, `68% -> 6X%+`, `123 -> 1XX+` only when the user approves those render values.
- Do not convert a share into an uplift, or an uplift into an absolute result.
- Do not swap `CTR`, `CVR`, `ARPU`, `ROI`, CPM, GMV, or their comparison bases.
- State the relevant scope and period. Do not label an eight-day effective run as the full project cycle.
- Do not mix product-task metrics with overall-project metrics.
- Do not rank values when the source order conflicts.
- Calculate derived values before generation and lock the final string. ImageGen never performs business math.

## Claim integrity

- Separate `completed_work` from `next_step`.
- Do not present a future recommendation as an executed method.
- Tie every business claim to a source or proof visual.
- State whether a number is an absolute value, count share, spend share, efficiency rate, uplift, ranking, or another defined type.
- For a share, record numerator and denominator. For an efficiency rate, record the formula and threshold. For an uplift or comparison, record the baseline. For a highest or cumulative result, record the time window and scope.
- Do not convert a creative label into an audience conclusion. `宝妈题材素材占比` describes a content classification unless platform audience or conversion data proves otherwise.
- Do not use `高效`, `稳定`, `健康`, `持续`, `闭环`, `底盘`, `增长`, or `爆款` as a headline shortcut. Each term needs a locked operational definition, comparison, time basis, and source.
- Do not infer a numerical content ratio merely because a reference case uses one.
- Do not reuse brands, dates, PR numbers, creator names, watermarks, or data visible in style references.

## Copy whitelist

Before generation, create an ordered `copy_manifest`. State in the prompt:

> Only render the quoted strings in this copy manifest. Do not add any other word, digit, brand, date, PR number, watermark, footnote, label, or filler.

Any extra number or business acronym in the output is a hard QA failure.

## Proof binding

- A proof image supports exactly the claim recorded in its `supports_claim_ids`; adjacency alone is not enough.
- A still frame cannot prove a time-based hook such as `三秒前置` unless the source contains time-coded evidence.
- A product-in-scene image proves product presence, not conversion efficiency.
- A person shown in a creator asset proves the creative depiction, not the reached audience.
- If the source image is redrawn, the model-generated person, packaging, UI, stain, testimonial, or result cannot be treated as factual evidence.
