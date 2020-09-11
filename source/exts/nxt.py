# Copyright (C) 2019, NGINX, Inc.
# Sphinx extension to support advanced markup capabilities in .rst files.
#
# Usage:
#
# conf.py:
#
# extensions += ['nxt']
#
# 1. Enables tooltips for terms in text and code-blocks.
#
# .rst file:
#
# .. markup:: (including literal blocks)
#
#    :nxt_term:`term <definition>` and more text
#
# .html file:
#
#  <span style="nxt_term" title="definition">term</span> and more text
#
# 2. Enables adaptive CSS-based tabbing on pages.
#
# .rst file:
#
# .. tabs::
#
#    .. tab:: Plain Text Foo
#
#       Foo bar foo bar foo bar:
#
#       .. markup::
#
#          Foo bar
#
#    .. tab:: Plain Text Bar
#
#       Foo bar foo bar foo bar:
#
#       .. markup::
#
#          Foo bar
#
# 3. Enables collapsible sections.
#
# .rst file:
#
# .. nxt_details:: Plaint Text Foo
#
#    Foo Bar
#
# .html file:
#
#  <details><summary>Plain Text Foo</summary>
#  Foo Bar
#  </details>

from docutils import nodes
from docutils.parsers.rst import Directive, directives, roles
from hashlib import md5 as hashlib_md5
from os import path, strerror
from secrets import token_urlsafe
from sphinx.builders.html import DirectoryHTMLBuilder
from sphinx.writers.html import HTMLTranslator
import re


# writer-related classes and functions

class nxt_details(nodes.container): pass
class nxt_tab_body(nodes.container): pass
class nxt_tab_head(nodes.Text): pass
class nxt_tabs(nodes.container): pass
class nxt_term(nodes.container): pass
# dummy classes, required for docutils dispatcher's Visitor pattern


nxt_term_regex = r'`({0}*[^\s])\s*<({0}+)>`'.format(r'[\w\s\.\,\?\!\-\/\:#_]')
# matches `text w/punctuation <text w/punctuation>` in ':nxt_term:' directives


def nxt_term_role_fn(name, rawtext, text, lineno, inliner,
        options={}, content=[]):
# ':nxt_term:' role handler for inline text outside literal blocks

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


class nxt_highlighter(object):
# extends default highlighter to handle ':nxt_term:' inside literal blocks

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


class nxt_builder(DirectoryHTMLBuilder):
    '''Adds custom function to enable MD5-based versioning.'''

    name = 'nxt_html'

    def __init__(self, app):
        DirectoryHTMLBuilder.__init__(self, app)


    def update_page_context(self, pagename, templatename, ctx, event_arg):
        '''Extends builder context to make the function available at build time.'''

        DirectoryHTMLBuilder.update_page_context(self, pagename, templatename, \
                                                 ctx, event_arg)

        def md5(fname):
            '''Calculates MD5 for a file relative to source directory.'''

            pathname = self.srcdir + '/' + fname
            hash = hashlib_md5()
            with open(pathname, 'rb') as f:
                for chunk in iter(lambda: f.read(65536), b''):
                    hash.update(chunk)

            return hash.hexdigest()

        ctx['md5'] = md5


class nxt_translator(HTMLTranslator):
    '''Adds dispatcher methods to handle 'nxt_tabs' and 'nxt_tab' doctree nodes,
    replaces default highlighter to enable ':nxt_term:' inside literal blocks,
    enables expandable .. nxt_details:: blocks.'''

    def __init__(self, builder, *args, **kwargs):
        HTMLTranslator.__init__(self, builder, *args, **kwargs)
        self.highlighter = nxt_highlighter(builder.highlighter)


    def visit_nxt_details(self, node):
        self.body.append('''
        <details>
        <summary onclick="this.addEventListener('click',
        e => e.preventDefault())"><span>{0}</span></summary>'''
        .format(node.summary_text))

        HTMLTranslator.visit_container(self,node)


    def depart_nxt_details(self, node):
        HTMLTranslator.depart_container(self,node)
        self.body.append('</details>')


    def visit_nxt_tabs(self, node):
        HTMLTranslator.visit_container(self,node)


    def depart_nxt_tabs(self, node):
        HTMLTranslator.depart_container(self,node)


    def visit_nxt_tab_head(self, node):
        self.body.append('''
        <input name={0} type=radio id={1} class="nojs" {2}/>'''
        .format(node.tabs_id, node.tab_id, node.checked))

        self.body.append('''
        <label for={0} id={1}><a href=#{1} onclick="nxt_tab_click(event)">'''
        .format(node.tab_id, node.label_id))

        HTMLTranslator.visit_Text(self,node)


    def depart_nxt_tab_head(self, node):
        self.body.append('</a></label>')
        HTMLTranslator.depart_Text(self,node)


    def visit_nxt_tab_body(self, node):
        HTMLTranslator.visit_container(self,node)


    def depart_nxt_tab_body(self, node):
        HTMLTranslator.depart_container(self,node)


    def visit_nxt_term(self, node):
        self.body.append('''<span class=nxt_term title="{1}">{0}</span>'''
        .format(node.term, node.tip))


    def depart_nxt_term(self, node):
        pass


# doctree-related classes

class DetailsDirective(Directive):
    '''Handles the '.. nxt_details::' directive, adding an 'nxt_details'
    container node.'''

    has_content = True

    def run(self):
        self.assert_has_content()
        env = self.state.document.settings.env

        node = nxt_details()
        node.summary_text = self.content[0]

        self.state.nested_parse(self.content[2:], self.content_offset, node)

        return [node]


class TabsDirective(Directive):
# handles the '.. tabs::' directive, adding an 'nxt_tabs' container node

    has_content = True
    option_spec = {
            'prefix': directives.unchanged
    }

    def run(self):
        self.assert_has_content()
        env = self.state.document.settings.env

        node = nxt_tabs()
        node['classes'] = ['nxt_tabs']
        env.temp_data['tabs_id'] = self.options.get('prefix', token_urlsafe())
        env.temp_data['tab_id'] = 0

        self.state.nested_parse(self.content, self.content_offset, node)

        return [node]


class TabDirective(Directive):
# handles the '.. tab::' directive, adding an 'nxt_tab' container node

    has_content = True

    def run(self):
        self.assert_has_content()
        env = self.state.document.settings.env

        tab_head = nxt_tab_head(self.content[0])

        tab_head.tabs_id = env.temp_data['tabs_id']
        tab_head.checked = 'checked' if env.temp_data['tab_id'] == 0 else ''
        tab_head.tab_id = '{0}_{1}'.\
            format(env.temp_data['tabs_id'], env.temp_data['tab_id'])
        tab_head.label_id = '{0}_{1}'.format(env.temp_data['tabs_id'],
                                re.sub('[^\w\-]+', '', self.content[0]))

        env.temp_data['tab_id'] += 1

        text = '\n'.join(self.content)
        tab_body = nxt_tab_body(text)
        self.state.nested_parse(self.content[2:], self.content_offset, \
            tab_body)

        return [tab_head, tab_body]


def setup(app):

    app.add_directive('nxt_details', DetailsDirective)
    app.add_directive('tabs', TabsDirective)
    app.add_directive('tab', TabDirective)

    app.add_builder(nxt_builder)
    app.set_translator('nxt_html', nxt_translator)

    roles.register_canonical_role('nxt_term', nxt_term_role_fn)
