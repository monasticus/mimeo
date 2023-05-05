import sys
from typing import List


def get_class_impl_error_msg(cls: str, methods_list: List[str]) -> str:
    py_major = sys.version_info.major
    py_minor = sys.version_info.minor
    methods = ', '.join(methods_list)
    if py_major >= 3 and py_minor >= 9:
        print("Python >= 3.9")
        plural = len(methods_list) > 1
        method = "methods" if plural else "method"
        return f"Can't instantiate abstract class {cls} with abstract {method} {methods}"
    else:
        print("Python < 3.9")
        return f"Can't instantiate abstract class {cls} with abstract methods {methods}"