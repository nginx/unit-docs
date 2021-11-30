"""
Copyright (C) 2019-2021, NGINX, Inc.

Sphinx extension to support advanced markup capabilities in .rst files.  All
capabilities introduced here require overriding the default translator, so the
extension unites several disparate featiures.

Usage:

conf.py:
    extensions += ['nxt']

Features:

1. Enables tooltips for terms in text and code-blocks.

.rst file:
    .. markup:: (including literal blocks)

       :nxt_hint:`term <Definition>` and more text

       .. code-block::
          code :nxt_hint:`code <Description>`
          code :nxt_ph:`placeholder <Description>`

.html file:
    <span style=nxt_hint title="Definition">term</span> and more text
    <span style=code>code <span title='Description' style=nxt_hint>code
    </span></span>
    <span style=code>code <span title='Description' style=nxt_ph>placeholder
    </span></span>

2. Enables adaptive CSS-based tabbing on pages.

.rst file:
    .. tabs::
       :prefix: tab-hash-id-prefix
       :toc:

       .. tab:: Plain Text Foo

          Foo bar foo bar foo bar:
          .. markup::
             Foo bar

       .. tab:: Plain Text Bar

          Foo bar foo bar foo bar:
          .. markup::
             Foo bar

The following in test.rst:

.. tabs::
   :prefix: foo

   .. tab:: bar
      ...

   .. tab:: baz
      ...

Produces two :ref: links, :ref:`test-foo-bar` and :ref:`test-foo-baz`, that
compile into /test/#foo-bar and /test/#foo-baz respectively.

3. Enables collapsible sections.

.rst file:
    .. nxt_details:: Plaint Text Foo
       Foo Bar

.html file:
    <details><summary>Plain Text Foo</summary>
    Foo Bar
    </details>
"""

import re
import pygments.lexers.data

from hashlib import md5 as hashlib_md5
from secrets import token_urlsafe

from docutils import nodes
from docutils.nodes import Element, Node, system_message
from docutils.parsers.rst import Directive, directives, roles
from docutils.parsers.rst.states import Inliner
from sphinx import addnodes
from sphinx.application import Sphinx
from sphinx.builders import Builder
from sphinx.builders.html import DirectoryHTMLBuilder
from sphinx.environment.adapters.toctree import TocTree
from sphinx.environment.collectors.toctree import TocTreeCollector
from sphinx.errors import ExtensionError
from sphinx.highlighting import PygmentsBridge
from sphinx.locale import __
from sphinx.transforms import SphinxContentsFilter
from sphinx.util import logging
from sphinx.writers.html import HTMLTranslator
from typing import Any, Dict, List, Tuple


# Writer-related classes and functions.


class nxt_tab_body(nodes.container):
    """Dummy class, required for docutils dispatcher's Visitor pattern."""


class nxt_tabs(nodes.container):
    """Dummy class, required for docutils dispatcher's Visitor pattern."""


class nxt_details(nodes.container):
    """Dummy class, required for docutils dispatcher's Visitor pattern.
    Only __init__ to initialize attributes.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.summary_text = None

class nxt_hint(nodes.container):
    """Dummy class, required for docutils dispatcher's Visitor pattern.
    Only __init__ to initialize attributes.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.term = None
        self.tip = None


