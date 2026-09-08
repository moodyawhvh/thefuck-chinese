# -*- coding: utf-8 -*-
# 修正器核心模块:收集所有可用规则,按优先级排序,
# 并为失败命令生成去重后的候选修正命令列表。
import sys
from .conf import settings
from .types import Rule
from .system import Path
from . import logs


def get_loaded_rules(rules_paths):
    """生成所有可用规则。

    :type rules_paths: [Path]
    :rtype: Iterable[Rule]

    """
    for path in rules_paths:
        # 跳过包标识文件 __init__.py,其余按 Rule 加载
        if path.name != '__init__.py':
            rule = Rule.from_path(path)
            if rule and rule.is_enabled:
                yield rule


def get_rules_import_paths():
    """生成所有规则的导入路径。

    :rtype: Iterable[Path]

    """
    # 内置规则:
    yield Path(__file__).parent.joinpath('rules')
    # 用户自定义规则:
    yield settings.user_dir.joinpath('rules')
    # 第三方规则包(thefuck_contrib_* 开头的包):
    for path in sys.path:
        for contrib_module in Path(path).glob('thefuck_contrib_*'):
            contrib_rules = contrib_module.joinpath('rules')
            if contrib_rules.is_dir():
                yield contrib_rules


def get_rules():
    """返回所有已启用的规则。

    :rtype: [Rule]

    """
    # 汇总所有导入路径下的规则文件,并按优先级排序
    paths = [rule_path for path in get_rules_import_paths()
             for rule_path in sorted(path.glob('*.py'))]
    return sorted(get_loaded_rules(paths),
                  key=lambda rule: rule.priority)


def organize_commands(corrected_commands):
    """生成排序后且无重复的命令。

    :type corrected_commands: Iterable[thefuck.types.CorrectedCommand]
    :rtype: Iterable[thefuck.types.CorrectedCommand]

    """
    try:
        # 第一个(优先级最高的)修正命令直接产出,
        # 保证用户按回车后立即执行最可能的修正
        first_command = next(corrected_commands)
        yield first_command
    except StopIteration:
        # 没有任何可用修正命令时直接返回
        return

    # 其余命令:按优先级排序并去除与第一个相同的重复项
    without_duplicates = {
        command for command in sorted(
            corrected_commands, key=lambda command: command.priority)
        if command != first_command}

    sorted_commands = sorted(
        without_duplicates,
        key=lambda corrected_command: corrected_command.priority)

    # 调试日志:输出完整的候选修正命令列表
    logs.debug(u'Corrected commands: {}'.format(
        ', '.join(u'{}'.format(cmd) for cmd in [first_command] + sorted_commands)))

    for command in sorted_commands:
        yield command


def get_corrected_commands(command):
    """返回一个生成器,产出排序且去重后的修正命令。

    :type command: thefuck.types.Command
    :rtype: Iterable[thefuck.types.CorrectedCommand]

    """
    # 遍历所有匹配该命令的规则,汇总其生成的修正命令
    corrected_commands = (
        corrected for rule in get_rules()
        if rule.is_match(command)
        for corrected in rule.get_corrected_commands(command))
    return organize_commands(corrected_commands)
