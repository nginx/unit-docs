SPHINX		= sphinx-build
SERVER		= python3 -mhttp.server
SOURCEDIR	= source
BUILDDIR	= build
DEPLOYDIR	= deploy

EXCLUDE = \
	--exclude='.*' \
	--exclude='*.inv' \
	--exclude='*.gz' \
	--exclude='*/pygments.css' \
	--exclude='/contents'

COMPRESS = \
	-name '*.html' \
	-o -name '*.css' \
	-o -name '*.js' \
	-o -name '*.svg' \
	-o -name '*.txt'


.PHONY: site serve check clean deploy do_gzip

site: $(BUILDDIR)
	@$(SPHINX) -b dirhtml "$(SOURCEDIR)" "$(BUILDDIR)"

$(BUILDDIR):
	mkdir "$(BUILDDIR)"

serve: site
	@cd "$(BUILDDIR)" && $(SERVER)

check:
	@$(SPHINX) -b linkcheck "$(SOURCEDIR)" .

clean:
	rm -rf $(BUILDDIR)

deploy: site
	rsync -rcv --delete $(EXCLUDE) "$(BUILDDIR)/" "$(DEPLOYDIR)"
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
