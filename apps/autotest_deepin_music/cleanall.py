#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@Author:huangmingqiang@uniontech.com
@Date  :2021/10/28 下午6:14
@Desc  :
"""
import os

from src.filectl import FileCtl
from src.cmdctl import CmdCtl
from src.button_center import ButtonCenter
from apps.autotest_deepin_music.config import Config


class CleanAll:
    """
    所有关于环境清理的方法
    """

    @classmethod
    def kill_all_process(cls):
        """杀掉所有进程"""
        app_list = [
            "dde-file-manager",
            "dde-grand-search",
            "deepin-screen-recorder",
            "deepin-movie",
            "deepin-music",
            "deepin-image-viewer",
            "deepin-album",
            "deepin-draw",
            "deepin-camera",
            "deepin-editor",
            # 'deepin-terminal',
            "deepin-compressor",
            "dde-control-center",
            "deepin-defender",
            # "dde-polkit-agent",
            "dman",  # 帮助
            "deepin-pin-screenshots",  # 贴图
        ]
        for i in app_list:
            CmdCtl.kill_process(i)

    @classmethod
    def clean_environment(cls):
        """clean_environment"""
        # 视频
        cls.clean_video()
        # 音乐
        cls.clean_music()
        # 图片
        cls.clean_picture()
        # 文档
        cls.clean_documents()
        # 桌面
        cls.clean_desktop()
        # 回收站
        cls.clean_trash()
        # 编辑器赔罪
        cls.kill_process_with_clean_env("deepin-editor")

    @classmethod
    def kill_process_with_clean_env(cls, process):
        """清理编辑器"""
        CmdCtl.kill_process(process)
        CmdCtl.run_cmd(
            f"rm -rf /home/{Config.USERNAME}/.config/deepin/{process}/*",
            command_log=False,
            interrupt=False
        )
        # 删除书签配置文件
        CmdCtl.run_cmd(
            f"rm -f /home/{Config.USERNAME}/.config/deepin/{process}.json",
            command_log=False,
            interrupt=False
        )

    @staticmethod
    def clean_desktop():
        """clean system_desktop"""
        FileCtl.delete_files(path="Desktop", ignores=("computer", "trash"))

    @staticmethod
    def clean_documents():
        """clean documents"""
        FileCtl.delete_files(path="Documents", ignores=("cd-desktop-app",))

    @staticmethod
    def clean_music():
        """clean music"""
        FileCtl.delete_files(path="Music", ignores=("bensound-sunny.mp3",))

    @staticmethod
    def clean_video():
        """clean video"""
        FileCtl.delete_files(path="Videos", ignores=("introduction.mp4",))

    @staticmethod
    def clean_picture():
        """clean picture"""
        FileCtl.delete_files(path="Pictures", ignores=("ATimage", "Wallpapers"))

    @staticmethod
    def clean_trash():
        """clean trash"""
        FileCtl.delete_files(path=".local/share/Trash")

    @staticmethod
    def kill_lastest_window(app_name):
        """kill_lastest_window
        主要用于关闭终端，通过终端批量运行用例时，如果用例中需要涉及关闭终端，调用此方法只会关闭最近新开的一个终端窗口
        如果你直接调用kill_process方法，会把所有终端都杀掉，用例也会停止运行。
        """
        os.system(f"xdotool windowclose {ButtonCenter.get_lastest_window_id(app_name)}")

    @staticmethod
    def clean_share_folder():
        """取消所有共享文件"""
        share_folder = CmdCtl.run_cmd(
            "net usershare list",
            interrupt=False,
            out_debug_flag=False,
            command_log=False,
        )
        if share_folder:
            share_folder = share_folder.split("\n")
            for folder in share_folder:
                CmdCtl.run_cmd(
                    f"net usershare delete {folder}",
                    interrupt=False,
                    out_debug_flag=False,
                    command_log=False,
                )
