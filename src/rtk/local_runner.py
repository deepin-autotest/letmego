#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.

# SPDX-License-Identifier: GPL-2.0-only
# pylint: disable=C0114
# pylint: disable=C0301,R0913,R0914,W0613,R0912,R0915,E0401,C0413,C0103,C0116
import json
from collections import Counter
from os import chdir
from os import environ
from os import listdir
from os import makedirs
from os import system
from os.path import exists
from os.path import isfile
from os.path import join
from os.path import expanduser
from time import sleep
from tkinter import Tk

import pytest
from allure_custom import AllureCustom
from allure_custom.conf import setting as al_setting

from setting.globalconfig import GetCfg
from setting.globalconfig import GlobalConfig

al_setting.html_title = GlobalConfig.REPORT_TITLE
al_setting.report_name = GlobalConfig.REPORT_NAME
al_setting.report_language = GlobalConfig.REPORT_LANGUAGE

import letmego

letmego.conf.setting.PASSWORD = GlobalConfig.PASSWORD
letmego.conf.setting.RUNNING_MAN_FILE = f"{GlobalConfig.REPORT_PATH}/_running_man.log"

from src import logger
from src.rtk._base import Args
from src.rtk._base import transform_app_name

environ["DISPLAY"] = ":0"


class LocalRunner:
    """
    本地执行工具
    """
    __author__ = "Mikigo <huangmingqiang@uniontech.com>"

    def __init__(
            self,
            app_name=None,
            keywords=None,
            tags=None,
            report_formats=None,
            max_fail=None,
            reruns=None,
            record_failed_case=None,
            clean=None,
            log_level=None,
            timeout=None,
            debug=False,
            noskip=None,
            ifixed=None,
            send_pms=None,
            task_id=None,
            suite_id=None,
            trigger=None,
            resolution=None,
            case_file=None,
            deb_path=None,
            pms_user=None,
            pms_password=None,
            pms_info_file=None,
            top=None,
            lastfailed=None,
            duringfail=None,
            repeat=None,
            project_name=None,
            build_location=None,
            line=None,
            exportcsv=None,
            autostart=None,
            **kwargs,
    ):
        logger("INFO")

        self.default = {
            Args.app_name.value: transform_app_name(app_name if app_name or case_file else GlobalConfig.APP_NAME),
            Args.keywords.value: keywords or GlobalConfig.KEYWORDS,
            Args.tags.value: tags or GlobalConfig.TAGS,
            Args.report_formats.value: report_formats or GlobalConfig.REPORT_FORMAT,
            Args.max_fail.value: max_fail or GlobalConfig.MAX_FAIL,
            Args.reruns.value: reruns or GlobalConfig.RERUN,
            Args.record_failed_case.value: record_failed_case or GlobalConfig.RECORD_FAILED_CASE,
            Args.clean.value: clean or GlobalConfig.CLEAN_ALL,
            Args.log_level.value: log_level or GlobalConfig.LOG_LEVEL,
            Args.timeout.value: timeout or GlobalConfig.CASE_TIME_OUT,
            Args.debug.value: debug or GlobalConfig.DEBUG,
            Args.noskip.value: noskip or GlobalConfig.NOSKIP,
            Args.ifixed.value: ifixed or GlobalConfig.IFIXED,
            Args.send_pms.value: send_pms or GlobalConfig.SEND_PMS,
            Args.task_id.value: task_id or GlobalConfig.TASK_ID,
            Args.suite_id.value: suite_id or GlobalConfig.SUITE_ID,
            Args.trigger.value: trigger or GlobalConfig.TRIGGER,
            Args.resolution.value: resolution or GlobalConfig.RESOLUTION,
            Args.case_file.value: case_file or GlobalConfig.CASE_FILE,
            Args.deb_path.value: deb_path or GlobalConfig.DEB_PATH,
            Args.duringfail.value: duringfail or GlobalConfig.DURING_FAIL,
            Args.repeat.value: repeat or GlobalConfig.REPEAT,
            Args.top.value: top or GlobalConfig.TOP,
            Args.pms_user.value: (pms_user or GlobalConfig.PMS_USER)
            if not pms_info_file
            else None,
            Args.pms_password.value: (pms_password or GlobalConfig.PMS_PASSWORD)
            if not pms_info_file
            else None,
            Args.pms_info_file.value: pms_info_file,
            Args.autostart.value: autostart or GlobalConfig.AUTOSTART,
        }
        self.lastfailed = lastfailed
        self.project_name = project_name
        self.build_location = build_location
        self.line = line
        self.exportcsv = exportcsv

        if not self.default.get(Args.debug.value) and not self.exportcsv:
            screen = Tk()
            x = screen.winfo_screenwidth()
            y = screen.winfo_screenheight()
            if self.default.get(Args.resolution.value) not in (f"{x}x{y}", "no"):
                logger.error(f"当前分辨率为：{x}x{y},您配置的分辨率为：{GlobalConfig.RESOLUTION}")
                raise ValueError

    @property
    def export_default(self):
        return self.default

    @staticmethod
    def make_dir(dirs):
        """make_dir"""
        try:
            dirs = expanduser(dirs)
            if not exists(dirs):
                makedirs(dirs)
        except FileExistsError:
            pass

    # 报告
    @classmethod
    def make_allure_report(cls, cmd, fmt, proj_path=None):
        """make_allure_report"""
        allure_report_path = f"{proj_path}/report/allure"
        if proj_path is None:
            allure_report_path = join(GlobalConfig.ALLURE_REPORT_PATH, fmt)
            cls.make_dir(allure_report_path)
        cmd.append(f"--alluredir={allure_report_path}")

    @classmethod
    def make_xml_report(cls, app_dir, case_file, cmd, fmt, proj_path=None):
        """make_xml_report"""
        xml_report_path = f"{proj_path}/report/xml"
        if proj_path is None:
            xml_report_path = join(GlobalConfig.XML_REPORT_PATH, fmt)
            cls.make_dir(xml_report_path)
        report_name = (
            case_file.replace("/", "_").replace(".", "_")
            if case_file
            else (app_dir if app_dir.startswith("autotest_") else "")
        )
        cmd.append(
            f"--junit-xml={xml_report_path}/{report_name}{'-' if report_name else ''}{GlobalConfig.TIME_STRING}.xml"
        )

    def create_pytest_cmd(self, app_dir, default=None, proj_path=None):
        """
         创建 Pytest 及其命令行参数
        :param app_dir:
        :return:
        """
        if default is None:
            default = self.default
        keywords_or_marker = True
        cmd = ["pytest"]
        if self.lastfailed:
            cmd.append("--lf")
            keywords_or_marker = False
        # 通过文件存放pms信息,Jenkins环境下不希望明文显示密码等信息,可信息存放在文件中
        elif default.get(Args.pms_info_file.value):
            pms_info_file_path = (
                f"{GlobalConfig.ROOT_DIR}/{default.get(Args.pms_info_file.value)}"
            )
            if not exists(pms_info_file_path):
                logger.error(pms_info_file_path)
                raise FileNotFoundError
            pms_cfg = GetCfg(pms_info_file_path, "pms")
            cmd.extend(["--pms_user", pms_cfg.get("PMS_USER", default="")])
            cmd.extend(["--pms_password", pms_cfg.get("PMS_PASSWORD", default="")])
            keywords_or_marker = False
        # 通过pms测试套执行用例
        elif default.get(Args.pms_user.value) and default.get(
                Args.pms_password.value
        ):
            cmd.extend(["--pms_user", default.get(Args.pms_user.value)])
            cmd.extend(["--pms_password", default.get(Args.pms_password.value)])
            keywords_or_marker = False
        # 通过本地测试套
        elif default.get(Args.case_file.value):
            file_path = (
                f"{GlobalConfig.ROOT_DIR}/{default.get(Args.case_file.value)}"
            )
            if (not exists(file_path)) or (not isfile(file_path)):
                logger.error(f"{file_path} 文件不存在.")
                raise FileNotFoundError
            if not default.get(Args.case_file.value).endswith(".txt"):
                logger.error(f"测试套文件{default.get(Args.case_file.value)},不是一个txt文件")
                raise FileNotFoundError
            logger.info(f"本地测试套文件：{file_path}")
            with open(file_path, "r", encoding="utf-8") as _f:
                txt_list = _f.readlines()
            if not txt_list:
                logger.error(f"{file_path},文件为空")
                raise ValueError
            taglines = [txt.strip() for txt in txt_list if txt]
            cmd.extend(taglines)

        if keywords_or_marker:
            if default.get(Args.keywords.value):
                cmd.extend(["-k", f"'{default.get(Args.keywords.value)}'"])
            if default.get(Args.tags.value):
                cmd.extend(["-m", f"'{default.get(Args.tags.value)}'"])

        if self.exportcsv:
            cmd.append("--co")
            return cmd

        if default.get(Args.noskip.value):
            cmd.extend(["--noskip", "yes"])
        if default.get(Args.ifixed.value):
            cmd.extend(["--ifixed", "yes"])
        if default.get(Args.send_pms.value):
            cmd.extend(["--send_pms", default.get(Args.send_pms.value)])
        if default.get(Args.suite_id.value):
            cmd.extend(["--suite_id", default.get(Args.suite_id.value)])
        if default.get(Args.task_id.value):
            cmd.extend(["--task_id", default.get(Args.task_id.value)])
        if default.get(Args.send_pms.value) and default.get(
                Args.trigger.value
        ):
            cmd.extend(["--trigger", default.get(Args.trigger.value)])

        cmd.extend(
            [
                f"--max_fail={float(default.get(Args.max_fail.value))}",
                f"--reruns={default.get(Args.reruns.value)}",
                f"--record_failed_case={default.get(Args.record_failed_case.value)}",
                f"--clean={default.get(Args.clean.value)}",
                f"--log_level={default.get(Args.log_level.value)}",
                f"--timeout={default.get(Args.timeout.value)}",
            ]
        )
        if default.get(Args.duringfail.value):
            cmd.append("--duringfail")
        if default.get(Args.top.value):
            cmd.extend(["--top", default.get(Args.top.value)])
        if default.get(Args.autostart.value):
            cmd.extend(["--autostart", default.get(Args.autostart.value)])
        if default.get(Args.repeat.value):
            cmd.extend(["--repeat", default.get(Args.repeat.value)])
        if self.line:
            cmd.extend(["--line", self.line])

        report_formats = default.get(Args.report_formats.value)
        if report_formats:
            report_formats = [i.strip() for i in report_formats.split(",")]
            # allure
            if (GlobalConfig.ReportFormat.ALLURE in report_formats) and (
                    GlobalConfig.ReportFormat.JSON not in report_formats
            ):
                self.make_allure_report(cmd, GlobalConfig.ReportFormat.ALLURE, proj_path)
            # xml
            if GlobalConfig.ReportFormat.XML in report_formats:
                self.make_xml_report(
                    app_dir,
                    default.get(Args.case_file.value),
                    cmd,
                    GlobalConfig.ReportFormat.XML,
                    proj_path,
                )
            # json
            if (GlobalConfig.ReportFormat.ALLURE not in report_formats) and (
                    GlobalConfig.ReportFormat.JSON in report_formats
            ):
                self.make_allure_report(cmd, GlobalConfig.ReportFormat.ALLURE, proj_path)
                self.make_dir(
                    join(GlobalConfig.REPORT_PATH, GlobalConfig.ReportFormat.JSON)
                )
            # allure json
            if (GlobalConfig.ReportFormat.ALLURE in report_formats) and (
                    GlobalConfig.ReportFormat.JSON in report_formats
            ):
                self.make_allure_report(cmd, GlobalConfig.ReportFormat.ALLURE, proj_path)
                self.make_dir(
                    join(GlobalConfig.REPORT_PATH, GlobalConfig.ReportFormat.JSON)
                )

        return cmd

    def change_working_dir(self):
        """
         切换工作区间
        :param app_name:
        :return:
        """
        app_name: str = self.default.get(Args.app_name.value)
        if app_name:
            real_app_name = app_name.replace("-", "_")
            applications = listdir(GlobalConfig.APPS_PATH)
            for working_dir in applications:
                if working_dir.endswith(real_app_name):
                    case_path = f"{GlobalConfig.APPS_PATH}/{working_dir}"
                    print(f"WorkSpace: \n{case_path}")
                    chdir(case_path)
                    return working_dir
            raise EnvironmentError(f"apps目录下未找到指定的{app_name}")
        return GlobalConfig.APPS_PATH

    def local_run(self):
        """
         执行用例
        :return:
        """
        if not self.default.get(Args.autostart.value):
            # 备份 allure 报告
            allure_report_path = join(GlobalConfig.ALLURE_REPORT_PATH, "allure")
            allure_report_back_path = join(
                GlobalConfig.ALLURE_REPORT_PATH, "allure_back", GlobalConfig.TIME_STRING
            )
            if exists(allure_report_path) and listdir(allure_report_path):
                makedirs(allure_report_back_path)
                system(f"mv {allure_report_path}/* {allure_report_back_path}/")

        app_dir = self.change_working_dir()
        run_test_cmd_list = self.create_pytest_cmd(app_dir)
        run_test_cmd = " ".join(run_test_cmd_list)

        if not self.default.get(Args.pms_info_file.value):
            print(f"Running: \n{run_test_cmd}")
        if self.default.get(Args.debug.value):
            logger.info("Debug 模式不执行用例!")
            return
        pytest.main([i.strip("'") for i in run_test_cmd_list[1:]])

        if self.exportcsv:
            return
        if self.project_name and self.build_location and self.line:
            self.write_json(
                project_name=self.project_name,
                build_location=self.build_location,
                line=self.line,
            )
        allure_report_path = join(
            GlobalConfig.ALLURE_REPORT_PATH, GlobalConfig.ReportFormat.ALLURE
        )
        allure_html_report_path = join(GlobalConfig.ALLURE_REPORT_PATH, "allure_html")

        json_report_path = join(
            GlobalConfig.ALLURE_REPORT_PATH, GlobalConfig.ReportFormat.JSON
        )

        if self.default.get(Args.report_formats.value):
            report_formats = [
                i.strip()
                for i in self.default.get(Args.report_formats.value).split(",")
            ]
            if (GlobalConfig.ReportFormat.ALLURE in report_formats) or (
                    GlobalConfig.ReportFormat.JSON in report_formats
            ):
                if exists(allure_html_report_path):
                    system(f"rm -rf {allure_html_report_path}")
                makedirs(allure_html_report_path)

                AllureCustom.gen(allure_report_path, allure_html_report_path)

                if GlobalConfig.ReportFormat.JSON in report_formats:
                    system(
                        f"cp {allure_html_report_path}/widgets/suites.json "
                        f"{json_report_path}/"
                        f"result_{self.default.get(Args.app_name.value)}_{GlobalConfig.TIME_STRING}_{GlobalConfig.HOST_IP.replace('.', '')}.json"
                    )

        # if exists(letmego.conf.setting.RUNNING_MAN_FILE):
        #     letmego.unregister_autostart_service()
        #     letmego.clean_running_man()

    @staticmethod
    def get_result():
        """
         获取结果
        :return:
        """
        with open(f"{GlobalConfig.ROOT_DIR}/ci_result.json", "r", encoding="utf-8") as _f:
            results_dict = json.load(_f)
        res = Counter([results_dict.get(i).get("result") for i in results_dict])
        total = sum(res.values())
        skiped = res.get("skip", 0)
        total = total - skiped  # 剔除skip的用例
        passed = res.get("pass", 0)
        failed = total - passed
        pass_rate = f"{round((passed / total) * 100, 1)}%" if passed else "0%"
        return total, failed, passed, pass_rate

    @classmethod
    def write_json(cls, project_name=None, build_location=None, line=None):
        """
         写json报告
        {
          "project_name": "",
          "build_location": "",
          "line": "",
          "total": "",
          "fail": "",
          "block": "",
          "pass": "",
          "pass_rate": ""
        }
        """
        json_tpl_path = f"{GlobalConfig.SETTING_PATH}/template/ci.json"

        if not exists(json_tpl_path):
            raise FileNotFoundError
        with open(json_tpl_path, "r", encoding="utf-8") as _f:
            results = json.load(_f)

        results["project_name"] = project_name
        results["build_location"] = build_location
        results["line"] = line
        (
            results["total"],
            results["fail"],
            results["pass"],
            results["pass_rate"],
        ) = cls.get_result()

        json_res_path = f"{GlobalConfig.ROOT_DIR}/{project_name}_at.json"
        with open(json_res_path, "w+", encoding="utf-8") as _f:
            _f.write(json.dumps(results, indent=2, ensure_ascii=False))
        sleep(1)
        with open(json_res_path, "r", encoding="utf-8") as _f:
            print("CICD数据结果:\n", _f.read())

    def install_deb(self):
        """
         安装本地 deb 包
        :return:
        """
        logger.info("安装deb包")
        system(
            f"cd {self.default.get(Args.deb_path.value)}/ && echo {GlobalConfig.PASSWORD} | sudo -S dpkg -i *.deb"
        )
        logger.info("deb包安装完成")


if __name__ == "__main__":
    LocalRunner().local_run()
