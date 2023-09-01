#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@File  :music_dbus_object.py
@Author:huangmingqiang@uniontech.com
@Date  :2020/6/30 上午11:21
@Desc  :
"""

from src import DbusUtils


class MusicDbus:
    """音乐的接口属性"""

    DBUS_NAME = "org.mpris.MediaPlayer2.DeepinMusic"
    OBJECT_PATH = "/org/mpris/MediaPlayer2"
    INTERFACE = "org.mpris.MediaPlayer2.Player"

    @staticmethod
    def music_dbus_object():
        """music_dbus_object"""
        return DbusUtils(MusicDbus.DBUS_NAME, MusicDbus.OBJECT_PATH, MusicDbus.INTERFACE)

    @classmethod
    def can_control(cls):
        """
        :param property_name:
        :return:
        """
        return cls.music_dbus_object().get_session_properties_value("CanControl")

    @classmethod
    def can_go_next(cls):
        """

        :param property_name:
        :return:
        """
        return cls.music_dbus_object().get_session_properties_value("CanGoNext")

    @classmethod
    def can_go_previous(cls):
        """

        :param property_name:
        :return:
        """
        return cls.music_dbus_object().get_session_properties_value("CanGoPrevious")

    @classmethod
    def can_pause(cls):
        """

        :param property_name:
        :return:
        """
        return cls.music_dbus_object().get_session_properties_value("CanPause")

    @classmethod
    def can_play(cls):
        """

        :param property_name:
        :return:
        """
        return cls.music_dbus_object().get_session_properties_value("CanPlay")

    @classmethod
    def can_seek(cls):
        """

        :param property_name:
        :return:
        """
        return cls.music_dbus_object().get_session_properties_value("CanSeek")

    @classmethod
    def shuffle(cls, property_name="Shuffle"):
        """

        :param property_name:
        :return:
        """
        return cls.music_dbus_object().get_session_properties_value(property_name)

    @classmethod
    def meta_data(cls, property_name="Metadata"):
        """

        :param property_name:
        :return: dict
        """
        return cls.music_dbus_object().get_session_properties_value(property_name)

    @classmethod
    def maximum_rate(cls, property_name="MaximumRate"):
        """

        :param property_name:
        :return:
        """
        return cls.music_dbus_object().get_session_properties_value(property_name)

    @classmethod
    def minimum_rate(cls, property_name="MinimumRate"):
        """

        :param property_name:
        :return:
        """
        return cls.music_dbus_object().get_session_properties_value(property_name)

    @classmethod
    def rate(cls, property_name="Rate"):
        """

        :param property_name:
        :return:
        """
        return cls.music_dbus_object().get_session_properties_value(property_name)

    @classmethod
    def volume(cls, property_name="Volume"):
        """
        音量的大小
        :param property_name:
        :return:
        """
        return cls.music_dbus_object().get_session_properties_value(property_name)

    @classmethod
    def position(cls, property_name="Position"):
        """

        :param property_name:
        :return:
        """
        return cls.music_dbus_object().get_session_properties_value(property_name)

    @classmethod
    def loop_status(cls, property_name="LoopStatus"):
        """

        :param property_name:
        :return:
        """
        return cls.music_dbus_object().get_session_properties_value(property_name)

    @classmethod
    def play_back_status(cls, property_name="PlaybackStatus"):
        """
        播放状态的属性返回值
        :return: Playing 播放/ Paused 暂停
        """
        return cls.music_dbus_object().get_session_properties_value(property_name)
