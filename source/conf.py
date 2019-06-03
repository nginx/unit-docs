# -*- coding: utf-8 -*-

import os, sys

highlight_language = 'json'

html_theme = 'theme'
html_theme_path = ["."]
html_use_index = False
html_add_permalinks = u'§'

html_extra_path = ['robots.txt', 'CHANGES.txt']

exclude_patterns = ['include']

sys.path.append(os.path.abspath('./exts'))
extensions = ['subs']
