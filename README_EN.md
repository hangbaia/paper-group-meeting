# paper-group-meeting —— Automated Group-Meeting Materials from a Paper

**English** | [中文](README.md)

Turn a single academic paper PDF into a complete group-meeting package:
deep parsing (MinerU) → chapter-by-chapter close reading → glossary → PPT outline → editable PPTX → per-slide speech script → presentation guide & Q&A prep → structured archiving.

> This repository is a **Trae Skill**: drop the folder into Trae's skill directory and run the whole pipeline with a single natural-language instruction.

## Features

- **Full chapter coverage**: follows the paper's own numbering (§1 / §2.1 / §3.2 …); every first- and second-level section is explained, none skipped.
- **Formulas thoroughly explained**: core formulas are cropped directly from the PDF (identical to the paper), each paired with a plain-language reading and the design rationale.
- **Chinese-first, jargon-free**: body text in Chinese; every key term gets a 10–25 character plain-language gloss on first appearance.
- **PPT quality spec built in**: elastic page allocation, layout safe areas, a one-line takeaway banner per slide, and a three-gate rendering self-check.
- **Graceful degradation**: if MinerU / ppt-master are unavailable, it falls back and still delivers the core materials.

## Requirements

- Windows + Trae client
- Python 3.11 (scripts are written for this version)
- MinerU (recommended, optional): enables high-quality parsing when the `mineru` CLI is available
- ppt-master (recommended, optional): generates editable PPTX

## Installation

Copy or link this folder into Trae's skill directory:

- Global: `C:\Users\<user>\.trae-cn\skills\paper-group-meeting`
- Project: `<workspace>\.trae\skills\paper-group-meeting`

## Usage

```
帮我生成 F:\papers\transformer.pdf 的组会材料
帮我生成 F:\papers\transformer.pdf 的组会材料 --template deep --duration 20min --focus method
```

Supported parameters are documented in `SKILL.md`; templates live in `templates/{standard,quick,deep}/`.

## Repository layout

```
paper-group-meeting/
├── SKILL.md                    # Skill entrypoint (executed by Trae)
├── config.json                 # Global config (paths, defaults, engines)
├── README.md                   # Chinese README
├── README_EN.md                # English README (this file)
├── templates/
│   ├── standard/               # Standard meeting (15 min, default)
│   ├── quick/                  # Quick report (5 min)
│   └── deep/                   # Deep dive (30 min)
├── parsers/
│   └── mineru-config.json      # MinerU parsing configuration
├── scripts/
│   ├── pdf_fallback.py         # Fallback parser (PyMuPDF) when MinerU is unavailable
│   └── build_archive.py        # Structured archiving script
└── examples/                   # Sample input / output
```

## Workflow

```
PDF deep parsing → close-reading analysis → glossary → PPT outline
                → PPTX generation (template re-draw / ppt-master) → rendering self-check
                → per-slide speech script → presentation guide & Q&A → structured archiving
```

## Dependencies

| Component | Purpose | How to get |
|---|---|---|
| MinerU (recommended) | Deep paper parsing (text / figures / tables / formulas / section hierarchy) | Not bundled; install from upstream: <https://github.com/opendatalab/MinerU> |
| ppt-master (recommended) | Outline → editable PPTX | Not bundled; install from upstream and point `ppt_master.skill_dir` in `config.json` to its directory |

> Both are independent third-party projects and are not redistributed here. When they are missing, the skill falls back automatically (see the pre-flight checks in `SKILL.md`).

## Notes

- MinerU 4.0's CLI is `mineru` (the older `magic-pdf` mentioned in legacy docs is deprecated).
- MinerU parses only the first 10 pages of a PDF by default; this skill always forces `--pages all`.
- High-quality local parsing requires a one-time model download and managed-service setup — see step 1 of `SKILL.md`.
- If `mineru` is not on `PATH` (common with the Microsoft Store build of Python), set your local `mineru.exe`
  path in `config.json` → `mineru.cli_path_absolute` (empty by default, meaning use `mineru` from `PATH`); add
  that Scripts directory to your user `PATH` and restart Trae to use `mineru` directly.

## Portability

- All default paths are **relative** and contain no machine-specific information — works right after cloning.
- If you place `ppt-master` and `MinerU` as siblings of this repository, the relative paths in `config.json`
  and `SKILL.md` work as-is; otherwise edit the corresponding fields per the dependency table above.
