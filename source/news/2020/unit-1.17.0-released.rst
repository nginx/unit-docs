:orphan:

####################
Unit 1.17.0 Released
####################

Hi,

I'm glad to announce a new release of NGINX Unit.

In addition to improved stability, this release introduces two handy features.

The first one is configured using the :samp:`return` and :samp:`location`
options of the action object.  It can be used to immediately generate a simple
HTTP response with an arbitrary status - for example, to deny access to some
resources:

.. code-block:: json

   {
       "match": {
           "uri": "*/.git/*"
       },

       "action": {
           "return": 403
       }
   }

Or, you can redirect a client to another resource:

.. code-block:: json

   {
       "match": {
           "host": "example.org",
       },

       "action": {
           "return": 301,
           "location": "http://www.example.org"
       }
   }

See the documentation for a detailed description of routing:
https://unit.nginx.org/configuration/#routes

The second new feature of the release is mostly syntax sugar rather than new
functionality.  Now, you can specify servers' weights in an upstream group
using fractional numbers.

Say, you have a bunch of servers and want one of them to receive half as many
requests as the others for some reason.  Previously, the only way to achieve
that was to double the weights of all the other servers:

.. code-block:: json

   {
       "192.168.0.101:8080": {
           "weight": 2
       },
       "192.168.0.102:8080": {
           "weight": 2
       },
       "192.168.0.103:8080": { },
       "192.168.0.104:8080": {
           "weight": 2
       }
   }

Using fractional weights, you can perform the update much easier by altering
the weight of the server in question:

.. code-block:: json

   {
       "192.168.0.101:8080": { },
       "192.168.0.102:8080": { },
       "192.168.0.103:8080": {
           "weight": 0.5
       },
       "192.168.0.104:8080": { }
   }

For details of server groups, see here:
https://unit.nginx.org/configuration/#proxying

.. code-block:: none

   Changes with Unit 1.17.0                                         16 Apr 2020

       *) Feature: a "return" action with optional "location" for immediate
          responses and external redirection.

       *) Feature: fractional weights support for upstream servers.

       *) Bugfix: accidental 502 "Bad Gateway" errors might have occurred in
          applications under high load.

       *) Bugfix: memory leak in the router; the bug had appeared in 1.13.0.

       *) Bugfix: segmentation fault might have occurred in the router process
          when reaching open connections limit.

       *) Bugfix: "close() failed (9: Bad file descriptor)" alerts might have
          appeared in the log while processing large request bodies; the bug
          had appeared in 1.16.0.

       *) Bugfix: existing application processes didn't reopen the log file.

       *) Bugfix: incompatibility with some Node.js applications.

       *) Bugfix: broken build on DragonFly BSD; the bug had appeared in
          1.16.0.


Please also see a blog post about the new features of our two previous releases:
https://www.nginx.com/blog/nginx-unit-1-16-0-now-available/

To keep the finger on the pulse, refer to our further plans in the roadmap here:
https://github.com/orgs/nginx/projects/1

Stay healthy, stay home!

wbr, Valentin V. Bartenev
