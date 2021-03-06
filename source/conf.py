# -*- coding: utf-8 -*-

import os, sys

project = 'NGINX Unit'
author = 'NGINX, Inc.'
copyright = '2017-2021'
version = '1.23.0'
release_date = 'March 25, 2021'
release = version

highlight_language = 'json'

html_theme = 'theme'
html_theme_path = ["."]
html_use_index = False
html_add_permalinks = u'§'
html_baseurl = 'https://unit.nginx.org/'
html_extra_path = ['robots.txt', 'CHANGES.txt', 'go']
html_context = {
    'release_date'  : release_date,
    'author'        : author,
    'nxt_baseurl'   : html_baseurl
}

rst_prolog = """
.. |release_date| replace:: {}
""".format(release_date)

edit_on_github_project = 'nginx/unit-docs'
edit_on_github_branch = 'master'

exclude_patterns = ['include']
suppress_warnings = ['misc.highlighting_failure']

sys.path.append(os.path.abspath('./exts'))
extensions = ['inline', 'nxt', 'subs', 'github']
