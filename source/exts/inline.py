"""
Copyright (C) 2019-2021, NGINX, Inc.

Sphinx extension to support replacements in inline literals.

Usage:

conf.py:
extensions += ['inline']

.rst file:
.. markup::
   :samp:`Unit |version|` and more text

.html file:
 <literal classes="samp" role="samp">Unit 1.22.0</literal> and more text
"""

import sphinx.roles as mod
from docutils.nodes import Node, system_message, Text
from docutils.parsers.rst import roles
from docutils.parsers.rst.states import Inliner
from sphinx.application import Sphinx
from typing import Any, Dict, Callable, List, Tuple


def new_literal_role(name: str, rawtext: str, text: str, lineno: int,
        inliner: Inliner, options: Dict = {}, content: List[str] = [],
        old_role: Callable[..., Tuple[List[Node], List[system_message]]]
        = None) -> Tuple[List[Node], List[system_message]]:
    """Extends the literal role handler to allow replace substitutions."""

    node, _ = old_role(typ, rawtext, text, lineno, inliner, options,
                       content)
    doc = inliner.document

    replacements = [(i.attributes['names'][0], i.children[0])
                    for i in doc.substitution_defs.values()]

    # some items due for replacement are stored as config values
    replacements.append(('version', Text(doc.settings.env.config.version)))

    for rep in replacements:
        node[0][0] = Text(node[0][0].replace('|' + rep[0] + '|', rep[1]))

    return node, _


def setup(app: Sphinx) -> None:
    """Overrides literal role handlers."""

    # Inject the old_role keyword argument to ensure a seamless override.
    def spliced_role(*args: Any, **kwargs: Any) -> \
            Tuple[List[Node], List[system_message]]:
        return new_literal_role(*arg, old_role=mod.EmphasizedLiteral, **kwarg)

    # Select all literal role names.
    names = [key for key, value in mod.specific_docroles.items()
             if value is mod.EmphasizedLiteral]

    # Override all literal roles with the extended handler.
    for name in names:
        roles.register_local_role(name, spliced_role)
