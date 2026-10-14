# 《{{title}}》精读笔记（章节全覆盖版）

> 模板：standard / paper-analysis | 目标读者：{{audience}} | 汇报时长：{{duration}} | 侧重：{{focus}}

## 0. 前置速查

### 表 1：基本信息卡

| 项目 | 内容 |
|---|---|
| 论文标题 | {{title}} |
| 发表来源 | {{venue}} |
| 研究领域 | {{field}} |
| 核心问题 | {{core_problem}} |
| 核心方案 | {{core_solution}} |

### 表 2：核心贡献速记

- **思想**：{{contribution_idea}}
- **方法**：{{contribution_method}}
- **效果**：{{contribution_effect}}

### 表 3：全文符号对照表

| 符号 | 全称 | 中文 | 维度 | 首次出现位置 |
|---|---|---|---|---|
{{symbol_table}}

> 规则：所有符号、缩略语第一次出现必须全称 + 中文；本表之外的符号在正文首次出现处就地解释。

---

## 1. 原文章节结构总览

```text
{{section_outline}}
```

---

## 2. 分章节逐节精读

> 硬性要求：原文章节编号必须完全一致；**所有一级、二级章节逐一讲解，不得跳过**；三级及以下按重要性选择性覆盖。
> 每节固定四段式：本节定位 → 核心内容 → 逻辑衔接 → 【隐含逻辑】。

<!-- SECTION:chapter_by_chapter -->

### §1 {{sec1_title}}

- **▶ 本节定位**：{{sec1_role}}
- **▶ 核心内容**：{{sec1_content}}
- **▶ 逻辑衔接**：{{sec1_link}}
- **▶ 【隐含逻辑】**：{{sec1_implicit}}

<!-- SECTION:sec1_intro -->

### §2 {{sec2_title}}

#### §2.1 {{sec2_1_title}}

<!-- SECTION:sec2_1 -->

#### §2.2 {{sec2_2_title}}

<!-- SECTION:sec2_2 -->

### §3 {{sec3_title}}

#### §3.1 {{sec3_1_title}}（整体架构）

<!-- SECTION:sec3_1 -->

#### §3.2 {{sec3_2_title}}

<!-- SECTION:sec3_2 -->

### §4 {{sec4_title}}

#### §4.1 {{sec4_1_title}}（实验设置：数据集、指标、基线、实现细节）

<!-- SECTION:sec4_1 -->

#### §4.2 {{sec4_2_title}}（主实验结果：结果解读、指标意义、数据集差异）

<!-- SECTION:sec4_2 -->

#### §4.3 {{sec4_3_title}}（消融实验：每个消融验证的假设、设置、结论）

<!-- SECTION:sec4_3 -->

### §5 {{sec5_title}}（讨论与结论：总结、局限性、未来工作）

<!-- SECTION:sec5 -->

---

## 3. 整体架构图逐模块详解

**架构总述与数据流方向**：{{architecture_overview}}

{{#if has_architecture_figure}}
> 对应原文图 {{architecture_figure_no}}（素材：`{{architecture_figure_file}}`）
{{/if}}

<!-- SECTION:architecture_modules -->

| 模块 | 输入 | 输出 | 核心操作 | 对应公式 | 设计目的 | 隐含维度 |
|---|---|---|---|---|---|---|
{{architecture_table}}

> 规则：架构图每个框必须覆盖，无遗漏；读者对着本表能复现原图。

---

## 4. 核心创新模块深度拆解

<!-- SECTION:innovation_modules -->

{{innovation_modules}}

---

## 5. 关键公式逐式详解

<!-- SECTION:formulas -->

{{#if formulas}}
{{formulas}}
{{/if}}

> 每个公式必须包含：公式本体（LaTeX）、符号说明（含维度）、物理意义、设计意图、链路位置。

---

## 6. 训练与推理完整流程

### 6.1 训练阶段

- **数据预处理**：{{train_preprocess}}
- **权重初始化**：{{train_init}}
- **优化配置**：{{train_optim}}
- **前向流程**：{{train_forward}}
- **损失构成**：{{train_loss}}
- **反向传播与参数更新/冻结**：{{train_backward}}

```text
{{train_pseudocode}}
```

### 6.2 推理阶段

- **输入格式**：{{infer_input}}
- **前向流程**：{{infer_forward}}
- **后处理**：{{infer_post}}
- **最终输出**：{{infer_output}}

```text
{{infer_pseudocode}}
```

---

## 7. 实验设计与结果深度解读

### 7.1 实验设计逻辑

{{experiment_design}}

### 7.2 主实验结果解读

{{main_results}}

> 规则：所有数字必须解释实际意义，不能只罗列。

### 7.3 消融实验结论

<!-- SECTION:ablations -->

{{ablations}}

---

## 8. 相关工作对比与领域定位

**领域发展时间线**：{{timeline}}

| 对比维度 | {{related_work_1}} | {{related_work_2}} | 本文 |
|---|---|---|---|
{{comparison_table}}

**本文定位**：{{positioning}}

---

## 9. 局限性与可改进方向

- **原文提到的局限性**：{{limitations_stated}}
- **补充的深层局限与适用边界**：{{limitations_implied}}
- **具体改进方向**：{{improvements}}

---

## 10. 对我们研究的落地启发

- **可直接复用的模块**：{{reusable_modules}}
- **可借鉴的设计思想**：{{design_ideas}}
- **可开展的验证实验**：{{followup_experiments}}
- **落地避坑指南**：{{pitfalls}}

---

> 质量红线自查：□ 未照搬摘要 □ 补充推导均标注【隐含逻辑】 □ 数字均解释意义 □ 符号首次出现均全称+中文 □ 一级二级章节无遗漏 □ 章节编号与原文一致
