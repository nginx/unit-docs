:orphan:

###################
Unit 1.8.0 Released
###################

Hi,

I'm glad to announce a new release of NGINX Unit.  This release contains two
big features that we have been working on diligently during the last months.

Some of you wonder why listener sockets are separated from applications in
Unit configuration API.  That was done intentionally to introduce advanced
routing between sockets and applications in the future, and this future is
finally happening.

Now you will be able to specify quite handy rules that will direct your
requests to a particular application depending on various parameters.

Please take a glance at the routing documentation:
https://unit.nginx.org/configuration/#routes

Currently, it only supports internal routing by Host, URI, and method request
parameters.  In the following releases, available options are going to be
expanded to allow matching arbitrary headers, arguments, cookies, source
and destination addresses.  We will also add regular expression patterns.

In future releases, these routing abilities will be handy for issuing redirects
and changing configuration on a per route basis.

As usual with Unit, all routing changes are fully dynamic and gracefully done
through its control API.

The second feature is even bigger.  We've merged the code that Maxim Romanov
developed in a separate branch last year to support running applications
leveraging certain technology described in the Java(tm) Servlet 3.1 (JSR-340)
specification.  This module is a **BETA** release as the module is untested and
presumed incompatible with the JSR-340 specification.

Now everybody can easily install it from our packages, try it with their Java
applications, and leave us feedback.  If you're a Jira user, please use this
HowTo: https://unit.nginx.org/howto/jira/

More documentation is available in :doc:`../../installation` and
:doc:`../../configuration/index` sections.

We intend to use our open-development process to refine and improve the
software and to eventually test and certify the software's compatibility
with the JSR-340 specification.  Unless and until the software has been
tested and certified, you should not deploy the software in support of
deploying or providing Java Servlet 3.1 applications.  You should instead
deploy production applications on pre-built binaries that have been tested
and certified to meet the JSR-340 compatibility requirements such as
certified binaries published for the JSR-340 reference implementation
available at https://javaee.github.io/glassfish/.

.. note::

   Java is a registered trademark of Oracle and/or its affiliates.


.. code-block:: none

   Changes with Unit 1.8.0                                          01 Mar 2019

       *) Change: now three numbers are always used for versioning: major,
          minor, and patch versions.

       *) Change: now QUERY_STRING is always defined even if the request does
          not include the query component.

       *) Feature: basic internal request routing by Host, URI, and method.

       *) Feature: experimental support for Java Servlet Containers.

       *) Bugfix: segmentation fault might have occurred in the router process.

       *) Bugfix: various potential memory leaks.

       *) Bugfix: TLS connections might have stalled.

       *) Bugfix: some Perl applications might have failed to send the response
          body.

       *) Bugfix: some compilers with specific flags might have produced
          non-functioning builds; the bug had appeared in 1.5.

       *) Bugfix: Node.js package had wrong version number when installed from
          sources.


Our versioning scheme is actually always supposed to have the third version
number, but the ".0" patch version was hidden.  In order to avoid any possible
confusion, it was decided to always show ".0" in version numbers.

For those who are interested in running Unit on CentOS, Fedora, and RHEL
with latest versions of PHP, the corresponding packages are now available
in Remi's RPM repository:
https://unit.nginx.org/installation/#community-remisrpm

Many kudos to Remi Collet for collaboration.

Note also that our technical writer Artem Konev has recently added more HowTos
to the site about configuring various applications, including WordPress, Flask,
and Django-based ones: https://unit.nginx.org/howto/

He will continue discovering and writing instructions for other applications.
If you're interested in some specific use cases and applications, please don't
hesitate to leave a feature request on the documentation GitHub:
https://github.com/nginx/unit-docs/issues

In the following releases, we will continue improving routing capabilities
and support for Java applications.  Among other big features we're working
on are WebSockets support and serving static media assets.

Stay tuned, give feedback, and help us to create the best software ever.

wbr, Valentin V. Bartenev
