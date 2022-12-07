:orphan:

#################
Unit 1.3 Released
#################

Hello,

I'm glad to announce a new release of NGINX Unit.

.. code-block:: none

   Changes with Unit 1.3                                            13 Jul 2018

       *) Change: UTF-8 characters are now allowed in request header field
          values.

       *) Feature: configuration of the request body size limit.

       *) Feature: configuration of various HTTP connection timeouts.

       *) Feature: Ruby module now automatically uses Bundler where possible.

       *) Feature: http.Flusher interface in Go module.

       *) Bugfix: various issues in HTTP connection errors handling.

       *) Bugfix: requests with body data might be handled incorrectly in PHP
          module.

       *) Bugfix: individual PHP configuration options specified via control
          API were reset to previous values after the first request in
          application process.


Here's an example configuration with new parameters:

.. code-block:: json

   {
       "settings": {
           "http": {
               "header_read_timeout": 30,
               "body_read_timeout": 30,
               "send_timeout": 30,
               "idle_timeout": 180,
               "max_body_size": 8388608
           }
       },

       "listeners": {
           "127.0.0.1:8034": {
               "application": "mercurial"
           }
       },

       "applications": {
           "mercurial": {
               "type": "python 2",
               "module": "hgweb",
               "path": "/data/hg"
           }
       }
   }

All timeouts values are specified in seconds.  The :samp:`max_body_size` value
is specified in bytes.

Please note that the parameters of the :samp:`http` object in this example are
set to their default values.  So, there's no need to set them explicitly if you
are happy with the values above.

Binary Linux packages and Docker images are available here:

- Packages:  https://unit.nginx.org/installation/#official-packages
- Docker:    https://hub.docker.com/r/nginx/unit/tags/

Also, please follow our blog posts to learn more about new features in
the recent versions of Unit: https://www.nginx.com/blog/tag/nginx-unit/

wbr, Valentin V. Bartenev
