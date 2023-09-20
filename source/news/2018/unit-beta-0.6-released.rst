:orphan:

######################
Unit Beta 0.6 Released
######################

Hello,

I'm glad to announce a new beta of NGINX Unit with advanced process management
and Perl/PSGI support.  One of the Perl applications that has been tested is
Bugzilla and it run with Unit flawlessly.

Here is a changes log of 0.5 and 0.6 versions:

.. code-block:: none

   Changes with Unit 0.5                                            08 Feb 2018

       *) Change: the "workers" application option was removed, the "processes"
          application option should be used instead.

       *) Feature: the "processes" application option with prefork and dynamic
          process management support.

       *) Feature: Perl application module.

       *) Bugfix: in reading client request body; the bug had appeared in 0.3.

       *) Bugfix: some Python applications might not work due to missing
          "wsgi.errors" environ variable.

       *) Bugfix: HTTP chunked responses might be encoded incorrectly on 32-bit
          platforms.

       *) Bugfix: infinite looping in HTTP parser.

       *) Bugfix: segmentation fault in router.


   Changes with Unit 0.6                                            09 Feb 2018

       *) Bugfix: the main process died when the "type" application option
          contained version; the bug had appeared in 0.5.


The announce of 0.5 has been skipped as a serious regression was found right
after the packages were built and published.

Besides the precompiled packages for CentOS, RHEL, Debian, Ubuntu, and Amazon
Linux, now you can try Unit using official Docker containers.  See the links
below for details:

- Packages:  https://unit.nginx.org/installation/#precompiled-packages
- Docker:    https://hub.docker.com/r/nginx/unit/tags/

wbr, Valentin V. Bartenev
