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
#    :nxt_hint:`term <definition>` and more text
#    .. code-block::
#       code :nxt_hint:`code <Desc>`
#       code :nxt_ph:`placeholder <Desc>`
#
# .html file:
#
#  <span style=nxt_hint title="definition">term</span> and more text
#  <span style=code>code <span title='Desc' style=nxt_hint>code</span></span>
#  <span style=code>code <span title='Desc' style=nxt_ph>placeholder</span>
#  </span>
#
# 2. Enables adaptive CSS-based tabbing on pages.
#
# .rst file:
#
# .. tabs::
#    :prefix: tab-hash-id-prefix
#    :toc:
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
from sphinx import addnodes
from sphinx.application import Sphinx
from sphinx.builders.html import DirectoryHTMLBuilder
from sphinx.domains.std import StandardDomain
from sphinx.environment.collectors.toctree import TocTreeCollector
from sphinx.errors import ExtensionError
from sphinx.locale import __
from sphinx.transforms import SphinxContentsFilter
from sphinx.environment.adapters.toctree import TocTree
from sphinx.writers.html import HTMLTranslator
from sphinx.util import logging
from typing import cast
import re


# writer-related classes and functions

class nxt_details(nodes.container): pass
class nxt_tab_body(nodes.container): pass
class nxt_tab_head(nodes.Text): pass
class nxt_tabs(nodes.container): pass
class nxt_hint(nodes.container): pass
# dummy classes, required for docutils dispatcher's Visitor pattern


logger = logging.getLogger(__name__)

nxt_plain_text = r'[\\\w\s\.\*\+\(\)\[\]\{\}\~\?\!\-\^\$\|\/\:\';,#_%&"]'
nxt_hint_regex = r'`({0}*[^\s])\s*<({0}+)>`'.format(nxt_plain_text)
# matches `text w/punctuation <text w/punctuation>` in nxt_* directives


def nxt_hint_role_fn(name, rawtext, text, lineno, inliner,
        options={}, content=[]):
# nxt_hint role handler for inline text outside code blocks

    node = nxt_hint()
    groups = re.search(nxt_hint_regex, \
        rawtext.replace('\n', ' ').replace('\r', ''))

    try:
        node.term, node.tip = groups.group(1), groups.group(2)
    except:
        msg = inliner.reporter.error(
            'Inline term "{0}" is invalid.'.format(text), line=lineno)
        prb = inliner.problematic(rawtext, rawtext, msg)
        return [prb], [msg]

    return [node], []


class nxt_highlighter(object):
# extends default highlighter with nxt_ph/nxt_hint directives in code blocks

    def __init__(self, highlighter):
        self.highlighter = highlighter

    def highlight_block(self, source, lang, opts=None, location=None,
                        force=False, **kwargs):

        ph_groups = re.findall(':nxt_ph:' + nxt_hint_regex, source)
        hint_groups = re.findall(':nxt_hint:' + nxt_hint_regex, source)

        for c, g in enumerate(ph_groups):
            source = re.sub(':nxt_ph:' + nxt_hint_regex,
                            'nxt_ph_' + str(c), source, count=1)

        for c, g in enumerate(hint_groups):
            source = re.sub(':nxt_hint:' + nxt_hint_regex,
                            'nxt_hint_' + str(c), source, count=1)

        highlighted = self.highlighter.highlight_block(source, lang, opts,
                          location, force, **kwargs)

        for c, g in enumerate(ph_groups):
            highlighted = highlighted.replace('nxt_ph_' + str(c),
                              '<span class=nxt_ph title="{0}">{1}</span>'.
                              format(g[1], g[0]), 1)

        for c, g in enumerate(hint_groups):
            highlighted = highlighted.replace('nxt_hint_' + str(c),
                              '<span class=nxt_hint title="{0}">{1}</span>'.
                              format(g[1], g[0]), 1)

        if ':nxt_ph;' in highlighted or ':nxt_hint:' in highlighted:
            raise ExtensionError(__('Could not lex nxt_* directive at {0}. ').
                                 format(location))

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
    '''Adds dispatcher methods to handle nxt_tabs and nxt_tab doctree nodes,
    replaces default highlighter to enable nxt_* directives inside code blocks,
    adds handlers to enable nxt_hint directives inline, enables expandable
    nxt_details blocks.'''

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


    def visit_nxt_hint(self, node):
        self.body.append('<span class=nxt_hint title="{1}">{0}</span>'
                         .format(node.term, node.tip))


    def depart_nxt_hint(self, node):
        pass


