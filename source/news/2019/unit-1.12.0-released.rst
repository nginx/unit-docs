:orphan:

####################
Unit 1.12.0 Released
####################

Hi,

I'm glad to announce a new release of NGINX Unit.

This is an ad-hoc release that focuses on fixing several annoying bugs and adds
compatibility with the upcoming PHP 7.4, scheduled for release on November 28,
2019.

.. code-block:: none

   Changes with Unit 1.12.0                                         03 Oct 2019

       *) Feature: compatibility with PHP 7.4.

       *) Bugfix: descriptors leak on process creation; the bug had appeared in
          1.11.0.

       *) Bugfix: TLS connection might be closed prematurely while sending
          response.

       *) Bugfix: segmentation fault might have occurred if an irregular file
          was requested.


Regarding our plans for the near future, see our earlier :doc:`announcement
<unit-1.11.0-released>`.

To know more about some features introduced recently, you can follow posts
about Unit in the official blog: https://www.nginx.com/blog/tag/nginx-unit/

We also updated our Docker images with an initialization script that
significantly simplifies the initial configuration of Unit daemon inside a
container.  Please check the documentation for instructions:
https://unit.nginx.org/installation/#initial-configuration

wbr, Valentin V. Bartenev
