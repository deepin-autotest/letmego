"""other_widget"""

from src.depends.dogtail.tree import SearchError
from src import Src, log, logger, sleep
from src import DbusUtils
from src import ElementNotFound
from apps.autotest_deepin_music.config import Config


# pylint: disable=R0901
@log
class DdeFileManagerWidget(Src):
    """DdeFileManagerWidget"""
    APP_NAME = "dde-file-manager"
    DESC = "/usr/bin/dde-file-manager"

    def __init__(self):
        """__init__"""
        Src.__init__(
            self,
            name=self.APP_NAME,
            description=self.DESC,
            config_path=Config.OTHER_INI_PATH,
        )

    def click_list_view_btn_in_desktop_plugs_by_ui(self):
        """
         调用文管，点击右下角“列表视图“
        :return:
        """
        self.move_to_and_click(*self.ui.btn_center("dde-file-manager-列表视图"))

    def click_music_dir_in_left_view_by_ui(self):
        """点击音乐目录"""
        self.move_to_and_click(*self.ui.btn_center("dde-file-manager-音乐"))

    def click_icon_view_in_right_view_by_right_menu(self):
        """右键菜单选择“图标视图”"""
        self.move_to_and_right_click(960, 540)
        self.select_menu(3)
        sleep(0.5)
        self.enter()

    def right_click_first_file_under_icon_in_right_view_by_ui(self, flag="not_trash"):
        """右键图标模式下的第一个文件"""
        if flag not in ("not_trash", "trash"):
            raise ValueError
        x_axios, y_axios = self.ui.btn_center("dde-file-manager-图标模式下的第一个文件")
        self.move_to_and_right_click(x_axios, y_axios + 56 if flag == "trash" else y_axios)

    def double_click_file_in_right_view_by_attr(self, file_name):
        """双击打开文管右侧文件"""
        try:
            self.dog.find_element_by_attr(f"$//{file_name}").point()
            self.double_click()
        except SearchError:
            raise ElementNotFound(file_name) from SearchError

    def double_click_first_file_under_icon_in_right_view_by_ui(self, flag="not_trash"):
        """双击图标模式下的第一个文件"""
        if flag not in ("not_trash", "trash"):
            raise ValueError
        x_axios, y_axios = self.ui.btn_center("dde-file-manager-图标模式下的第一个文件")
        self.double_click(x_axios, y_axios + 56 if flag == "trash" else y_axios)


class KillDfm:
    """KillDfm"""
    dbus_name = "com.deepin.filemanager.filedialog"
    object_path = "/com/deepin/filemanager/filedialogmanager"
    interface = "com.deepin.filemanager.filedialogmanager"
    bus = [dbus_name, object_path, interface]

    @classmethod
    def get_dialog(cls):
        """获取文管插件dialog"""
        all_dialogs = (
            DbusUtils(*cls.bus).session_object_methods().get_dbus_method("dialogs")()
        )
        return all_dialogs

    @classmethod
    def kill_dfm(cls):
        """杀掉文管插件"""
        all_dialogs = cls.get_dialog()
        for dialog in all_dialogs:
            DbusUtils(*cls.bus).session_object_methods().get_dbus_method("destroyDialog")(dialog)