class nxt_collector(TocTreeCollector):
    '''Replaces TocTreeCollector.process_doc's nested build_doc function to
    include tab titles in the resulting TOC.'''

    def process_doc(self, app, doctree):
        # type: (Sphinx, nodes.Node) -> None
        """Build a TOC from the doctree and store it in the inventory.
        Copied intact from Sphinx 1.8.0 sources with nxt_tab_head traversal
        added; look for 'Extension code starts here'."""
        docname = app.env.docname
        numentries = [0]  # nonlocal again...

        def traverse_in_section(node, cls):
            # type: (nodes.Node, Any) -> List[nodes.Node]
            """Like traverse(), but stay within the same section."""
            result = []
            if isinstance(node, cls):
                result.append(node)
            for child in node.children:
                if isinstance(child, nodes.section):
                    continue
                result.extend(traverse_in_section(child, cls))
            return result

        def build_toc(node, depth=1):
            # type: (nodes.Node, int) -> List[nodes.Node]
            entries = []
            for sectionnode in node:
                # find all toctree nodes in this section and add them
                # to the toc (just copying the toctree node which is then
                # resolved in self.get_and_resolve_doctree)
                if isinstance(sectionnode, addnodes.only):
                    onlynode = addnodes.only(expr=sectionnode['expr'])
                    blist = build_toc(sectionnode, depth)
                    if blist:
                        onlynode += blist.children  # type: ignore
                        entries.append(onlynode)
                    continue
                if not isinstance(sectionnode, nodes.section):
                    # Extension code starts here
                    for tabnode in traverse_in_section(sectionnode,
                            nxt_tab_head):
                        if tabnode.tab_toc:
                            nodetext = [nodes.Text(tabnode)]
                            anchorname = '#' + tabnode.label_id
                            numentries[0] += 1
                            reference = nodes.reference(
                                '', '', internal=True, refuri=docname,
                                anchorname=anchorname, *nodetext)
                            para = addnodes.compact_paragraph('', '', reference)
                            item = nodes.list_item('', para)
                            entries.append(item)
                    # Extension code ends here
                    for toctreenode in traverse_in_section(sectionnode,
                                                           addnodes.toctree):
                        item = toctreenode.copy()
                        entries.append(item)
                        # important: do the inventory stuff
                        TocTree(app.env).note(docname, toctreenode)
                    continue
                title = sectionnode[0]
                # copy the contents of the section title, but without references
                # and unnecessary stuff
                visitor = SphinxContentsFilter(doctree)
                title.walkabout(visitor)
                nodetext = visitor.get_entry_text()
                if not numentries[0]:
                    # for the very first toc entry, don't add an anchor
                    # as it is the file's title anyway
                    anchorname = ''
                else:
                    anchorname = '#' + sectionnode['ids'][0]
                numentries[0] += 1
                # make these nodes:
                # list_item -> compact_paragraph -> reference
                reference = nodes.reference(
                    '', '', internal=True, refuri=docname,
                    anchorname=anchorname, *nodetext)
                para = addnodes.compact_paragraph('', '', reference)
                item = nodes.list_item('', para)
                sub_item = build_toc(sectionnode, depth + 1)
                item += sub_item
                entries.append(item)
            if entries:
                return nodes.bullet_list('', *entries)
            return []
        toc = build_toc(doctree)
        if toc:
            app.env.tocs[docname] = toc
        else:
            app.env.tocs[docname] = nodes.bullet_list('')
        app.env.toc_num_entries[docname] = numentries[0]


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
            'prefix': directives.unchanged,
            'toc': directives.unchanged
    }

    def run(self):
        self.assert_has_content()
        env = self.state.document.settings.env

        node = nxt_tabs()
        node['classes'] = ['nxt_tabs']
        env.temp_data['tabs_id'] = self.options.get('prefix', token_urlsafe())
        env.temp_data['tab_id'] = 0
        if 'toc' in self.options:
            env.temp_data['tab_toc'] = True
            node['classes'].append('nxt_toc')
        else:
            env.temp_data['tab_toc'] = False

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
        tab_head.label_id = '{0}-{1}'.format(env.temp_data['tabs_id'],
                            re.sub('[^\w\-]+', '', self.content[0])).lower()
        tab_head.tab_toc = env.temp_data['tab_toc']

        env.temp_data['tab_id'] += 1

        text = '\n'.join(self.content)
        tab_body = nxt_tab_body(text)
        self.state.nested_parse(self.content[2:], self.content_offset, \
            tab_body)

        return [tab_head, tab_body]


def register_tabs_as_label(app: Sphinx, document: nodes.Node) -> None:
    docname = app.env.docname
    labels = app.env.domaindata['std']['labels']
    anonlabels = app.env.domaindata['std']['anonlabels']
    for node in document.traverse(nxt_tab_head):
        if node.label_id in labels:
            logger.warning(__('duplicate label %s, other instance in %s'),
                           node.label_id,
                           app.env.doc2path(labels[node.label_id][0]),
                           location=node)
        anonlabels[node.label_id] = docname, node.label_id
        labels[node.label_id] = docname, node.label_id, node.astext()


def setup(app):

    app.add_directive('nxt_details', DetailsDirective)
    app.add_directive('tabs', TabsDirective)
    app.add_directive('tab', TabDirective)

    app.add_env_collector(nxt_collector)
    app.add_builder(nxt_builder)
    app.set_translator('nxt_html', nxt_translator)
    app.connect('doctree-read', register_tabs_as_label)

    roles.register_canonical_role('nxt_hint', nxt_hint_role_fn)
