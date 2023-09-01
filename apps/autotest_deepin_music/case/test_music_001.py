#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@File  :test_music_001.py
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

    def test_music_001(self):
        """右键菜单添加歌曲到我的歌单"""

        # 1.启动音乐导入歌曲，点击“我的歌单”右边“+”
        music = DeepinMusicWidget()
        music.click_add_music_list_btn_in_music_by_ui()
        # 3.点击“所有音乐”
        music.click_all_music_in_music_by_ui()
        # 4.选择“所有音乐”任意歌曲，右键唤起右键菜单
        music.right_click_first_music_in_all_music_list_view_by_ui()
        # 5.选择“添加到歌单”点击“新建歌单”
        DeepinMusicWidget.select_menu(2)
        DeepinMusicWidget.select_submenu(4)
        # 断言：判断新建歌单中存在添加的音乐
        music.click_first_new_music_list_in_music_by_ui()
        raise AssertionError
        # self.assert_music_image_exist("music_001_2")

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
