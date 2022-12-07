:orphan:

####################
Unit 1.27.0 Released
####################

We are pleased to announce NGINX Unit 1.27. This release brings a new level of
maturity to Unit for serving static assets.  We love using Unit as a
cloud-native web server, and this release brings some missing features to this
use case.

- Redirecting HTTP requests to HTTPS
- Configurable filename for path-only URIs


**********************************
Redirecting HTTP Requests to HTTPS
**********************************

Since we added TLS support and certificate management to Unit, we’ve been asked
to simplify redirecting plaintext HTTP requests to the TLS-enabled listener.
This is now possible by configuring the :samp:`location` value of a route
action to contain variables.  Indeed, a new variable, :samp:`$request_uri`, is
now available that contains the path-and-query parts of the original URI,
preserving any encoding needed by the browser.

A full example is provided below.

.. code-block:: json

   {
       "listeners": {
           "*:443": {
               "tls": {
                   "certificate": "example.com"
               },
               "pass": "routes"
           },
           "*:80": {
               "pass": "routes"
           }
        },

       "routes": [
           {
               "match": {
                   "scheme": "http"
               },
               "action": {
                   "return": 301,
                   "location": "https://${host}${request_uri}"
               }
           }
   }

This configuration enables Unit to listen on plaintext and TLS-enabled ports,
ensuring that any requests received on the plaintext port notify the browser to
resubmit on the TLS-enabled port.  See more details in the :ref:`documentation
<configuration-variables>`.


****************************************
Configurable Filename for Path-Only URIs
****************************************

While it is conventional for :file:`index.html` to represent the resource to be
served when a path-only URI is requested, i. e. one without a filename suffix,
this convention is rooted in history.  It comes from a time in the early 1990s
when HTTP was used exclusively to index and navigate HTML pages.

You can now use a different default filename by specifying the index for a
route action. A full example is provided below.

.. code-block:: json

   "routes": [
       {
           "match": {
               "uri": "/cms/*"
           },
           "action": {
               "share": "/var/cms$uri",
               "index": "default.html"
           }
       },
       {
           "action": {
               "share": "/var/www$uri"
           }
       }
   ]

This configuration enables Unit to serve :file:`default.html` for path-only
URIs made to :samp:`/cms/*` and the default :file:`index.html` filename for all
other path-only URIs.  See more details in the :ref:`documentation
<configuration-static>`.


**************
Full Changelog
**************

This release also includes a number of bug fixes.  The full changelog can be
seen below.

.. code-block:: none

   Changes with Unit 1.27.0                                         02 Jun 2022

       *) Feature: ability to specify a custom index file name when serving
          static files.

       *) Feature: variables support in the "location" option of the "return"
          action.

       *) Feature: support empty strings in the "location" option of the
          "return" action.

       *) Feature: added a new variable, $request_uri, that includes both the
          path and the query parts as per RFC 3986, sections 3-4.

       *) Feature: Ruby Rack environment parameter "SCRIPT_NAME" support.

       *) Feature: compatibility with GCC 12.

       *) Bugfix: Ruby Sinatra applications don't work without custom logging.

       *) Bugfix: the controller process could crash when a chain of more than
          four certificates was uploaded.

       *) Bugfix: some Perl applications failed to process the request body,
          notably with Plack.

       *) Bugfix: some Spring Boot applications failed to start, notably with
          Grails.

       *) Bugfix: incorrect Python protocol auto detection (ASGI or WSGI) for
          native callable object, notably with Falcon.

       *) Bugfix: ECMAScript modules did not work with the recent Node.js
          versions.


****************
Platform Updates
****************

Official packages are now available for the following Linux distributions:

- :ref:`Fedora 36 <installation-precomp-fedora>`
- :ref:`RHEL 9 <installation-precomp-rhel>`
- :ref:`Ubuntu 22.04 <installation-precomp-ubuntu>`

:ref:`Docker images <installation-docker>` have been updated to use the latest
language versions:

- Go 1.18
- PHP 8.1
- Ruby 3.1


**********************************
Community, Roadmap and Open Issues
**********************************

We continue to receive valuable bug reports and feature requests to our `GitHub
issues page <https://github.com/nginx/unit/issues>`__.  Although we are a small
team, every issue is reviewed, and we aim to respond within 2-3 days. Since the
last release, we refreshed our `GitHub README
<https://github.com/nginx/unit#readme>`__ with a super-quick-start guide and
added `contribution guidelines
<https://github.com/nginx/unit/blob/master/CONTRIBUTING.md>`__ to help you get
involved. For other discussions, please join us at the :samp:`#unit-users`
channel on the `NGINX Community Slack
<https://nginxcommunity.slack.com/join/shared_invite/zt-1aaa22w80-~_~wSMNyPxLPLp5xunOC7w>`__
or the `mailing list
<https://mailman.nginx.org/mailman3/lists/unit.nginx.org/>`__.

Although this release focuses on bug fixes and web server features, we have
advanced in several other projects that you can expect to see in forthcoming
releases this year:

- Custom logging (which brings lots of new variables and places you can use
  them)

- JavaScript-in-the-configuration (already available as an `experimental patch
  <https://github.com/nginx/unit/issues/652>`__)

- Statistics API to provide true observability for Unit

- CLI tool for easier command-line management of Unit

Finally, you may have noticed our new mascot, the "tribot" - we hope you like
it too! If you’re lucky, you can even find a `T-shirt
<https://swag-nginx.com/collections/tees/products/unit-tee-straight-fit>`__
at NGINX events this year!
