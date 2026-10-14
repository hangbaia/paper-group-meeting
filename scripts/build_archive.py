#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""按学术规范归档组会材料包。

用法示例：
  python build_archive.py --title "Attention-Is-All-You-Need" --output-root "./group-meeting-materials" \
    --paper "F:/papers/attention.pdf" --parsed "F:/temp/论文结构化全文.md" --images "F:/temp/图片素材" \
    --analysis "论文精读笔记.md" --glossary "术语大白话解释.md" \
    --outline "PPT汇报大纲.md" --pptx "组会汇报.pptx" \
    --script "逐页讲稿.md" --guide "演讲指南与QA预案.md"

未提供的可选文件会被跳过，并在 README.md 中标注缺失项。
"""

from __future__ import annotations

import argparse
import shutil
import sys
from datetime import date
from pathlib import Path

SECTIONS = {
    "00_原文与解析素材": "原论文、结构化全文、公式与图片素材",
    "01_论文深度解读": "章节全覆盖的精读级论文理解",
    "02_专业术语表": "核心术语的中英对照与大白话解释",
    "03_PPT相关": "PPT 汇报大纲与生成的 PPTX 文件",
    "04_演讲准备": "逐页讲稿、演讲指南与 Q&A 预案",
}

FILE_MAP = [
    ("paper", "00_原文与解析素材", "原论文.pdf", "论文原文 PDF"),
    ("parsed", "00_原文与解析素材", "论文结构化全文.md", "保留原文章节层级的结构化全文"),
    ("formulas", "00_原文与解析素材", "公式汇总.tex", "全文公式的 LaTeX 汇总"),
    ("analysis", "01_论文深度解读", "论文精读笔记（章节全覆盖版）.md", "精读级论文解读，一级/二级章节全覆盖"),
    ("glossary", "02_专业术语表", "术语大白话解释.md", "专业术语的学术定义 + 大白话解释"),
    ("outline", "03_PPT相关", "PPT汇报大纲.md", "PPT 大纲，可直接交给 ppt-master 重新生成"),
    ("pptx", "03_PPT相关", "组会汇报.pptx", "组会汇报 PPT 文件"),
    ("script", "04_演讲准备", "逐页讲稿.md", "逐页口语化讲稿，含时长标注"),
    ("guide", "04_演讲准备", "演讲指南与QA预案.md", "汇报逻辑、时间分配、Q&A 预案与技巧"),
]

README_TEMPLATE = """# {title} 组会材料包

生成日期：{today}
汇报时长设定：{duration}

## 目录说明

| 目录 | 内容 |
|---|---|
{section_rows}

## 建议使用顺序

1. 先读 `01_论文深度解读/论文精读笔记（章节全覆盖版）.md`，建立全局认知；遇到不懂的术语查 `02_专业术语表/`。
2. 打开 `03_PPT相关/组会汇报.pptx` 对照 `PPT汇报大纲.md` 检查要点是否有遗漏。
3. 按 `04_演讲准备/逐页讲稿.md` 练习一遍，卡壳处回看 `演讲指南与QA预案.md` 的对应预案。
4. 汇报前重点过一遍 `演讲指南与QA预案.md` 的时间分配表与 Q&A 部分。

## 文件清单

{file_rows}

## 素材来源

- 原文解析：{parse_engine}
- PPT 生成：{ppt_engine}

> 本材料仅用于个人学习汇报，请尊重论文版权。
"""


def _section_rows() -> str:
    return "\n".join(f"| `{name}/` | {desc} |" for name, desc in SECTIONS.items())


def main() -> int:
    parser = argparse.ArgumentParser(description="归档组会材料包")
    parser.add_argument("--title", required=True, help="论文短标题")
    parser.add_argument("--output-root", required=True, help="归档根目录")
    parser.add_argument("--date", default=date.today().strftime("%Y%m%d"), help="日期，默认今天")
    parser.add_argument("--duration", default="15min", help="汇报时长设定")
    parser.add_argument("--parse-engine", default="MinerU", help="解析引擎说明")
    parser.add_argument("--ppt-engine", default="ppt-master", help="PPT 生成引擎说明")
    parser.add_argument("--images", help="图片素材目录（整个目录复制）")
    for key, _, _, _ in FILE_MAP:
        parser.add_argument(f"--{key}", help=f"对应文件：{key}")
    args = parser.parse_args()

    archive = Path(args.output_root).expanduser().resolve() / f"{args.title}_组会材料_{args.date}"
    archive.mkdir(parents=True, exist_ok=True)
    for name in SECTIONS:
        (archive / name).mkdir(exist_ok=True)

    copied: list[str] = []
    missing: list[str] = []

    for key, section, target_name, _desc in FILE_MAP:
        src_value = getattr(args, key)
        if not src_value:
            missing.append(f"{section}/{target_name}（未提供）")
            continue
        src = Path(src_value).expanduser().resolve()
        if not src.is_file():
            missing.append(f"{section}/{target_name}（源文件不存在：{src}）")
            continue
        shutil.copy2(src, archive / section / target_name)
        copied.append(f"{section}/{target_name}")

    if args.images:
        images_src = Path(args.images).expanduser().resolve()
        if images_src.is_dir():
            target = archive / "00_原文与解析素材" / "图片素材"
            if target.exists():
                shutil.rmtree(target)
            shutil.copytree(images_src, target)
            copied.append(f"00_原文与解析素材/图片素材/（{len(list(target.iterdir()))} 个条目）")
        else:
            missing.append("00_原文与解析素材/图片素材/（源目录不存在）")
    else:
        missing.append("00_原文与解析素材/图片素材/（未提供）")

    readme = README_TEMPLATE.format(
        title=args.title,
        today=args.date,
        duration=args.duration,
        section_rows=_section_rows(),
        file_rows="\n".join(f"- [x] `{item}`" for item in copied)
        + ("\n" + "\n".join(f"- [ ] {item}" for item in missing) if missing else ""),
        parse_engine=args.parse_engine,
        ppt_engine=args.ppt_engine,
    )
    (archive / "README.md").write_text(readme, encoding="utf-8")

    print(f"ARCHIVE_PATH={archive}")
    print(f"已归档 {len(copied)} 项，缺失 {len(missing)} 项")
    for item in missing:
        print(f"  缺失: {item}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
