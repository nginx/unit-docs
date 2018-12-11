
#####
About
#####

NGINX Unit is a dynamic web and application server, designed to run applications
in multiple languages.  Unit is lightweight, polyglot, and dynamically
configured via API.  The design of the server allows reconfiguration of
specific application parameters as needed by the engineering or operations.

| Current latest version is 1.6, released on November 15, 2018.
| See the changelog `here </CHANGES.txt>`_.

The sources are distributed under the Apache 2.0 license.

Key Features
************

- Fully dynamic reconfiguration using RESTful JSON API
- Multiple application languages and versions can run simultaneously
- Dynamic application process management
- :ref:`SSL/TLS support (OpenSSL 1.0.1 and later) <configuration-ssl>`
- TCP, HTTP, HTTPS, HTTP/2 routing and proxying *(coming soon)*

Supported Application Languages
*******************************

- Python
- PHP
- Go
- Perl
- Ruby
- :ref:`JavaScript (Node.js) <installation-nodejs-package>`
- Java (`coming soon <https://github.com/mar0x/unit>`_)

Demo
****

.. raw:: html

    <div class="video">
    <iframe type="text/html"
            src="https://www.youtube.com/embed/I4IWEz2lBWU?modestbranding=1&amp;rel=0&amp;showinfo=0&amp;color=white"
            frameborder="0" allowfullscreen="1">
    </iframe>
    </div>