class nxt_tab_head(nodes.Text):
    """Dummy class, required for docutils dispatcher's Visitor pattern.
    Only __init__ to initialize attributes.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.checked = None
        self.rstref_id = None
        self.anchor_id = None
        self.tab_id = None
        self.tab_toc = None
        self.tabs_id = None


# Regex to match `text w/punctuation <text w/punctuation>` in nxt_* directives.
NXT_PLAIN_TEXT = r'[\\\w\s\.\*\+\(\)\[\]\{\}\~\?\!\-\^\$\|\/\:\';,#_%&"]'
NXT_HINT_REGEX = fr'`({NXT_PLAIN_TEXT}*[^\s])\s*<({NXT_PLAIN_TEXT}+)>`'
NXT_VAR_REGEX = r'(\$[a-zA-Z_]+|\${[a-zA-Z_]+})'


def nxt_hint_role_fn(_: str, rawtext: str, text: str, lineno: int, inliner:
        Inliner, *args: Any) -> Tuple[List[Node], List[system_message]]:
    """The nxt_hint role handler for inline text outside code blocks."""

    node = nxt_hint()
    groups = re.search(NXT_HINT_REGEX,
                       rawtext.replace('\n', ' ').replace('\r', ''))

    try:
        node.term, node.tip = groups.group(1), groups.group(2)
    except IndexError:
        msg = inliner.reporter.error(
            f'Inline term "{text}" is invalid.', line=lineno)
        prb = inliner.problematic(rawtext, rawtext, msg)
        return [prb], [msg]

    return [node], []


class NxtHighlighter:
    """Extends default highlighter with nxt_ph and nxt_hint directives
    in code blocks.
    """

    def __init__(self, highlighter: PygmentsBridge) -> None:
        self.highlighter = highlighter

    def highlight_block(self, source: str, lang: str, opts: Dict = None,
            force: bool = False, location: Any = None, **kwargs: Any) -> str:
        """Preserves nxt_ directives, highlights syntax, replaces directives.
        """


        groups = {}

        groups['var'] = re.findall(NXT_VAR_REGEX, source)
        for i in range(len(groups['var'])):
            source = re.sub(NXT_VAR_REGEX, f'nxt_var_{i}', source, count=1)

        categories = ['ph', 'hint']
        for cat in categories:
            groups[cat] = re.findall(f':nxt_{cat}:{NXT_HINT_REGEX}', source)
            for i in range(len(groups[cat])):
                source = re.sub(f':nxt_{cat}:{NXT_HINT_REGEX}',
                                f'nxt_{cat}_{i}', source, count=1)

        highlighted = self.highlighter.highlight_block(
            source, lang, opts, force, location, **kwargs)

        for cat in categories:
            for i, group in enumerate(groups[cat]):
                txt, hnt = group
                for j, var in enumerate(groups['var']):
                    hnt = hnt.replace(f'nxt_var_{j}', var, 1)

                highlighted = highlighted.replace(f'nxt_{cat}_' + str(i),
                    f'<span class=nxt_{cat} title="{hnt}">{txt}</span>', 1)

            if f':nxt_{cat}:' in highlighted:
                raise ExtensionError(
                    __(f'Could not lex nxt_* entity at {location}. '))

        for i, var in enumerate(groups['var']):
            highlighted = highlighted.replace(f'nxt_var_{i}',
                f'<span class=nxt_var>{var}</span>', 1)

        return highlighted


class NxtBuilder(DirectoryHTMLBuilder):
    """Adds a custom function to enable MD5-based versioning."""

    name = 'nxt_html'

    def __init__(self, app: Sphinx) -> None:
        super().__init__(app)

    def update_page_context(self, pagename: str, templatename: str,
            ctx: Dict, event_arg: Any) -> None:
        """Extends builder context to make the MD5 function available at
        build time.
        """

        def md5(fname: str) -> str:
            """Calculates MD5 for a file relative to source directory."""

            pathname = self.srcdir + '/' + fname
            hsh = hashlib_md5()

            with open(pathname, 'rb') as hashed_file:
                for chunk in iter(lambda: hashed_file.read(65536), b''):
                    hsh.update(chunk)

            return hsh.hexdigest()

        DirectoryHTMLBuilder.update_page_context(self, pagename, templatename,
                                                 ctx, event_arg)
        ctx['md5'] = md5


class NxtTranslator(HTMLTranslator):
    """Adds dispatcher methods to handle nxt_tabs and nxt_tab doctree nodes,
    replaces default highlighter to enable nxt_* directives inside code blocks,
    adds handlers to enable nxt_hint directives inline, enables expandable
    nxt_details blocks.
    """

    def __init__(self, document: nodes.document, builder: Builder) -> None:
        super().__init__(document, builder)
        self.highlighter = NxtHighlighter(builder.highlighter)

    def visit_nxt_details(self, node: Element) -> None:
        """Handles the nxt_details directive."""

        self.body.append(f"""<details>
            <summary onclick="this.addEventListener('click',
            e => e.preventDefault())"><span>{node.summary_text}</span>
            </summary>""")

        HTMLTranslator.visit_container(self, node)

    def depart_nxt_details(self, node: Element) -> None:
        """Handles the nxt_details directive."""

        HTMLTranslator.depart_container(self, node)
        self.body.append('</details>')

    def visit_nxt_hint(self, node: Element) -> None:
        """Handles the nxt_hint directive *outside* literal blocks."""
        self.body.append(f'''<span class=nxt_hint title="{node.tip}">
                         {node.term}</span>''')

    def depart_nxt_hint(self, node: Element) -> None:
        """Handles the nxt_hint directive *outside* literal blocks."""

    def visit_nxt_tab_body(self, node: Element) -> None:
        """Handles the nxt_tab_body node in an individual tab."""
        HTMLTranslator.visit_container(self, node)

    def depart_nxt_tab_body(self, node: Element) -> None:
        """Handles the nxt_tab_body node in an individual tab."""
        HTMLTranslator.depart_container(self, node)

    def visit_nxt_tab_head(self, node: Element) -> None:
        """Handles the nxt_tab_head node in an individual tab."""
        self.body.append(f"""<input name={node.tabs_id} type=radio
            id={node.tab_id} class=nojs {node.checked}/>""")

        self.body.append(f"""<label for={node.tab_id} id={node.anchor_id}>
            <a href=#{node.anchor_id} onclick="nxt_tab_click(event)">""")

        HTMLTranslator.visit_Text(self, node)

    def depart_nxt_tab_head(self, node: Element) -> None:
        """Handles the nxt_tab_head node in an individual tab."""
        self.body.append('</a></label>')
        HTMLTranslator.depart_Text(self, node)

    def visit_nxt_tabs(self, node: Element) -> None:
        """Handles the nxt_tabs node in a tab group."""
        HTMLTranslator.visit_container(self, node)

    def depart_nxt_tabs(self, node: Element) -> None:
        """Handles the nxt_tabs node in a tab group."""
        HTMLTranslator.depart_container(self, node)

    def unimplemented_visit(self, node: Element) -> None:
        """Dummpy implementation for an abstract method."""

    def unknown_visit(self, node: Element) -> None:
        """Dummpy implementation for an abstract method."""


