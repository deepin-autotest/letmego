#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@Author:huangmingqiang@uniontech.com
@Date  :2020/10/22 下午5:35
@Desc  :
"""

from src import ElementNotFound
from src import AssertCommon
from apps.autotest_deepin_music.widget.deepin_music_dbus import MusicDbus
from apps.autotest_deepin_music.widget.base_widget import BaseWidget
from apps.autotest_deepin_music.config import Config


class DeepinMusicAssert(AssertCommon):
    """音乐的断言类"""

    @staticmethod
    def get_music_equalizer_style():
        """均衡器的音乐模式"""
        try:
            style_temp = (
                BaseWidget()
                .dog.find_element_by_attr("$//Dequalizer//ContentScrollArea//Dequalizer")
                .children[2]
            )
            style = str(style_temp).rsplit("|", maxsplit=1)[-1].lstrip().replace("]", "")
        except IndexError:
            return False
        return style

    # @staticmethod
    # def get_music_playing_name_by_ui(music_name_len=39):
    #     """get_music_playing_name_by_ui"""
    #     x, y = BaseWidget().ui.window_left_top_position()
    #     w, h = BaseWidget().ui.window_sizes()
    #     x1, y1 = x + 202, y + h - 60
    #     x2, y2 = x + 202 + music_name_len, y + h - 60 + 15
    #     pyscreenshot.grab(bbox=(x1, y1, x2, y2)).save(Config.SCREEN_CACHE)
    #     ocr_txt = ImageUtils.get_image_string(Config.SCREEN_CACHE).strip()
    #     logger.info(ocr_txt)
    #     return ocr_txt

    # @staticmethod
    # def get_music_playing_name(music_name_len=112):
    #     """获取播放音乐的名称"""
    #     try:
    #         _x, _y, _w, _h = (
    #             BaseWidget().dog.app_element("FooterWidget").child("btCover").extents
    #         )
    #         pyscreenshot.grab(
    #             bbox=(_x + _w, _y, _x + _w + music_name_len, _y + 28)
    #         ).save(Config.SCREEN_CACHE)
    #         sleep(2)
    #         return ImageUtils.get_image_string(Config.SCREEN_CACHE).strip()
    #     except:
    #         return None

    # @staticmethod
    # def get_max_vol_in_equalizer_preamplifier():
    #     """获取均衡器-前置放大器的最大音量"""
    #     x, y = BaseWidget().ui.window_left_top_position()
    #     pyscreenshot.grab(bbox=(x + 230, y + 190, x + 270, y + 224)).save(
    #         Config.SCREEN_CACHE
    #     )
    #     return ImageUtils.get_image_string(Config.SCREEN_CACHE).strip()

    @staticmethod
    def play_list_music_exists():
        """判断播放列表中是否存在音乐"""
        try:
            BaseWidget().dog.app_element("forwardWidget").children[0][2][0]
        except ElementNotFound:
            return False
        return True

    @staticmethod
    def get_new_music_list_name():
        """获取新建歌单的名称"""
        try:
            new_music_list_name_temp = BaseWidget().dog.app_element("customizeListview").children[0]
            new_music_list_name = (
                str(new_music_list_name_temp).rsplit("|", maxsplit=1)[-1].lstrip().rstrip("]")
            )
        except ElementNotFound:
            return False
        return new_music_list_name

    @staticmethod
    def assert_music_list_name_exists(txt="你好"):
        """音乐歌单中存在名称"""
        try:
            BaseWidget().dog.app_element("customizeListview").isChild(txt)
        except:
            raise ElementNotFound("音乐歌单中不存在名称") from Exception

    @staticmethod
    def assert_play_list_exists_file():
        """'播放列表'中是否存在音乐"""
        try:
            print(BaseWidget().dog.app_element("PlayQueue").children[3][0])
        except:
            raise AssertionError("播放列表中不存在音乐") from Exception

    @staticmethod
    def assert_music_playing_status():
        """断言音乐的播放状态为playing"""
        if not MusicDbus.play_back_status() == "Playing":
            raise AssertionError("音乐未播放")

    @staticmethod
    def assert_music_stopped_status():
        """断言音乐的播放状态为stopped"""
        if not MusicDbus.play_back_status() == "Stopped":
            raise AssertionError("音乐未停止播放")

    @staticmethod
    def assert_music_paused_status():
        """断言音乐的播放状态为stopped"""
        if not MusicDbus.play_back_status() == "Paused":
            raise AssertionError("音乐未暂停播放")

    @classmethod
    def assert_music_image_exist(cls, image, rate=0.9):
        """断言音乐中存在图片"""
        cls.assert_image_exist(f"{Config.ASSERT_RES_PATH}/{image}", rate)

    @classmethod
    def assert_music_image_not_exist(cls, image, rate=0.9):
        """断言音乐中不存在图片"""
        cls.assert_image_not_exist(f"{Config.ASSERT_RES_PATH}/{image}", rate)

    @staticmethod
    def assert_music_default_size(size):
        """断言默认窗口大小"""
        if size != (1070, 680):
            raise AssertionError(f"当前尺寸{size} 不等于 默认尺寸(1070, 680)")
