"""
Copyright (C) 2019-2023, NGINX, Inc.

Sphinx extension to support replace directives in code-block snippets.

Usage:

conf.py:
    extensions += ['subs']

.rst file:
    .. |token| replace:: some text

    .. subs-code-block:: none
       |token| and more text

.html file:
    some text and more text
"""
from docutils.nodes import Node, Text
from sphinx.application import Sphinx
from sphinx.directives.code import CodeBlock
from typing import List


class SubsCodeBlock(CodeBlock):
    """Extends code-block to enable replace directive substitutions."""

    def run(self) -> List[Node]:

        new_content = []
        doc = self.state.document

        replacements = [
            (i.attributes["names"][0], i.children[0])
            for i in doc.substitution_defs.values()
        ]

        # Config values need to be added manually at this time.
        replacements.append(("version", Text(doc.settings.env.config.version)))

        for item in self.content:
            for rep in replacements:
                item = item.replace("|" + rep[0] + "|", rep[1])
            new_content.append(item)

        self.content = new_content

        return CodeBlock.run(self)


def setup(app: Sphinx) -> None:
    """Connects the extension to the app."""

    app.add_directive("subs-code-block", SubsCodeBlock)
