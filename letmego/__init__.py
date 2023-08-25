import inspect
import os
import re
import threading
import weakref
from functools import wraps
from letmego.conf import setting


class Singleton(type):
    """单例模式"""

    _instance_lock = threading.Lock()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        Singleton.__instance = None
        # 初始化存放实例地址
        self._cache = weakref.WeakValueDictionary()

    def __call__(self, *args, **kwargs):
        # 提取类初始化时的参数
        kargs = "".join([f"{key}" for key in args]) if args else ""
        kkwargs = "".join([f"{key}" for key in kwargs]) if kwargs else ""
        # 判断相同参数的实例师否被创建
        if kargs + kkwargs not in self._cache:  # 存在则从内存地址中取实例
            with Singleton._instance_lock:
                Singleton.__instance = super().__call__(*args, **kwargs)
                self._cache[kargs + kkwargs] = Singleton.__instance
        # 不存在则新建实例
        else:
            Singleton.__instance = self._cache[kargs + kkwargs]
        return Singleton.__instance


def is_static_method(klass_or_instance, attr: str):
    """Test if a value of a class is static method.
    example::
        class MyClass(object):
            @staticmethod
            def add_two(a, b):
                return a + b
    :param klass_or_instance: the class
    :param attr: attribute name
    """
    if attr.startswith("_"):
        return False
    value = getattr(klass_or_instance, attr)
    # is a function or method
    if inspect.isroutine(value):
        if isinstance(value, property):
            return False
        args = []
        for param in inspect.signature(value).parameters.values():
            kind = param.kind
            name = param.name
            if kind is inspect._ParameterKind.POSITIONAL_ONLY:
                args.append(name)
            elif kind is inspect._ParameterKind.POSITIONAL_OR_KEYWORD:
                args.append(name)
        # Can't be a regular method, must be a static method
        if len(args) == 0:
            return True
        # must be a regular method
        if args[0] == "self":
            return False
        return inspect.isfunction(value)
    return False


def _trace(func):
    @wraps(func)
    def wrapped(*a, **kw):
        try:
            # 对象实例化后调用类方法报错处理
            if (
                    isinstance(a[0], inspect._findclass(func))
                    and func.__name__ != "__init__"
            ):
                if func:
                    if any(
                            [
                                inspect.ismethod(func),
                                is_static_method(
                                    inspect._findclass(func),
                                    func.__name__,
                                ),
                            ]
                    ):
                        a = list(a)[1:]
        except IndexError:
            pass
        frame = inspect.currentframe()
        case_filename = str(frame.f_back.f_code.co_filename)
        page_class_name = inspect._findclass(func).__name__
        page_func_name = func.__name__
        page_func_line = str(frame.f_back.f_lineno)
        case_func_name = str(frame.f_back.f_code.co_name)
        case_class_name = re.findall(r"<.*?\.test.*?\.(.*?) object at .*?>", str(frame.f_back.f_locals.get("self")))
        if case_class_name:
            case_class_name = case_class_name[0]
        running_man = f"{case_filename}-{case_class_name}-{case_func_name}-{page_class_name}-{page_func_name}-{page_func_line}"
        running_man_file = os.path.expanduser(setting.RUNNING_MAN_FILE)
        marks = []
        if os.path.exists(running_man_file):
            with open(running_man_file, "r", encoding="utf-8") as f:
                marks = f.readlines()
        if f"{running_man}\n" not in marks:
            with open(running_man_file, "a+", encoding="utf-8") as f:
                f.write(f"{running_man}\n")
        else:
            return None
        return func(*a, **kw)

    return wrapped


def letmego(cls):
    """
    类装饰器
    :param cls:
    :return:
    """
    for name, obj in inspect.getmembers(
            cls, lambda x: inspect.isfunction(x) or inspect.ismethod(x)
    ):
        if hasattr(getattr(cls, name), "__letmego"):
            if not getattr(cls, name).__letmego:
                setattr(cls, name, _trace(obj))
                setattr(getattr(cls, name), "__letmego", True)
        else:
            setattr(cls, name, _trace(obj))
            setattr(getattr(cls, name), "__letmego", True)
    return cls