class NxtCollector(TocTreeCollector):
    """Replaces TocTreeCollector.process_doc's nested build_doc function to
    include tab titles in the resulting TOC.
    """

    def process_doc(self, app: Sphinx, doctree: Node) -> None:
        """Build a TOC from the doctree and store it in the inventory.
        Copied intact from Sphinx 1.8.0 sources with nxt_tab_head traversal
        added; look for 'Extension code starts here'.
        """

        docname = app.env.docname
        numentries = [0]  # nonlocal again...

        def traverse_in_section(node: Node, cls: Any) -> List[Node]:
            """Like traverse(), but stay within the same section."""

            result = []
            if isinstance(node, cls):
                result.append(node)
            for child in node.children:
                if isinstance(child, nodes.section):
                    continue
                result.extend(traverse_in_section(child, cls))
            return result

        def build_toc(node: Node, depth: int = 1) -> List[Node]:
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
                    # Extension code starts here.
                    for tabnode in traverse_in_section(
                        sectionnode, nxt_tab_head):
                        if tabnode.tab_toc:
                            nodetext = [nodes.Text(tabnode)]
                            anchorname = '#' + tabnode.anchor_id
                            numentries[0] += 1
                            reference = nodes.reference(
                                '', '', internal=True, refuri=docname,
                                anchorname=anchorname, *nodetext)
                            para = addnodes.compact_paragraph('', '',
                                                              reference)
                            item = nodes.list_item('', para)
                            entries.append(item)
                    # Extension code ends here.
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


# Doctree-related classes and functions.


class DetailsDirective(Directive):
    """Handles the nxt_details directive, adding an nxt_details
    container node.
    """

    has_content = True

    def run(self) -> List[Node]:
        self.assert_has_content()

        node = nxt_details()
        node.summary_text = self.content[0]

        self.state.nested_parse(self.content[2:], self.content_offset, node)

        return [node]


