#!/usr/bin/env python3

# Copyright (C) NGINX, Inc.
# Script generates sitemap.xml for https://unit.nginx.org
# Reference: https://www.sitemaps.org/protocol.html
# Usage: sitemaps.py <base URL> <index.html> <staging directory> > sitemap.xml

def main():

    import os, sys
    from datetime import datetime

    base_url = sys.argv[1].strip("/")
    index_file = sys.argv[2]
    base_dir = os.path.abspath(sys.argv[3])

    print("""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">""")

    for curr_dir, _, files in os.walk(base_dir):
        if index_file not in files:
            continue

        loc = curr_dir.replace(base_dir, base_url) + "/"

        index_file_stat = os.stat(curr_dir + "/" + index_file)
        dt = datetime.utcfromtimestamp(index_file_stat.st_mtime)
        lastmod = dt.strftime("%Y-%m-%dT%H:%M:%SZ")

        print("Sitemap: {0} ({1})".format(loc, lastmod), file=sys.stderr)

        print("""    <url>
        <loc>{0}</loc>
        <lastmod>{1}</lastmod>
    </url>""".format(loc, lastmod))

    print("</urlset>")


if __name__ == "__main__":
    main()
