# paper-group-meeting —— 论文组会材料全自动生成

把一篇学术论文 PDF 变成整套组会汇报材料包：MinerU 深度解析 → 章节全覆盖精读 → 专业术语表 → PPT 大纲 → ppt-master 生成 PPTX → 逐页讲稿 → 演讲指南与 Q&A → 结构化归档。

## 环境

- Windows + Trae 客户端
- Python 3.11（脚本基于此版本编写）
- MinerU（推荐，非必需）：`mineru` CLI 可用时启用高质量解析
- ppt-master（推荐，非必需）：生成可编辑 PPTX

## 安装

将本文件夹复制/链接到 Trae 的 skill 目录即可：

- 全局：`C:\Users\<用户>\.trae-cn\skills\paper-group-meeting`
- 项目：`<工作区>\.trae\skills\paper-group-meeting`

## 使用

```
帮我生成 F:\papers\transformer.pdf 的组会材料
帮我生成 F:\papers\transformer.pdf 的组会材料 --template deep --duration 20min --focus method
```

支持的参数见 `SKILL.md`；模板见 `templates/{standard,quick,deep}/`。

## 目录结构

```
paper-group-meeting/
├── SKILL.md                    # Skill 主指令文件（Trae 读取执行）
├── config.json                 # 全局配置（路径、默认参数、引擎）
├── README.md                   # 本说明
├── templates/
│   ├── standard/               # 标准组会（15min，默认）
│   ├── quick/                  # 快速汇报（5min）
│   └── deep/                   # 深度研讨（30min）
├── parsers/
│   └── mineru-config.json      # MinerU 解析参数配置
├── scripts/
│   ├── pdf_fallback.py         # MinerU 不可用时的降级解析（PyMuPDF）
│   └── build_archive.py        # 结构化归档脚本
└── examples/                   # 输入 / 输出示例
```

## 依赖组件

| 组件 | 作用 | 获取 |
|---|---|---|
| MinerU（推荐） | 论文深度解析（正文/图片/表格/公式/章节） | 本仓库不包含，请从上游安装：<https://github.com/opendatalab/MinerU> |
| ppt-master（推荐） | 大纲 → 可编辑 PPTX | 本仓库不包含，请从上游安装，并在 `config.json` 的 `ppt_master.skill_dir` 指向其目录 |

> 二者均为独立的第三方项目，不随本仓库分发；未安装时技能会走降级路径（见 `SKILL.md` 前置检查）。

## 已知说明

- MinerU 4.0 的 CLI 是 `mineru`（文档旧版写的 `magic-pdf` 已弃用）。
- MinerU 默认只解析 PDF 前 10 页，技能内已强制 `--pages all`。
- 本地高品质解析需一次模型下载与托管服务配置，见 `SKILL.md` 步骤 1。
- 若 `mineru` 不在 PATH（Windows 应用商店版 Python 常见），把你本机的 `mineru.exe` 路径填到
  `config.json` 的 `mineru.cli_path_absolute`（默认留空，表示直接用 PATH 上的 `mineru`）；把该 Scripts
  目录加入用户 PATH 后重启 Trae 即可直接用 `mineru`。

## 可移植性说明

- 默认路径均为**相对路径**，不含任何机器相关信息，克隆后即可使用。
- 若把 `ppt-master`、`MinerU` 放在本仓库同级目录，`config.json` 与 `SKILL.md` 中的相对路径可直接生效；
  否则请按上面「依赖组件」表修改 `config.json` 的对应字段。