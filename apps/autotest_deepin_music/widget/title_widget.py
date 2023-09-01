"""title_widget"""
from src import sleep
from apps.autotest_deepin_music.widget.base_widget import BaseWidget


# pylint: disable=R0901
class TitleWidget(BaseWidget):
    """TitleWidget"""
    def click_menu_in_music_by_ui(self):
        """菜单"""
        self.move_to_and_click(*self.ui.btn_center("菜单"))

    def click_close_btn_in_music_by_ui(self):
        """x"""
        self.move_to_and_click(*self.ui.btn_center("x"))

    def click_add_btn_on_title_by_ui(self):
        """点击标题栏添加音乐+号"""
        self.move_to_and_click(*self.ui.btn_center("标题栏+号"))

    def click_max_btn_in_music_by_ui(self):
        """最大化"""
        self.move_to_and_click(*self.ui.btn_center("最大化"))

    def click_search_edit_in_music_by_ui(self):
        """点击搜索框"""
        self.move_to_and_click(*self.ui.btn_center("搜索"))

    def sendkey_to_search_in_music_by_ui(self, txt="sunny"):
        """搜索框输入文本"""
        self.click_search_edit_in_music_by_ui()
        self.input_message(txt)
        self.enter()
        sleep(1)

    def right_click_search_edit_in_music_by_ui(self):
        """右键搜索框"""
        self.move_to_and_right_click(*self.ui.btn_center("搜索"))
