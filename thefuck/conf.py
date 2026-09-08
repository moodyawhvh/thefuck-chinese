# -*- coding: utf-8 -*-
# 配置模块:负责加载并合并来自三个来源的设置(优先级从低到高):
# 默认值 -> 用户 settings.py 文件 -> 环境变量 -> 命令行参数。
import os
import sys
from warnings import warn
from six import text_type
from . import const
from .system import Path

try:
    import importlib.util

    def load_source(name, pathname, _file=None):
        # 新版 Python(>=3.5)通过 importlib 按路径动态加载模块
        module_spec = importlib.util.spec_from_file_location(name, pathname)
        module = importlib.util.module_from_spec(module_spec)
        module_spec.loader.exec_module(module)
        return module
except ImportError:
    # 兼容旧版 Python:退回使用 imp.load_source
    from imp import load_source


class Settings(dict):
    # 继承 dict 的设置容器,支持以属性方式读写配置项(如 settings.debug)
    def __getattr__(self, item):
        return self.get(item)

    def __setattr__(self, key, value):
        self[key] = value

    def init(self, args=None):
        """用 `settings.py` 文件和环境变量中的值填充 `settings`。"""
        from .logs import exception

        self._setup_user_dir()
        self._init_settings_file()

        try:
            # 先从用户配置文件加载(失败不中断,继续用环境变量/默认值)
            self.update(self._settings_from_file())
        except Exception:
            exception("Can't load settings from file", sys.exc_info())

        try:
            # 再从环境变量加载,覆盖文件中的同名配置
            self.update(self._settings_from_env())
        except Exception:
            exception("Can't load settings from env", sys.exc_info())

        # 最后应用命令行参数,优先级最高
        self.update(self._settings_from_args(args))

    def _init_settings_file(self):
        # 用户配置文件不存在时,基于默认设置生成带注释的初始 settings.py
        settings_path = self.user_dir.joinpath('settings.py')
        if not settings_path.is_file():
            with settings_path.open(mode='w') as settings_file:
                settings_file.write(const.SETTINGS_HEADER)
                for setting in const.DEFAULT_SETTINGS.items():
                    settings_file.write(u'# {} = {}\n'.format(*setting))

    def _get_user_dir_path(self):
        """返回表示用户配置目录的 Path 对象"""
        xdg_config_home = os.environ.get('XDG_CONFIG_HOME', '~/.config')
        user_dir = Path(xdg_config_home, 'thefuck').expanduser()
        legacy_user_dir = Path('~', '.thefuck').expanduser()

        # 为了向后兼容,若旧的 '~/.thefuck' 目录存在则继续使用它:
        if legacy_user_dir.is_dir():
            warn(u'Config path {} is deprecated. Please move to {}'.format(
                legacy_user_dir, user_dir))
            return legacy_user_dir
        else:
            return user_dir

    def _setup_user_dir(self):
        """返回用户配置目录,不存在时自动创建。"""
        user_dir = self._get_user_dir_path()

        # 确保自定义规则目录 rules/ 存在
        rules_dir = user_dir.joinpath('rules')
        if not rules_dir.is_dir():
            rules_dir.mkdir(parents=True)
        self.user_dir = user_dir

    def _settings_from_file(self):
        """从配置文件加载设置。"""
        settings = load_source(
            'settings', text_type(self.user_dir.joinpath('settings.py')))
        # 只取默认设置中出现过的键,忽略文件里的其他内容
        return {key: getattr(settings, key)
                for key in const.DEFAULT_SETTINGS.keys()
                if hasattr(settings, key)}

    def _rules_from_env(self, val):
        """把环境变量中的规则列表字符串转换成 Python 列表。"""
        val = val.split(':')
        if 'DEFAULT_RULES' in val:
            # DEFAULT_RULES 是占位符,展开为内置的默认规则集合
            val = const.DEFAULT_RULES + [rule for rule in val if rule != 'DEFAULT_RULES']
        return val

    def _priority_from_env(self, val):
        """从环境变量解析规则优先级键值对。"""
        for part in val.split(':'):
            try:
                rule, priority = part.split('=')
                yield rule, int(priority)
            except ValueError:
                # 格式不合法的片段直接跳过
                continue

    def _val_from_env(self, env, attr):
        """把环境变量字符串转换为对应的 Python 类型。"""
        val = os.environ[env]
        if attr in ('rules', 'exclude_rules'):
            return self._rules_from_env(val)
        elif attr == 'priority':
            return dict(self._priority_from_env(val))
        elif attr in ('wait_command', 'history_limit', 'wait_slow_command',
                      'num_close_matches'):
            return int(val)
        elif attr in ('require_confirmation', 'no_colors', 'debug',
                      'alter_history', 'instant_mode'):
            # 布尔型配置:字符串 'true'(不区分大小写)视为 True
            return val.lower() == 'true'
        elif attr in ('slow_commands', 'excluded_search_path_prefixes'):
            return val.split(':')
        else:
            return val

    def _settings_from_env(self):
        """从环境变量加载设置。"""
        return {attr: self._val_from_env(env, attr)
                for env, attr in const.ENV_TO_ATTR.items()
                if env in os.environ}

    def _settings_from_args(self, args):
        """从命令行参数加载设置。"""
        if not args:
            return {}

        from_args = {}
        if args.yes:
            # --yes 表示执行修正命令前不再要求确认
            from_args['require_confirmation'] = not args.yes
        if args.debug:
            from_args['debug'] = args.debug
        if args.repeat:
            from_args['repeat'] = args.repeat
        return from_args


# 全局唯一的设置实例,初始值为内置默认配置
settings = Settings(const.DEFAULT_SETTINGS)
