"""The Mimeo Context Manager module.

It exports only one class:
    * MimeoContextManager
        An OnlyOneAlive class managing Mimeo Contexts.
"""
from __future__ import annotations

import random
from types import TracebackType

from mimeo.config import MimeoConfig
from mimeo.config import constants as cc
from mimeo.context import MimeoContext
from mimeo.context.exc import (InvalidReferenceValueError,
                               NoCorrespondingReferenceError,
                               NonPopulatedReferenceError,
                               ReferenceNotFoundError, VarNotFoundError)
from mimeo.meta import Alive, OnlyOneAlive


class MimeoContextManager(Alive, metaclass=OnlyOneAlive):
    """An OnlyOneAlive class managing Mimeo Contexts.

    It allows you to initialize a context, get the currently processing
    context, switch it or reach any other. Besides that it gives you
    access to Mimeo Vars and Mimeo Refs.
    The only way to use it successfully it is by `with` statement:
        with MimeoContextManager(mimeo_config) as mimeo_mng:
            ...

    Methods
    -------
    get_context(self, context: str) -> MimeoContext
        Return a Mimeo Context with a specific name.
    get_current_context(self) -> MimeoContext
        Return the current Mimeo Context.
    set_current_context(self, context: MimeoContext)
        Set the current Mimeo Context.
    get_var(self, variable_name: str) -> str | int | bool | dict
        Return a specific Mimeo Var value.
    cache_ref(self, field_name: str, field_value: str | int | float | bool)
        Cache a field's value in references.
    get_ref(self, ref_name: str) -> str | int | float | bool
        Get a reference value.
    get_ref_names(self) -> list[str]
        Get reference names.
    """

    def __init__(
            self,
            mimeo_config: MimeoConfig | None = None,
    ):
        """Initialize MimeoContextManager class.

        Parameters
        ----------
        mimeo_config : MimeoConfig
            The Mimeo Configuration
        """
        super().__init__()
        self._mimeo_config: MimeoConfig = mimeo_config
        self._vars: dict = {}
        self._refs: dict = {}
        self._contexts: dict = {}
        self._current_context: MimeoContext | None = None

    def __enter__(
            self,
    ) -> MimeoContextManager:
        """Enter the MimeoContextManager instance.

        Extends Alive __enter__ function and initializes vars.

        Returns
        -------
        self : MimeoContextManager
            A MimeoContextManager instance
        """
        super().__enter__()
        self._vars = self._mimeo_config.vars
        self._refs = {ref: [] for ref in self._mimeo_config.refs}
        return self

    def __exit__(
            self,
            exc_type: type | None,
            exc_val: BaseException | None,
            exc_tb: TracebackType | None,
    ) -> None:
        """Exit the MimeoContextManager instance.

        Extends Alive __enter__ function and removes internal
        attributes.

        Parameters
        ----------
        exc_type : type | None
            An exception's type
        exc_val : BaseException | None
            An exception's value
        exc_tb  TracebackType | None
            An exception's traceback

        Returns
        -------
        None
            A None value
        """
        super().__exit__(exc_type, exc_val, exc_tb)
        self._vars = None
        self._contexts = None

    def get_context(
            self,
            context: str,
    ) -> MimeoContext:
        """Return a Mimeo Context with a specific name.

        If the context does not exist, it is initialized.

        Parameters
        ----------
        context : str
            A context's name

        Returns
        -------
        MimeoContext
            A specific Mimeo Context

        Raises
        ------
        InstanceNotAliveError
            If the MimeoContextManager instance is not alive
        """
        super().assert_alive()
        if context not in self._contexts:
            self._contexts[context] = MimeoContext(context)
        return self._contexts[context]

    def get_current_context(
            self,
    ) -> MimeoContext:
        """Return the current Mimeo Context.

        Returns
        -------
        MimeoContext
            The current Mimeo Context

        Raises
        ------
        InstanceNotAliveError
            If the MimeoContextManager instance is not alive
        """
        super().assert_alive()
        return self._current_context

    def set_current_context(
            self,
            context: MimeoContext,
    ):
        """Set the current Mimeo Context.

        Parameters
        ----------
        context : MimeoContext
            A Mimeo Context to be set as the current one

        Raises
        ------
        InstanceNotAliveError
            If the MimeoContextManager instance is not alive
        """
        super().assert_alive()
        self._current_context = context

    def get_var(
            self,
            variable_name: str,
    ) -> str | int | bool | dict:
        """Return a specific Mimeo Var value.

        Parameters
        ----------
        variable_name : str
            The Mimeo Var name

        Returns
        -------
        value : str | int | bool | dict
            The Mimeo Var value

        Raises
        ------
        InstanceNotAliveError
            If the MimeoContextManager instance is not alive
        VarNotFoundError
            If the Mimeo Var with the `variable_name` provided does not
            exist
        """
        super().assert_alive()
        value = self._vars.get(variable_name)
        if value is None:
            raise VarNotFoundError(variable_name)
        return value

    def cache_ref(
            self,
            field_name: str,
            field_value: str | int | float | bool,
    ):
        """Cache a field's value in references.

        It saves the field's value in all references having context configured
        to the current and field's to the one provided. When there's such a reference
        the field's value is not cached.

        Parameters
        ----------
        field_name : str
            A field name
        field_value : str | int | float | bool
            A field value

        Raises
        ------
        InvalidReferenceValueError
            If the field's value is not atomic one
        """
        if isinstance(field_value, (dict, list)):
            raise InvalidReferenceValueError(field_value)
        ref_names = [ref_name
                     for ref_name, ref_meta in self._mimeo_config.refs.items()
                     if ref_meta[cc.REFS_DETAIL_CONTEXT] == self._current_context.name
                     and ref_meta[cc.REFS_DETAIL_FIELD] == field_name]
        for ref_name in ref_names:
            self._refs[ref_name].append(field_value)

    def get_ref(
            self,
            ref_name: str,
    ) -> str | int | float | bool:
        """Get a reference value.

        It provides a reference value depending on its type. For 'any' returns a value
        on any index. For 'parallel' it uses a value produced in a corresponding
        iteration for a source context.

        Parameters
        ----------
        ref_name : str
            A reference name

        Returns
        -------
        str | int | float | bool
            A reference value

        Raises
        ------
        ReferenceNotFoundError
            If there's such a reference configured
        NonPopulatedReferenceError
            If the reference has no values
        NoCorrespondingReferenceError
            If there was no value cached in a corresponding iteration of the source
            context
        """
        ref_meta = self._mimeo_config.refs.get(ref_name)
        if not ref_meta:
            raise ReferenceNotFoundError(ref_name)

        values = self._refs.get(ref_name)
        if len(values) == 0:
            raise NonPopulatedReferenceError(ref_name)

        if ref_meta[cc.REFS_DETAIL_TYPE] == cc.REFS_TYPE_PARALLEL:
            curr_iter = self._current_context.curr_iteration().id
            index = curr_iter - 1
            if index >= len(values):
                raise NoCorrespondingReferenceError(ref_name, curr_iter)
        else:
            index = random.randrange(0, len(values))
        return values[index]

    def get_ref_names(
            self,
    ) -> list[str]:
        """Get reference names.

        Returns
        -------
        list
            List of reference names
        """
        return list(self._mimeo_config.refs.keys())

