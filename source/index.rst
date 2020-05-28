.. include:: include/replace.rst

#####
About
#####

NGINX Unit is a lightweight dynamic open-source server for diverse web
applications; to install it, see :ref:`here <installation-precomp-pkgs>`.

Built from scratch, Unit can run web apps in different language versions; fully
configurable in runtime with zero interruption, it enables on-the-fly granular
management for engineering and operations.

| The latest version is |version|, released on May 28, 2020.
| See the changelog `here </CHANGES.txt>`_; a GitHub-based
  `roadmap <https://github.com/orgs/nginx/projects/1>`_ outlines
  our further plans.

The sources are available under the Apache |_| 2.0 license.

************
Key Features
************

- Configuration :ref:`updates dynamically <configuration-mgmt>` via a RESTful
  JSON API
- Disparate :ref:`language versions <configuration-applications>` run
  simultaneously
- Application processes :ref:`scale on demand <configuration-proc-mgmt-prcs>`
- :ref:`SSL/TLS <configuration-ssl>` is supported seamlessly (OpenSSL |_| 1.0.1
  and later)
- Extensive :ref:`request routing <configuration-routes>`,
  :ref:`load balancing <configuration-upstreams>`, and
  :ref:`static file serving <configuration-static>` options are available
- Server-side WebSockets are implemented for :ref:`Node.js
  <configuration-external>` and Java
- Applications can rely on namespace and file system :ref:`isolation
  <configuration-proc-mgmt-isolation>`
- HTTP requests can be :ref:`proxied <configuration-routes-proxy>` elsewhere
  during routing

***********************
Supported App Languages
***********************

- `Assembly <https://www.nginx.com/blog/nginx-unit-adds-assembly-language-support/>`_
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
