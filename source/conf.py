# -*- coding: utf-8 -*-

import os, sys

project = 'NGINX Unit'
author = 'NGINX, Inc.'
copyright = '2017-2025'
version = '1.34.2'
release_date = 'Feb 26, 2025'
release = version
needs_sphinx = '6.2'

highlight_language = 'json'

root_doc = 'contents'
html_theme = 'theme'
html_theme_path = ["."]
html_use_index = False
html_permalinks = True
html_permalinks_icon = u'§'
html_baseurl = 'https://unit.nginx.org/'
html_extra_path = ['robots.txt', 'CHANGES.txt', 'go', '404.html']
html_context = {
    'release_date'  : release_date,
    'author'        : author,
    'nxt_baseurl'   : html_baseurl,
    'nxt_rss_file'  : 'rss.xml'
}

rst_prolog = """
.. |release_date| replace:: {}
""".format(release_date)

edit_on_github_project = 'nginx/unit-docs'
edit_on_github_discussion = 'nginx/unit'
edit_on_github_branch = 'main'

exclude_patterns = ['include']
suppress_warnings = ['misc.highlighting_failure']

sys.path.append(os.path.abspath('./exts'))
extensions = ['inline', 'nxt', 'subs', 'github']
smartquotes_action = 'qe'
