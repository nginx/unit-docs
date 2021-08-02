#!/usr/bin/env python3

# Copyright (C) NGINX, Inc.
# Script generates sitemap.xml for https://unit.nginx.org, with an option to
# exclude some globs specified in a file
# Reference: https://www.sitemaps.org/protocol.html
# Usage: sitemaps.py <base URL> <index.html> <staging directory> > sitemap.xml

def main():

    import argparse, fnmatch, os, sys
    from datetime import datetime

    parser = argparse.ArgumentParser(
        description="Script generates sitemap.xml for https://unit.nginx.org")
    parser.add_argument("base_url", nargs="?", help="website's base URL")
    parser.add_argument("index_file", nargs="?",
        help="index file name, e. g. index.html")
    parser.add_argument("base_dir", nargs="?",
        help="base website directory to generate the sitemap for")
    parser.add_argument("-e", metavar="FNAME", nargs="?",
        help="file of globs to exclude")
    args = parser.parse_args()

    base_url = args.base_url.strip("/")
    base_dir = os.path.abspath(args.base_dir)
    if args.e:
        with open(args.e, "r") as f:
            globs = [base_dir + "/" + l.strip() for l in f.readlines()]

    print("""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">""")

    for curr_dir, _, files in os.walk(base_dir):
        if args.index_file not in files:
            continue

        index_file_name = curr_dir + "/" + args.index_file
        if args.e and any(fnmatch.fnmatch(index_file_name, g) for g in globs):
            print("Sitemap: skipping glob match: {0}".format(index_file_name),
                file=sys.stderr)
            continue
        index_file_stat = os.stat(index_file_name)

        loc = curr_dir.replace(base_dir, base_url) + "/"
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
