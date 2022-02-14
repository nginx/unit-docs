:orphan:

######################
Unit Beta 0.7 Released
######################

Hello,

I'm glad to announce a new beta of NGINX Unit with a number of bugfixes and
Ruby/Rack support.  Now you can easily run applications like Redmine with Unit.

The full list of supported languages today is PHP, Python, Go, Perl, and Ruby.
More languages are coming.

.. code-block:: none

   Changes with Unit 0.7                                            22 Mar 2018

       *) Feature: Ruby application module.

       *) Bugfix: in discovering modules.

       *) Bugfix: various race conditions on reconfiguration and during
          shutting down.

       *) Bugfix: tabs and trailing spaces were not allowed in header fields
          values.

       *) Bugfix: a segmentation fault occurred in Python module if
          start_response() was called outside of WSGI callable.

       *) Bugfix: a segmentation fault might occur in PHP module if there was
          an error while initialization.


Binary Linux packages and Docker images are available here:

- Packages:  https://unit.nginx.org/installation/#precompiled-packages
- Docker:    https://hub.docker.com/r/nginx/unit/tags/

Packages and images for the new Ruby module will be built next week.

wbr, Valentin V. Bartenev