class TabsDirective(Directive):
    """Handles the tabs directive, adding an nxt_tabs container node."""

    has_content = True
    option_spec = {
        'prefix': directives.unchanged,
        'toc': directives.unchanged
    }

    def run(self) -> List[Node]:
        self.assert_has_content()
        env = self.state.document.settings.env

        node = nxt_tabs()
        node['classes'] = ['nxt_tabs']
        if 'tabs_id' in env.temp_data:
            env.temp_data['tabs_id'].append(self.options.get('prefix',
                                                             token_urlsafe()))
        else:
            env.temp_data['tabs_id'] = [self.options.get('prefix',
                                                         token_urlsafe())]

        if 'tab_id' in env.temp_data:
            env.temp_data['tab_id'].append(0)
        else:
            env.temp_data['tab_id'] = [0]

        if 'toc' in self.options:
            env.temp_data['tab_toc'] = True
            node['classes'].append('nxt_toc')
        else:
            env.temp_data['tab_toc'] = False

        self.state.nested_parse(self.content, self.content_offset, node)

        env.temp_data['tabs_id'].pop()
        env.temp_data['tab_id'].pop()

        return [node]


class TabDirective(Directive):
    """Handles the tab directive, adding an nxt_tab container node."""

    has_content = True

    def run(self) -> List[Node]:
        self.assert_has_content()
        env = self.state.document.settings.env

        tab_head = nxt_tab_head(self.content[0])

        tab_head.tabs_id = env.temp_data['tabs_id'][-1]
        tab_head.checked = 'checked' if env.temp_data['tab_id'][-1] == 0 else ''
        tab_head.tab_id = '{}_{}'.format(env.temp_data['tabs_id'][-1],
            env.temp_data['tab_id'][-1])
        tab_head.rstref_id = '{}-{}-{}'.format(env.docname,
            env.temp_data['tabs_id'][-1],
            re.sub(r'[^\w\-]+', '', self.content[0])).lower()
        tab_head.anchor_id = tab_head.rstref_id.split('-', 1)[1]
        tab_head.tab_toc = env.temp_data['tab_toc']

        env.temp_data['tab_id'][-1] += 1

        text = '\n'.join(self.content)
        tab_body = nxt_tab_body(text)
        self.state.nested_parse(self.content[2:], self.content_offset,
                                tab_body)

        return [tab_head, tab_body]


def register_tabs_as_label(app: Sphinx, document: nodes.document) -> None:
    """Registers tabs as anchors in TOC."""

    docname = app.env.docname
    labels = app.env.domaindata['std']['labels']
    anonlabels = app.env.domaindata['std']['anonlabels']

    for node in document.traverse(nxt_tab_head):
        if node.rstref_id in labels:
            logging.getLogger(__name__).warning(
                __('duplicate label %s, other instance in %s'),
                node.rstref_id,
                app.env.doc2path(labels[node.rstref_id][0]),
                location=node)
        anonlabels[node.rstref_id] = docname, node.anchor_id
        labels[node.rstref_id] = docname, node.anchor_id, node.astext()


def setup(app: Sphinx) -> None:
    """Connects the extension to the app."""
    pygments.lexers.data.JsonLexer.constants = \
        set('truefalsenullxphi_0123456789')
    # Adding 'nxt_ph_N' and 'nxt_hint_N' to the charset allows
    # NxtHightlighter.highlight_block() to run w/o resetting lexer to 'none'
    # when constants such as false and true are commented with nxt_ directives.

    app.add_directive('nxt_details', DetailsDirective)
    app.add_directive('tabs', TabsDirective)
    app.add_directive('tab', TabDirective)

    app.add_env_collector(NxtCollector)
    app.add_builder(NxtBuilder)
    app.set_translator('nxt_html', NxtTranslator)
    app.connect('doctree-read', register_tabs_as_label)

    roles.register_canonical_role('nxt_hint', nxt_hint_role_fn)
