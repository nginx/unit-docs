:orphan:

#################
Unit 1.5 Released
#################

Hello,

I'm glad to announce a new release of NGINX Unit.

This release introduces preliminary Node.js support.

Currently it lacks WebSockets, and there's a known problem with "promises".
However, our admirable users have already started testing it even before
the release: https://medium.com/house-organ/what-an-absolute-unit-a36851e72554

Now it even easier, since Node.js package is published in `npm
<https://www.npmjs.com>`__: https://www.npmjs.com/package/unit-http

So feel free to try it and give us feedback on:

 - Github: https://github.com/nginx/unit/issues
 - Mailing list: https://mailman.nginx.org/mailman/listinfo/unit

We will continue improving Node.js support in future releases.

Among other features we are working on right now: WebSockets, Java module,
flexible request routing, and serving of static media assets.

.. code-block:: none

   Changes with Unit 1.5                                            25 Oct 2018

       *) Change: the "type" of application object for Go was changed to
          "external".

       *) Feature: initial version of Node.js package with basic HTTP
          request-response support.

       *) Feature: compatibility with LibreSSL.

       *) Feature: --libdir and --incdir ./configure options to install libunit
          headers and static library.

       *) Bugfix: connection might be closed prematurely while sending
          response; the bug had appeared in 1.3.

       *) Bugfix: application processes might have stopped handling requests,
          producing "last message send failed: Resource temporarily
          unavailable" alerts in log; the bug had appeared in 1.4.

       *) Bugfix: Go applications didn't work when Unit was built with musl C
          library.


wbr, Valentin V. Bartenev
