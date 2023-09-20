:orphan:

####################
Unit 1.16.0 Released
####################

Hi,

I'm glad to announce a new release of NGINX Unit.

.. attention::

   To all Unit package maintainers: please don't miss the new :samp:`--tmp`
   configure option.  It specifies the directory where the Unit daemon
   stores temporary files (i.e. large request bodies) at runtime.

In this release, we continue improving the functionality related to proxying
and static media asset handling.

Now, the new :samp:`upstreams` object enables creating server groups for
weighted round-robin load balancing:

.. code-block:: json

   {
       "listeners": {
           "*:80": {
               "pass": "upstreams/rr-lb"
           }
       },

       "upstreams": {
           "rr-lb": {
               "servers": {
                   "192.168.0.100:8080": { },
                   "192.168.0.101:8080": {
                       "weight": 2
                   }
               }
           }
       }
   }


See the docs for details:
https://unit.nginx.org/configuration/#configuration-upstreams

So far, it's rather basic, but many more proxying and load-balancing
features are planned for future releases.

By its design, the new :samp:`fallback` option is somewhat similar to the
:samp:`try_files` directive in :program:`nginx`.  It allows proceeding to
another action if a file isn't available:

.. code-block:: json

   {
       "share": "/data/www/",

       "fallback": {
           "pass": "applications/php"
       }
   }

In the example above, an attempt is made first to serve a request
with a file from the :file:`/data/www/` directory.  If there's no such
file, the request is passed to the :samp:`php` application.

Also, you can chain such fallback actions:

.. code-block:: json

   {
       "share": "/data/www/",

       "fallback": {
           "share": "/data/cache/",

           "fallback": {
               "proxy": "http://127.0.0.1:9000"
           }
       }
   }


More info: https://unit.nginx.org/configuration/#configuration-fallback

Finally, configurations you upload can use line (:samp:`//`) and block
(:samp:`/* */`) comments.  Now, Unit doesn't complain; instead, it strips them
from the JSON payload.  This comes in handy if you store your configuration in
a file and edit it manually.

.. code-block:: none

   Changes with Unit 1.16.0                                         12 Mar 2020

       *) Feature: basic load-balancing support with round-robin.

       *) Feature: a "fallback" option that performs an alternative action if a
          request can't be served from the "share" directory.

       *) Feature: reduced memory consumption by dumping large request bodies
          to disk.

       *) Feature: stripping UTF-8 BOM and JavaScript-style comments from
          uploaded JSON.

       *) Bugfix: negative address matching in router might work improperly in
          combination with non-negative patterns.

       *) Bugfix: Java Spring applications failed to run; the bug had appeared
          in 1.10.0.

       *) Bugfix: PHP 7.4 was broken if it was built with thread safety
          enabled.

       *) Bugfix: compatibility issues with some Python applications.


To keep the finger on the pulse, see our further plans in the roadmap here:
https://github.com/orgs/nginx/projects/1

Also, good news for macOS users!  Now, there's a Homebrew tap for Unit:
https://unit.nginx.org/installation/#homebrew

Stay healthy!

wbr, Valentin V. Bartenev
