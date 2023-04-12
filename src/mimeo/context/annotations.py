import functools

from mimeo.config.mimeo_config import MimeoTemplate
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


def mimeo_context_switch(func):
    @functools.wraps(func)
    def switch_context(*args, **kwargs):
        context_mng = MimeoContextManager()
        prev_context = context_mng.get_current_context()

        if "template" in kwargs:
            template = kwargs["template"]
        else:
            template = next(arg for arg in args if isinstance(arg, MimeoTemplate))
        context_name = template.model.context_name
        next_context = context_mng.get_context(context_name)
        context_mng.set_current_context(next_context)
        result = func(*args, **kwargs)

        context_mng.set_current_context(prev_context)
        return result

    return switch_context


def mimeo_next_iteration(func):
    @functools.wraps(func)
    def next_iteration(*args, **kwargs):
        MimeoContextManager().get_current_context().next_iteration()
        result = func(*args, **kwargs)
        return result

    return next_iteration


def mimeo_clear_iterations(func):
    @functools.wraps(func)
    def clear_iterations(*args, **kwargs):
        MimeoContextManager().get_current_context().clear_iterations()
        result = func(*args, **kwargs)
        return result

    return clear_iterations
