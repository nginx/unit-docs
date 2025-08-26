:orphan:

####################
Unit 1.35.0 Released
####################

We are pleased to announce the release of NGINX Unit 1.35.0. This release
includes a number of new features and changes:

************************
HTTP compression support
************************

We are pleased to release the initial implementation of HTTP compression
support, an oft-asked for feature.

It supports any or all of zlib (deflate, gzip), zstd and brotli.

It will compress both static and application (with some restrictions)
responses.

If building from source, support can be enabled by specifying any or all
of

.. code-block::

  --zlib --zstd --brotli

to ``./configure``

zlib can use either the traditional zlib library or the new
zlib-ng-compat library.

This can then be configured via the standard Unit configuration.

There is a new '/settings/http/compression' object that is used to
describe the compression configuration. E.g.

.. code-block:: json

  "compression": {
      "types": [
              "text/*"
      ],
      "compressors": [
          {
              "encoding": "gzip",
              "level": 3,
              "min_length": 4096
          },
          {
              "encoding": "deflate",
              "min_length": 0
          },
          {
              "encoding": "zstd",
          },
          {
              "encoding": "br",
              "min_length": 1024
          }
      ]
  }

The first item ``types`` is an array of MIME types that are considered for
compression.

These are MIME types as recognised by Unit, you may need to add your own
via the ``/settings/http/static/mime_types`` object.

Then we have ``compressors`` this is an array of objects describing the
compression methods to enable, if you specify a compression method here
that hasn't been built into Unit, you will get a configuration error.

Each compression object has a *required* ``encoding`` member that defines
the compression method to enable.

An optional ``level`` member with defines the compression level to use,
this value is specific to each compressor, if it's not specified then
the default for that compression method will be used.

An optional ``min_length`` member that specifies the minimum amount of
data to be considered for compression. If set to 0 or not specified then
there is no minimum amount before compression may happen.

Compression will happen for both static and application responses.

For application responses, compressed responses will be sent chunked.
Also with application responses we will only consider compressing output
where we know the content length.

**********************
Improved compatibility
**********************

Unit 1.35.0 introduces support for Ruby 3.4 and Django 5.x

Websockets with the Python Litestar framework has been fixed. Also a
long standing issue related to Firefox and websockets has also been
fixed.

***
njs
***

This version of Unit requires njs >= 0.9.0

*******
Changes
*******

We now flow the correct server listen socket port number through to
applications via SERVER_PORT rather than hard coding it to 80.

Thus the SERVER_PORT variable will now contain the port number that the
connection was accept(2)ed on.

**********
Developers
**********

GCC 15 introduced a new warning, *Wunterminated-string-initialization* to
catch things like

.. code-block:: c

  static const char str[11] = "Hello World";

which will now produce a warning with
``-Wunterminated-string-initialization`` or ``-Wextra``

However there are often times when you want non-NUL terminated string
literals. E.g.

.. code-block:: c

  static const char hex[16] = "0123456789ABCDEF";

which is used as a lookup table and will only ever be accessed via
individual indices 0-15.

To accommodate such things we introduce a new macro

.. code-block:: c

  NXT_NONSTRING

which is an alias for

.. code-block:: c

  __attribute__((__nonstring__))

which will quell the warning, e.g.

.. code-block:: c

  static const char hex[16] NXT_NONSTRING = "0123456789ABCDEF";

**************
Full Changelog
**************

.. code-block:: none

  Changes with Unit 1.35.0                                   26 Aug 2025

    *) Security: fix missing websocket payload length validation in the
                 Java language module which could lead to Java language
                 module processes consuming excess CPU. (CVE-2025-1695).

    *) Change: if building with njs, version 0.9.0 or later is now
               required.

    *) Feature: HTTP compression.

    *) Feature: Django 5.x compatibility.

    *) Feature: Python Litestar WebSockets compatibility.

    *) Feature: GCC 15 compatibility.

    *) Feature: Ruby 3.4 compatibility.

    *) Bugfix: set SERVER_PORT to the actual value.

    *) Bugfix: fix issue in node.js with duplicate headers in response.

    *) Bugfix: fix WebSockets with Firefox.

    *) Bugfix: fix incorrect websocket payload length calculation in the
               Java language module.

    *) Bugfix: fix instability issues due to OpenTelemetry (OTEL)
               support.

    *) Bugfix: fix issues with building OpenTelemetry (OTEL) support on
               various platforms, including macOS.
