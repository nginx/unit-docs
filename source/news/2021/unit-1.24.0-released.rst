:orphan:

####################
Unit 1.24.0 Released
####################

Hi,

I'm glad to announce a new release of NGINX Unit.

This one is full of shiny new features.  But before I dive into the details,
let me introduce our new developers without whom this release wouldn't be so
feature-rich.  Please, welcome Zhidao Hong (洪志道) and Oisín Canty.

Zhidao has already been contributing to various nginx open-source projects for
years as a community member, and I'm very excited to finally have him on board.

Oisín is a university student who's very interested in Unit; he joined our dev
team as an intern and already shown solid coding skills, curiosity, and
attention to details, which is so important to our project.  Good job!

Now, back to the features.  I'd like to highlight the first of our improvements
in serving static media assets.


*******************
MIME Type Filtering
*******************

Now, you can restrict file serving by MIME type:

.. code-block:: json

   {
       "share": "/www/data",
       "types": [ "image/*", "video/*" ]
   }

The configuration above allows only files with various video and image
extensions, but all other requests will return status code 403.

In particular, this goes well with the :samp:`fallback` option that performs
another action if the :samp:`share` returns a 40x error:

.. code-block:: json

   {
       "share": "/www/data",
       "types": [ "!application/x-httpd-php" ],

       "fallback": {
           "pass": "applications/php"
       }
   }

Here, all requests to existing files other than :file:`.php` will be served as
static content while the rest will be passed to a PHP application.

More examples and documentation snippets are available here:
https://unit.nginx.org/configuration/#mime-filtering


**************************************************
Chrooting and Path Restrictions When Serving Files
**************************************************

As we take security seriously, now Unit introduces the ability to chroot
not only its application processes but also the static files it serves on
a per-request basis.  Additionally, you can restrict traversal of mounting
points and symbolic link resolution:

.. code-block:: json

   {
       "share": "/www/data/static/",
       "chroot": "/www/data/",
       "follow_symlinks": false,
       "traverse_mounts": false
   }

See here for more information:
https://unit.nginx.org/configuration/#path-restrictions

For details of Unit application process isolation abilities:
https://unit.nginx.org/configuration/#process-isolation


Other notable features unrelated to static file serving:

- Multiple WSGI/ASGI Python entry points per process.  It allows loading
  multiple modules or app entry points into a single Python process, choosing
  between them when handling requests with the full power of Unit's routes
  system.

  See here for Python's :samp:`targets` object description:
  https://unit.nginx.org/configuration/#configuration-python-targets

  And here, more info about Unit's internal routing:
  https://unit.nginx.org/configuration/#routes

- Automatic overloading of :program:`http` and :program:`websocket` modules in
  Node.js.  Now you can run Node.js apps on Unit without touching their
  sources: https://unit.nginx.org/configuration/#node-js

- Applying OpenSSL configuration commands

  Finally, you can control various TLS settings via OpenSSL's generic
  configuration interface with all the dynamic power of Unit:
  https://unit.nginx.org/configuration/#ssl-tls-configuration

The full changelog for the release:

.. code-block:: none

   Changes with Unit 1.24.0                                         27 May 2021

       *) Change: PHP added to the default MIME type list.

       *) Feature: arbitrary configuration of TLS connections via OpenSSL
          commands.

       *) Feature: the ability to limit static file serving by MIME types.

       *) Feature: support for chrooting, rejecting symlinks, and rejecting
          mount point traversal on a per-request basis when serving static
          files.

       *) Feature: a loader for automatically overriding the "http" and
          "websocket" modules in Node.js.

       *) Feature: multiple "targets" in Python applications.

       *) Feature: compatibility with Ruby 3.0.

       *) Bugfix: the router process could crash while closing a TLS
          connection.

       *) Bugfix: a segmentation fault might have occurred in the PHP module if
          fastcgi_finish_request() was used with the "auto_globals_jit" option
          enabled.


That's all for today, but even more exciting features are poised for the
upcoming releases:

- statistics API
- process control API
- variables from regexp captures in the :samp:`match` object
- simple request rewrites using variables
- variables support in static file serving options
- ability to override client IP from the X-Forwarded-For header
- TLS sessions cache and tickets

Also, please check our GitHub to follow the development and discuss new
features: https://github.com/nginx/unit

Stay tuned!

wbr, Valentin V. Bartenev
