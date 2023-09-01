#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.

# SPDX-License-Identifier: GPL-2.0-only
# pylint: disable=C0114
# pylint: disable=E0401,C0413,R0902,R0913,R0914,W0613,C0301,C0415,C0103
import re
import sys
from configparser import ConfigParser
from itertools import cycle
from os import listdir
from os import makedirs
from os import popen
from os import system
from os.path import exists
from os.path import splitext
# from threading import Thread
# from multiprocessing import Process as Thread
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import wait
from concurrent.futures import ALL_COMPLETED
from time import sleep
from time import strftime

from allure_custom import AllureCustom
from allure_custom.conf import setting

from setting.globalconfig import GlobalConfig

setting.html_title = GlobalConfig.REPORT_TITLE
setting.report_name = GlobalConfig.REPORT_NAME
setting.report_language = GlobalConfig.REPORT_LANGUAGE

from src.cmdctl import CmdCtl
from src import logger
from src.rtk._base import Args
from src.rtk._base import transform_app_name


class RemoteRunner:
    """
    远程执行器：控制多台测试机远程执行用例。
    在 setting/remote.ini 里面配置要执行的测试机信息。
    """

    __author__ = "Mikigo <huangmingqiang@uniontech.com>"

    def __init__(
            self,
            remote_kwargs: dict = None,
            local_kwargs: dict = None,
    ):
        self.remote_kwargs = remote_kwargs
        self.local_kwargs = local_kwargs
        logger("INFO")
        conf = ConfigParser()
        conf.read(f"{GlobalConfig.SETTING_PATH}/remote.ini")
        self.parallel = conf.getboolean("remote", "PARALLEL")
        self.clean_server_report_dir = conf.getboolean(
            "remote", "CLEAN_SERVER_REPORT_DIR"
        )
        self.clean_client_report_dir = conf.getboolean(
            "remote", "CLEAN_CLIENT_REPORT_DIR"
        )
        self.send_code = conf.getboolean("remote", "SEND_CODE")
        self.scan = conf.getint("remote", "SCAN")
        self.client_env = conf.getboolean("remote", "BUILD_ENV")
        self.client_password = conf.get("remote", "CLIENT_PASSWORD")

        self._default = {
            Args.client_password.value: remote_kwargs.get("client_password") or self.client_password,
        }

        self.ini_client_dict = {
            op: [
                conf.get(op, "user"),
                conf.get(op, "ip"),
                conf.get(op, "password", fallback=self._default.get(Args.client_password.value)),
            ]
            for op in filter(lambda x: "client" in x, conf.sections())
        }

        cli_client_dict = {}
        if remote_kwargs.get("clients"):
            clients = remote_kwargs.get("clients").split("/")
            for index, client in enumerate(clients):
                client_info = re.findall(r"^(.+?)@(\d+\.\d+\.\d+\.\d+):{0,1}(.*?)$", client)
                if client_info:
                    _c = list(client_info[0])
                    if _c[2] == "":
                        _c[2] = self._default.get(Args.client_password.value)
                    cli_client_dict[f"client{index + 1}"] = _c

        if not cli_client_dict and not self.ini_client_dict:
            raise ValueError(
                "未获取到测试机信息,请检查 setting/remote.ini 中 CLIENT LIST 是否配置，"
                "或通过命令行 python3 manage.py remote -c user@ip:password 传入。"
            )

        self.default = {
            Args.app_name.value: transform_app_name(local_kwargs.get("app_name") or GlobalConfig.APP_NAME),
            Args.clients.value: cli_client_dict or self.ini_client_dict,
            Args.send_code.value: remote_kwargs.get("send_code") or self.send_code,
            Args.build_env.value: remote_kwargs.get("build_env") or self.client_env,
            Args.parallel.value: remote_kwargs.get("parallel") or self.parallel,
        }
        # 客户端地址
        if "/home/" not in GlobalConfig.ROOT_DIR:
            raise EnvironmentError
        self.server_project_path = "/".join(GlobalConfig.ROOT_DIR.split("/")[3:])
        self.client_report_path = (
            lambda x: f"/home/{x}/{self.server_project_path}/report"
        )
        self.client_allure_report_path = lambda \
                x: f"/home/{x}/{self.server_project_path}/{GlobalConfig.report_cfg.get('ALLURE_REPORT_PATH', default='report')}/allure".replace(
            "//", "/"
        )
        self.client_xml_report_path = lambda \
                x: f"/home/{x}/{self.server_project_path}/{GlobalConfig.report_cfg.get('XML_REPORT_PATH', default='report')}/xml".replace(
            "//", "/"
        )
        self.client_list = list(self.default.get(Args.clients.value).keys())
        _pty = "t"
        if len(self.client_list) >=2:
            _pty = "T"
        self.ssh = f"sshpass -p '%s' ssh -{_pty}"
        self.scp = "sshpass -p '%s' scp -r"
        self.rsync = "sshpass -p '%s' rsync -av -e ssh"
        self.empty = "> /dev/null 2>&1"
        self.strf_time = strftime("%m%d%p%I%M%S")

    def send_code_to_client(self, user, _ip, password):
        """
         发送代码到测试机
        :param user: 用户名
        :param _ip: 测试机IP
        :param password: 测试机密码
        :return:
        """
        logger.info(f"发送代码到测试机 - < {user}@{_ip} >")
        system(
            f"{self.ssh % password} {user}@{_ip} "
            f""""echo '{password}' | sudo -S rm -rf ~/{self.server_project_path}" {self.empty}"""
        )
        system(
            f'{self.ssh % password} {user}@{_ip} "mkdir -p ~/{self.server_project_path}" {self.empty}'
        )
        # 过滤目录
        app_name: str = self.default.get(Args.app_name.value)
        exclude = ""
        for i in [
            "report",
            "__pycache__",
            ".pytest_cache",
            ".vscode",
            ".idea",
            ".git",
            "docs",
            "README.md",
            "README.zh_CN.md",
            "RELEASE.md",
        ]:
            exclude += f"--exclude='{i}' "
        if app_name:
            for i in listdir(GlobalConfig.APPS_PATH):
                if i == "__init__.py":
                    continue
                if app_name.replace("-", "_") not in i:
                    exclude += f"--exclude='{i}' "
        system(
            f"{self.rsync % (password,)} {exclude} {GlobalConfig.ROOT_DIR}/* "
            f"{user}@{_ip}:~/{self.server_project_path}/ {self.empty}"
        )
        logger.info(f"代码发送成功 - < {user}@{_ip} >")

    def build_client_env(self, user, _ip, password):
        """
         测试机环境安装
        :param user: 用户名
        :param _ip: 测试机IP
        :param password: 测试机密码
        :return:
        """
        logger.info(f"安装环境 - < {user}@{_ip} >")
        system(
            f"{self.ssh % password} {user}@{_ip} "
            f'''"rm -rf ~/.local/share/virtualenvs/{self.server_project_path.split('/')[-1]}*"'''
        )
        system(
            f"{self.ssh % password} {user}@{_ip} "
            f'"cd ~/{self.server_project_path}/ && bash env.sh"'
        )
        logger.info(f"环境安装完成 - < {user}@{_ip} >")

    def send_code_and_env(self, user, _ip, password):
        """
         发送代码到测试机并且安装环境
        :param user: 用户名
        :param _ip: 测试机IP
        :param password: 测试机密码
        :return:
        """
        self.send_code_to_client(user, _ip, password)
        self.build_client_env(user, _ip, password)

    def install_deb(self, user, _ip, password):
        """
         安装 deb 包
        :param user:
        :param _ip:
        :param password:
        :return:
        """
        logger.info(f"安装deb包 - < {user}@{_ip} >")
        system(
            f"{self.scp % password} {self.default.get(Args.deb_path.value)}/*.deb {user}@{_ip}:{self.default.get(Args.deb_path.value)}/"
        )
        system(
            f'''{self.ssh % password} {user}@{_ip} "cd {self.default.get(Args.deb_path.value)}/ && echo {password} | sudo -S dpkg -i *.deb"'''
        )
        logger.info(f"deb包安装完成 - < {user}@{_ip} >")

    def mul_do(self, func_obj, client_list):
        """
         异步发送代码
        :param func_obj: 函数对象
        :param client_list: 测试机列表
        :return:
        """
        if len(client_list) >= 2:
            executor = ThreadPoolExecutor()
            _ps = []
            for client in client_list[:-1]:
                user, _ip, password = self.default.get(Args.clients.value).get(client)
                _p1 = executor.submit(func_obj, user, _ip, password)
                _ps.append(_p1)
            user, _ip, password = self.default.get(Args.clients.value).get(client_list[-1])
            func_obj(user, _ip, password)
            wait(_ps, return_when=ALL_COMPLETED)
        else:
            user, _ip, password = self.default.get(Args.clients.value).get(client_list[0])
            func_obj(user, _ip, password)

    def get_client_test_status(self, user, _ip, password):
        """
         获取测试机是否有用例执行
        :param user: 用户名
        :param _ip: 测试机IP
        :param password: 测试机密码
        :return:
        """
        status_test = popen(
            f'{self.ssh % password} {user}@{_ip} "ps -aux | grep pytest | grep -v grep"'
        ).read()
        return bool(status_test)

    @staticmethod
    def make_dir(dirs):
        """make_dir"""
        if not exists(dirs):
            makedirs(dirs)

    def run_pytest_cmd(self, user, _ip, password):
        """
         创建 Pytest 命令行参数
        :param user: 用户名
        :param _ip: 测试机IP
        :param password: 测试机密码
        :return:
        """
        # pylint: disable=too-many-branches
        real_app_name = ""
        cmd = [
            self.ssh % password,
            f"{user}@{_ip}",
            '"',
            "cd",
        ]

        l_args = list(self.local_kwargs.items())
        real_app_name = ""
        _tmp_args = []
        for i in l_args:
            if i[1] is None:
                continue
            i = list(i)
            i[0] = f"--{i[0]}"
            i[1] = f"'{i[1]}'"
            if i[0] == "--app_name":
                real_app_name = f"apps/autotest_{self.default.get(Args.app_name.value).replace('-', '_')}"
                continue

            _tmp_args.extend(i)
        cmd.extend([
            f"~/{self.server_project_path}/{real_app_name}",
            "&&",
            "pipenv",
            "run",
        ])
        from src.rtk.local_runner import LocalRunner
        lr = LocalRunner(debug=True)
        lr_args = {k:v for k, v in lr.export_default.items() if v}
        rr_args = {k:v for k, v in self.local_kwargs.items() if v}
        lr_args.update(rr_args)
        pytest_cmd = lr.create_pytest_cmd(real_app_name, default=lr_args, proj_path=f"/home/{user}/{self.server_project_path}")

        cmd.extend(pytest_cmd)
        cmd.append('"')

        cmd_str = " ".join(cmd)
        logger.info(f"\n{cmd_str}\n")
        if self.default.get(Args.debug.value):
            logger.info("DEBUG 模式不执行用例!")
        else:
            system(cmd_str)

    def pytest_co_cmd(self):
        """
         创建收集用例的命令行参数
        :return:
        """
        app_dir = (
            f"autotest_{self.default.get(Args.app_name.value).replace('-', '_')}"
            if self.default.get(Args.app_name.value)
            else ""
        )
        cmd = [
            "pytest",
            f"{GlobalConfig.APPS_PATH}/{app_dir}",
        ]
        if self.default.get(Args.keywords.value):
            cmd.extend(["-k", f"'{self.default.get(Args.keywords.value)}'"])
        if self.default.get(Args.tags.value):
            cmd.extend(["-m", f"'{self.default.get(Args.tags.value)}'"])
        if self.default.get(Args.noskip.value):
            cmd.extend(["--noskip", self.default.get(Args.noskip.value)])
        if self.default.get(Args.ifixed.value):
            cmd.extend(["--ifixed", self.default.get(Args.ifixed.value)])
        if self.default.get(Args.send_pms.value):
            cmd.extend(["--send_pms", self.default.get(Args.send_pms.value)])
        if self.default.get(Args.task_id.value):
            cmd.extend(["--task_id", self.default.get(Args.task_id.value)])
        if self.default.get(Args.trigger.value):
            cmd.extend(["--trigger", "auto"])
        cmd.append("--co")
        collect_only_cmd = " ".join(cmd)
        logger.info(f"Collecting: \n{collect_only_cmd}")
        collect_only_log = CmdCtl.run_cmd(collect_only_cmd)
        re_expr = compile(r"<Module (.*?\.py)>")
        cases = re.findall(re_expr, collect_only_log)
        if not cases:
            logger.error("未收集到用例")
            sys.exit(0)
        return cases

    def pre_env(self):
        """
         前置环境处理
        :return:
        """
        # rm hosts
        system(f"rm -rf ~/.ssh/known_hosts {self.empty}")
        # rm server report
        if self.clean_server_report_dir:
            system(f"rm -rf {GlobalConfig.REPORT_PATH}/* {self.empty}")
        # rm client report
        if not self.default.get(Args.send_code.value) and self.clean_client_report_dir:
            for client in self.default.get(Args.clients.value):
                user, _ip, password = self.default.get(Args.clients.value).get(client)
                system(
                    f"""{self.ssh % password} {user}@{_ip} "rm -rf {self.client_report_path(user)}/*" {self.empty}"""
                )
        # delete ssh ask
        sudo = f"echo '{GlobalConfig.PASSWORD}' | sudo -S"
        if "StrictHostKeyChecking no" not in popen("cat /etc/ssh/ssh_config").read():
            system(
                f"""{sudo} sed -i "s/#   StrictHostKeyChecking ask/ StrictHostKeyChecking no/g" /etc/ssh/ssh_config {self.empty}"""
            )
        # install sshpass
        if "(C)" not in popen("sshpass -V").read():
            system(f"{sudo} apt update {self.empty}")
            system(f"{sudo} apt install sshpass {self.empty}")

    def scp_report(self, user, _ip, password):
        """
         远程复制报告
        :param user:
        :param _ip:
        :param password:
        :return:
        """
        server_allure_path = f"{GlobalConfig.REPORT_PATH}/allure/{self.strf_time}_ip{_ip}_{self.default.get(Args.app_name.value)}"
        self.make_dir(server_allure_path)
        system(
            f"{self.scp % password} {user}@{_ip}:{self.client_allure_report_path(user)}/* {server_allure_path}/ {self.empty}"
        )
        generate_allure_html = f"{server_allure_path}/html"

        AllureCustom.gen(server_allure_path, generate_allure_html)

    def get_report(self, client_list):
        """
         回传测试报告
        :param client_list: 客户端列表
        :return:
        """
        # mul get report
        if len(self.default.get(Args.clients.value)) >= 2:
            _ps = []
            executor = ThreadPoolExecutor()
            for client in client_list[:-1]:
                user, _ip, password = self.default.get(Args.clients.value).get(client)
                _p4 = executor.submit(self.scp_report, user, _ip, password)
                _ps.append(_p4)
                sleep(2)
            user, _ip, password = self.default.get(Args.clients.value).get(client_list[-1])
            self.scp_report(user, _ip, password)
            wait(_ps, return_when=ALL_COMPLETED)
        else:
            user, _ip, password = self.default.get(Args.clients.value).get(client_list[0])
            self.scp_report(user, _ip, password)

    def parallel_run(self, client_list):
        """
         并行跑
        :param client_list:
        :return:
        """
        _ps = []
        executor = ThreadPoolExecutor()
        for client in client_list[:-1]:
            user, _ip, password = self.default.get(Args.clients.value).get(client)
            _p3 = executor.submit(self.run_pytest_cmd,  user, _ip, password)
            _ps.append(_p3)
            sleep(1)
        user, _ip, password = self.default.get(Args.clients.value).get(client_list[-1])
        self.run_pytest_cmd(
            user,
            _ip,
            password,
        )
        wait(_ps, return_when=ALL_COMPLETED)
        sleep(5)

    def nginx_run(self, client_list):
        """
         分布式执行
        :param client_list: 客户端列表
        :return:
        """
        # pylint: disable=too-many-nested-blocks
        case_files = self.pytest_co_cmd()
        logger.info(f"Collected {len(case_files)} case.")
        # sort case
        case_files.sort(key=lambda x: int(re.findall(r"(\d+)", x)[0]))
        _ps = []
        executor = ThreadPoolExecutor()
        for case in case_files:
            counter = {}
            try:
                # pylint: disable=unsubscriptable-object
                for client in cycle(client_list)[::-1]:
                    user, _ip, password = self.default.get(Args.clients.value).get(client)
                    if not self.get_client_test_status(user, _ip, password):
                        _p2 = executor.submit(
                            self.run_pytest_cmd,
                            user,
                            _ip,
                            password,
                            f"{splitext(case)[0]} and ({self.default.get(Args.keywords.value)})",
                            self.default.get(Args.tags.value),
                        )
                        _ps.append(_p2)
                        # relax and wait for pytest start
                        for _ in range(self.scan):
                            if self.get_client_test_status(user, _ip, password):
                                counter[client] = 0
                                break
                            # else:
                            sleep(1)
                        else:
                            client_list.remove(client)
                    else:
                        # relax
                        counter[client] = counter.get(client, 0) + 1
                        if counter.get(client) >= self.scan:
                            client_list.remove(client)
                        sleep(1)
            except ValueError:
                break
        # Wait for all child processes to end
        wait(_ps, return_when=ALL_COMPLETED)

    def remote_run(self):
        """
         远程执行主函数
        :return:
        """
        client_list = list(self.default.get(Args.clients.value).keys())
        self.pre_env()
        logger.info(
            "\n测试机列表:\n" + "\n".join([str(i) for i in self.default.get(Args.clients.value).items()])
        )
        if self.default.get(Args.build_env.value):
            self.mul_do(self.send_code_and_env, client_list)
        else:
            if self.default.get(Args.send_code.value):
                self.mul_do(self.send_code_to_client, client_list)
        if self.default.get(Args.deb_path.value):
            self.mul_do(self.install_deb, client_list)
        if self.default.get(Args.parallel.value):
            self.parallel_run(client_list)
        else:
            self.nginx_run(client_list)
        # collect and integrate result data after all tests.
        self.get_report(client_list)
