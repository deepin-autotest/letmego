from letmego import letmego
# import inspect

@letmego
class Page:

    def click_some_element_self(self):
        """点击某个元素（实例方法）"""
        print("click self")

    @classmethod
    def click_some_element_cls(cls):
        """点击某个元素（类方法）"""
        print("click cls")

    @staticmethod
    def click_some_element_static():
        """点击某个元素（静态方法）"""
        print("click static")