# pylint: disable=R0904
@log
class DdeFileDialogWidget(Src):
    """DdeFileDialogWidget"""
    APP_NAME = "dde-file-dialog"
    DESC = "/usr/bin/dde-file-dialog"

    def __init__(self, file_box=True):
        """__init__"""
        self.file_box = file_box
        kwargs = {}
        kwargs["name"] = self.APP_NAME
        kwargs["description"] = self.DESC
        kwargs["check_start"] = True
        kwargs["config_path"] = Config.OTHER_INI_PATH
        Src.__init__(self, **kwargs)
        # setattr(self.ui, "window_info", self.window_info)

    @classmethod
    def find_manual_music(cls, *elements, rate=0.9):
        """查找图片坐标"""
        element = tuple(map(lambda x: f"{Config.PIC_RES_PATH}/{x}", elements))
        return cls.find_image(*element, rate=rate)

    def click_dir_in_desktop_plugs_by_ui(self, dir_name, flag, offset_y=None):
        """
         调用文管插件，点击指定文件夹
        :param dir_name:  文件名
        :param flag: import 导入窗口， export 导出窗口
        :return:
        """
        if flag in ("import", "export"):
            _x, _y = self.ui.btn_center(dir_name, offset_y=offset_y)
            if flag != "import":
                _y = _y - 38
            self.move_to_and_click(_x, _y)
        else:
            logger.error("flag Error")

    def click_open_btn_in_desktop_plugs_by_ui(self):
        """
         调用文管插件，点击右下角“打开“
        :return:
        """
        self.move_to_and_click(*self.ui.btn_center("打开"))

    def click_cancel_btn_in_desktop_plugs_save_by_ui(self):
        """
         调用文管插件，点击右下角“取消“
        :return:
        """
        self.move_to_and_click(*self.ui.btn_center("取消保存"))

    def click_cancel_btn_in_desktop_plugs_import_by_ui(self):
        """
         调用文管插件，点击右下角“取消“
        :return:
        """
        self.move_to_and_click(*self.ui.btn_center("取消打开"))

    def click_ok_btn_in_pop_up_window_by_ui(self):
        """
         点击小弹窗“关闭”按钮
        :return:
        """
        self.move_to_and_click(*self.ui.btn_center("关闭弹窗-确定"))

    def click_cancel_btn_in_pop_up_window_by_ui(self):
        """
         点击小弹窗的“取消”按钮
        :return:
        """
        self.move_to_and_click(*self.ui.btn_center("关闭弹窗-取消"))

    def click_formate_box_in_desktop_plugs_by_ui(self, flag="import"):
        """
         调用文管插件，点击右下角“格式框“
        :param flag: import 导入插件框，其他，导出插件框
        :return:
        """
        _x, _y = self.ui.btn_center("格式框")
        if flag != "import":
            _y = _y - 40
        self.move_to_and_click(_x, _y)

    def click_recent_dir_in_desktop_plugs_by_ui(self, flag="import"):
        """
         调用文管插件，点击右下角“最近使用“
        :param flag: import 导入插件框，export，导出插件框
        :return:
        """
        if flag in ("import", "export"):
            _x, _y = self.ui.btn_center("最近使用")
            if flag != "import":
                _x, _y = 0, 0
            self.move_to_and_click(_x, _y)
        else:
            logger.error("flag Error")

    def click_home_dir_in_desktop_plugs_by_ui(self, flag="import"):
        """
         调用文管插件，点击右下角“主目录“
        :param flag: import 导入插件框，其他，导出插件框
        :return:
        """
        self.click_dir_in_desktop_plugs_by_ui("主目录", flag)

    def click_desktop_dir_in_desktop_plugs_by_ui(self, flag="import"):
        """
         调用文管插件，点击右下角“桌面“
        :param flag: import 导入插件框，其他，导出插件框
        :return:
        """
        self.click_dir_in_desktop_plugs_by_ui("桌面", flag)

    def click_videos_dir_in_desktop_plugs_by_ui(self, flag="import"):
        """
         调用文管插件，点击右下角“视频“
        :param flag: import 导入插件框，其他，导出插件框
        :return:
        """
        self.click_dir_in_desktop_plugs_by_ui("视频", flag)

    def click_music_dir_in_desktop_plugs_by_ui(self, flag="import"):
        """
         调用文管插件，点击右下角“音乐“
        :param flag: import 导入插件框，其他，导出插件框
        :return:
        """
        self.click_dir_in_desktop_plugs_by_ui("音乐", flag)

    def click_pictures_dir_in_desktop_plugs_by_ui(self, flag="import"):
        """
         调用文管插件，点击右下角“图片“
        :param flag: import 导入插件框，其他，导出插件框
        :return:
        """
        self.click_dir_in_desktop_plugs_by_ui("图片", flag, offset_y=38)

    def click_documents_dir_in_desktop_plugs_by_ui(self, flag="import"):
        """
         调用文管插件，点击右下角“文档“
        :param flag: import 导入插件框，其他，导出插件框
        :return:
        """
        self.click_dir_in_desktop_plugs_by_ui("文档", flag)

    def click_downloads_dir_in_desktop_plugs_by_ui(self, flag="import"):
        """
         调用文管插件，点击右下角“下载“
        :param flag: import 导入插件框，其他，导出插件框
        :return:
        """
        self.click_dir_in_desktop_plugs_by_ui("下载", flag)

    def click_computer_dir_in_desktop_plugs_by_ui(self, flag="import"):
        """
         调用文管插件，点击右下角“计算机“
        :param flag: import 导入插件框，其他，导出插件框
        :return:
        """
        self.click_dir_in_desktop_plugs_by_ui("计算机", flag)

    def click_save_btn_in_desktop_plugs_by_ui(self):
        """
         调用文管插件，点击右下角“保存“（左右布局）
        :return:
        """
        self.move_to_and_click(*self.ui.btn_center("保存"))

    def click_blank_space_in_desktop_plugs_by_ui(self):
        """
         点击文管插件空白处
        :return:
        """
        self.move_to_and_click(*self.ui.btn_center("空白处"), _type="xdotool")

    def click_icon_view_btn_in_desktop_plugs_by_ui(self):
        """
         调用文管插件，点击右下角“图标视图“
        :return:
        """
        self.move_to_and_click(*self.ui.btn_center("图标视图"))

    def click_list_view_btn_in_desktop_plugs_by_ui(self):
        """
         调用文管插件，点击右下角“列表视图“
        :return:
        """
        self.move_to_and_click(*self.ui.btn_center("列表视图"))

    def click_first_file_in_desktop_plugs_by_ui(self):
        """
         调用文管插件，点击“列表视图下第一个文件“
        :return:
        """
        self.move_to_and_click(*self.ui.btn_center("列表视图下第一个文件"))

    def double_click_first_file_in_desktop_plugs_by_ui(self):
        """
         调用文管插件，双击“列表视图下第一个文件“
        :return:
        """
        self.move_to_and_double_click(*self.ui.btn_center("列表视图下第一个文件"))

    def right_click_first_file_in_desktop_plugs_by_ui(self):
        """
         调用文管插件，右键“列表视图下第一个文件“
        :return:
        """
        self.move_to_and_right_click(*self.ui.btn_center("列表视图下第一个文件"))

    def click_second_file_in_desktop_plugs_by_ui(self):
        """
         调用文管插件，点击右下角“列表视图下第二个文件“
        :return:
        """
        self.move_to_and_click(*self.ui.btn_center("列表视图下第二个文件"))

    def double_click_second_file_in_desktop_plugs_by_ui(self):
        """
         调用文管插件，双击右下角“列表视图下第二个文件“
        :return:
        """
        self.move_to_and_click(*self.ui.btn_center("列表视图下第二个文件"))

    def double_click_third_file_in_desktop_plugs_by_ui(self):
        """
         调用文管插件，双击“列表视图下第三个文件“
        :return:
        """
        self.move_to_and_double_click(*self.ui.btn_center("列表视图下第三个文件"))

    def click_third_file_in_desktop_plugs_by_ui(self):
        """
         调用文管插件，点击右下角“列表视图下第三个文件“
        :return:
        """
        self.move_to_and_click(*self.ui.btn_center("列表视图下第三个文件"))

    def double_click_file_in_desktop_plugs_right_view_by_attr(self, element):
        """
         双击桌面目录元素
        :param element: 文件名
        :return:
        """
        self.dog.find_element_by_attr(f"$//{element}").doubleClick()

    def click_file_in_desktop_plugs_by_attr(self, filename):
        """
         调用文管插件，点击指定文件
        :param filename: 文件名称
        :return:
        """
        self.dog.find_element_by_attr(f"$//{filename}").point()
        # self.dog.app_element('file_view').child(filename).point()
        self.click()

    def double_click_file_in_desktop_plugs_by_attr(self, filename):
        """
         调用文管插件，双击指定文件
        :param filename: 文件名称
        :return:
        """
        self.dog.find_element_by_attr(f"$//{filename}").point()
        self.double_click()

    def right_click_file_in_desktop_plugs_by_attr(self, filename):
        """
         调用文管插件，右键点击指定文件
        :param filename: 文件名称
        :return:
        """
        self.dog.find_element_by_attr(f"$//{filename}").point()
        # self.dog.app_element('file_view').child(filename).point()
        self.move_to_and_right_click()

    def right_click_deepin_music_on_desktop_by_image(self):
        """
         右键点击音乐图标
        :return:
        """
        self.right_click_element_in_desktop_by_image("deepin_music")

    def right_click_element_in_desktop_by_image(self, *pic):
        """
         右键桌面元素
        :param pic: 图片路径
        :return:
        """
        self.move_to_and_right_click(*self.find_manual_music(*pic))
