"""window_widget"""
from src import ElementNotFound
from apps.autotest_deepin_music.widget.base_widget import BaseWidget


# pylint: disable=R0901,R0904
class WindowWidget(BaseWidget):
    """WindowWidget"""
    def click_music_in_music_list_by_attr(self):
        """点击"音乐列表"的音乐"""
        try:
            self.dog.app_element("playListView").children[0].click()
        except (IndexError, ElementNotFound) as exc:
            raise ElementNotFound("音乐列表") from exc

    def click_import_btn_in_music_by_ui(self):
        """添加歌曲目录"""
        self.move_to_and_click(*self.ui.btn_center("添加歌曲目录"))

    def hover_add_btn_in_music_by_ui(self):
        """hover 标题栏的加号，显示添加音乐"""
        self.move_to(*self.ui.btn_center("添加音乐-加号"))

    def click_add_btn_in_music_by_ui(self):
        """通过标题栏的加号添加音乐"""
        self.move_to_and_click(*self.ui.btn_center("添加音乐-加号"))

    def click_import_music_btn_in_music_by_ui(self):
        """添加歌曲文件"""
        self.move_to_and_click(*self.ui.btn_center("添加歌曲文件"))

    def click_scan_text_in_music_by_ui(self):
        """扫描"""
        self.move_to_and_click(*self.ui.btn_center("扫描"))

    def click_add_music_list_btn_in_music_by_ui(self):
        """点击新建歌单按钮"""
        self.move_to_and_click(*self.ui.btn_center("新建歌单+"))

    def click_cd_btn_in_music_by_ui(self):
        """点击专辑"""
        self.move_to_and_click(*self.ui.btn_center("专辑按钮"))

    def right_cd_btn_in_music_by_ui(self):
        """右键专辑"""
        self.move_to_and_right_click(*self.ui.btn_center("专辑按钮"))

    def click_singer_btn_in_music_by_ui(self):
        """点击演唱者"""
        self.move_to_and_click(*self.ui.btn_center("演唱者按钮"))

    def right_singer_btn_in_music_by_ui(self):
        """右键演唱者"""
        self.move_to_and_right_click(*self.ui.btn_center("演唱者按钮"))

    def click_all_music_in_music_by_ui(self):
        """点击所有音乐"""
        self.move_to_and_click(*self.ui.btn_center("所有音乐按钮"))

    def right_all_music_in_music_by_ui(self):
        """点击所有音乐"""
        self.move_to_and_right_click(*self.ui.btn_center("所有音乐按钮"))

    def click_my_collection_view_in_music_by_ui(self):
        """点击我的收藏"""
        self.move_to_and_click(*self.ui.btn_center("我的收藏按钮"))

    def right_my_collection_view_in_music_by_ui(self):
        """点击我的收藏"""
        self.move_to_and_right_click(*self.ui.btn_center("我的收藏按钮"))

    def my_collection_center_in_music_by_ui(self):
        """返回我的收藏的中心坐标"""
        return self.ui.btn_center("我的收藏按钮")

    def click_icon_mode_in_music_by_ui(self):
        """矩阵模式"""
        self.move_to_and_click(*self.ui.btn_center("矩阵按钮"))

    def click_list_mode_in_music_by_ui(self):
        """列表模式"""
        self.move_to_and_click(*self.ui.btn_center("列表按钮"))

    def click_music_dropdown_in_music_by_ui(self):
        """排序按钮"""
        self.move_to_and_click(*self.ui.btn_center("排序按钮"))

    def click_music_sort_in_music_by_ui(self):
        """排序"""
        self.move_to_and_click(*self.ui.btn_center("排序"))

    def click_playall_btn_in_second_page_in_music_by_ui(self):
        """二级页面的-播放所有"""
        self.move_to_and_click(*self.ui.btn_center("播放所有-二级界面"))

    def click_playall_btn_in_first_page_in_music_by_ui(self):
        """一级页面的-播放所有"""
        self.move_to_and_click(*self.ui.btn_center("播放所有-一级界面"))

    def click_play_random_in_music_by_ui(self):
        """随机播放"""
        self.move_to_and_click(*self.ui.btn_center("随机播放"))

    def double_click_search_icon_file_by_ui(self):
        """双击搜索试图下的音乐图标"""
        self.move_to_and_double_click(*self.ui.btn_center("搜索试图下的音乐-icon"))

    def click_search_icon_file_in_music_by_ui(self):
        """左键点击搜索试图下的音乐图标"""
        self.move_to_and_click(*self.ui.btn_center("搜索试图下的音乐-icon"))

    def right_click_search_icon_file_in_music_by_ui(self):
        """右键点击搜索试图下的音乐图标"""
        self.move_to_and_right_click(*self.ui.btn_center("搜索试图下的音乐-icon"))

    def right_click_search_list_file_in_music_by_ui(self):
        """右键点击搜索试图下的音乐"""
        self.move_to_and_right_click(*self.ui.btn_center("搜索试图下的音乐-list"))

    def click_prev_btn_in_music_by_ui(self):
        """点击上一首按钮"""
        self.move_to_and_click(*self.ui.btn_center("上一首"))

    def move_to_prev_btn_in_music_by_ui(self):
        """移动到上一首按钮"""
        self.move_to(*self.ui.btn_center("上一首"))

    def click_next_btn_in_music_by_ui(self):
        """点击下一首按钮"""
        self.move_to_and_click(*self.ui.btn_center("下一首"))

    def move_to_next_btn_in_music_by_ui(self):
        """移动到下一首按钮"""
        self.move_to(*self.ui.btn_center("下一首"))

    def click_play_btn_in_music_by_ui(self):
        """点击播放按钮"""
        self.move_to_and_click(*self.ui.btn_center("播放按钮"))

    def move_to_play_btn_in_music_by_ui(self):
        """移动到播放按钮"""
        self.move_to(*self.ui.btn_center("播放按钮"))

    def click_cover_in_music_by_ui(self):
        """播放模式，显示歌词"""
        self.move_to_and_click(*self.ui.btn_center("工具栏-文件图标"))

    def click_collection_btn_in_music_by_ui(self):
        """点击收藏按钮"""
        self.move_to_and_click(*self.ui.btn_center("加收藏按钮"))

    def move_to_collection_btn_in_music_by_ui(self):
        """移动到收藏按钮"""
        self.move_to(*self.ui.btn_center("加收藏按钮"))

    def click_lyric_in_music_by_ui(self):
        """点击显示歌词按钮"""
        self.move_to_and_click(*self.ui.btn_center("显示歌词按钮"))

    def move_to_lyric_in_music_by_ui(self):
        """移动到显示歌词按钮"""
        self.move_to(*self.ui.btn_center("显示歌词按钮"))

    def click_play_mode_btn_in_music_by_ui(self):
        """点击播放模式按钮"""
        self.move_to_and_click(*self.ui.btn_center("播放模式按钮"))

    def move_to_play_mode_btn_in_music_by_ui(self):
        """移动到播放模式按钮"""
        self.move_to(*self.ui.btn_center("播放模式按钮"))

    def click_sound_in_music_by_ui(self):
        """音量"""
        self.move_to_and_click(*self.ui.btn_center("音量"))

    def move_to_sound_in_music_by_ui(self):
        """移动到音量"""
        self.move_to(*self.ui.btn_center("音量"))

    def click_play_list_btn_in_music_by_ui(self):
        """点击播放列表按钮"""
        self.move_to_and_click(*self.ui.btn_center("播放列表按钮"))

    def move_to_play_list_btn_in_music_by_ui(self):
        """移动到播放列表按钮"""
        self.move_to(*self.ui.btn_center("播放列表按钮"))

    def click_lowest_sound_in_scroll_bar_by_ui(self):
        """点击音量条【调节控件】下方的高亮区域"""
        x_axios, y_axios = self.ui.btn_center("音量")
        self.move_to_and_click(x_axios, y_axios - 92)

    def click_mute_btn_in_scroll_bar_by_ui(self):
        """点击音量条上的【静音按钮】"""
        x_axios, y_axios = self.ui.btn_center("音量")
        self.move_to_and_click(x_axios, y_axios - 66)

    def click_clear_all_btn_in_music_by_ui(self):
        """清空列表"""
        self.move_to_and_click(*self.ui.btn_center("清空列表"))

    def drag_music_to_my_collection_in_music_by_attr(self):
        """拖拽音乐到我的收藏"""
        self.click_music_in_music_list_by_attr()
        self.drag_to(*self.ui.btn_center("我的收藏按钮"))

    def drag_music_to_first_new_music_list_in_music_by_attr(self):
        """拖拽音乐到新建歌单"""
        self.click_music_in_music_list_by_attr()
        self.drag_to(*self.ui.btn_center("新建歌单"))

    def right_click_first_new_music_list_in_music_by_ui(self):
        """右键点击新建歌单"""
        self.move_to_and_right_click(*self.ui.btn_center("新建歌单"))

    def double_click_first_new_music_list_in_music_by_ui(self):
        """双击点击新建歌单"""
        self.move_to_and_double_click(*self.ui.btn_center("新建歌单"))

    def click_first_new_music_list_in_music_by_ui(self):
        """点击新建歌单"""
        self.move_to_and_click(*self.ui.btn_center("新建歌单"))

    def move_to_first_new_music_list_in_music_by_ui(self):
        """移动新建歌单"""
        self.move_to(*self.ui.btn_center("新建歌单"))

    def drag_new_music_list_sorting_in_music_by_ui(self):
        """拖拽新建歌单到新建歌单三"""
        self.click_first_new_music_list_in_music_by_ui()
        self.drag_to(*self.ui.btn_center("新建歌单3"))

    def click_add_music_list_in_music_by_ui(self):
        """在空白的歌单中添加音乐"""
        self.move_to_and_click(*self.ui.btn_center("歌单-添加音乐"))

    def click_delete_btn_in_pop_up_window_by_ui(self):
        """点击删除按钮"""
        self.move_to_and_click(*self.ui.btn_center("删除弹窗-确定"))

    def delete_first_new_music_list_ui(self):
        """删除“新建歌单”"""
        self.right_click_first_new_music_list_in_music_by_ui()
        self.reverse_select_menu(1)
        self.click_delete_btn_in_pop_up_window_by_ui()

    def click_rename_first_new_music_list_in_music_by_ui(self):
        """重命名新建歌单"""
        self.right_click_first_new_music_list_in_music_by_ui()
        self.reverse_select_menu(2)

    def click_add_first_new_music_list_in_music_by_ui(self):
        """在新建歌单中添加音乐"""
        self.right_click_first_new_music_list_in_music_by_ui()
        self.reverse_select_menu(3)

    def double_click_music_in_second_page_in_cd_list_view_by_ui(self):
        """双击专辑"音乐列表"的音乐"""
        self.move_to_and_double_click(*self.ui.btn_center("专辑-二级页面中的音乐"))

    def right_click_music_in_second_page_in_cd_list_view_by_ui(self):
        """右键点击专辑中的音乐"""
        self.move_to_and_right_click(*self.ui.btn_center("专辑-二级页面中的音乐"))

    def click_music_in_second_page_in_cd_list_view_by_ui(self):
        """点击专辑中的音乐"""
        self.move_to_and_click(*self.ui.btn_center("专辑-二级页面中的音乐"))

    def right_click_first_music_in_all_music_list_view_by_ui(self):
        """列表模式下，右键点击"音乐列表"的音乐"""
        self.move_to_and_right_click(*self.ui.btn_center("所有音乐中的第一首音乐-list视图"))

    def move_to_first_music_in_all_music_list_view_by_ui(self):
        """列表模式下，右键点击"音乐列表"的音乐"""
        self.move_to(*self.ui.btn_center("所有音乐中的第一首音乐-list视图"))

    def click_close_first_music_info_in_all_music_list_view_by_ui(self):
        """列表模式下，关闭第一首歌曲的信息弹窗窗口"""
        _x, _y = self.ui.window_right_top_position()
        # _w, _h = self.__obj.window_sizes()
        self.move_to_and_click(_x - 26, _y + 26)

    def get_mainwindow_size_in_music_by_ui(self):
        """获取音乐窗口大小"""
        return self.ui.window_sizes()

    def click_first_music_in_all_music_list_view_by_ui(self):
        """列表模式下，点击"音乐列表"的音乐"""
        self.move_to_and_click(*self.ui.btn_center("所有音乐中的第一首音乐-list视图"))

    def right_click_first_music_in_search_in_music_list_by_ui(self):
        """右键点击"搜索界面的第一首音乐"""
        self.move_to_and_right_click(*self.ui.btn_center("搜索界面的第一首音乐"))

    def double_click_first_music_in_all_music_list_view_by_ui(self):
        """列表模式下，双击“音乐列表”的音乐"""
        self.move_to_and_double_click(*self.ui.btn_center("所有音乐中的第一首音乐-list视图"))

    def double_click_first_music_in_all_music_icon_view_by_ui(self):
        """平铺模式下，双击“音乐列表”的音乐"""
        self.move_to_and_double_click(*self.ui.btn_center("所有音乐中的第一首音乐-icon视图"))

    def move_to_first_music_in_all_music_icon_view_by_ui(self):
        """平铺模式下，移动到“音乐列表”的音乐"""
        self.move_to(*self.ui.btn_center("所有音乐中的第一首音乐-icon视图"))

    def click_first_music_in_all_music_icon_view_by_ui(self):
        """平铺模式下，单击“音乐列表”的音乐"""
        self.move_to_and_click(*self.ui.btn_center("所有音乐中的第一首音乐-icon视图"))

    def double_click_second_music_in_all_music_by_ui(self):
        """双击“音乐列表”的第二首音乐"""
        self.move_to_and_double_click(*self.ui.btn_center("所有音乐中的第二首音乐"))

    def click_second_music_in_all_music_by_ui(self):
        """点击“音乐列表”的第二首音乐"""
        self.move_to_and_click(*self.ui.btn_center("所有音乐中的第二首音乐"))

    def right_click_second_music_in_all_music_by_ui(self):
        """右键点击“音乐列表”的第二首音乐"""
        self.move_to_and_right_click(*self.ui.btn_center("所有音乐中的第二首音乐"))

    def double_click_first_singer_in_singer_list_view_by_ui(self):
        """列表模式下，双击“演唱者”，进入演唱者列表"""
        self.move_to_and_double_click(*self.ui.btn_center("演唱者-一级页面-list视图"))

    def double_click_first_singer_in_singer_icon_view_by_ui(self):
        """平铺模式下，双击“演唱者”，进入演唱者列表"""
        _x, _y = self.ui.btn_center("演唱者-一级页面-icon视图")
        self.double_click(_x, _y, interval=0.2)

    def click_first_singer_in_singer_icon_view_by_ui(self):
        """平铺模式下，点击“演唱者”，播放音乐"""
        self.move_to_and_click(*self.ui.btn_center("演唱者-一级页面-icon视图"))

    def double_click_first_cd_in_music_list_view_by_ui(self):
        """列表模式下，双击“专辑”，进入专辑者列表 (位置同演唱者)"""
        self.move_to_and_double_click(*self.ui.btn_center("演唱者-一级页面-list视图"))

    def right_click_singer_file_in_music_by_ui(self):
        """右键点击演唱者列表中的“演唱者”"""
        self.move_to_and_right_click(*self.ui.btn_center("演唱者-二级页面"))

    def click_singer_file_in_music_by_ui(self):
        """点击演唱者列表中的“演唱者”"""
        self.move_to_and_click(*self.ui.btn_center("演唱者-二级页面"))

    def double_click_singer_file_in_music_by_ui(self):
        """双击演唱者列表中的“演唱者”"""
        self.move_to_and_double_click(*self.ui.btn_center("演唱者-二级页面"))

    def click_back_btn_in_music_by_ui(self):
        """在专辑界面点击返回按钮"""
        self.move_to_and_click(*self.ui.btn_center("返回按钮"))

    def first_add_music_by_ui(self):
        """打开应用，添加音乐"""
        self.click_scan_text_in_music_by_ui()

    def right_click_music_in_play_list_by_attr(self):
        """右键单击"播放列表"中的音乐"""
        # 播放列表UI bug
        try:
            self.dog.app_element("PlayQueue").children[3][0].click(button=3)
        except IndexError:
            raise ElementNotFound("播放列表") from IndexError

    def click_music_in_play_list_by_attr(self):
        """单击"播放列表"中的音乐"""
        # 播放列表UI bug
        try:
            self.dog.app_element("PlayQueue").children[3][0].click()
        except IndexError:
            raise ElementNotFound("播放列表") from IndexError

    def move_to_music_in_play_list_by_attr(self):
        """单击"播放列表"中的音乐"""
        # 播放列表UI bug
        try:
            self.dog.app_element("PlayQueue").children[3][0].point()
        except IndexError:
            raise ElementNotFound("播放列表") from IndexError

if __name__ == '__main__':
    WindowWidget().click_scan_text_in_music_by_ui()