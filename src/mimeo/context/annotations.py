import functools

from mimeo.context import MimeoContext, MimeoContextManager


def mimeo_context(func):
    @functools.wraps(func)
    def inject_context(*args, **kwargs):
        if any(isinstance(arg, MimeoContext) for arg in args) or "context" in kwargs:
            result = func(*args, **kwargs)
        else:
            result = func(*args, **kwargs, context=MimeoContextManager().get_current_context())
        return result

    return inject_context
