:orphan:

####################
Unit 1.20.0 Released
####################

Hi,

I'm glad to announce a new release of NGINX Unit.

It is yet another big release, featuring ASGI support for Python and a long list
of other improvements and bug fixes.

`ASGI 3.0 <https://asgi.readthedocs.io/en/latest/>`__ is a modern standardized
interface that enables writing natively asynchronous web applications making
use of the async/await feature available in latest versions of Python.  Now,
Unit fully supports it along with WSGI.  Even more, Unit automatically detects
the interface your Python app is using (ASGI or WSGI); the configuration
experience remains the same, though.  Also, our take on ASGI relies on Unit's
native high-perf capabilities to implement WebSockets.

To learn more about the new feature, check out the documentation:
https://unit.nginx.org/configuration/#python

In addition, we've prepared for you a couple of howtos on configuring popular
ASGI-based frameworks with Unit:

 - :doc:`Quart <../../howto/quart>` (note a simple WebSocket app)

 - :doc:`Starlette <../../howto/starlette>`

Finally, we've updated the Django howto to include the :ref:`ASGI alternative
<howto/django-interface-asgi>`.

.. code-block:: none

   Changes with Unit 1.20.0                                         08 Oct 2020

       *) Change: the PHP module is now initialized before chrooting; this
          enables loading all extensions from the host system.

       *) Change: AVIF and APNG image formats added to the default MIME type
          list.

       *) Change: functional tests migrated to the pytest framework.

       *) Feature: the Python module now fully supports applications that use
          the ASGI 3.0 server interface.

       *) Feature: the Python module now has a built-in WebSocket server
          implementation for applications, compatible with the HTTP & WebSocket
          ASGI Message Format 2.1 specification.

       *) Feature: automatic mounting of an isolated "/tmp" file system into
          chrooted application environments.

       *) Feature: the $host variable contains a normalized "Host" request
          value.

       *) Feature: the "callable" option sets Python application callable
          names.

       *) Feature: compatibility with PHP 8 RC 1. Thanks to Remi Collet.

       *) Feature: the "automount" option in the "isolation" object allows to
          turn off the automatic mounting of language module dependencies.

       *) Bugfix: "pass"-ing requests to upstreams from a route was broken; the
          bug had appeared in 1.19.0. Thanks to 洪志道 (Hong Zhi Dao) for
          discovering and fixing it.

       *) Bugfix: the router process could crash during reconfiguration.

       *) Bugfix: a memory leak occurring in the router process; the bug had
          appeared in 1.18.0.

       *) Bugfix: the "!" (non-empty) pattern was matched incorrectly; the bug
          had appeared in 1.19.0.

       *) Bugfix: fixed building on platforms without sendfile() support,
          notably NetBSD; the bug had appeared in 1.16.0.


I would very much like to highlight one of these changes.  Perhaps the least
noticeable, it is still important for the entire project: our functional tests
moved to a more feature-rich pytest framework from the native Python unittest
module that we've used previously.  This change should enable us to write more
sophisticated tests, boosting the overall quality of our future releases.

All in all, this is a genuinely solid release, but I'm still more excited
about the things yet to come.  Yes, even more great features are coming our
way very shortly!  Right now, we are tinkering with route matching patterns
to support regular expressions; working on keepalive connection caching;
adding multithreading to application modules; and finally, fabricating the
metrics API!

We encourage you to follow our roadmap on GitHub, where your ideas and requests
are always more than welcome: https://github.com/orgs/nginx/projects/1

Stay tuned!

wbr, Valentin V. Bartenev
