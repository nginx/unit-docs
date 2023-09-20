:orphan:

###################
Unit 1.9.0 Released
###################

Hi,

I'm glad to announce a new release of NGINX Unit.

In this release, we continue improving routing capabilities for more advanced
and precise request matching.  Besides that, the control API was extended with
POST operations to simplify array manipulation in configuration.

Please check the documentation about new features:

- Matching rules: https://unit.nginx.org/configuration/#matching-conditions
- API operations: https://unit.nginx.org/controlapi/

If you prefer to perceive information visually, here's a recording of NGINX
Meetup that gives a good overview of dynamic application routing, although
doesn't discuss new features from this release:
https://www.youtube.com/watch?v=5O4TjbbxTxw

Also, a number of annoying bugs were fixed; thanks to your feedback,
the Node.js module now works fine with more applications.


.. code-block:: none

   Changes with Unit 1.9.0                                          30 May 2019

       *) Feature: request routing by arguments, headers, and cookies.

       *) Feature: route matching patterns allow a wildcard in the middle.

       *) Feature: POST operation for appending elements to arrays in
          configuration.

       *) Feature: support for changing credentials using CAP_SETUID and
          CAP_SETGID capabilities on Linux without running main process as
          privileged user.

       *) Bugfix: memory leak in the router process might have happened when a
          client prematurely closed the connection.

       *) Bugfix: applying a large configuration might have failed.

       *) Bugfix: PUT and DELETE operations on array elements in configuration
          did not work.

       *) Bugfix: request schema in applications did not reflect TLS
          connections.

       *) Bugfix: restored compatibility with Node.js applications that use
          ServerResponse._implicitHeader() function; the bug had appeared in
          1.7.

       *) Bugfix: various compatibility issues with Node.js applications.


With this release, packages for Ubuntu 19.04 "disco" are also available.  See
the website for a full list of available repositories:
https://unit.nginx.org/installation/

Meanwhile, we continue working on WebSocket support.  It's almost ready and
has great chances to be included in the next release for Node.js and Java
modules.

Work on proxying and static files serving is also in progress; this will
take a bit more time.

wbr, Valentin V. Bartenev
