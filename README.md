# ImageGen OnePage Skill

一个面向 Codex 的纯 ImageGen 营销案例 OnePage 工作流。最终交付物必须是由 ImageGen 整图生成或整图编辑得到的位图，不使用 PPT、HTML、SVG、Canvas 或本地脚本拼版。

Skill 位于 [`imagegen-onepage/`](imagegen-onepage/)。将该目录复制到 `~/.codex/skills/` 后，可使用类似请求触发：

> 使用 $imagegen-onepage，把这份营销案例资料生成一张 16:9 中文 OnePage。

新版会在调用 ImageGen 前先输出一张可审核的“渲染授权卡”，包括证据支持的主题、参考案例原创变化、文字线框、区域坐标、逐元素形状与展示方式、图片说明和裁切计划，以及生成次数预算。只有预检脚本返回 `render_authorized: true` 才会生成；交付前还会校验实际调用谱系与预算。

```bash
python3 imagegen-onepage/scripts/validate_brief.py /path/to/case-brief.json
python3 imagegen-onepage/scripts/validate_run_log.py /path/to/run-log.json
```

公开版本包含工作流、数据脱敏规则、提示词蓝图、质量门禁、Brief 模板与校验脚本。为避免版权和项目数据风险，不包含第三方案例原图；实际使用时请提供已获授权的品牌、产品、证据与风格参考。
