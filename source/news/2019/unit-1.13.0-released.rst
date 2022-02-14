:orphan:

####################
Unit 1.13.0 Released
####################

Hi,

I'm glad to announce a new release of NGINX Unit.

This release expands Unit's functionality as a generic web server by
introducing basic HTTP reverse proxying.

See the details in our documentation:
https://unit.nginx.org/configuration/#proxying

Compared to mature proxy servers and load balancers, Unit's proxy features
are limited now, but we'll continue the advance.

Also, this release improves the user experience for Python and Ruby modules and
remediates compatibility issues with existing applications in these languages.

Our long-term goal is to turn Unit into the ultimate high-performance building
block that will be helpful and easy to use with web services of any kind. To
accomplish this, Unit's future releases will focus on the following aspects:

- security, isolation, and DoS protection
- ability to run various types of dynamic applications
- connectivity with load balancing and fault tolerance
- efficient serving of static media assets
- statistics and monitoring

.. code-block:: none

   Changes with Unit 1.13.0                                         14 Nov 2019

      *) Feature: basic support for HTTP reverse proxying.

      *) Feature: compatibility with Python 3.8.

      *) Bugfix: memory leak in Python application processes when the close
         handler was used.

      *) Bugfix: threads in Python applications might not work correctly.

      *) Bugfix: Ruby on Rails applications might not work on Ruby 2.6.

      *) Bugfix: backtraces for uncaught exceptions in Python 3 might be
         logged with significant delays.

      *) Bugfix: explicit setting a namespaces isolation option to false might
         have enabled it.


Please feel free to share your experiences and ideas on GitHub:
https://github.com/nginx/unit/issues

Or via Unit mailing list: https://mailman.nginx.org/mailman/listinfo/unit

wbr, Valentin V. Bartenev
