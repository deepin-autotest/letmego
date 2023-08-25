import pytest
from test.page import Page


class Test1:

    def test_001(self):
        """test 001"""

        Page().click_some_element_self()
        Page().click_some_element_cls()
        Page().click_some_element_static()
        # 和 10 行相同的步骤
        Page().click_some_element_self()
