import pytest
from test.page import Page
from letmego import letmego

@letmego
class Test:

    def test_001(self):
        """test 001"""


        Page().click_some_element_self()
        Page().click_some_element_cls()
        Page().click_some_element_static()
        Page().click_some_element_self()
