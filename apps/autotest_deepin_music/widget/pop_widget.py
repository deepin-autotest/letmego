"""pop_widget"""
from apps.autotest_deepin_music.widget.base_widget import BaseWidget


# pylint: disable=R0901,R0904
class PopWidget(BaseWidget):
    """PopWidget"""
    def click_min_to_tray_in_close_pop_window_in_music_by_ui(self):
        """x-最小化到托盘"""
        self.move_to_and_click(*self.ui.btn_center("x-最小化到托盘"))

    def click_exit_in_close_pop_window_in_music_by_ui(self):
        """x-退出"""
        self.move_to_and_click(*self.ui.btn_center("x-退出"))

    def click_not_ask_in_close_pop_winddow_in_music_by_ui(self):
        """x-不再询问"""
        self.move_to_and_click(*self.ui.btn_center("x-不再询问"))

    def click_autoplay_in_music_setting_by_ui(self):
        """启动时自动播放"""
        self.move_to_and_click(*self.ui.btn_center("设置-启动时自动播放"))

    def click_close_main_window_in_music_setting_by_ui(self):
        """设置-关闭主窗口"""
        self.move_to_and_click(*self.ui.btn_center("设置-关闭主窗口"))

    def click_exit_in_close_main_window_in_music_setting_by_ui(self):
        """设置-关闭主窗口-退出"""
        self.move_to_and_click(*self.ui.btn_center("设置-关闭主窗口-退出"))

    def click_min_to_tray_in_close_main_window_in_music_setting_by_ui(self):
        """设置-关闭主窗口-最小化到托盘"""
        self.move_to_and_click(*self.ui.btn_center("设置-关闭主窗口-最小化到托盘"))

    def click_ask_every_time_in_close_main_window_in_music_setting_by_ui(self):
        """设置-关闭主窗口-每次询问"""
        self.move_to_and_click(*self.ui.btn_center("设置-关闭主窗口-每次询问"))

    def click_shotcutkey_in_music_setting_by_ui(self):
        """设置-快捷键"""
        self.move_to_and_click(*self.ui.btn_center("设置-快捷键"))

    def click_play_or_stop_in_music_setting_by_ui(self):
        """快捷键-播放/暂停"""
        self.move_to_and_click(*self.ui.btn_center("快捷键-播放/暂停"))

    def click_prev_in_music_setting_by_ui(self):
        """快捷键-上一首"""
        self.move_to_and_click(*self.ui.btn_center("快捷键-上一首"))

    def click_next_in_music_setting_by_ui(self):
        """快捷键-下一首"""
        self.move_to_and_click(*self.ui.btn_center("快捷键-下一首"))

    def click_louder_in_music_setting_by_ui(self):
        """快捷键-音量增大"""
        self.move_to_and_click(*self.ui.btn_center("快捷键-音量增大"))

    def click_lower_voice_in_music_setting_by_ui(self):
        """快捷键-音量减小"""
        self.move_to_and_click(*self.ui.btn_center("快捷键-音量减小"))

    def click_menu_in_music_by_ui(self):
        """点击菜单"""
        self.move_to_and_click(*self.ui.btn_center("菜单"))

    def click_equalizer_in_music_by_ui(self):
        """点击均衡器"""
        self.click_menu_in_music_by_ui()
        self.reverse_select_menu(6)

    def click_switch_btn_in_equalizer_by_ui(self):
        """点击均衡器-开关"""
        self.move_to_and_click(*self.ui.btn_center("均衡器-开关"))

    def click_switch_select_box_in_equalizer_by_ui(self):
        """均衡器-下拉框"""
        self.move_to_and_click(*self.ui.btn_center("均衡器-下拉框"))

    def click_restore_btn_in_equalizer_by_ui(self):
        """点击均衡器恢复默认"""
        self.move_to_and_click(*self.ui.btn_center("均衡器-恢复默认"))

    def click_baudpre_in_equalizer_by_ui(self):
        """点击前置放大器滑块区"""
        self.move_to_and_click(*self.ui.btn_center("均衡器-前置放大器"))

    def point_baudpre_in_equalizer_by_ui(self):
        """移动到前置放大器滑块区"""
        self.move_to(*self.ui.btn_center("均衡器-前置放大器"))

    def click_delete_btn_in_pop_up_window_by_ui(self):
        """点击本地删除小弹窗里面的“删除”按钮"""
        self.move_to_and_click(*self.ui.btn_center("删除弹窗-确定"))

    def click_remove_btn_in_pop_up_window_by_ui(self):
        """点击从歌单中删除小弹窗里面的“移除”按钮"""
        self.move_to_and_click(*self.ui.btn_center("删除弹窗-移除"))

    def click_cancel_btn_in_pop_up_window_by_ui(self):
        """点击从歌单中删除小弹窗里面的“取消”按钮"""
        self.move_to_and_click(*self.ui.btn_center("删除弹窗-取消"))

    def click_fading_in_music_setting_by_ui(self):
        """点击设置开启淡入淡出"""
        self.move_to_and_click(*self.ui.btn_center("设置-开启淡入淡出"))
