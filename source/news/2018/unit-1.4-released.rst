:orphan:

#################
Unit 1.4 Released
#################

Hello,

I'm glad to announce a new release of NGINX Unit.

The key feature of the new version is dynamically configurable TLS support
with certificate storage API that provides detailed information about your
certificate chains, including common and alternative names as well as
expiration dates.

See the documentation for details:
https://unit.nginx.org/certificates/

This is just our first step in TLS support.  More configuration options
and various TLS-related features will be added in the future.

Full-featured HTTP/2 support is also in our sights.

.. code-block:: none

   Changes with Unit 1.4                                            20 Sep 2018

       *) Change: the control API maps the configuration object only at
          "/config/".

       *) Feature: TLS support for client connections.

       *) Feature: TLS certificates storage control API.

       *) Feature: Unit library (libunit) to streamline language module
          integration.

       *) Feature: "408 Request Timeout" responses while closing HTTP
          keep-alive connections.

       *) Feature: improvements in OpenBSD support. Thanks to David Carlier.

       *) Bugfix: a segmentation fault might have occurred after
          reconfiguration.

       *) Bugfix: building on systems with non-default locale might be broken.

       *) Bugfix: "header_read_timeout" might not work properly.

       *) Bugfix: header fields values with non-ASCII bytes might be handled
          incorrectly in Python 3 module.


In a few weeks, we are going to add preliminary Node.js support.  It's almost
ready; our QA engineers are already testing it.

Now we are also working on Java module, WebSockets support, flexible request
routing, and serving of static media assets.

Please also welcome Artem Konev, who joined our team as a technical writer.  He
has already started improving documentation on the website and updated it with
the configuration options currently available:
https://github.com/nginx/unit-docs/

Of course, the website still leaves much to be desired, so Artem will strive to
provide industry-grade documentation for Unit.  You are welcome to join this
effort with your ideas, suggestions, and edits: just send a pull request or
open an issue in our documentation repository on GitHub:
https://github.com/nginx/unit-docs/

Stay tuned!

wbr, Valentin V. Bartenev

