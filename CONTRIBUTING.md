> 🌐 本文档由 [nvbn/thefuck](https://github.com/nvbn/thefuck) 翻译,英文原版见原项目。

# 报告问题

如果你使用 The Fuck 时遇到了任何问题,我们很抱歉,但我们会尽力修复。实际上,也许问题已经被修复了,所以第一件事是升级 The Fuck,然后看看 Bug 是否依然存在。

如果问题依然存在(再次抱歉),请先检查该问题是否已被报告过;如果没有,请在 [GitHub](https://github.com/nvbn/thefuck) 上提交 issue,并附上以下基本信息:
  - `thefuck --version` 的输出(类似 `The Fuck 3.1 using
    Python 3.5.0` 这样的内容);
  - 你使用的 shell 及其版本(`bash`、`zsh`、*Windows PowerShell* 等);
  - 你使用的系统(Debian 7、ArchLinux、Windows 等);
  - 如何复现这个 Bug;
  - 在导出 `THEFUCK_DEBUG=true` 后 The Fuck 的输出(通常是在运行 The Fuck 之前,在 shell 中执行 `export THEFUCK_DEBUG=true`);
  - 如果该 Bug 只在某个特定应用程序下出现,请提供该应用程序的输出及其版本;
  - 其他你认为相关的信息。

只有掌握了足够的信息,我们才能动手修复问题。

# 提交 Pull Request

我们非常欢迎向[官方仓库](https://github.com/nvbn/thefuck)提交 pull request,包括新规则、新功能、Bug 修复等。

# 开发

本地开发有两种方式:

- 使用本地安装的 Python 3 并搭建虚拟环境进行开发
- 使用自动化的 VSCode Dev Container 进行开发

## 使用本地 Python 环境开发

[创建并激活一个 Python 3 虚拟环境。](https://docs.python.org/3/tutorial/venv.html)

以开发模式安装 `The Fuck`:

```bash
pip install -r requirements.txt
python setup.py develop
```

运行代码风格检查:

```bash
flake8
```

运行单元测试:

```bash
pytest
```

运行单元测试和功能测试(需要 docker):

```bash
pytest --enable-functional
```

发布包到 PyPI:

```bash
sudo apt-get install pandoc
./release.py
```

## 使用 Dev Container 开发

为了让本地开发更轻松,本仓库内置了 [VSCode Devcontainer](https://code.visualstudio.com/docs/remote/remote-overview)。它可以帮你启动一个预装了本项目全部必要依赖的 Docker 容器,开箱即用,无需在本地安装和配置 Python。

### 前置条件

使用该容器需要:
- [Docker](https://www.docker.com/products/docker-desktop)
- [VSCode](https://code.visualstudio.com/)
- [VSCode 远程开发扩展](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack)
- [仅限 Windows 用户]:[安装 WSL2 并配置 Docker 使用它](https://docs.docker.com/docker-for-windows/wsl/)

完整的[安装说明见这里](https://code.visualstudio.com/docs/remote/containers#_installation)。

### 运行容器

假设你已具备上述前置条件:

1. 打开 VSCode
1. 打开命令面板(Mac 上按 CMD+SHIFT+P,Windows 上按 CTRL+SHIFT+P)
1. 选择 `Remote-Containers: Reopen in Container`。
1. 容器会被构建,自动安装所有 pip 依赖,随后你的 VSCode 会自动挂载进去。
1. 之后你的 VSCode 和容器就相当于一个用完即弃的一次性环境。
