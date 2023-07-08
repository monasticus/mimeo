"""The Mimeo JSON Generator module.

It exports only one class:
    * JSONGenerator
        A Generator implementation producing data in the JSON format.
"""
from __future__ import annotations

import json
import logging
from typing import Iterator

from mimeo.config import constants as cc
from mimeo.config.mimeo_config import MimeoConfig, MimeoTemplate
from mimeo.context import MimeoContext
from mimeo.context.decorators import mimeo_context
from mimeo.generators import Generator
from mimeo.utils import MimeoRenderer

logger = logging.getLogger(__name__)


class JSONGenerator(Generator):
    """A Generator implementation producing data in the JSON format.

    This Generator is instantiated for the 'json' output format
    and produces data using Mimeo Configuration.

    Methods
    -------
    generate(
        templates: list | Iterator[MimeoTemplate],
        parent: dict = None
    ) -> Iterator[dict]
        Generate JSON data based on the Mimeo Configuration.
    stringify(
        data: json
    ) -> str
        Stringify data generated by the generate() method.
    """

    def __init__(
            self,
            mimeo_config: MimeoConfig,
    ):
        """Initialize JSONGenerator class.

        Parameters
        ----------
        mimeo_config : MimeoConfig
            A Mimeo Configuration
        """
        self._indent: int = mimeo_config.output.indent

    @classmethod
    def generate(
            cls,
            templates: list | Iterator[MimeoTemplate],
            parent: dict | list | None = None,
    ) -> Iterator[dict]:
        """Generate JSON data based on the Mimeo Configuration.

        This function is used recursively when a Mimeo Configuration
        contains nested templates.
        It iterates through all templates configured and yields data
        units.

        Parameters
        ----------
        templates : list | Iterator[MimeoTemplate]
            A collection of Mimeo Templates to process
        parent : dict | list | None, default None
            A parent node for the currently processed template.
            It is passed only when a Mimeo Config contain nested
            templates.

        Returns
        -------
        Iterator[ElemTree.Element]
            Iterator for generated nodes
        """
        for template in templates:
            for data_unit in cls._process_single_template(template, parent):
                yield data_unit

    def stringify(
            self,
            data_unit: dict,
    ) -> str:
        """Stringify JSON data generated by the generate() method.

        Parameters
        ----------
        data_unit: dict
            A single data unit generated by the generate() method

        Returns
        -------
        str
            Stringified data unit
        """
        if self._indent is not None and self._indent != 0:
            return json.dumps(data_unit, indent=self._indent)

        return json.dumps(data_unit)

    @classmethod
    @mimeo_context
    def _process_node(
            cls,
            parent: dict | list | None,
            node_meta: dict,
            context: MimeoContext | None = None,
    ) -> dict | list:
        """Process a single template's node.

        Extends Generator's implementation by setting a parent node when it is None.
        It is required for JSON format to initialize an object.

        Parameters
        ----------
        parent : dict | list | None
            A parent node
        node_meta : dict
            Node's metadata
        context : MimeoContext, default None
            The current Mimeo Context (injected by MimeoContextManager)

        Returns
        -------
        dict | list
            A single data unit generated within a single template iteration.

        Raises
        ------
        InvalidSpecialFieldValueError
            If a special field value is dict or list
        SpecialFieldNotFoundError
            If a special field does not exist.
        """
        parent = parent if parent is not None else {}
        return super()._process_node(parent, node_meta, context)

    @classmethod
    def _pre_process_node(
            cls,
            node_meta: dict,
    ) -> dict:
        """Pre-process node's metadata.

        This function adjusts existing node's metadata and completes it with custom
        properties:
        * the name property is changed only for special fields
          - field name is extracted
        * the mimeo_util property is being initialized
          - True if element's value is a parametrized mimeo_util. Otherwise, False.
        * the special property is being initialized
          - True, when a field is special. Otherwise, False.

        Parameters
        ----------
        node_meta : dict
            Initial node's metadata

        Returns
        -------
        dict
            Complete node's metadata
        """
        name = node_meta["name"]
        value = node_meta["value"]
        is_mimeo_util = MimeoRenderer.is_parametrized_mimeo_util(value)
        is_special_field = name is not None and MimeoRenderer.is_special_field(name)
        if is_special_field:
            name = MimeoRenderer.get_special_field_name(name)

        return cls._node_meta(
            name=name,
            value=value,
            is_mimeo_util=is_mimeo_util,
            is_special_field=is_special_field)

    @classmethod
    def _process_complex_value(
            cls,
            parent: dict | list,
            node_meta: dict,
    ) -> dict | list:
        """Process a node with a complex value.

        The node is processed accordingly to its value type.
        When the type is dict, and it includes the _templates_ property, node
        is processed in a special way.

        Parameters
        ----------
        parent : dict | list
            A parent node
        node_meta : dict
            Node's metadata

        Returns
        -------
        dict | list
            A processed node

        Raises
        ------
        InvalidSpecialFieldValueError
            If a special field value is dict or list
        SpecialFieldNotFoundError
            If a special field does not exist.
        """
        if (isinstance(node_meta["value"], dict) and
                cc.TEMPLATES_KEY not in node_meta["value"]):
            func = cls._process_dict_value
        elif isinstance(node_meta["value"], list):
            func = cls._process_list_value
        else:
            func = cls._process_templates_value
        return func(parent, node_meta)

    @classmethod
    def _process_dict_value(
            cls,
            parent: dict | list,
            node_meta: dict,
    ) -> dict | list:
        """Process a node with a dictionary value.

        It iterates through the dictionary items and processes each of them.

        Parameters
        ----------
        parent : dict | list
            A parent node
        node_meta : dict
            Node's metadata

        Returns
        -------
        dict | list
            A processed node

        Raises
        ------
        InvalidSpecialFieldValueError
            If a special field value is dict or list
        SpecialFieldNotFoundError
            If a special field does not exist.

        Examples
        --------
        parent = {}
        node_meta = cls._node_meta(
            name="SomeField",
            value={"SomeChild1": 1, "SomeChild2": 2},
        )
        cls._process_dict_value(parent, node_meta)
        ->
        {
          "SomeField": {
            "SomeChild1": 1,
            "SomeChild2": 2,
          },
        }

        parent = []
        node_meta = cls._node_meta(
            name=None,
            value={"SomeChild1": 1, "SomeChild2": 2},
        )
        cls._process_dict_value(parent, node_meta)
        ->
        [
          {
            "SomeChild1": 1,
            "SomeChild2": 2,
          },
        ]
        """
        element = cls._create_node(parent, node_meta)
        for child_tag, child_value in node_meta["value"].items():
            cls._process_node(element, cls._node_meta(child_tag, child_value))
        return parent

    @classmethod
    def _process_list_value(
            cls,
            parent: dict | list,
            node_meta: dict,
    ) -> dict | list:
        """Process a node with a list value.

        It iterates through the list items and processes each of them: generates
        a child element for each value as direct children of the parent.

        Parameters
        ----------
        parent : dict | list
            A parent node
        node_meta : dict
            Node's metadata

        Returns
        -------
        dict | list
            A processed node

        Raises
        ------
        InvalidSpecialFieldValueError
            If the special field value is dict or list
        SpecialFieldNotFoundError
            If the special field does not exist.

        Examples
        --------
        parent = {}
        node_meta = cls._node_meta(
            name="SomeField",
            value=[
                'value-1',
                {'SomeChild1': True, 'SomeChild2': False},
                {'_mimeo_util': {'_name': 'auto_increment', 'pattern': '{}'}}
            ],
        )
        cls._process_list_value_with_atomic_children(parent, node_meta)
        ->
        {
          "SomeField": [
            "value-1",
            {
                "SomeChild1": True,
                "SomeChild2": False,
            },
            1,
          ],
        }

        parent = []
        node_meta = cls._node_meta(
            name=None,
            value=[
                'value-1',
                {'SomeChild1': True, 'SomeChild2': False},
                {'_mimeo_util': {'_name': 'auto_increment', 'pattern': '{}'}}
            ],
        )
        cls._process_list_value_with_atomic_children(parent, node_meta)
        ->
        [
          [
            "value-1",
            {
                "SomeChild1": True,
                "SomeChild2": False,
            },
            1,
          ],
        ]
        """
        element = cls._create_node(parent, node_meta)
        for child in node_meta["value"]:
            node_meta = cls._node_meta(None, child)
            cls._process_node(element, node_meta)
        return parent

    @classmethod
    def _process_templates_value(
            cls,
            parent: dict | list,
            node_meta: dict,
    ) -> dict | list:
        """Process a node with a dictionary value storing templates.

        It iterates through the templates and generates data based on them.
        If parent is a dict, the property name will take a value of an array.
        All properties at the same level as _templates_ will be ignored.

        Parameters
        ----------
        parent : dict | None
            A parent node
        node_meta : dict
            Node's metadata

        Returns
        -------
        dict | list
            A processed node

        Raises
        ------
        InvalidSpecialFieldValueError
            If a special field value is dict or list
        SpecialFieldNotFoundError
            If a special field does not exist.

        Examples
        --------
        parent = []
        node_meta = cls._node_meta(
            name=None,
            value={"_templates_": [
                {
                  "count": 10,
                  "model": {
                    "SomeChild": {
                      "Node1": 1,
                      "Node2": "value-2",
                      "Node3": true
                    }
                  }
                }
            ]},
        )
        cls._process_templates_value(parent, node_meta)
        ->
        [
          {
            "SomeChild": {
              "Node1": 1,
              "Node2": "value-2",
              "Node3": true,
            },
          },
          {
            "SomeChild": {
              "Node1": 1,
              "Node2": "value-2",
              "Node3": true,
            },
          },
          ... x10
        ]

        parent = {}
        node_meta = cls._node_meta(
            name="SomeField",
            value={"_templates_": [
                {
                  "count": 10,
                  "model": {
                    "SomeChild": {
                      "Node1": 1,
                      "Node2": "value-2",
                      "Node3": true
                    }
                  }
                }
            ]},
        )
        cls._process_templates_value(parent, node_meta)
        ->
        {
          "SomeField": [
            {
              "SomeChild": {
                "Node1": 1,
                "Node2": "value-2",
                "Node3": true,
              },
            },
            {
              "SomeChild": {
                "Node1": 1,
                "Node2": "value-2",
                "Node3": true,
              },
            },
            ... x10
          ],
        }
        """
        templates = (MimeoTemplate(template)
                     for template in node_meta["value"][cc.TEMPLATES_KEY])
        target = parent
        if isinstance(parent, dict):
            parent[node_meta["name"]] = []
            target = parent[node_meta["name"]]

        target.extend(cls.generate(templates))
        return parent

    @classmethod
    def _process_atomic_value(
            cls,
            parent: dict | list,
            node_meta: dict,
            context: MimeoContext,
    ) -> dict | list:
        """Process a node with an atomic value.

        A parametrized Mimeo Util is considered as an atomic value as representing one.
        It renders a value for the node.

        Parameters
        ----------
        parent : dict | list
            A parent node
        node_meta : dict
            Node's metadata
        context : MimeoContext, default None
            The current Mimeo Context (injected by MimeoContextManager)

        Returns
        -------
        dict | list
            A processed node

        Raises
        ------
        InvalidSpecialFieldValueError
            If a special field value is dict or list
        SpecialFieldNotFoundError
            If a special field does not exist.

        Examples
        --------
        context = MimeoContextManager().get_current_context()
        parent = {}
        node_meta = cls._node_meta(
            name="SomeField",
            value="value-1",
        )
        cls._process_atomic_value(parent, node_meta, context)
        ->
        {
          "SomeField": "value-1"
        }

        context = MimeoContextManager().get_current_context()
        parent = []
        node_meta = cls._node_meta(
            name=None,
            value="value-1",
        )
        cls._process_atomic_value(parent, node_meta, context)
        ->
        [
          "value-1"
        ]
        """
        value = MimeoRenderer.render(node_meta["value"])
        if node_meta["special"]:
            context.curr_iteration().add_special_field(node_meta["name"], value)
        if isinstance(parent, dict):
            parent[node_meta["name"]] = value
        elif isinstance(parent, list):
            parent.append(value)
        logger.fine("Rendered value [%s]", value)
        return parent

    @staticmethod
    def _create_node(
            parent: dict | list,
            node_meta: dict,
    ) -> dict | list:
        """Create an JSON element based on the `parent` and entry value types.

        Parameters
        ----------
        parent : dict | list
            A parent node
        node_meta : dict
            Node's metadata

        Returns
        -------
        dict | list
            If the new node's value is dict, returns dict. Otherwise, a list.

        Examples
        --------
        parent = {}
        node_meta = cls._node_meta(
            name="SomeEntity",
            value={"SomeField": "value-1"},
        )
        node = cls._create_node(parent, node_meta)
        ->
        parent: {"SomeEntity": {}}
        node: {}

        parent = []
        node_meta = cls._node_meta(
            name=None,
            value={"SomeField": "value-1"},
        )
        node = cls._create_node(parent, node_meta)
        ->
        parent: [{}]
        node: {}

        parent = []
        node_meta = cls._node_meta(
            name=None,
            value=["value-1"],
        )
        node = cls._create_node(parent, node_meta)
        ->
        parent: [[]]
        node: []

        parent = {}
        node_meta = cls._node_meta(
            name="SomeEntity",
            value=["value-1"],
        )
        node = cls._create_node(parent, node_meta)
        ->
        parent: {"SomeEntity": []}
        node: []
        """
        new_node = {} if isinstance(node_meta["value"], dict) else []
        if isinstance(parent, list):
            parent.append(new_node)
            return parent[-1]

        parent[node_meta["name"]] = new_node
        return parent[node_meta["name"]]
