<div align="center">

# thefuck 中文翻译版

**[中文版] thefuck — 自动纠正你上一条输错的终端命令的强大工具**

[![原项目](https://img.shields.io/badge/原项目-nvbn--thefuck-blue?style=flat-square&logo=github)](https://github.com/nvbn/thefuck)
[![中文文档](https://img.shields.io/badge/中文文档-README.zh--CN.md-orange?style=flat-square)](README.zh-CN.md)
[![GitHub Stars](https://img.shields.io/github/stars/nvbn/thefuck?style=flat-square&label=原项目Stars)](https://github.com/nvbn/thefuck/stargazers)
[![微信联系](https://img.shields.io/badge/微信-uaycar-brightgreen?style=flat-square&logo=wechat)](#)

</div>

---

> 这是 [nvbn/thefuck](https://github.com/nvbn/thefuck) 的中文翻译版本。
> 完整源代码请访问原项目:https://github.com/nvbn/thefuck

**代部署 / 定制服务 / 技术咨询 请添加微信:uaycar**

---

## 📖 项目简介

thefuck(即 The Fuck)是一款广受欢迎的开源命令行纠错工具:当你把上一条终端命令敲错时,只需输入 `fuck`,它就会自动匹配内置规则、分析报错原因,给出修正后的命令,回车确认后立即重新执行。无论是拼写错误、参数顺序、缺少 sudo,还是忘记上游分支,它都能一键救场。项目灵感来自一条推文,目前在 GitHub 上拥有数万 Star,是命令行效率工具里的经典之作。

## ✨ 主要特性

- 输错命令后输入 `fuck`,一键自动纠正并重跑,支持 `enter/↑/↓/ctrl+c` 交互选择
- 内置上百条纠错规则,覆盖 git、docker、npm、pip、apt、brew 等常见工具的典型报错
- 支持拼写纠正(如 `puthon` → `python`)、参数补全(如 `git push` 自动加 `--set-upstream`)
- 权限不足时自动加 `sudo`,目录不存在时自动 `mkdir -p`,细节场景考虑周全
- 支持 Bash、Zsh、Fish、PowerShell、tcsh 等主流 Shell,别名可自定义
- 提供 `--yeah`(-y)免确认模式、`-r` 递归修正模式
- 提供实验性即时模式(instant mode),响应更快
- 支持通过 `settings.py` 或环境变量精细配置规则、优先级、确认策略等
- 可自己编写 Python 规则文件,扩展性强;跨平台支持 macOS、Linux、Windows、FreeBSD

## 📁 文件说明

| 文件 | 说明 |
|:-----|:-----|
| README.md | 本文件(中文简介) |
| README.zh-CN.md | 详细中文文档(完整汉化) |

## 🚀 快速开始

1. 准备环境:Python 3.5+、pip、python-dev;
2. macOS / Linux 可用 Homebrew 安装:
   ```bash
   brew install thefuck
   ```
3. Ubuntu / Mint 使用 apt + pip 安装:
   ```bash
   sudo apt update
   sudo apt install python3-dev python3-pip python3-setuptools
   pip3 install thefuck --user
   ```
4. 其他系统直接用 pip:`pip install thefuck`;
5. 在 `.bash_profile`、`.bashrc` 或 `.zshrc` 中配置别名:
   ```bash
   eval $(thefuck --alias)
   # 别名可以随便改,比如周一犯困的时候:
   eval $(thefuck --alias FUCK)
   ```
6. 执行 `source ~/.bashrc`(或你的 Shell 配置文件)让别名立即生效;
7. 之后敲错命令,直接输入 `fuck`,回车确认即可自动修正执行;免确认可加 `-y`,递归修正用 `-r`。

完整源代码与最新版本请访问原项目:https://github.com/nvbn/thefuck

## 📞 联系方式

**代部署 / 定制服务 / 技术咨询 请添加微信:uaycar**

---

本项目为 [nvbn/thefuck](https://github.com/nvbn/thefuck) 的中文翻译版本,所有代码版权归原项目作者所有,遵循其原始许可证。

**如果觉得有用,请给原项目点个 Star!** ⭐
