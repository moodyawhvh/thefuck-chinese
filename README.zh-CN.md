# thefuck 中文文档

[![原项目](https://img.shields.io/badge/原项目-nvbn--thefuck-blue?style=flat-square&logo=github)](https://github.com/nvbn/thefuck)
[![微信联系](https://img.shields.io/badge/微信-uaycar-brightgreen?style=flat-square&logo=wechat)](#)

> 本文档是 [nvbn/thefuck](https://github.com/nvbn/thefuck) 官方 README 的中文翻译版,版权归原作者所有,遵循 MIT 许可证。
> **代部署 / 定制服务 / 技术咨询 请添加微信:uaycar**

## 简介

*The Fuck* 是一款出色的命令行纠错工具,灵感来自 [@liamosaur](https://twitter.com/liamosaur/) 的一条[推文](https://twitter.com/liamosaur/status/506975850596536320),它可以自动纠正你上一条控制台命令中的错误。如果觉得它响应偏慢,可以尝试[实验性即时模式](#实验性即时模式)。

示例:

```bash
➜ apt-get install vim
E: Could not open lock file /var/lib/dpkg/lock - open (13: Permission denied)
E: Unable to lock the administration directory (/var/lib/dpkg/), are you root?

➜ fuck
sudo apt-get install vim [enter/↑/↓/ctrl+c]
[sudo] password for nvbn:
Reading package lists... Done
...
```

更多示例:

```bash
➜ git push
fatal: The current branch master has no upstream branch.

➜ fuck
git push --set-upstream origin master [enter/↑/↓/ctrl+c]
```

```bash
➜ puthon
zsh: command not found: puthon

➜ fuck
python [enter/↑/↓/ctrl+c]
```

如果你不怕盲目执行修正后的命令,可以在[设置](#设置)中关闭 `require_confirmation` 选项。

## 环境要求

- python(3.5+)
- pip
- python-dev

## 安装

macOS 或 Linux 可通过 [Homebrew](https://brew.sh/) 安装:

```bash
brew install thefuck
```

Ubuntu / Mint:

```bash
sudo apt update
sudo apt install python3-dev python3-pip python3-setuptools
pip3 install thefuck --user
```

FreeBSD:

```bash
pkg install thefuck
```

ChromeOS(使用 [chromebrew](https://github.com/skycocker/chromebrew)):

```bash
crew install thefuck
```

Arch 系发行版:

```bash
sudo pacman -S thefuck
```

其他系统使用 `pip` 安装:

```bash
pip install thefuck
```

也可以改用系统包管理器安装(OS X、Ubuntu、Arch),参见[安装 Wiki](https://github.com/nvbn/thefuck/wiki/Installation)。

建议把下面的命令放入 `.bash_profile`、`.bashrc`、`.zshrc` 等启动脚本中:

```bash
eval $(thefuck --alias)
# 别名可以随便取,比如周一犯困的时候:
eval $(thefuck --alias FUCK)
```

其他 Shell(Bash、Zsh、Fish、PowerShell、tcsh)的别名配置参见 [Shell 别名 Wiki](https://github.com/nvbn/thefuck/wiki/Shell-aliases)。

修改只在新的 Shell 会话中生效,想立即生效请执行 `source ~/.bashrc`(或对应的配置文件如 `.zshrc`)。

不想确认直接执行,用 `--yeah` 选项(简写 `-y`,特别烦躁时也可以用 `--hard`):

```bash
fuck --yeah
```

需要递归修正直到成功,用 `-r` 选项:

```bash
fuck -r
```

## 更新与卸载

更新:

```bash
pip3 install thefuck --upgrade
```

**注意:别名功能在 *The Fuck* v1.34 中有过变更。**

卸载时反过来操作即可:从 Shell 配置中删除或注释掉 thefuck 别名行,再用对应的包管理器(brew、pip3、pkg、crew、pip)卸载程序本体。

## 工作原理

*The Fuck* 会尝试将上一条命令与规则库匹配;匹配成功后,按规则生成新命令并执行。默认启用的规则有上百条,以下为代表性条目(完整列表见[原项目 README](https://github.com/nvbn/thefuck#how-it-works)):

- `sudo` — 命令因权限失败时自动在前面加 `sudo`;
- `no_command` — 纠正拼写错误的命令,例如 `vom` → `vim`;
- `cd_correction` — 对失败的 `cd` 做拼写检查与纠正;
- `cd_mkdir` — 进入目录前先创建它;
- `git_push` — 给失败的 `git push` 补上 `--set-upstream origin $branch`;
- `git_not_command` — 纠正错误的 git 子命令,例如 `git brnch`;
- `git_stash` — 在 rebase 或切换分支前先 stash 本地修改;
- `docker_not_command` — 纠正错误的 docker 子命令,例如 `docker tags`;
- `pip_install` — 通过加 `--user` 或前缀 `sudo` 解决 `pip install` 权限问题;
- `python_module_error` — 遇到 ModuleNotFoundError 时尝试 `pip install` 对应模块;
- `mkdir_p` — 创建缺少父目录的目录时自动加 `-p`;
- `rm_dir` — 删除目录时自动加 `-rf`;
- `npm_wrong_command` — 纠正错误的 npm 命令,例如 `npm urgrade`;
- `apt_get` — 软件未安装时直接用 apt 安装(平台专属);
- `brew_install` — 纠正 `brew install` 的 formula 名称(平台专属);
- `history` — 尝试用历史记录中最相似的命令替换。

另有少量规则随包附带但默认不启用,例如 `git_push_force`(给 `git push` 加 `--force-with-lease`)和 `rm_root`(给 `rm -rf /` 加 `--no-preserve-root`)。

## 自定义规则

在 `~/.config/thefuck/rules` 下创建 `your-rule-name.py` 即可添加自己的规则。规则文件必须包含两个函数:

```python
match(command: Command) -> bool
get_new_command(command: Command) -> str | list[str]
```

还可以包含可选函数 `side_effect(old_command: Command, fixed_command: str) -> None`,以及可选变量 `enabled_by_default`、`requires_output`、`priority`。`Command` 对象有三个属性:`script`、`output`、`script_parts`。3.0 版本起,规则中的设置项需通过 `from thefuck.conf import settings` 引入。一个用 `sudo` 运行脚本的简单示例:

```python
def match(command):
    return ('permission denied' in command.output.lower()
            or 'EACCES' in command.output)

def get_new_command(command):
    return 'sudo {}'.format(command.script)

enabled_by_default = True
```

更多规则示例、工具函数与平台辅助模块见[原项目源码目录](https://github.com/nvbn/thefuck/tree/master/thefuck/rules)。

## 设置

可在 `$XDG_CONFIG_HOME/thefuck/settings.py`(默认 `~/.config`)中修改参数,常用项包括:

- `rules` — 启用的规则列表,默认 `thefuck.const.DEFAULT_RULES`;
- `exclude_rules` — 禁用的规则列表,默认 `[]`;
- `require_confirmation` — 执行新命令前是否需要确认,默认 `True`;
- `wait_command` — 获取上一条命令输出的最长等待秒数;
- `priority` — 规则优先级字典,数值越小越先匹配;
- `debug` — 是否开启调试输出,默认 `False`;
- `num_close_matches` — 建议候选的最大数量,默认 `3`。

示例:

```python
rules = ['sudo', 'no_command']
exclude_rules = ['git_push']
require_confirmation = True
wait_command = 10
priority = {'sudo': 100, 'no_command': 9999}
num_close_matches = 5
```

也可以用环境变量配置,如 `THEFUCK_RULES`、`THEFUCK_EXCLUDE_RULES`、`THEFUCK_REQUIRE_CONFIRMATION`、`THEFUCK_PRIORITY`、`THEFUCK_DEBUG` 等,命名规律为 `THEFUCK_` + 大写参数名:

```bash
export THEFUCK_RULES='sudo:no_command'
export THEFUCK_REQUIRE_CONFIRMATION='true'
```

## 第三方规则包

想发布一组非公开规则并分享给他人,可以创建名为 `thefuck_contrib_*` 的 Python 包,把规则放在其中的 `rules` 模块里,*The Fuck* 会自动发现并加载。

## 实验性即时模式

默认模式需要重新执行上一条命令来获取输出;即时模式通过 [script](https://en.wikipedia.org/wiki/Script_(Unix)) 记录终端输出再读取日志,从而节省时间。目前仅支持 Python 3 下的 bash 或 zsh,且 zsh 需关闭 autocorrect 功能。启用方式是在别名初始化时加上 `--enable-experimental-instant-mode`:

```bash
eval $(thefuck --alias --enable-experimental-instant-mode)
```

## 开发与许可证

参与开发请阅读原项目的 [CONTRIBUTING.md](https://github.com/nvbn/thefuck/blob/master/CONTRIBUTING.md)。项目基于 MIT 许可证发布,详见 [LICENSE.md](https://github.com/nvbn/thefuck/blob/master/LICENSE.md)。

---

> 本中文文档为社区翻译,仅供学习参考;如有出入以[原项目 README](https://github.com/nvbn/thefuck) 为准。
> **代部署 / 定制服务 / 技术咨询 请添加微信:uaycar**
> 如果觉得有用,请给原项目点个 Star!⭐
