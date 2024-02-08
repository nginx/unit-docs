.. meta::
   :og:description: A detailed inventory of Unit's key features.

.. include:: include/replace.rst

############
Key features
############

From the start,
our vision for Unit was
versatility,
speed,
and reliability.
Here's how we
tackle these goals.


***********
Flexibility
***********

- The
  :ref:`entire configuration <configuration-api>`
  is managed dynamically over HTTP
  via a friendly
  :ref:`RESTful JSON API <configuration-mgmt>`.

- Updates to the configuration
  are performed granularly at runtime
  with zero interruption.

- Requests are
  :ref:`routed <configuration-routes>`
  between
  :ref:`static content <configuration-static>`,
  upstream
  :ref:`servers <configuration-proxy>`,
  and local
  :ref:`apps <configuration-applications>`.

- Request filtering and dispatching uses elaborate
  :ref:`matching rules <configuration-routes-matching>`
  that enable
  :ref:`regular expressions <configuration-routes-matching-patterns>`,
  :ref:`response header <configuration-response-headers>` awareness,
  and
  :program:`njs`
  :doc:`scripting <scripting>`.

- Apps in multiple languages and language versions run
  :ref:`side by side <configuration-applications>`.

- Server-side :ref:`WebAssembly <configuration-wasm>`
  is natively supported.

- Common
  :ref:`language-specific APIs <howto-frameworks>`
  for all supported languages run seamlessly.

- Upstream
  :ref:`server groups <configuration-upstreams>`
  provide dynamic load balancing
  using a weighted round-robin method.

- Originating IP identification
  :ref:`supports <configuration-listeners-xff>`
  **X-Forwarded-For** and similar header fields.


************
Performance
************

- Requests are asynchronously processed in threads
  with efficient event loops
  (:program:`epoll`, :program:`kqueue`).

- Syscalls and data copy operations
  are kept to a necessary minimum.

- 10,000 inactive HTTP keep-alive connections
  take up only a few MBs of memory.

- Router and app processes rely on low-latency IPC
  built with lock-free queues
  over shared memory.

- Built-in
  :ref:`statistics <configuration-stats>`
  provide insights
  into Unit's performance.

- The number of per-app processes
  is defined statically or
  :ref:`scales <configuration-proc-mgmt-prcs>`
  preemptively
  within given limits.

- App and instance usage statistics
  are collected and
  :ref:`exposed <configuration-stats>`
  via the API.

- Multithreaded request processing
  is supported for
  :ref:`Java <configuration-java>`,
  :ref:`Perl <configuration-perl>`,
  :ref:`Python <configuration-python>`,
  and
  :ref:`Ruby <configuration-ruby>`
  apps.


*********************
Security & robustness
*********************

- Client connections
  are handled
  by a separate non-privileged router process.

- Low-resource conditions
  (out of memory or descriptors)
  and app crashes
  are handled gracefully.

- :ref:`SSL/TLS <configuration-ssl>`
  with
  :ref:`SNI <configuration-listeners-ssl>`,
  :ref:`session cache and tickets <configuration-listeners-ssl-sessions>`
  is integrated
  (OpenSSL |_| 1.0.1 and later).

- Different apps
  are isolated
  in separate processes.

- Apps can be additionally containerized
  with namespace and file system
  :ref:`isolation <configuration-proc-mgmt-isolation>`.

- Static file serving benefits from
  :ref:`chrooting <configuration-share-path>`,
  symlink and mount point
  :ref:`traversal restrictions <configuration-share-resolution>`.


***********************
Supported app languages
***********************

Unit interoperates with:

- `Binary-compiled languages
  <https://www.nginx.com/blog/nginx-unit-adds-assembly-language-support/>`_
  in general:
  using the embedded :program:`libunit` library.

- :ref:`Go <configuration-go>`:
  by
  :ref:`overriding <updating-go-apps>`
  the :program:`http` module.

- :ref:`JavaScript (Node.js) <configuration-nodejs>`:
  by automatically
  :ref:`overloading <installation-nodejs-package>`
  the :program:`http` and :program:`websocket` modules.

- :ref:`Java <configuration-java>`:
  by using the Servlet Specification 3.1 and WebSocket APIs.

- :ref:`Perl <configuration-perl>`:
  by using PSGI.

- :ref:`PHP <configuration-php>`:
  by using a custom SAPI module.

- :ref:`Python <configuration-python>`:
  by using WSGI or ASGI
  with WebSocket support.

- :ref:`Ruby <configuration-ruby>`:
  by using the Rack API.

- :ref:`WebAssembly <configuration-wasm>`:
  by using Wasmtime.
