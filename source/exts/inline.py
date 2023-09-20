"""
Copyright (C) 2019-2023, NGINX, Inc.

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

from docutils.nodes import Node, system_message, Text
from docutils.parsers.rst import roles
from sphinx.application import Sphinx
from sphinx.roles import EmphasizedLiteral, specific_docroles
from typing import List


class NxtEmphasizedLiteral(EmphasizedLiteral):
    def parse(self, text: str) -> List[Node]:

        doc = self.inliner.document
        replacements = [
            (i.attributes["names"][0], i.children[0])
            for i in doc.substitution_defs.values()
        ]

        # some items due for replacement are stored as config values
        replacements.append(("version", Text(doc.settings.env.config.version)))

        for rep in replacements:
            text = text.replace("|" + rep[0] + "|", rep[1])

        return super().parse(text)


def setup(app: Sphinx) -> None:
    """Overrides literal role handlers."""

    # Select all literal role names.
    for rolename, nodeclass in specific_docroles.items():
        if isinstance(nodeclass, EmphasizedLiteral):
            # Override all literal roles with the extended handler.
            roles.register_local_role(rolename, NxtEmphasizedLiteral())
