:orphan:

####################
Unit 1.10.0 Released
####################

Hi,

I'm glad to announce a new release of NGINX Unit.

This release includes a number of improvements in various language modules and,
finally, basic handling of incoming WebSocket connections, currently only for
Node.js.  Next in line to obtain WebSocket support is the Java module; it's
almost ready but requires some polishing.

To handle WebSocket connections in your Node.js app via Unit, use the server
object from the :program:`unit-http` module instead of the default one:

.. code-block:: javascript

   var webSocketServer = require('unit-http/websocket').server;

Another interesting and long-awaited feature in this release is the splitting
of :envvar:`PATH_INFO` in the PHP module.  Now, Unit can properly handle
requests like :samp:`/app.php/some/path?some=args`, which are often used to
implement "user-friendly" URLs in PHP applications.


.. code-block:: none

   Changes with Unit 1.10.0                                         22 Aug 2019

       *) Change: matching of cookies in routes made case sensitive.

       *) Change: decreased log level of common errors when clients close
          connections.

       *) Change: removed the Perl module's "--include=" ./configure option.

       *) Feature: built-in WebSocket server implementation for Node.js module.

       *) Feature: splitting PATH_INFO from request URI in PHP module.

       *) Feature: request routing by scheme (HTTP or HTTPS).

       *) Feature: support for multipart requests body in Java module.

       *) Feature: improved API compatibility with Node.js 11.10 or later.

       *) Bugfix: reconfiguration failed if "listeners" or "applications"
          objects were missing.

       *) Bugfix: applying a large configuration might have failed.


Please welcome our new junior developer, Axel Duch.  For this release, he
implemented scheme matching in request routing; now, he works to further extend
the request routing capabilities with source and destination address matching.

In parallel, Tiago Natel de Moura, who also joined the development recently,
has achieved significant progress in the effort to add various process
isolation features to Unit.  You can follow his recent work on Linux namespaces
support in the following pull request: https://github.com/nginx/unit/pull/289

See also his email about the feature:
https://mailman.nginx.org/pipermail/nginx/2019-August/058321.html

In the meantime, we are about to finish the first round of adding basic
support for serving static media assets and proxying in Unit.

Stay tuned!

wbr, Valentin V. Bartenev
