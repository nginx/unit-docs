"""
Copyright (C) 2019-2023, NGINX, Inc.

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
       :hash: anchor-id

       Foo Bar

.html file:
    <details><summary>Plain Text Foo</summary>
    Foo Bar
    </details>

 4. Enables adding files to an RSS feed and a responsive news collection:

 *.rst file:

  #######
  Foo Bar
  #######

  .. nxt_news_entry::
     :author: Jane Doe
     :email: unit@nginx.org
     :date: date
     :title: Foo bar
     :description: Bar foo foo bar lorem ipsum
     :url: https://example.com/news/article/

Each directive renders a news entry; URLs can be relative (site-local) or
external; if there's no URL, no link is generated.

  .. nxt_news_recent::
     :number: 10

Lists N latest news entries from the entire site, reverse sorted by date.

 rss.xml (filename can be set in conf.py):

<?xml version="1.0" encoding="utf-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
    <channel>
        <atom:link href="https://unit.nginx.org/rss.xml" rel="self"
            type="application/rss+xml" />
        <title>NGINX Unit</title>
        <link>https://unit.nginx.org/</link>
        <copyright>NGINX, Inc., 2017-2023</copyright>
        <description>NGINX Unit news and articles</description>
        <generator>nxt-newsfeed</generator>
            <item>
                <title>Foo bar</title>
                <link>https://example.com/news/article/</link>
                <guid>https://example.com/news/article/</guid>
                <author>unit@nginx.org (Jane Doe)</author>
                <description>Bar foo foo bar lorem ipsum</description>
                <pubDate>date in RFC-822</pubDate>
            </item>
    </channel>
</rss>
"""

import re
import xml.dom.minidom

from email.utils import format_datetime
from datetime import datetime, timezone
from hashlib import md5 as hashlib_md5
from urllib.parse import urlparse
from secrets import token_urlsafe
from typing import Any, Dict, List, Tuple, Type, TypeVar

try:
    from zoneinfo import ZoneInfo
except ImportError:
    from backports.zoneinfo import ZoneInfo

import pygments.lexers.data

from docutils import nodes
from docutils.nodes import Element, Node, system_message
from docutils.parsers.rst import Directive, directives, roles
from docutils.parsers.rst.states import Inliner
from sphinx import addnodes
from sphinx.application import Sphinx
from sphinx.builders import Builder
from sphinx.builders.dirhtml import DirectoryHTMLBuilder
from sphinx.environment import BuildEnvironment
from sphinx.environment.adapters.toctree import TocTree
from sphinx.environment.collectors.toctree import TocTreeCollector
from sphinx.errors import ExtensionError
from sphinx.highlighting import PygmentsBridge
from sphinx.locale import __
from sphinx.transforms import SphinxContentsFilter
from sphinx.util import logging
from sphinx.writers.html import HTMLTranslator


N = TypeVar("N")


def nxt_make_id(s: str) -> str:
    """Creates a href-able id from a string by stripping extra characters."""
    return re.sub(r"[^\w\-]+", "", s).lower()


# Writer-related classes and functions.


class nxt_news_recent(nodes.raw):
    """Dummy class, required for docutils dispatcher's Visitor pattern."""


class nxt_news_entry(nodes.raw):
    """Dummy class, required for docutils dispatcher's Visitor pattern."""


class nxt_tab_body(nodes.container):
    """Dummy class, required for docutils dispatcher's Visitor pattern."""


class nxt_tabs(nodes.container):
    """Dummy class, required for docutils dispatcher's Visitor pattern."""


