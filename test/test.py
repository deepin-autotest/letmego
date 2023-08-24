import pytest
from test.page import Page


def test_001():
    """test 001"""
    Page().click_some_element_self()
    Page().click_some_element_cls()
    Page().click_some_element_static()