:orphan:

####################
Unit 1.26.1 Released
####################

Hi,

I'm glad to announce a new release of NGINX Unit.

This is a minor bugfix release that aims to eliminate some annoying regressions
revealed after the :doc:`release of Unit 1.26.0 <unit-1.26.0-released>` two
weeks ago.

Notably, the shared `OPcache
<https://www.php.net/manual/en/book.opcache.php>`__ implementation in that
release required introducing some major architectural changes, but our
functional tests didn't catch some regressions caused by these changes.  Still,
thanks to our active community, the issues were reported shortly after the
release, and now we can provide an updated version.  We will also improve our
functional testing to avoid such regressions in the future.

The most painful and visible one was that sometimes Unit daemon couldn't
completely exit, leaving some zombie processes.  However, the second attempt to
stop it always succeeded.  Also, some `DragonFly BSD
<https://www.dragonflybsd.org>`__ kernel interfaces are seemingly broken,
preventing the Unit daemon from functioning, so we disabled their use when
compiling for DragonFly BSD.

.. code-block:: none

   Changes with Unit 1.26.1                                         02 Dec 2021

   - Bugfix: occasionally, the Unit daemon was unable to fully terminate;
     the bug had appeared in 1.26.0.

   - Bugfix: a prototype process could crash on an application process
     exit; the bug had appeared in 1.26.0.

   - Bugfix: the router process crashed on reconfiguration if "access_log"
     was configured without listeners.

   - Bugfix: a segmentation fault occurred in the PHP module if chdir() or
     fastcgi_finish_request() was called in the OPcache preloading script.

   - Bugfix: fatal errors on DragonFly BSD; the bug had appeared in
     1.26.0.

To know more about the bunch of changes introduced in Unit 1.26 and the roadmap
for 1.27, please see the previous announcement:
https://mailman.nginx.org/pipermail/unit/2021-November/000288.html

Thank you again for keeping your finger on the pulse, reporting issues and
submitting feature requests via our GitHub issue tracker:
https://github.com/nginx/unit/issues

Stay tuned!

wbr, Valentin V. Bartenev
