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
from docutils.nodes import Text
from docutils.parsers.rst import roles


def new_literal_role(typ, rawtext, text, lineno, inliner, options=None,
                     content=None, old_role=None):
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


def setup(app):
    """Overrides literal role handlers."""

    # Inject the old_role keyword argument to ensure a seamless override.
    def spliced_role(*arg, **kwarg):
        return new_literal_role(*arg, old_role=mod.EmphasizedLiteral, **kwarg)

    # Select all literal role names.
    names = [key for key, value in mod.specific_docroles.items()
             if value is mod.EmphasizedLiteral]

    # Override all literal roles with the extended handler.
    for name in names:
        roles.register_local_role(name, spliced_role)
