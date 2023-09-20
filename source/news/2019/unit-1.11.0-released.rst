:orphan:

####################
Unit 1.11.0 Released
####################

Hi,

I'm glad to announce a new release of NGINX Unit.

This release improves the stability of Go applications and introduces
three major features:


***************************************
1. Ability to Serve Static Media Assets
***************************************

With this feature, we're only at the beginning of a long road to transform
Unit into a full-fledged web server, capable of acting as a building block
for web services of any kind.

In this release, the support for static files is very simple; you can only
specify the document root directory for Unit to handle:

.. code-block:: json

   {
       "share": "/data/www/example.com"
   }

Also, you can fine-tune MIME types:

.. code-block:: json

   {
       "mime_types": {
           "text/plain": [
               "readme",
               ".c",
               ".h"
           ],

           "application/msword": ".doc"
       }
   }

Use encoding to access object members with names that contain "/" characters
directly by their URI: :samp:`GET
/config/settings/http/static/mime_types/text%2Fplain/`

See the documentation for details:
https://unit.nginx.org/configuration/#static-files

In the upcoming releases, we'll extend this area of functionality to handle
more use cases in the most performant manner.

Unfortunately, basic proxying support did not make it to this release, as
tests have revealed that it needs more work.  There are excellent chances
that the feature will be included in the next release in a month or so.


************************
2. Application Isolation
************************

This capability increases the security of running applications, allowing to
run them in isolated environments based on Linux namespaces.  This is very
similar to how Docker containers work.

The configuration is pretty straightforward: you can customize the isolation
level and configure UID/GID mapping between the host and the container:

.. code-block:: json

   {
       "namespaces": {
           "credential": true,
           "pid": true,
           "network": true,
           "mount": false,
           "uname": true,
           "cgroup": false
       },

       "uidmap": [
           {
               "container": 1000,
               "host": 812,
               "size": 1
           }
       ],

       "gidmap": [
           {
               "container": 1000,
               "host": 812,
               "size": 1
           }
       ]
   }

See the documentation for details:
https://unit.nginx.org/configuration/#process-isolation

This feature was implemented by Tiago de Bem Natel de Moura, who has joined
our team recently; he will continue working on security features hardening
and container support of Unit.


****************************************
3. WebSockets in Java Servlet Containers
****************************************

WebSocket connection offloading was first introduced in the previous release
for Node.js only; now it's extended to JSC as well.  We will continue advancing
application language support further to provide equally broad opportunities,
whichever language you may prefer.


.. code-block:: none

   Changes with Unit 1.11.0                                        19 Sep 2019

      *) Feature: basic support for serving static files.

      *) Feature: isolation of application processes with Linux namespaces.

      *) Feature: built-in WebSocket server implementation for Java Servlet
         Containers.

      *) Feature: direct addressing of API configuration options containing
         slashes "/" using URI encoding (%2F).

      *) Bugfix: segmentation fault might have occurred in Go applications
         under high load.

      *) Bugfix: WebSocket support was broken if Unit was built with some
         linkers other than GNU ld (e.g. gold or LLD).


That's all for this release.  Try, test, leave feedback, and stay tuned!

wbr, Valentin V. Bartenev
