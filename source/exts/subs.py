# Copyright (C) 2019, NGINX, Inc.
# Sphinx extension to support 'replace' directives in 'code-block' snippets.
# Usage:
#
# conf.py:
#
# extensions += ['subs']
#
# .rst file:
#
# .. |token| replace:: some text
#
# .. subs-code-block:: none
#
#    |token| and more text
#
# .html file:
#
#  some text and more text

from sphinx.directives.code import CodeBlock

class SubsCodeBlock(CodeBlock):

    def run(self):

        new_content = []

        replacements = [(i.attributes['names'][0], i.children[0]) for \
            i in self.state.document.substitution_defs.values()]

        for item in self.content:
            for rep in replacements:
                item = item.replace('|' + rep[0] + '|', rep[1])

            new_content.append(item)

        self.content = new_content

        return CodeBlock.run(self)


def setup(app):

    app.add_directive('subs-code-block', SubsCodeBlock)
