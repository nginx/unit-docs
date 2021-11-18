SPHINX		?= sphinx-build
SERVER		?= python3 -mhttp.server

SITEMAP		?= python3 sitemaps.py
URL		?= https://unit.nginx.org
GOOGLE		?= https://www.google.com/webmasters/tools/ping?sitemap=
BING		?= http://www.bing.com/ping?sitemap=

# https://github.com/tdewolff/minify/tree/master/cmd/minify
MINIFY		?= minify

BUILDDIR	?= build
DEPLOYDIR	?= deploy

EXCLUDE = \
	--exclude='.*' \
	--exclude='*.inv' \
	--exclude='*/pygments.css' \
	--exclude='/contents' \
	--exclude='searchindex.js' \
	--exclude='/search'

COMPRESS = -size +1000c \
	\( -name '*.html' \
	-o -name '*.css' \
	-o -name '*.js' \
	-o -name '*.svg' \
	-o -name '*.txt' \
	-o -name '*.xml' \)


.PHONY: site serve check clean deploy do_gzip

site: $(BUILDDIR)
	@$(SPHINX) -E -b nxt_html source "$(BUILDDIR)"

$(BUILDDIR):
	mkdir "$(BUILDDIR)"

serve: site
	@cd "$(BUILDDIR)" && $(SERVER)

check:
	@$(SPHINX) -b linkcheck -d "$(BUILDDIR)/.doctrees" source .

clean:
	rm -rf $(BUILDDIR)

ping:
	curl "$(GOOGLE)$(URL)/sitemap.xml"
	curl "$(BING)$(URL)/sitemap.xml"

deploy: site
	$(eval TMP := $(shell mktemp -d))
	mkdir "$(BUILDDIR)"/keys/
	curl https://nginx.org/keys/nginx_signing.key \
		| tee "$(BUILDDIR)"/keys/nginx_signing.key | gpg --dearmor \
		| tee "$(BUILDDIR)"/keys/nginx-keyring.gpg > /dev/null
	gpg --dry-run --quiet --import --import-options import-show \
		"$(BUILDDIR)"/keys/nginx-keyring.gpg
	rsync -rv $(EXCLUDE) "$(BUILDDIR)/" "$(TMP)"
	$(MINIFY) -vr "$(TMP)" -o "$(TMP)"
	$(MINIFY) -v --type html "$(TMP)/go" -o "$(TMP)/go"
	rsync -rcv --delete --exclude='*.gz' --exclude='/sitemap.xml' \
		"$(TMP)/" "$(DEPLOYDIR)"
	$(SITEMAP) "$(URL)" index.html "$(DEPLOYDIR)" -e sitemapexclude.txt \
		> "$(TMP)/sitemap.xml"
	$(MINIFY) -v "$(TMP)/sitemap.xml" -o "$(TMP)/sitemap.xml"
	rsync -rcv "$(TMP)/sitemap.xml" "$(DEPLOYDIR)"
	-rm -rf "$(TMP)"
	$(MAKE) do_gzip
	chmod -R g=u "$(DEPLOYDIR)"

do_gzip: $(addsuffix .gz, $(shell find "$(DEPLOYDIR)" $(COMPRESS) 2>/dev/null))

	find "$(DEPLOYDIR)" -type f ! -name '*.gz' \
		-exec test \! -e {}.gz \; -print

	find "$(DEPLOYDIR)" -type f -name '*.gz' | \
		while read f ; do test -e "$${f%.gz}" || rm -fv "$$f" ; done

$(DEPLOYDIR)/%.gz: $(DEPLOYDIR)/%
	rm -f $<.gz
	zopfli -c $< > $<.gz
	touch -r $< $<.gz
