#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""MinerU 不可用时的降级 PDF 解析器（基于 PyMuPDF）。

产出：
  {out}/论文结构化全文.md   分页正文 + 启发式章节标题层级
  {out}/图片素材/p{N}_img{M}.png  每页内嵌图片
  {out}/图片素材/提取说明.md      提取失败/被跳过的图片位置记录

用法：
  python pdf_fallback.py "paper.pdf" -o "F:/temp/group-meeting-xxx"
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

HEADING_RE = re.compile(r"^\s*(\d{1,2}(?:\.\d{1,2}){0,3})\.?\s+([A-Z\u4e00-\u9fff][^\n]{0,80})$")
MIN_IMAGE_BYTES = 3 * 1024


def _level(numbering: str) -> int:
    return min(numbering.count(".") + 1, 6)


def parse_pdf(pdf_path: Path, out_dir: Path) -> int:
    try:
        import pymupdf as fitz  # PyMuPDF >= 1.24
    except ImportError:
        try:
            import fitz
        except ImportError:
            print("ERROR: 需要 PyMuPDF，请执行 pip install pymupdf", file=sys.stderr)
            return 2

    out_dir.mkdir(parents=True, exist_ok=True)
    images_dir = out_dir / "图片素材"
    images_dir.mkdir(exist_ok=True)

    doc = fitz.open(pdf_path)
    md_lines: list[str] = [f"# {pdf_path.stem}（PyMuPDF 降级解析）", ""]
    notes: list[str] = []
    image_count = 0

    for page_index in range(doc.page_count):
        page_no = page_index + 1
        page = doc[page_index]
        md_lines.append(f"\n<!-- 原文第 {page_no} 页 -->\n")

        for block in page.get_text("dict")["blocks"]:
            if block.get("type") == 1:
                image_count += 1
                raw = block.get("image") or b""
                name = f"p{page_no}_img{image_count}.png"
                if len(raw) < MIN_IMAGE_BYTES:
                    notes.append(f"- 第 {page_no} 页第 {image_count} 张图：尺寸过小（{len(raw)} 字节），已跳过")
                    continue
                try:
                    (images_dir / name).write_bytes(raw)
                    md_lines.append(f"\n![原文第 {page_no} 页插图](../图片素材/{name})\n")
                except OSError as exc:
                    notes.append(f"- 第 {page_no} 页第 {image_count} 张图：写入失败（{exc}）")
                continue

            text = "\n".join(
                span["text"] for line in block.get("lines", []) for span in line.get("spans", [])
            ).strip()
            if not text:
                continue
            match = HEADING_RE.match(text)
            if match and len(text) < 90:
                md_lines.append(f"\n{'#' * (_level(match.group(1)) + 1)} {match.group(1)} {match.group(2)}\n")
            else:
                md_lines.append(text + "\n")

    page_count = doc.page_count
    doc.close()

    (out_dir / "论文结构化全文.md").write_text("\n".join(md_lines), encoding="utf-8")

    if notes:
        (images_dir / "提取说明.md").write_text(
            "# 图片提取说明\n\n以下位置未能成功提取图片，请在解读文档中标注：\n\n" + "\n".join(notes) + "\n",
            encoding="utf-8",
        )

    print(f"OK: 共解析 {page_count} 页，提取图片 {image_count} 张")
    print(f"输出目录：{out_dir}")
    print("提示：降级解析不做公式 LaTeX 化与 OCR，安装 MinerU 可获得更佳效果。")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="PyMuPDF 降级 PDF 解析")
    parser.add_argument("pdf", help="论文 PDF 路径")
    parser.add_argument("-o", "--output", required=True, help="输出目录")
    args = parser.parse_args()

    pdf_path = Path(args.pdf).expanduser().resolve()
    if not pdf_path.is_file():
        print(f"ERROR: 文件不存在：{pdf_path}", file=sys.stderr)
        return 1
    return parse_pdf(pdf_path, Path(args.output).expanduser().resolve())


if __name__ == "__main__":
    raise SystemExit(main())
