"""
Copyright (C) 2020-2021, NGINX, Inc.

Sphinx extension to add ReadTheDocs-style "Edit on GitHub" links to the
sidebar.  Loosely based on https://github.com/astropy/astropy/pull/347

Usage:

layout.html:
    {% if edit_on_github_url %}
        <div class="nxt_github_link">
            <a href="{{ edit_on_github_url }}"><div></div>Improve this page</a>
        </div>
    {% endif %}
"""

import os
import warnings


def get_github_url(app, view, path):
    """Forms a URL of the corresponding GitHub page."""

    project = app.config.edit_on_github_project
    branch = app.config.edit_on_github_branch
    return f'https://github.com/{project}/{view}/{branch}/source/{path}'


def html_page_context(app, pagename, templatename, context, doctree):
    """Adds GitHub URL for the page to the page context."""

    if templatename != 'page.html':
        return

    if not app.config.edit_on_github_project:
        warnings.warn("edit_on_github_project not specified")
        return

    path = os.path.relpath(doctree.get('source'), app.builder.srcdir)
    context['edit_on_github_url'] = get_github_url(app, 'edit', path)


def setup(app):
    """Connects the extension to the app."""

    app.add_config_value('edit_on_github_project', '', True)
    app.add_config_value('edit_on_github_branch', 'master', True)

    app.connect('html-page-context', html_page_context)
