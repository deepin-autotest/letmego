#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@Author: huangmingqiang@uniontech.com
@Desc  :
"""
import os
import letmego
from apps.autotest_deepin_music.cleanall import CleanAll

from src import sleep
from src import log
from public.dde_dock_public_widget.dde_dock_public_widget import DdeDockPublicWidget
from apps.autotest_deepin_music.widget.window_widget import WindowWidget
from apps.autotest_deepin_music.widget.title_widget import TitleWidget
from apps.autotest_deepin_music.widget.pop_widget import PopWidget
from apps.autotest_deepin_music.widget.other_widget import DdeFileManagerWidget


# pylint: disable=R0901
@letmego.mark
@log
class DeepinMusicWidget(WindowWidget, TitleWidget, PopWidget):
    """音乐业务层"""

    @staticmethod
    def reboot():
        """letmego reboot"""
        os.system("echo '1' | sudo -S reboot")

    def remove_from_playlist_with_one_file_in_music_by_ui(self):
        """一条音乐从本地删除"""
        self.right_click_first_music_in_all_music_list_view_by_ui()
        self.select_menu(4)
        sleep(1)
        self.click_remove_btn_in_pop_up_window_by_ui()

    def drag_folder_from_file_manager_to_play_list_in_music_by_attr(self, is_folder=True):
        """从文管中拖拽文件夹到音乐列表中"""
        # 双击桌面的计算图标
        self.run_cmd("rm -rf ~/.config/deepin/dde-file-manager.json", interrupt=False)
        DdeDockPublicWidget().open_file_manager_in_dock_by_attr()
        sleep(1)
        # 将文管向上拖拽
        _dde_file_manager = DdeFileManagerWidget()
        _x, _y = _dde_file_manager.dog.element_center("DMainWindowTitlebar")
        self.move_to(_x, _y)
        self.drag_to(_x - 400, 40)
        sleep(1)
        _dde_file_manager.click_music_dir_in_left_view_by_ui()
        sleep(1)
        _dde_file_manager.click_list_view_btn_in_desktop_plugs_by_ui()
        sleep(1)
        if is_folder is True:
            _x1, _y1 = _dde_file_manager.ocr("auto", return_first=True, lang="en")
            self.move_to(_x1, _y1)
        if is_folder is False:
            _x1, _y1 = _dde_file_manager.ocr("bensound-sunny", return_first=True, lang="en")
            self.move_to(_x1, _y1)
            # _dde_file_manager.dog.find_element_by_attr("$//bensound-sunny.mp3").point()
        if is_folder == "other":
            _x1, _y1 = _dde_file_manager.ocr("ac3", return_first=True, lang="en")
            self.move_to(_x1, _y1)
            # _dde_file_manager.dog.find_element_by_attr("$//ac3.ac3").point()
        _x, _y = self.ui.btn_center("添加音乐-加号")
        self.mouse_down()
        self.move_to(_x, _y + 200, duration=1.5)
        sleep(1)
        self.mouse_up()
        CleanAll.kill_process_with_clean_env("dde-file-manager")

    def drag_folder_from_file_manager_to_left_music_play_list_in_music_by_attr(
        self, is_folder=True
    ):
        """从文管中拖拽文件夹到音乐的左侧所有音乐"""
        # 双击桌面的计算图标
        self.run_cmd("rm -rf ~/.config/deepin/dde-file-manager.json", interrupt=False)
        DdeDockPublicWidget().open_file_manager_in_dock_by_attr()
        sleep(1)
        # 将文管向右下拖拽
        _dde_file_manager = DdeFileManagerWidget()
        _x, _y = _dde_file_manager.dog.element_center("DMainWindowTitlebar")
        self.move_to(_x, _y)
        self.drag_to(_x + 400, 100)
        sleep(1)
        _dde_file_manager.click_music_dir_in_left_view_by_ui()
        sleep(1)
        _dde_file_manager.click_list_view_btn_in_desktop_plugs_by_ui()
        sleep(1)
        if is_folder is True:
            _x1, _y1 = _dde_file_manager.ocr("auto", return_first=True, lang="en")
            self.move_to(_x1, _y1)
        if is_folder is False:
            _x1, _y1 = _dde_file_manager.ocr("bensound-sunny", return_first=True, lang="en")
            self.move_to(_x1, _y1)
            # _dde_file_manager.dog.find_element_by_attr("$//bensound-sunny.mp3").point()
        if is_folder == "other":
            _x1, _y1 = _dde_file_manager.ocr("ac3", return_first=True, lang="en")
            self.move_to(_x1, _y1)
            # _dde_file_manager.dog.find_element_by_attr("$//ac3.ac3").point()
        _x, _y = self.ui.btn_center("所有音乐按钮")
        self.mouse_down()
        self.move_to(_x, _y, duration=1.5)
        sleep(1)
        self.mouse_up()
        CleanAll.kill_process_with_clean_env("dde-file-manager")

    def drag_folder_from_file_manager_to_left_cd_play_list_in_music_by_attr(self, is_folder=True):
        """从文管中拖拽文件夹到音乐的左侧专辑"""
        # 双击桌面的计算图标
        self.run_cmd("rm -rf ~/.config/deepin/dde-file-manager.json", interrupt=False)
        DdeDockPublicWidget().open_file_manager_in_dock_by_attr()
        sleep(1)
        # 将文管向右下拖拽
        _dde_file_manager = DdeFileManagerWidget()
        _x, _y = _dde_file_manager.dog.element_center("DMainWindowTitlebar")
        self.move_to(_x, _y)
        self.drag_to(_x + 400, 100)
        sleep(1)
        _dde_file_manager.click_music_dir_in_left_view_by_ui()
        sleep(1)
        _dde_file_manager.click_list_view_btn_in_desktop_plugs_by_ui()
        sleep(1)
        if is_folder is True:
            _x1, _y1 = _dde_file_manager.ocr("auto", return_first=True, lang="en")
            self.move_to(_x1, _y1)
        if is_folder is False:
            _x1, _y1 = _dde_file_manager.ocr("bensound-sunny", return_first=True, lang="en")
            self.move_to(_x1, _y1)
            # _dde_file_manager.dog.find_element_by_attr("$//bensound-sunny.mp3").point()
        if is_folder == "other":
            _x1, _y1 = _dde_file_manager.ocr("ac3", return_first=True, lang="en")
            self.move_to(_x1, _y1)
            # _dde_file_manager.dog.find_element_by_attr("$//ac3.ac3").point()
        _x, _y = self.ui.btn_center("专辑按钮")
        self.mouse_down()
        self.move_to(_x, _y, duration=1.5)
        sleep(1)
        self.mouse_up()
        CleanAll.kill_process_with_clean_env("dde-file-manager")

    def drag_folder_from_file_manager_to_left_collection_play_list_in_music_by_attr(
        self, is_folder=True
    ):
        """从文管中拖拽文件夹到音乐的左侧专辑"""
        # 双击桌面的计算图标
        self.run_cmd("rm -rf ~/.config/deepin/dde-file-manager.json", interrupt=False)
        DdeDockPublicWidget().open_file_manager_in_dock_by_attr()
        sleep(1)
        # 将文管向右下拖拽
        _dde_file_manager = DdeFileManagerWidget()
        _x, _y = _dde_file_manager.dog.element_center("DMainWindowTitlebar")
        self.move_to(_x, _y)
        self.drag_to(_x + 400, 100)
        sleep(1)
        _dde_file_manager.click_music_dir_in_left_view_by_ui()
        sleep(1)
        _dde_file_manager.click_list_view_btn_in_desktop_plugs_by_ui()
        sleep(1)
        if is_folder is True:
            _x1, _y1 = _dde_file_manager.ocr("auto", return_first=True, lang="en")
            self.move_to(_x1, _y1)
        if is_folder is False:
            _x1, _y1 = _dde_file_manager.ocr("bensound-sunny", return_first=True, lang="en")
            self.move_to(_x1, _y1)
            # _dde_file_manager.dog.find_element_by_attr("$//bensound-sunny.mp3").point()
        if is_folder == "other":
            _x1, _y1 = _dde_file_manager.ocr("ac3", return_first=True, lang="en")
            self.move_to(_x1, _y1)
            # _dde_file_manager.dog.find_element_by_attr("$//ac3.ac3").point()
        _x, _y = self.ui.btn_center("我的收藏按钮")
        self.mouse_down()
        self.move_to(_x, _y, duration=1.5)
        sleep(1)
        self.mouse_up()
        CleanAll.kill_process_with_clean_env("dde-file-manager")

    @staticmethod
    def right_click_music_on_dock_tray_by_attr():
        """右键点击任务栏托盘的音乐图标"""
        DdeDockPublicWidget().dog.app_element("Form_normalcontainer").child(
            "Btn_deepin-music"
        ).click(button=3)

    @staticmethod
    def click_select_music_in_desktop_plugs_by_attr(file_list):
        """文管插件多选文件"""
        sleep(1)
        DdeDockPublicWidget().press_key_down("ctrl")
        for file in file_list:
            DeepinMusicWidget.ocr(*DeepinMusicWidget.ocr(file, return_first=True, lang="en"))
            sleep(0.5)
        DdeDockPublicWidget().press_key_up("ctrl")


if __name__ == "__main__":
    DeepinMusicWidget().del_lrc_music_by_cmd()
