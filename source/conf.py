# -*- coding: utf-8 -*-

import os, sys

project = 'NGINX Unit'
author = 'NGINX, Inc.'
copyright = '2017-2020'
version = '1.17.0'
release = version

html_context = {
    'author' : author
}

highlight_language = 'json'

html_theme = 'theme'
html_theme_path = ["."]
html_use_index = False
html_add_permalinks = u'§'

html_extra_path = ['robots.txt', 'CHANGES.txt', 'go']

exclude_patterns = ['include']

sys.path.append(os.path.abspath('./exts'))
extensions = ['inline', 'nxt', 'subs']
