# Copyright (C) 2019, NGINX, Inc.
# Sphinx extension to support tooltips for terms in text and code-blocks.
#
# Usage:
#
# conf.py:
#
# extensions += ['terms']
#
# .rst file:
#
# .. markup:: (including code-blocks)
#
#    :nxt_term:`term <definition>` and more text
#
# .html file:
#
#  <span style="nxt_term" title="definition">term</span> and more text

from docutils import nodes
from docutils.parsers.rst import roles
from sphinx.writers.html import HTMLTranslator
import re

nxt_term_regex = r'`({0}*[^\s])\s*<({0}+)>`'.format(r'[\w\s\.\,\?\!\-\/\:#_]')
# matches `simple text w/punctuation <simple text w/punctuation>`

def nxt_term_role_fn(name, rawtext, text, lineno, inliner,
        options={}, content=[]):
# :nxt_term: directive handler for inline text
    node = nxt_term()
    groups = re.search(nxt_term_regex, \
        rawtext.replace('\n', ' ').replace('\r', ''))

    try:
        node.term, node.tip = groups.group(1), groups.group(2)
    except:
        msg = inliner.reporter.error(
            'Inline term "%s" is invalid.' % text, line=lineno)
        prb = inliner.problematic(rawtext, rawtext, msg)
        return [prb], [msg]

    return [node], []

class nxt_term(nodes.container): pass
# required for the docutils dispatcher

class nxt_highlighter(object):
    def __init__(self, highlighter):
        self.highlighter = highlighter

    def highlight_block(self, *args, **kwargs):
        groups = re.findall(nxt_term_regex, args[0])

        rawsource = args[0]

        for c, g in enumerate(groups):
            rawsource = re.sub(':nxt_term:' + nxt_term_regex, \
                'nxt_term_{0}'.format(c), rawsource, count=1)

        highlighted = self.highlighter.highlight_block(rawsource, *args[1:], \
            **kwargs)

        for c, g in enumerate(groups):
            highlighted = re.sub('nxt_term_{0}'.format(c),      \
                '<span class="nxt_term" title="{0}">{1}</span>'.\
                format(g[1], g[0]), highlighted, count=1)

        return highlighted


class nxt_translator(HTMLTranslator):
    def __init__(self, builder, *args, **kwargs):
        HTMLTranslator.__init__(self, builder, *args, **kwargs)
        self.highlighter = nxt_highlighter(builder.highlighter)

    def visit_nxt_term(self, node):
        self.body.append('<span class="nxt_term" title="{1}">{0}</span>'.\
                         format(node.term, node.tip))
        return nodes.SkipNode

    def depart_nxt_term(self, node):
        return nodes.SkipNode


def setup(app):

    app.set_translator('dirhtml', nxt_translator)
    roles.register_canonical_role('nxt_term', nxt_term_role_fn)
