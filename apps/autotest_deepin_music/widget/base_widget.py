#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@Author: huangmingqiang@uniontech.com
@Desc  :
"""
import shutil
from os.path import exists
from os import popen
from src import logger
from src import sleep
from src import Src
from apps.autotest_deepin_music.config import Config
from apps.autotest_deepin_music.cleanall import CleanAll


# pylint: disable=R0901
class BaseWidget(Src):
    """音乐基类"""

    PACKAGE = "deepin-music"
    DESC = "/usr/bin/deepin-music"

    def __init__(self, check_start=True):
        """__init__"""
        Src.__init__(
            self,
            name=self.PACKAGE,
            description=self.DESC,
            config_path=Config.UI_INI_PATH,
            check_start=check_start,
        )

    @classmethod
    def find_manual_music(cls, *elements, rate=0.9):
        """查找图片坐标"""
        element = tuple(map(lambda x: f"{Config.PIC_RES_PATH}/{x}", elements))
        return cls.find_image(*element, rate=rate)

    @classmethod
    def clean_music_app_by_cmd(cls):
        """删除音乐的数据库"""
        popen(f"rm -rf /home/{Config.USERNAME}/.cache/deepin/deepin-music/*")
        popen(f"rm -rf /home/{Config.USERNAME}/.config/deepin/deepin-music*")
        cls.kill_process("deepin-music")

    @classmethod
    def close_music_and_clean_sqlite_by_cmd(cls):
        """关闭音乐"""
        cls.kill_process("deepin-music")
        cls.delete_music_sqlite_by_cmd()
        cls.esc()

    @classmethod
    def delete_music_sqlite_by_cmd(cls):
        """删除音乐的数据库"""
        cls.run_cmd(f"rm -rf /home/{Config.USERNAME}/.cache/deepin/deepin-music/mediameta.sqlite")

    @classmethod
    def sendkeys_to_new_music_list_by_cmd(cls):
        """重命名新建歌单为‘你好’"""
        cls.ctrl_a()
        cls.backspace()
        cls.input_message("你好")
        sleep(1)
        cls.enter()

    @classmethod
    def copy_other_music_by_py(cls, music_name="a-test"):
        """复制另一首音乐到“音乐”目录下"""
        shutil.copyfile(
            "/usr/share/music/bensound-sunny.mp3",
            f"/home/{Config.USERNAME}/Music/{music_name}.mp3",
        )

    @classmethod
    def delete_copy_music_by_cmd(cls):
        """删除复制的音乐"""
        cls.run_cmd(f"rm -rf /home/{Config.USERNAME}/Music/a-test.mp3")

    @staticmethod
    def recovery_music_by_cmd(exclusive=True):
        """恢复音乐文件"""
        if not exists(f"/home/{Config.USERNAME}/Music/bensound-sunny.mp3"):
            shutil.copyfile(
                "/usr/share/music/bensound-sunny.mp3",
                f"/home/{Config.USERNAME}/Music/bensound-sunny.mp3",
            )
        BaseWidget.run_cmd(
            (f"echo '{Config.PASSWORD}'|sudo -S chmod -R 777 "
             f"/home/{Config.USERNAME}/Music/bensound-sunny.mp3")
        )
        if exclusive:
            CleanAll.clean_music()

    @classmethod
    def recovery_many_music_by_cmd(cls):
        """恢复大量音乐"""
        if not exists(f"/home/{Config.USERNAME}/Music/auto"):
            if not exists(f"{Config.CASE_RES_PATH}/auto"):
                logger.info(f"下载测试资源 {Config.SOURCE_URL}/多媒体/音乐/autoUse/1auto.zip")
                cls.run_cmd(
                    f"cd {Config.CASE_RES_PATH}/ && "
                    f"wget {Config.SOURCE_URL}/多媒体/音乐/autoUse/1auto.zip && "
                    "unzip 1auto.zip;"
                    "rm -rf 1auto.zip",
                    timeout=None,
                    interrupt=False,
                    out_debug_flag=False,
                )
        cls.run_cmd(
            f"ln -s {Config.CASE_RES_PATH}/auto /home/{Config.USERNAME}/Music/auto",
            timeout=None,
            interrupt=False,
            out_debug_flag=False,
        )

    @classmethod
    def recovery_sorted_music_by_cmd(cls):
        """恢复排序音乐"""
        if not exists(f"{Config.CASE_RES_PATH}/sorted"):
            logger.info(f"下载测试资源 {Config.SOURCE_URL}/多媒体/音乐/autoUse/sorted_music.zip")
            cls.run_cmd(
                f"mkdir {Config.CASE_RES_PATH}/sorted && "
                f"cd {Config.CASE_RES_PATH}/sorted && "
                f"wget {Config.SOURCE_URL}/多媒体/音乐/autoUse/sorted_music.zip && "
                "unzip sorted_music.zip;"
                "rm -rf sorted_music.zip",
                timeout=None,
                interrupt=False,
                out_debug_flag=False,
            )
        cls.run_cmd(
            f"ln -s {Config.CASE_RES_PATH}/sorted /home/{Config.USERNAME}/Music/sorted",
            timeout=None,
            interrupt=False,
            out_debug_flag=False,
        )

    @classmethod
    def recovery_deep_path_sorted_music_by_cmd(cls):
        """恢复有路径的排序音乐"""
        if not exists(f"{Config.CASE_RES_PATH}/deep_path"):
            cls.run_cmd(
                f"mkdir -p {Config.CASE_RES_PATH}/deep_path && "
                f"cd {Config.CASE_RES_PATH}/deep_path && "
                f"wget {Config.SOURCE_URL}/多媒体/音乐/autoUse/sorted_music.zip && "
                "unzip sorted_music.zip;"
                "rm -rf sorted_music.zip",
                timeout=None,
                interrupt=False,
                out_debug_flag=False,
            )
        cls.run_cmd(
            f"ln -s {Config.CASE_RES_PATH}/deep_path /home/{Config.USERNAME}/Music/deep_path",
            timeout=None,
            interrupt=False,
            out_debug_flag=False,
        )

    @classmethod
    def recovery_pages_music_by_cmd(cls):
        """恢复可以翻页的音乐"""
        if not exists(f"{Config.CASE_RES_PATH}/40"):
            cls.run_cmd(
                f"cd {Config.CASE_RES_PATH}/ && "
                f"wget {Config.SOURCE_URL}/多媒体/音乐/autoUse/40.zip && "
                "unzip 40.zip; "
                "rm -rf 40.zip",
                timeout=None,
                interrupt=False,
                out_debug_flag=False,
            )
        cls.run_cmd(
            f"ln -s {Config.CASE_RES_PATH}/40 /home/{Config.USERNAME}/Music/40",
            timeout=None,
            interrupt=False,
            out_debug_flag=False,
        )

    @classmethod
    def recovery_uos_music_by_cmd(cls):
        """恢复单个文件的音乐文件"""
        if not exists(f"/home/{Config.USERNAME}/Music/ac3.ac3"):
            cls.run_cmd(
                f"cd /home/{Config.USERNAME}/Music;"
                f"wget {Config.SOURCE_URL}/多媒体/音乐/autoUse/ac3.ac3",
                timeout=None,
                interrupt=False,
                out_debug_flag=False,
            )

    @classmethod
    def recovery_format_music_by_cmd(cls, name):
        """恢复单个文件的不同格式"""

        # 将自带的mp3 清除掉
        if exists(f"/home/{Config.USERNAME}/Music/bensound-sunny.mp3"):
            cls.run_cmd(f"rm -rf /home/{Config.USERNAME}/Music/bensound-sunny.mp3")

        if not exists(f"/home/{Config.USERNAME}/Music/{name}.{name}"):
            cls.run_cmd(
                f"cd /home/{Config.USERNAME}/Music;"
                f"wget {Config.SOURCE_URL}/多媒体/音乐/autoUse/{name}.{name}",
                interrupt=False,
                out_debug_flag=False,
            )

    @classmethod
    def recovery_lrc_music_by_cmd(cls):
        """恢复带歌词的音乐文件"""

        # 将自带的mp3 清除掉
        if exists(f"/home/{Config.USERNAME}/Music/bensound-sunny.mp3"):
            cls.run_cmd(f"rm -rf /home/{Config.USERNAME}/Music/bensound-sunny.mp3")

        if not exists(f"/home/{Config.USERNAME}/Music/auto"):
            cls.run_cmd(
                f"mkdir /home/{Config.USERNAME}/Music/auto;"
                f"cd /home/{Config.USERNAME}/Music/auto;"
                f"wget {Config.SOURCE_URL}/多媒体/音乐/autoUse/lrc.zip;"
                "unzip lrc.zip;"
                "rm -rf lrc.zip;",
                interrupt=False,
                out_debug_flag=False,
            )

    @classmethod
    def del_lrc_music_by_cmd(cls):
        """删除带歌词的音乐文件"""
        if exists(f"/home/{Config.USERNAME}/Music/auto"):
            cls.run_cmd(f"rm -rf  /home/{Config.USERNAME}/Music/auto")

    @classmethod
    def del_recovery_pages_music_by_cmd(cls):
        """删除40个音乐文件"""
        if exists(f"/home/{Config.USERNAME}/Music/40"):
            cls.run_cmd(f"rm -rf  /home/{Config.USERNAME}/Music/40")


if __name__ == "__main__":
    BaseWidget.recovery_deep_path_sorted_music_by_cmd()
