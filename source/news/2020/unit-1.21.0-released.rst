:orphan:

####################
Unit 1.21.0 Released
####################

Hi,

I'm glad to announce a new release of NGINX Unit.

Our two previous releases were thoroughly packed with new features and
capabilities, but Unit 1.21.0 isn't an exception either.  This is our
third big release in a row, with only six weeks since the previous one!

Perhaps, the most notable feature of this release is the support for
multithreaded request handling in application processes.  Now, you can
fine-tune the number of threads used for request handling in each
application process; this improves scaling and optimize memory usage.

As a result, your apps can use a combination of multiple processes and
multiple threads per each process for truly dynamic scaling; the feature
is available for any Java, Python, Perl, or Ruby apps out of the box
without any need to update their code.

Moreover, if you make use of ASGI support in Unit (introduced in the
:doc:`previous release <unit-1.20.0-released>`), each thread of each process of
your application can run asynchronously.  Pretty neat, huh?

To configure the number of threads per process, use the "threads" option
of the application object: https://unit.nginx.org/configuration/#applications

Yet another cool feature is the long-awaited support for regular expressions.
In Unit, they enable granular request filtering and routing via our compound
matching rules; now, with PCRE syntax available, your request matching
capabilities are limited only by your imagination.  For details and examples,
see our documentation: https://unit.nginx.org/configuration/#routes

.. code-block:: none

   Changes with Unit 1.21.0                                         19 Nov 2020

       *) Change: procfs is mounted by default for all languages when "rootfs"
          isolation is used.

       *) Change: any characters valid according to RFC 7230 are now allowed in
          HTTP header field names.

       *) Change: HTTP header fields with underscores ("_") are now discarded
          from requests by default.

       *) Feature: optional multithreaded request processing for Java, Python,
          Perl, and Ruby apps.

       *) Feature: regular expressions in route matching patterns.

       *) Feature: compatibility with Python 3.9.

       *) Feature: the Python module now supports ASGI 2.0 legacy applications.

       *) Feature: the "protocol" option in Python applications aids choice
          between ASGI and WSGI.

       *) Feature: the fastcgi_finish_request() PHP function that finalizes
          request processing and continues code execution without holding onto
          the client connection.

       *) Feature: the "discard_unsafe_fields" HTTP option that enables
          discarding request header fields with irregular (but still valid)
          characters in the field name.

       *) Feature: the "procfs" and "tmpfs" automount isolation options to
          disable automatic mounting of eponymous filesystems.

       *) Bugfix: the router process could crash when running Go applications
          under high load; the bug had appeared in 1.19.0.

       *) Bugfix: some language dependencies could remain mounted after using
          "rootfs" isolation.

       *) Bugfix: various compatibility issues in Java applications.

       *) Bugfix: the Java module built with the musl C library couldn't run
          applications that use "rootfs" isolation.


Also, packages for Ubuntu 20.10 "Groovy" are available in our repositories:
https://unit.nginx.org/installation/#ubuntu-2010

Thanks to Sergey Osokin, the FreeBSD port of Unit now provides an almost
exhaustive set of language modules: https://www.freshports.org/www/unit/

We encourage you to follow our roadmap on GitHub, where your ideas and requests
are always more than welcome: https://github.com/orgs/nginx/projects/1

Stay tuned!

wbr, Valentin V. Bartenev