class nxt_details(nodes.container):
    """Dummy class, required for docutils dispatcher's Visitor pattern.
    Only __init__ to initialize attributes.
    """

    def __init__(self, st: str, h: str, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.summary_text = st
        self.rstref_id = h
        self.anchor_id = h


class nxt_hint(nodes.container):
    """Dummy class, required for docutils dispatcher's Visitor pattern.
    Only __init__ to initialize attributes.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.term = None
        self.tip = None


class nxt_tab_head(nodes.Element):
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
NXT_HINT_REGEX = rf"`({NXT_PLAIN_TEXT}*[^\s])\s*<({NXT_PLAIN_TEXT}+)>`"
NXT_VAR_REGEX = r"(\$[a-zA-Z_]+|\${[a-zA-Z_]+})"
NXT_NJSTEMPL_REGEX = r"\"(`.*?`)\""
NXT_JSTRIM_REGEX = (
    r'<div class="highlight"><pre><span></span>(.*?)\n</pre></div>\n'
)


def nxt_hint_role_fn(
    _: str, rawtext: str, text: str, lineno: int, inliner: Inliner, *args: Any
) -> Tuple[List[Node], List[system_message]]:
    """The nxt_hint role handler for inline text outside code blocks."""

    node = nxt_hint()
    groups = re.search(
        NXT_HINT_REGEX, rawtext.replace("\n", " ").replace("\r", "")
    )

    try:
        node.term, node.tip = groups.group(1), groups.group(2)
    except IndexError:
        msg = inliner.reporter.error(
            f'Inline term "{text}" is invalid.', line=lineno
        )
        prb = inliner.problematic(rawtext, rawtext, msg)
        return [prb], [msg]

    return [node], []


class NxtHighlighter:
    """Extends default highlighter with nxt_ph and nxt_hint directives
    in code blocks.
    """

    def __init__(self, highlighter: PygmentsBridge) -> None:
        self.highlighter = highlighter

    def highlight_block(
        self,
        source: str,
        lang: str,
        opts: Dict = None,
        force: bool = False,
        location: Any = None,
        **kwargs: Any,
    ) -> str:
        """Preserves nxt_ directives, highlights syntax, replaces directives."""

        groups = {}

        if lang == "json":
            groups["njs"] = re.findall(NXT_NJSTEMPL_REGEX, source)
            for i in range(len(groups["njs"])):
                source = re.sub(
                    NXT_NJSTEMPL_REGEX, f'"nxt_njs_{i}"', source, count=1
                )

            groups["var"] = re.findall(NXT_VAR_REGEX, source)
            for i in range(len(groups["var"])):
                source = re.sub(NXT_VAR_REGEX, f"nxt_var_{i}", source, count=1)

        categories = ["ph", "hint"]
        for cat in categories:
            groups[cat] = re.findall(f":nxt_{cat}:{NXT_HINT_REGEX}", source)
            for i in range(len(groups[cat])):
                source = re.sub(
                    f":nxt_{cat}:{NXT_HINT_REGEX}",
                    f"nxt_{cat}_{i}",
                    source,
                    count=1,
                )

        highlighted = self.highlighter.highlight_block(
            source, lang, opts, force, location, **kwargs
        )

        for cat in categories:
            for i, group in enumerate(groups[cat]):
                txt, hnt = group
                if lang == "json":
                    for j, var in enumerate(groups["var"]):
                        hnt = hnt.replace(f"nxt_var_{j}", var, 1)

                highlighted = highlighted.replace(
                    f"nxt_{cat}_" + str(i),
                    f'<span class=nxt_{cat} title="{hnt}">{txt}</span>',
                    1,
                )

            if f":nxt_{cat}:" in highlighted:
                raise ExtensionError(
                    __(f"Could not lex nxt_* entity at {location}. ")
                )

        if lang == "json":
            for i, njs in enumerate(groups["njs"]):
                njs = self.highlighter.highlight_block(
                    njs, "javascript", opts, force, location, **kwargs
                )
                njs = re.sub(NXT_JSTRIM_REGEX, r"\1", njs, count=1)
                highlighted = highlighted.replace(f"nxt_njs_{i}", njs, 1)

            for i, var in enumerate(groups["var"]):
                highlighted = highlighted.replace(
                    f"nxt_var_{i}", f"<span class=nxt_var>{var}</span>", 1
                )

        return highlighted


class NxtBuilder(DirectoryHTMLBuilder):
    """Adds a custom function to enable MD5-based versioning."""

    name = "nxt_html"

    def __init__(self, app: Sphinx, env: BuildEnvironment = None) -> None:
        super().__init__(app, env)

    def update_page_context(
        self, pagename: str, templatename: str, ctx: Dict, event_arg: Any
    ) -> None:
        """Extends builder context to make the MD5 function available at
        build time.
        """

        def md5(fname: str) -> str:
            """Calculates MD5 for a file relative to source directory."""

            pathname = self.srcdir + "/" + fname
            hsh = hashlib_md5()

            with open(pathname, "rb") as hashed_file:
                for chunk in iter(lambda: hashed_file.read(65536), b""):
                    hsh.update(chunk)

            return hsh.hexdigest()

        DirectoryHTMLBuilder.update_page_context(
            self, pagename, templatename, ctx, event_arg
        )
        ctx["md5"] = md5


class NxtTranslator(HTMLTranslator):
    """Adds dispatcher methods to handle nxt_tabs and nxt_tab doctree nodes,
    replaces default highlighter to enable nxt_* directives inside code blocks,
    adds handlers to enable nxt_hint directives inline, enables expandable
    nxt_details blocks.  Also handles the news entries.
    """

    def __init__(self, document: nodes.document, builder: Builder) -> None:
        super().__init__(document, builder)
        self.highlighter = NxtHighlighter(builder.highlighter)

    def visit_nxt_details(self, node: Element) -> None:
        """Handles the nxt_details directive."""

        self.body.append(
            f"""<details id={node.rstref_id}_
            onclick="window.location.hash='#{node.anchor_id}'">
            <summary><span>{node.summary_text}</span></summary>"""
        )

        HTMLTranslator.visit_container(self, node)

    def depart_nxt_details(self, node: Element) -> None:
        """Handles the nxt_details directive."""

        HTMLTranslator.depart_container(self, node)
        self.body.append("</details>")

    def visit_nxt_hint(self, node: Element) -> None:
        """Handles the nxt_hint directive *outside* literal blocks."""
        self.body.append(
            f"""<span class=nxt_hint title="{node.tip}">
                         {node.term}</span>"""
        )

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
        self.body.append(
            f"""<input name={node.tabs_id} type=radio
            id={node.tab_id} class=nojs {node.checked}/>
            <label for={node.tab_id} id={node.anchor_id}>
            <a href=#{node.anchor_id} onclick="nxt_tab_click(event)">"""
        )

    def depart_nxt_tab_head(self, node: Element) -> None:
        """Handles the nxt_tab_head node in an individual tab."""
        self.body.append("</a></label>")

    def visit_nxt_tabs(self, node: Element) -> None:
        """Handles the nxt_tabs node in a tab group."""
        HTMLTranslator.visit_container(self, node)

    def depart_nxt_tabs(self, node: Element) -> None:
        """Handles the nxt_tabs node in a tab group."""
        HTMLTranslator.depart_container(self, node)

    def __write_news_entry(self, e: List[dict], prefix: str = "") -> None:
        date = datetime.fromisoformat(e["date"]).strftime("%B %-d, %Y")
        if "relurl" in e:
            self.body.append(
                f"""
                <div class=nxt_news_item>
                <h2>
                    <a href={e["relurl"]}>{e['title']}</a>
                    <a class=headerlink href={prefix + e['anchor']}
                        title="Permalink to this headline">§</a>
                </h2>
                <p class=nxt_news_authordate>
                    {e['author']}&nbsp;on&nbsp;{date}
                </p>
                <p>{e['description']}</p>"""
            )
            domain = urlparse(e["relurl"]).netloc
            if domain.startswith("www."):
                domain = domain[4:]
            self.body.append(
                f"""
                <p class=nxt_newslink>
                <a href={e["relurl"]}>Details</a>"""
                + (f" on {domain.capitalize()}" if domain else "")
                + "</p>"
            )
        self.body.append("</div>")

    def visit_nxt_news_recent(self, node: Element) -> None:
        """Handles the nxt_news_recent directive."""
        if not NewsEntryDirective.items:
            return

        sorted_entries = sorted(
            NewsEntryDirective.items, key=lambda x: x["date"], reverse=True
        )[: node.number]

        self.body.append("<div class=nxt_news>")
        for e in sorted_entries:
            self.__write_news_entry(e, node.prefix)

    def depart_nxt_news_recent(self, node: Element) -> None:
        """Handles the nxt_news_recent directive."""
        self.body.append("</div>")

    def visit_nxt_news_entry(self, node: Element) -> None:
        """Handles the nxt_news_entry directive."""
        self.__write_news_entry(node.options, node.prefix)

    def depart_nxt_news_entry(self, node: Element) -> None:
        """Handles the nxt_news_entry directive."""

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
        Copied intact from Sphinx 4.3 sources with nxt_tab_head traversal added;
        look for 'Extension code starts here'.
        """
        docname = app.env.docname
        numentries = [0]  # nonlocal again...

        def traverse_in_section(node: Element, cls: Type[N]) -> List[N]:
            """Like traverse(), but stay within the same section."""
            result: List[N] = []
            if isinstance(node, cls):
                result.append(node)
            for child in node.children:
                if isinstance(child, nodes.section):
                    continue
                elif isinstance(child, nodes.Element):
                    result.extend(traverse_in_section(child, cls))
            return result

        def build_toc(node: Element, depth: int = 1) -> nodes.bullet_list:
            entries: List[Element] = []
            for sectionnode in node:
                # find all toctree nodes in this section and add them
                # to the toc (just copying the toctree node which is then
                # resolved in self.get_and_resolve_doctree)
                if isinstance(sectionnode, nodes.section):
                    title = sectionnode[0]
                    # copy the contents of the section title, but without references
                    # and unnecessary stuff
                    visitor = SphinxContentsFilter(doctree)
                    title.walkabout(visitor)
                    nodetext = visitor.get_entry_text()
                    if not numentries[0]:
                        # for the very first toc entry, don't add an anchor
                        # as it is the file's title anyway
                        anchorname = ""
                    else:
                        anchorname = "#" + sectionnode["ids"][0]
                    numentries[0] += 1
                    # make these nodes:
                    # list_item -> compact_paragraph -> reference
                    reference = nodes.reference(
                        "",
                        "",
                        internal=True,
                        refuri=docname,
                        anchorname=anchorname,
                        *nodetext,
                    )
                    para = addnodes.compact_paragraph("", "", reference)
                    item: Element = nodes.list_item("", para)
                    sub_item = build_toc(sectionnode, depth + 1)
                    if sub_item:
                        item += sub_item
                    entries.append(item)
                elif isinstance(sectionnode, addnodes.only):
                    onlynode = addnodes.only(expr=sectionnode["expr"])
                    blist = build_toc(sectionnode, depth)
                    if blist:
                        onlynode += blist.children
                        entries.append(onlynode)
                elif isinstance(sectionnode, nodes.Element):
                    for toctreenode in traverse_in_section(
                        sectionnode, addnodes.toctree
                    ):
                        item = toctreenode.copy()
                        entries.append(item)
                        # important: do the inventory stuff
                        TocTree(app.env).note(docname, toctreenode)

                # Extension code starts here.
                if not isinstance(sectionnode, nodes.section):
                    for tabnode in traverse_in_section(
                        sectionnode, nxt_tab_head
                    ):
                        if tabnode.tab_toc:
                            nodetext = [nodes.Text(tabnode.children[0])]
                            anchorname = "#" + tabnode.anchor_id
                            numentries[0] += 1
                            reference = nodes.reference(
                                "",
                                "",
                                internal=True,
                                refuri=docname,
                                anchorname=anchorname,
                                *nodetext,
                            )
                            para = addnodes.compact_paragraph(
                                "", "", reference
                            )
                            item = nodes.list_item("", para)
                            entries.append(item)

                    for newsnode in traverse_in_section(
                        sectionnode, nxt_news_entry
                    ):
                        nodetext = [nodes.Text(newsnode.options["title"])]
                        if "relurl" in newsnode.options:
                            anchorname = newsnode.options["relurl"]
                        else:
                            anchorname = "#" + nxt_make_id(
                                newsnode.options["title"]
                            )

                        numentries[0] += 1
                        reference = nodes.reference(
                            "",
                            "",
                            internal=True,
                            refuri=docname,
                            anchorname=anchorname,
                            *nodetext,
                        )
                        para = addnodes.compact_paragraph("", "", reference)
                        item = nodes.list_item("", para)
                        entries.append(item)
                # Extension code ends here.

            if entries:
                return nodes.bullet_list("", *entries)
            return None

        toc = build_toc(doctree)
        if toc:
            app.env.tocs[docname] = toc
        else:
            app.env.tocs[docname] = nodes.bullet_list("")
        app.env.toc_num_entries[docname] = numentries[0]


class NewsRecentDirective(Directive):
    """Handles the '.. nxt_news_recent::' directive, adding N latest news items."""

    has_content = True

    option_spec = {"number": directives.unchanged_required}

    def run(self) -> List[Node]:

        node = nxt_news_recent()
        node.number = int(self.options["number"])
        node.prefix = "../" * (
            self.state.document.settings.env.docname.count("/") + 1
        )
        return [node]


class NewsEntryDirective(Directive):
    """Handles the '.. nxt_news_entry' directive, adding a class-local
    news item for _recent and _list directives and emitting a news entry.
    """

    items = []

    has_content = True

    option_spec = {
        "author": directives.unchanged_required,
        "date": directives.unchanged_required,
        "description": directives.unchanged,
        "email": directives.unchanged_required,
        "title": directives.unchanged_required,
        "url": directives.unchanged,
    }

    def run(self) -> List[Node]:
        env = self.state.document.settings.env
        self.items.append(self.options)
        node = nxt_news_entry()
        node.options = self.options
        node.prefix = "../" * (env.docname.count("/") + 1)
        self.options["anchor"] = (
            env.docname.rsplit("/", 1)[0]
            + "/#"
            + nxt_make_id(self.options["title"])
        )
        if "url" in self.options:
            self.options["relurl"] = (
                "" if "://" in self.options["url"] else node.prefix
            ) + self.options["url"]
        return [node]


# Doctree-related classes and functions.


class NxtDetailsDirective(Directive):
    """Handles the nxt_details directive, adding an nxt_details
    container node.
    """

    has_content = True
    option_spec = {"hash": directives.unchanged_required}

    def run(self) -> List[Node]:
        self.assert_has_content()

        if (hsh := self.options.get("hash")) is None:
            raise ExtensionError(
                __(
                    f"Empty hash property in the nxt_details directive at line "
                    f"{self.lineno} in {self.state.document.current_source}."
                )
            )

        node = nxt_details(self.content[0], hsh)

        self.state.nested_parse(self.content[2:], self.content_offset, node)

        return [node]


class NxtTabsDirective(Directive):
    """Handles the tabs directive, adding an nxt_tabs container node."""

    has_content = True
    option_spec = {"prefix": directives.unchanged, "toc": directives.unchanged}

    def run(self) -> List[Node]:
        self.assert_has_content()
        env = self.state.document.settings.env

        node = nxt_tabs()
        node["classes"] = ["nxt_tabs"]
        if "tabs_id" in env.temp_data:
            env.temp_data["tabs_id"].append(
                self.options.get("prefix", token_urlsafe())
            )
        else:
            env.temp_data["tabs_id"] = [
                self.options.get("prefix", token_urlsafe())
            ]

        if "tab_id" in env.temp_data:
            env.temp_data["tab_id"].append(0)
        else:
            env.temp_data["tab_id"] = [0]

        if "toc" in self.options:
            env.temp_data["tab_toc"] = True
            node["classes"].append("nxt_toc")
        else:
            env.temp_data["tab_toc"] = False

        self.state.nested_parse(self.content, self.content_offset, node)

        env.temp_data["tabs_id"].pop()
        env.temp_data["tab_id"].pop()

        return [node]


class NxtTabDirective(Directive):
    """Handles the tab directive, adding an nxt_tab container node."""

    has_content = True

    def run(self) -> List[Node]:
        self.assert_has_content()
        env = self.state.document.settings.env

        tab_head = nxt_tab_head()
        tab_head += nodes.Text(self.content[0])

        tab_head.tabs_id = env.temp_data["tabs_id"][-1]
        tab_head.checked = (
            "checked" if env.temp_data["tab_id"][-1] == 0 else ""
        )
        tab_head.tab_id = "{}_{}".format(
            env.temp_data["tabs_id"][-1], env.temp_data["tab_id"][-1]
        )
        tab_head.rstref_id = "{}-{}-{}".format(
            env.docname,
            env.temp_data["tabs_id"][-1],
            nxt_make_id(self.content[0]),
        )
        tab_head.anchor_id = tab_head.rstref_id.split("-", 1)[1]
        tab_head.tab_toc = env.temp_data["tab_toc"]

        env.temp_data["tab_id"][-1] += 1

        text = "\n".join(self.content)
        tab_body = nxt_tab_body(text)
        self.state.nested_parse(
            self.content[2:], self.content_offset, tab_body
        )

        return [tab_head, tab_body]


def nxt_register_nodes_as_labels(
    app: Sphinx, document: nodes.document
) -> None:
    """Registers tabs and details as anchors for ref directives."""

    docname = app.env.docname
    labels = app.env.domaindata["std"]["labels"]
    anonlabels = app.env.domaindata["std"]["anonlabels"]

    for cls in (nxt_tab_head, nxt_details):
        for node in document.traverse(cls):
            if node.rstref_id in labels:
                logging.getLogger(__name__).warning(
                    __("duplicate label %s, other instance in %s"),
                    node.rstref_id,
                    app.env.doc2path(labels[node.rstref_id][0]),
                    location=node,
                )
            anonlabels[node.rstref_id] = docname, node.anchor_id
            labels[node.rstref_id] = docname, node.anchor_id, node.astext()


def nxt_write_rss(app: Sphinx, error: Exception) -> None:
    """Writes the .rss file."""
    cfg = app.config

    lines = [
        f"""<?xml version="1.0" encoding="utf-8"?>
        <rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
        <channel>
        <atom:link href="{cfg.html_baseurl}{cfg.html_context['nxt_rss_file']}"
              rel="self" type="application/rss+xml" />
        <title>{cfg.project}</title>
        <link>{cfg.html_baseurl}</link>
        <copyright>{cfg.author}, {cfg.copyright}</copyright>
        <description>{cfg.project} news and articles</description>
        <generator>nxt-newsfeed</generator>"""
    ]

    sorted_entries = sorted(
        NewsEntryDirective.items, key=lambda x: x["date"], reverse=True
    )

    for e in sorted_entries:
        date = datetime.fromisoformat(e["date"])
        # FIXME: Remove this after posting an article in 2024.
        #
        # Our previous code allowed the local system timezone to influence how
        # timestamps were serialized into <pubDate> fields.
        #
        # We need to fix that, but we also need to continue generating the old
        # values for old posts. Otherwise we'd confuse RSS feed readers.
        #
        # We can reliably reproduce the old values by:
        #
        #    1. Starting with a timezone-naive datetime
        #    2. Marking it as being in the Europe/London timezone
        #    3. Shifting it into UTC
        #    4. Stripping the timezone info, so it is again timezone-naive
        #
        # The last step produces RFC 2822 timestamps with the "-0000" offset,
        # instead of timezone-aware UTC "+0000" offset.
        #
        # We can remove this hack once we've published a few posts in 2024.
        if date.year < 2024:
            date = (
                date.replace(tzinfo=ZoneInfo("Europe/London"))
                .astimezone(timezone.utc)
                .replace(tzinfo=None)
            )
        date = format_datetime(date)
        lines.append(
            f"""<item><title>{e['title']}</title>
            <author>{e['email']} ({e['author']})</author>
            <pubDate>{date}</pubDate>"""
        )

        if "url" in e:  # adjusting for local links
            url = ("" if "://" in e["url"] else cfg.html_baseurl) + e["url"]
            lines.append(f"<link>{url}</link><guid>{url}</guid>")

        if "description" in e:
            lines.append(f'<description>{e["description"]}</description>')

        lines.append("</item>")

    lines.append("</channel></rss>")

    dom = xml.dom.minidom.parseString(re.sub("&", "&amp;", "".join(lines)))
    with open(
        app.outdir + "/" + cfg.html_context["nxt_rss_file"],
        "w",
        encoding="utf-8",
    ) as f:
        f.write(dom.toprettyxml())


def setup(app: Sphinx) -> None:
    """Connects the extension to the app."""
    pygments.lexers.data.JsonLexer.constants = set(
        "truefalsenullxphi_0123456789"
    )
    # Adding 'nxt_ph_N' and 'nxt_hint_N' to the charset allows
    # NxtHightlighter.highlight_block() to run w/o resetting lexer to 'none'
    # when constants such as false and true are commented with nxt_ directives.

    app.add_directive("nxt_details", NxtDetailsDirective)
    app.add_directive("tabs", NxtTabsDirective)
    app.add_directive("tab", NxtTabDirective)
    app.add_directive("nxt_news_entry", NewsEntryDirective)
    app.add_directive("nxt_news_recent", NewsRecentDirective)

    app.add_env_collector(NxtCollector)
    app.add_builder(NxtBuilder)
    app.set_translator("nxt_html", NxtTranslator)

    app.connect("doctree-read", nxt_register_nodes_as_labels)
    app.connect("build-finished", nxt_write_rss)

    roles.register_canonical_role("nxt_hint", nxt_hint_role_fn)
