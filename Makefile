SPHINX		?= sphinx-build
SERVER		?= python3 -mhttp.server

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
	-o -name '*.txt' \)


.PHONY: site serve check clean deploy do_gzip

site: $(BUILDDIR)
	@$(SPHINX) -b dirhtml source "$(BUILDDIR)"

$(BUILDDIR):
	mkdir "$(BUILDDIR)"

serve: site
	@cd "$(BUILDDIR)" && $(SERVER)

check:
	@$(SPHINX) -b linkcheck -d "$(BUILDDIR)/.doctrees" source .

clean:
	rm -rf $(BUILDDIR)

deploy: site
	$(eval TMP := $(shell mktemp -d))
	rsync -rv $(EXCLUDE) "$(BUILDDIR)/" "$(TMP)"
	$(MINIFY) -vr "$(TMP)" -o "$(TMP)"
	rsync -rcv --delete --exclude='*.gz' "$(TMP)/" "$(DEPLOYDIR)"
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
