"""The Mimeo Context package.

The context package contains classes providing data used by
Mimeo-Template-dependent utilities.

This package exports the following classes:
- MimeoIteration:
    A class representing a single iteration in a Mimeo Template.
- MimeoContext:
    A class managing Mimeo-Template-dependent utilities.
- MimeoContextManager:
    An OnlyOneAlive class managing Mimeo Contexts.

To use this package, simply import the desired class:
    from mimeo.context import MimeoContextManager
"""
from .mimeo_iteration import MimeoIteration
from .mimeo_context import MimeoContext
from .mimeo_context_manager import MimeoContextManager
