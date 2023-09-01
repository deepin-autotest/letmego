#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.

# SPDX-License-Identifier: GPL-2.0-only
# pylint: disable=C0114
from configparser import RawConfigParser  # 解决读取log报错
from enum import unique
from enum import Enum
from getpass import getuser
from os import popen
from os.path import abspath
from os.path import dirname
from os.path import join
from platform import machine
from time import strftime


# pylint: disable=C0116,C0103,C0103,C0115,R0903

class GetCfg:
    """Gets the value in the configuration file"""

    def __init__(self, config_file: str, option: [str, None] = None):
        self.config_file = config_file
        self.option = option
        self.conf = RawConfigParser()
        self.conf.read(self.config_file, encoding="utf-8")

    def get(self, key: str, op: [str, None] = None, default=None) -> str:
        if op is None and self.option is not None:
            op = self.option
        if op is None and self.option is None:
            raise ValueError("option is None")
        return self.conf.get(op, key, fallback=default)

    def get_bool(self, key: str, op: [str, None] = None, default=False) -> bool:
        if op is None and self.option is not None:
            op = self.option
        if op is None and self.option is None:
            raise ValueError("option is None")
        return self.conf.getboolean(op, key, fallback=default)


class _GlobalConfig:
    """Basic framework global configuration"""
    PROJECT_NAME = "YouQu"

    class DirName:
        SRC = "src"
        APPS = "apps"
        DOCS = "docs"
        PUBLIC = "public"
        REPORT = "report"
        SETTING = "setting"

    # ====================== ABSOLUTE PATH ======================
    # Root dir
    ROOT_DIR = dirname(dirname(abspath(__file__)))
    # apps path
    APPS_PATH = join(ROOT_DIR, DirName.APPS)
    # setting path
    SETTING_PATH = join(ROOT_DIR, DirName.SETTING)
    # Default does not exist
    REPORT_PATH = join(ROOT_DIR, DirName.REPORT)

    # ====================== GLOBAL CONFIG INI ======================
    # Get config file object
    GLOBAL_CONFIG_FILE_PATH = join(SETTING_PATH, "globalconfig.ini")
    # [case]
    case_cfg = GetCfg(GLOBAL_CONFIG_FILE_PATH, "case")
    APP_NAME = case_cfg.get("APP_NAME", default="")
    KEYWORDS = case_cfg.get("KEYWORDS", default="")
    TAGS = case_cfg.get("TAGS", default="")
    CASE_FILE = case_cfg.get("CASE_FILE", default="")
    # [runner]
    runner_cfg = GetCfg(GLOBAL_CONFIG_FILE_PATH, "runner")
    RERUN = runner_cfg.get("RERUN", default=1)
    RECORD_FAILED_CASE = runner_cfg.get("RECORD_FAILED_CASE", default=1)
    MAX_FAIL = runner_cfg.get("MAX_FAIL", default=1)
    CASE_TIME_OUT = runner_cfg.get("CASE_TIME_OUT", default=200)
    CLEAN_ALL = runner_cfg.get("CLEAN_ALL", default="yes")
    RESOLUTION = runner_cfg.get("RESOLUTION", default="1920x1080")
    NOSKIP = runner_cfg.get_bool("NOSKIP", default=False)
    IFIXED = runner_cfg.get_bool("IFIXED", default=False)
    DURING_FAIL = runner_cfg.get_bool("DURING_FAIL", default=False)
    AUTOSTART = runner_cfg.get_bool("AUTOSTART", default=False)
    TOP = runner_cfg.get("TOP", default="")
    REPEAT = runner_cfg.get("REPEAT", default="")
    DEB_PATH = runner_cfg.get("DEB_PATH", default="~/Downloads/")
    DEBUG = runner_cfg.get_bool("DEBUG", default=False)
    # [report]
    report_cfg = GetCfg(GLOBAL_CONFIG_FILE_PATH, "report")
    REPORT_TITLE = report_cfg.get("REPORT_TITLE", default="YouQu Report")
    REPORT_NAME = report_cfg.get("REPORT_NAME", default="YouQu Report")
    REPORT_LANGUAGE = report_cfg.get("REPORT_LANGUAGE", default="zh")
    REPORT_FORMAT = report_cfg.get("REPORT_FORMAT", default="allure, xml, json")
    ALLURE_REPORT_PATH = join(
        ROOT_DIR, report_cfg.get("ALLURE_REPORT_PATH", default="report/")
    )
    XML_REPORT_PATH = join(
        ROOT_DIR, report_cfg.get("XML_REPORT_PATH", default="report/")
    )
    JSON_REPORT_PATH = join(
        ROOT_DIR, report_cfg.get("JSON_REPORT_PATH", default="report/")
    )
    # [globalconfig]
    global_cfg = GetCfg(GLOBAL_CONFIG_FILE_PATH, "globalconfig")
    PASSWORD = global_cfg.get("PASSWORD", default="1")
    if not PASSWORD:
        raise ValueError("测试机密码不能未空")
    IMAGE_MATCH_NUMBER = global_cfg.get("IMAGE_MATCH_NUMBER", default=1)
    IMAGE_MATCH_WAIT_TIME = global_cfg.get("IMAGE_MATCH_WAIT_TIME", default=1)
    IMAGE_RATE = global_cfg.get("IMAGE_RATE", default=0.9)
    SCREEN_CACHE = global_cfg.get("SCREEN_CACHE", default="/tmp/screen.png")
    TMPDIR = global_cfg.get("TMPDIR", default="/tmp/tmpdir")
    SYS_THEME = global_cfg.get("SYS_THEME", default="deepin")
    OCR_SERVER_HOST = global_cfg.get("OCR_SERVER_HOST", default="localhost")
    OPENCV_SERVER_HOST = global_cfg.get("OPENCV_SERVER_HOST", default="localhost")

    # [pms]
    pms_cfg = GetCfg(GLOBAL_CONFIG_FILE_PATH, "pms")
    PMS_USER = pms_cfg.get("PMS_USER", default="")
    PMS_PASSWORD = pms_cfg.get("PMS_PASSWORD", default="")
    SUITE_ID = pms_cfg.get("SUITE_ID", default="")
    SEND_PMS = pms_cfg.get("SEND_PMS", default="")
    if SEND_PMS not in ("", "async", "finish"):
        raise ValueError
    TASK_ID = pms_cfg.get("TASK_ID", default="")
    TRIGGER = pms_cfg.get("TRIGGER", default="auto")
    if TRIGGER not in ("auto", "hand"):
        raise ValueError
    SEND_PMS_RETRY_NUMBER = pms_cfg.get("SEND_PMS_RETRY_NUMBER", default=2)
    # ====================== 动态获取变量 ======================
    # username
    USERNAME = getuser()
    # IP
    OS_VERSION = GetCfg("/etc/os-version", "Version")
    HOST_IP = str(popen("hostname -I |awk '{print $1}'").read()).strip("\n").strip()
    PRODUCT_INFO = popen("cat /etc/product-info").read()
    VERSION = (OS_VERSION.get("EditionName[zh_CN]") or "") + (
            OS_VERSION.get("MinorVersion") or ""
    )
    # machine type
    # e.g. x86_64
    SYS_ARCH = machine()
    LANGUAGE_INI = GetCfg(join(SETTING_PATH, "template/language.ini"), "language")

    current_tag = GetCfg(f"{ROOT_DIR}/CURRENT", "current").get("tag")

    class ArchName:
        x86 = "x86_64"
        arm = "aarch64"
        mips = "mips64"
        longxin = "loongarch64"
        sw = "sw_64"

    class ReportFormat:
        ALLURE = "allure"
        XML = "xml"
        JSON = "json"

    TIME_STRING = strftime("%Y%m%d%H%M%S")

    slp_cfg = GetCfg(f"{SETTING_PATH}/sleepx.ini", "sleepx")

    # 显示服务器
    # 直接读环境变量XDG_SESSION_TYPE会有问题，采用读文件的方式获取
    DISPLAY_SERVER = (
        popen("cat ~/.xsession-errors | grep XDG_SESSION_TYPE | head -n 1")
            .read()
            .split("=")[-1]
            .strip("\n")
    )

    class DisplayServer:
        wayland = "wayland"
        x11 = "x11"

    IS_X11 = DISPLAY_SERVER == DisplayServer.x11
    IS_WAYLAND = DISPLAY_SERVER == DisplayServer.wayland

    top_cmd = "top -b -d 3 -w 512"

    # [export_csv]
    export_csv = GetCfg(GLOBAL_CONFIG_FILE_PATH, "export_csv")
    CSV_FILE = export_csv.get("CSV_FILE", default="case_list.csv")
    CSV_HEARD = export_csv.get("CSV_HEARD", default="用例级别,用例类型,测试级别,是否跳过").replace(" ", "")
    # [log_cli]
    log_cli = GetCfg(GLOBAL_CONFIG_FILE_PATH, "log_cli")
    LOG_LEVEL = log_cli.get("LOG_LEVEL", default="INFO")
    CLASS_NAME_STARTSWITH = tuple(
        log_cli.get("CLASS_NAME_STARTSWITH", default="Assert").replace(" ", "").split(",")
    )
    CLASS_NAME_ENDSWITH = tuple(
        log_cli.get("CLASS_NAME_ENDSWITH", default="Widget").replace(" ", "").split(",")
    )
    CLASS_NAME_CONTAIN = tuple(
        log_cli.get("CLASS_NAME_CONTAIN", default="ShortCut").replace(" ", "").split(",")
    )
    GITHUB_URL = "https://github.com/linuxdeepin/deepin-autotest-framework"
    DOCS_URL = "https://linuxdeepin.github.io/deepin-autotest-framework"
    PyPI_URL = "https://pypi.org/project/youqu"


GlobalConfig = _GlobalConfig()


@unique
class ConfStr(Enum):
    SKIP = "skip"
    SKIPIF = "skipif"
    FIXED = "fixed"
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"
    REMOVED = "removed"
    RERUN = "rerun"
    AUTO = "auto"
    ASYNC = "async"
    FINISH = "finish"
    SKIP_INDEX = "skip_index"
    FIXED_INDEX = "fixed_index"
    REMOVED_INDEX = "removed_index"
    PMS_ID_INDEX = "pms_id_index"


@unique
class FixedCsvTitle(Enum):
    skip_reason = "跳过原因"
    fixed = "确认修复"
    removed = "废弃用例"
    pms_case_id = "PMS用例ID"
    case_level = "用例级别"


@unique
class SystemPath(Enum):
    SRC_PATH = join(GlobalConfig.ROOT_DIR, "src")
    DEPENDS_PATH = join(SRC_PATH, "depends")
    APPS_PATH = GlobalConfig.APPS_PATH
