#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@File  :test_music_002.py
@Author:huangmingqiang@uniontech.com
@Date  :2020/6/17 上午9:35
@Desc  :
"""
import os
from apps.autotest_deepin_music.widget.deepin_music_widget import DeepinMusicWidget
from apps.autotest_deepin_music.case.base_case import BaseCase
from public.dde_dock_public_widget.dde_dock_public_widget import DdeDockPublicWidget
from src import ApplicationStartError, sleep


class TestMusic(BaseCase):
    """
    音乐用例
    """
    
    def setup_method(self):
        """方法前置步骤"""
        try:
            DdeDockPublicWidget().open_music_in_dock_by_attr()
            DeepinMusicWidget.recovery_music_by_cmd()
            music = DeepinMusicWidget()
            music.first_add_music_by_ui()
        except ApplicationStartError:
            pass

    def test_music_002(self):
        """演唱者-列表字段"""

        # 1.启动音乐，导入歌曲
        # 2.点击左侧工具栏的演唱者，查看列表页
        try:
            music = DeepinMusicWidget()
            music.click_singer_btn_in_music_by_ui()
            # 3.改为缩略图展示
            music.click_icon_mode_in_music_by_ui()
        except ApplicationStartError:
            pass
        # reboot
        DeepinMusicWidget.reboot()
        # 继续
        DdeDockPublicWidget().open_music_in_dock_by_attr()
        DeepinMusicWidget.recovery_music_by_cmd()
        music = DeepinMusicWidget()
        music.first_add_music_by_ui()
        # 之前跑过的用例
        music = DeepinMusicWidget()
        music.click_singer_btn_in_music_by_ui()
        music.click_icon_mode_in_music_by_ui()
        # 断言：音乐是否展示为缩略图
        self.assert_music_image_exist("music_002")

    def teardown_method(self):
        """方法后置"""
        DeepinMusicWidget.clean_music_app_by_cmd()
        DeepinMusicWidget.close_music_and_clean_sqlite_by_cmd()
        sleep(1)