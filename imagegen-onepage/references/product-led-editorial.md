# Product-led editorial three-act

Use this layout when a case has a clear product anchor, two strong approved results, three compact method acts, and enough real proof to support an external-facing story. The visual goal is an advertising-quality product hero joined to an editorial evidence report.

Do not use it when the product cannot be shown faithfully, the case needs more than three primary acts, the audience needs a complete operational SOP, or the available evidence is mostly long text.

## Composition contract

- Use one complete 16:9 canvas with 3-4% safe margins.
- Divide height into a 44-47% hero, a 38-42% analytical body, and an 11-15% conclusion region.
- Build the hero as an asymmetric composition, approximately 44:26:24 plus gutters:
  - left: partner identities, editorial headline, subtitle, two hero KPIs, and one thin secondary KPI rail;
  - center: one faithful product group shown at advertising scale, unframed and fully visible;
  - right: one verified result badge and optional real proof.
- Let the product occupy about 21-27% of canvas width and 36-40% of canvas height. A restrained support surface may cross the hero/body boundary by 1-2% of canvas height to create depth.
- Divide the body at about 28% and 60% of canvas width. Use unequal modules near 28:32:40, not equal thirds.
- Top-align all three module titles and body starts. End all body content on one shared baseline.
- Give the three modules different evidence grammars:
  - act I: an unframed three-item strategy list with one consistent line-icon system;
  - act II: up to three horizontal evidence bands, each binding one content theme to real proof and one mechanism statement;
  - act III: a three- or four-node micro-timeline followed by larger result or replication proofs.
- Use only one conclusion treatment: either one editorial summary sentence or one formula line. Do not use both by default.

## Visual system

- Keep neutral white or warm white dominant. Use an approximate role balance of 70% neutral, 20% pale brand tint, 8% dark brand accent, and 2% result accent.
- Localize pale color and soft atmosphere in the hero. Keep dense body-copy surfaces nearly flat and high contrast.
- Use at most two typography roles: a high-contrast Chinese editorial serif for the headline, Roman numerals, and hero KPI values; a crisp Chinese sans serif for labels and body copy.
- Create hierarchy through scale and whitespace. Target headline and KPI values at roughly four to five times the body-copy scale, and module headings at roughly twice the body-copy scale.
- Use thin low-contrast rules for organization. Do not turn the page into a bordered grid.
- Frame only repeated evidence objects. Keep visual corner radii restrained, around 6-8 px at presentation scale, with no shadow or a very light shadow.
- Use one light direction. Optional atmosphere may include one soft directional light band and one small category-relevant tactile prop.
- Treat a result badge or laurel as semantic evidence, not decoration. Use no more than one and only for a locked, supportable result.
- Adapt the product support surface to the category: beauty may use a restrained cosmetic plinth, food a credible table or ingredient context, and technology a simple material plane. Never default every category to a pink pedestal.

## Density limits

- Headline: preferably no more than 16 Chinese characters; subtitle: no more than 24.
- Hero KPIs: exactly two. Secondary KPIs: three to five.
- Product group: one, with no more than two primary SKUs unless the story requires a set.
- Strategy actions: no more than three, with no more than two short lines each.
- Content themes: no more than three.
- Timeline: three or four nodes with no more than three attached data notes.
- Real proof visuals: three to six readable groups across the whole page.
- Visible Chinese copy: target 160-220 characters and do not exceed about 240 without explicit approval.

## Evidence and adaptation rules

- Bind each proof group to exactly one claim. A thumbnail may identify the evidence type; the adjacent locked copy must carry the conclusion.
- Never create fake creators, backend screens, chats, dashboards, awards, or product labels.
- This public skill intentionally bundles no reference-case images. Use this text specification directly or apply it to a user-provided reference under the role contract below.
- When using a user-provided case as the layout or style anchor, forbid all influence from its brand, palette-specific product cues, people, copy, metrics, dates, watermarks, and screenshots.
- Preserve the topology while translating color by role. Do not inherit a reference's pink palette unless it is appropriate to the approved brand.
- Replace category-specific props with meaningful equivalents or remove them. Do not substitute generic decorative spheres, bokeh, or floating objects.
- Do not mix this topology with a five-stage execution topology in the same generation call.

## Prompt block

```text
Layout blueprint: product-led editorial three-act.

Use a complete 16:9 canvas with 3-4% safe margins. Divide the page vertically into a 44-47% product-led hero, a 38-42% three-act analytical body, and an 11-15% single conclusion region.

In the hero, use an asymmetric composition near 44:26:24 plus gutters: oversized editorial title and exactly two dominant KPIs on the left; one large faithful product group on a restrained category-appropriate support surface in the center; one verified result statement and optional real proof on the right. Place 3-5 secondary KPIs in one thin aligned rail.

Below, create exactly three top-aligned modules with approximate widths 28:32:40, separated by thin low-contrast vertical rules. Act I contains three concise strategy actions with one line-icon system. Act II contains no more than three content themes, each bound to readable real proof and one short mechanism statement. Act III contains one three- or four-node timeline and up to three larger result or replication proofs. Give each act a distinct information form; do not make three matching card columns.

Use oversized Chinese editorial serif type only for the headline, Roman numerals, and hero KPI values; use crisp Chinese sans serif for all body copy. Keep the canvas mostly neutral white, derive pale surfaces and dark accents from the supplied brand, use one light direction, avoid decorative objects without category meaning, and render only one final conclusion treatment.
```

## QA checks

- At fit-to-window, identify the product, thesis, and two hero KPIs immediately.
- Confirm the product is unframed, faithful, fully visible, and large enough to act as a visual anchor.
- Confirm the hero remains asymmetric and the body remains unequal at approximately 28:32:40.
- Confirm the three acts use visibly different information forms rather than repeated cards.
- Confirm all proof groups remain understandable and support their adjacent claim.
- Confirm only one final conclusion appears.
- Fail the layout when microtext, equal columns, card repetition, decorative clutter, or an invented badge makes it read like a generic presentation template.
