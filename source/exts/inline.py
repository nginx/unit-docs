# Copyright (C) 2019, NGINX, Inc.
# Sphinx extension to support replacements in inline literals.
#
# Usage:
#
# conf.py:
#
# extensions += ['inline']
#
# .rst file:
#
# .. markup::
#
#    :samp:`Unit |version|` and more text
#
# .html file:
#
#  <literal classes="samp" role="samp">Unit 1.13.0</literal> and more text

from docutils.nodes import Text
from docutils.parsers.rst import roles
import sphinx.roles as mod


def new_literal_role(typ, rawtext, text, lineno, inliner,
                      options={}, content=[], old_role=None):

        node, _ = old_role(typ, rawtext, text, lineno, inliner,
                       options, content)
        doc = inliner.document

        replacements = [(i.attributes['names'][0], i.children[0]) for \
            i in doc.substitution_defs.values()]

        # some items due for replacement are stored as config values
        replacements.append(('version', Text(doc.settings.env.config.version)))

        for rep in replacements:
            node[0][0] = Text(node[0][0].replace('|' + rep[0] + '|', rep[1]))

        return node, _


def setup(app):

    names = [key for key, value in mod.specific_docroles.items() \
                if value is mod.emph_literal_role]

    def spliced_role(*args, **kwargs):
        return new_literal_role(*args, old_role=mod.emph_literal_role, **kwargs)

    for name in names:
        roles.register_local_role(name, spliced_role)
