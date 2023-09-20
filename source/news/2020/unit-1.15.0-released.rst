:orphan:

####################
Unit 1.16.0 Released
####################

Hi,

I'm glad to announce a new release of NGINX Unit.

This is mostly a bugfix release that eliminates a few nasty issues.
Also, it addresses incompatibilities caused by a minor API change in
the recently released major version of Ruby.

.. code-block:: none

   Changes with Unit 1.15.0                                         06 Feb 2020

       *) Change: extensions of dynamically requested PHP scripts were
          restricted to ".php".

       *) Feature: compatibility with Ruby 2.7.

       *) Bugfix: segmentation fault might have occurred in the router process
          with multiple application processes under load; the bug had appeared
          in 1.14.0.

       *) Bugfix: receiving request body over TLS connection might have
          stalled.


More features are planned for the next release that is expected in the
beginning of March.  Among them are basic load balancing in the proxy module
and :samp:`try_files`-like functionality for more sophisticated request
routing.

Stay tuned!

wbr, Valentin V. Bartenev
