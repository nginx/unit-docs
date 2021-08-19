.. meta::
   :og:description: A versatile open-source server for a diverse Web.

.. include:: include/replace.rst

#####
About
#####

NGINX Unit is a polyglot app server, a reverse proxy, and a static file server,
:ref:`available <installation-prereqs>` for Unix-like systems. It was
built by `nginx <https://nginx.org/en/>`_ team members from scratch to be
highly efficient and fully configurable at runtime.

| The latest version is |version|, released on |release_date|.
| See the changelog `here </CHANGES.txt>`_; a GitHub-based
  `roadmap <https://github.com/orgs/nginx/projects/1>`_ outlines
  our further plans.

| The sources are distributed under the `Apache 2.0
  <https://hg.nginx.org/unit/file/tip/LICENSE>`_ license.
| Commercial support is available from `NGINX, Inc
  <https://www.nginx.com/support/>`_.

************
Key Features
************

===========
Flexibility
===========

- :ref:`Entire configuration <configuration-full-example>` is managed
  dynamically over HTTP via a user-friendly :ref:`RESTful JSON API
  <configuration-mgmt>`

- Updates to the configuration are performed granularly at runtime with
  zero interruption

- Requests are :ref:`routed <configuration-routes>` between :ref:`static
  content <configuration-static>`, upstream :ref:`servers
  <configuration-proxy>`, and local :ref:`apps <configuration-applications>`

- Requests are filtered and dispatched with complex :ref:`matching rules
  <configuration-routes-matching>` that support :ref:`regular expressions
  <installation-config-src-pcre>`

- Apps in multiple languages and language versions run :ref:`side by side
  <configuration-applications>`

- App runtimes seamlessly support :ref:`common language-specific APIs
  <howto-frameworks>` for each supported language

- Upstream :ref:`server groups <configuration-upstreams>` enable dynamic
  load balancing using a weighted round-robin method

- Originating IP identification :ref:`supports <configuration-listeners-xff>`
  :samp:`X-Forwarded-For` or similar header fields


============
Performance
============

- Requests are asynchronously processed in threads with efficient event loops
  (epoll/kqueue)

- Syscalls and data copy operations are kept to a necessary minimum

- 10,000 inactive HTTP keep-alive connections take up only a few MBs of memory

- Router and app processes rely on low-latency IPC built with lock-free queues
  over shared memory

- The number of per-app processes is defined statically or :ref:`scales
  <configuration-proc-mgmt-prcs>` preemptively within given limits

- Multithreaded request processing can be enabled for :ref:`Java
  <configuration-java>`, :ref:`Perl <configuration-perl>`, :ref:`Python
  <configuration-python>`, and :ref:`Ruby <configuration-ruby>` apps


=====================
Security & Robustness
=====================

- Client connections are handled by a separate non-privileged router process

- Low-resource conditions (out of memory or descriptors) and app crashes are
  handled gracefully

- :ref:`SSL/TLS <configuration-ssl>` with :ref:`SNI <configuration-listeners>`,
  :ref:`session cache and tickets <configuration-listeners-ssl-sessions>` is
  supported seamlessly (OpenSSL |_| 1.0.1 and later)

- Different apps are isolated in separate processes

- Apps can be containerized with namespace and file system :ref:`isolation
  <configuration-proc-mgmt-isolation>`

- Static file serving can benefit from :ref:`chrooting
  <configuration-share-path>`, symlink and mount point :ref:`traversal
  restrictions <configuration-share-resolution>`


***********************
Supported App Languages
***********************

- `Assembly
  <https://www.nginx.com/blog/nginx-unit-adds-assembly-language-support/>`_:
  via the embedded :program:`libunit` library

- :ref:`Go <configuration-go>`: by :ref:`overloading <installation-go-package>`
  the :program:`http` module

- :ref:`JavaScript (Node.js) <configuration-nodejs>`: by automatically
  :ref:`overloading <installation-nodejs-package>` the :program:`http` and
  :program:`websocket` modules

- :ref:`Java <configuration-java>`: via the Servlet Specification 3.1 and
  WebSocket APIs

- :ref:`Perl <configuration-perl>`: via PSGI

- :ref:`PHP <configuration-php>`: via a custom SAPI module

- :ref:`Python <configuration-python>`: via WSGI and ASGI with WebSocket
  support

- :ref:`Ruby <configuration-ruby>`: via the Rack API


****************
Reporting Issues
****************

All security-related issues concerning Unit should be reported to
`security-alert@nginx.org
<security-alert@nginx.org?subject=NGINX%20Unit%20security%20issue>`__.  For our
mutual convenience, consult the `CVSS v3.1
<https://www.first.org/cvss/v3.1/specification-document>`__ specification
before reporting an issue.

With other issue types, please refer to :doc:`troubleshooting` for guidance.


****
Demo
****

.. raw:: html

    <div class="video">
    <iframe src="https://www.youtube.com/embed/I4IWEz2lBWU?modestbranding=1&amp;rel=0&amp;showinfo=0&amp;color=white"
            allowfullscreen>
    </iframe>
    </div>
