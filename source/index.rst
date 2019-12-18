.. include:: include/replace.rst

#####
About
#####

NGINX Unit is a lightweight, dynamic, open-source server for diverse web
applications; to install it, see :ref:`here <installation-precomp-pkgs>`.

Built from scratch, Unit can run web apps in many language versions at once; it
is also fully configurable in runtime with zero interruption, enabling
on-the-fly granular management for engineering and operations.

| The latest version is |version|, released on December 26, 2019.
| See the changelog `here </CHANGES.txt>`_.

The sources are distributed under the Apache |_| 2.0 license.

************
Key Features
************

- Configuration :ref:`updates dynamically <configuration-mgmt>` via a RESTful
  JSON API
- Multiple :ref:`language versions <configuration-applications>` run
  simultaneously
- Application processes :ref:`scale on demand <configuration-proc-mgmt-prcs>`
- :ref:`SSL/TLS <configuration-ssl>` support is built-in (OpenSSL |_| 1.0.1 and
  later)
- Extensive :ref:`request routing <configuration-routes>` capabilities and
  static content :ref:`support <configuration-static>`
- Built-in WebSocket server implementation for
  :ref:`Node.js <configuration-external>` and Java
- Application namespace :ref:`isolation <configuration-proc-mgmt-isolation>`
- HTTP request :ref:`proxying <configuration-routes-proxy>` in routes

***********************
Supported App Languages
***********************

- :ref:`Python <configuration-python>`
- :ref:`PHP <configuration-php>`
- :ref:`Go <configuration-external>`
- :ref:`Perl <configuration-perl>`
- :ref:`Ruby <configuration-ruby>`
- :ref:`JavaScript (Node.js) <configuration-external>`
- :ref:`Java <configuration-java>`

****
Demo
****

.. raw:: html

    <div class="video">
    <iframe src="https://www.youtube.com/embed/I4IWEz2lBWU?modestbranding=1&amp;rel=0&amp;showinfo=0&amp;color=white"
            allowfullscreen>
    </iframe>
    </div>
