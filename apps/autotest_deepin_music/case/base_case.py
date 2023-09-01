#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@File  :base_case.py
@Author:huangmingqiang@uniontech.com
@Date  :2020/6/17 上午9:45
@Desc  :
"""
from src import sleep
from public.dde_dock_public_widget.dde_dock_public_widget import DdeDockPublicWidget
from apps.autotest_deepin_music.widget.other_widget import DdeFileDialogWidget
from apps.autotest_deepin_music.widget.deepin_music_widget import DeepinMusicWidget
from apps.autotest_deepin_music.deepin_music_assert import DeepinMusicAssert


class BaseCase(DeepinMusicAssert):
    """
    音乐的基本用例
    """

    APP_NAME = "deepin-music"
    HELP_APP_NAME = "dman"
    DDE_FILE_MANAGER = "dde-file-manager"

    # def setup_method(self):
    #     """方法前置步骤"""
    #     DdeDockPublicWidget().open_music_in_dock_by_attr()
    #     DeepinMusicWidget.recovery_music_by_cmd()
    #     music = DeepinMusicWidget()
    #     music.first_add_music_by_ui()
    #
    # def teardown_method(self):
    #     """方法后置"""
    #     DeepinMusicWidget.clean_music_app_by_cmd()
    #     DeepinMusicWidget.close_music_and_clean_sqlite_by_cmd()
    #     sleep(1)
