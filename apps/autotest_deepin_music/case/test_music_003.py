#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@File  :test_music_003.py
@Author:huangmingqiang@uniontech.com
@Date  :2020/6/17 上午9:35
@Desc  :
"""
from apps.autotest_deepin_music.widget.deepin_music_widget import DeepinMusicWidget
from apps.autotest_deepin_music.case.base_case import BaseCase
from public.dde_dock_public_widget.dde_dock_public_widget import DdeDockPublicWidget
from src import sleep


class TestMusic(BaseCase):
    """
    音乐用例
    """

    def test_music_003(self):
        """专辑-列表字段"""

        # 1.启动音乐，导入歌曲
        # 2.点击左侧工具栏的专辑，查看列表页
        music = DeepinMusicWidget()
        music.click_cd_btn_in_music_by_ui()
        # 3.改为缩略图展示
        music.click_icon_mode_in_music_by_ui()
        # 断言
        self.assert_music_image_exist("music_003")

    def setup_method(self):
        """方法前置步骤"""
        DdeDockPublicWidget().open_music_in_dock_by_attr()
        DeepinMusicWidget.recovery_music_by_cmd()
        music = DeepinMusicWidget()
        music.first_add_music_by_ui()

    def teardown_method(self):
        """方法后置"""
        DeepinMusicWidget.clean_music_app_by_cmd()
        DeepinMusicWidget.close_music_and_clean_sqlite_by_cmd()
        sleep(1)

