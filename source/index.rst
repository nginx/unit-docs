.. meta::
   :og:description: A versatile open-source server for a diverse Web.

.. include:: include/replace.rst

#####
About
#####

NGINX Unit is a polyglot app server, a reverse proxy, and a static file server,
available for :ref:`Unix-like systems <source-prereqs>`.  It was built by
`nginx <https://nginx.org/en/>`_ team members from scratch to be highly
efficient and fully configurable at runtime.

| The latest version is |version|, released on |release_date|.
| See the changelog `here </CHANGES.txt>`_; a GitHub-based
  `roadmap <https://github.com/orgs/nginx/projects/1>`_ outlines
  our plans for the future.

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

- The :ref:`entire configuration <configuration-full-example>` is managed
  dynamically over HTTP via a friendly :ref:`RESTful JSON API
  <configuration-mgmt>`

- Updates to the configuration are performed granularly at runtime with zero
  interruption

- Requests are :ref:`routed <configuration-routes>` between :ref:`static
  content <configuration-static>`, upstream :ref:`servers
  <configuration-proxy>`, and local :ref:`apps <configuration-applications>`

- Request filtering and dispatching uses elaborate :ref:`matching rules
  <configuration-routes-matching>` that allow :ref:`regular expressions
  <configuration-routes-matching-patterns>`

- Apps in multiple languages and language versions run :ref:`side by side
  <configuration-applications>`

- Common :ref:`language-specific APIs <howto-frameworks>` for all supported
  languages run seamlessly

- Upstream :ref:`server groups <configuration-upstreams>` provide dynamic
  load balancing using a weighted round-robin method

- Originating IP identification :ref:`supports <configuration-listeners-xff>`
  :samp:`X-Forwarded-For` and similar header fields


============
Performance
============

- Requests are asynchronously processed in threads with efficient event loops
  (:program:`epoll`, :program:`kqueue`)

- Syscalls and data copy operations are kept to a necessary minimum

- 10,000 inactive HTTP keep-alive connections take up only a few MBs of memory

- Router and app processes rely on low-latency IPC built with lock-free queues
  over shared memory

- The number of per-app processes is defined statically or :ref:`scales
  <configuration-proc-mgmt-prcs>` preemptively within given limits

- Multithreaded request processing is supported for :ref:`Java
  <configuration-java>`, :ref:`Perl <configuration-perl>`, :ref:`Python
  <configuration-python>`, and :ref:`Ruby <configuration-ruby>` apps


=====================
Security & Robustness
=====================

- Client connections are handled by a separate non-privileged router process

- Low-resource conditions (out of memory or descriptors) and app crashes are
  handled gracefully

- :ref:`SSL/TLS <configuration-ssl>` with
  :ref:`SNI <configuration-listeners-ssl>`, :ref:`session cache and tickets
  <configuration-listeners-ssl-sessions>` is integrated (OpenSSL |_| 1.0.1 and
  later)

- Different apps are isolated in separate processes

- Apps can be additionally containerized with namespace and file system
  :ref:`isolation <configuration-proc-mgmt-isolation>`

- Static file serving benefits from :ref:`chrooting
  <configuration-share-path>`, symlink and mount point :ref:`traversal
  restrictions <configuration-share-resolution>`


***********************
Supported App Languages
***********************

Unit interoperates with:

- `Binary-compiled languages
  <https://www.nginx.com/blog/nginx-unit-adds-assembly-language-support/>`_ in
  general: using the embedded :program:`libunit`
  library

- :ref:`Go <configuration-go>`: by :ref:`overriding <installation-go-package>`
  the :program:`http` module

- :ref:`JavaScript (Node.js) <configuration-nodejs>`: by automatically
  :ref:`overloading <installation-nodejs-package>` the :program:`http` and
  :program:`websocket` modules

- :ref:`Java <configuration-java>`: using the Servlet Specification 3.1 and
  WebSocket APIs

- :ref:`Perl <configuration-perl>`: using PSGI

- :ref:`PHP <configuration-php>`: using a custom SAPI module

- :ref:`Python <configuration-python>`: using WSGI or ASGI with WebSocket
  support

- :ref:`Ruby <configuration-ruby>`: using the Rack API


****************
Reporting Issues
****************

Please report any security-related issues concerning Unit to
`security-alert@nginx.org <security-alert@nginx.org>`__.  For our mutual
convenience, specifically mention NGINX Unit in the subject and follow the
`CVSS v3.1 <https://www.first.org/cvss/v3.1/specification-document>`__
specification.

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
