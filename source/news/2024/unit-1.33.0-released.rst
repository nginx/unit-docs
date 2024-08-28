:orphan:

####################
Unit 1.33.0 Released
####################

We are pleased to announce the release of NGINX Unit 1.33.0. This release includes
a number of new features and changes:

*************************
New configuration options
*************************

This release introduces two new configuration options:

#. `listen_threads`

   This option can be set under `/settings/listen_threads` and controls the
   number of threads the router process creates to handle client
   connections. By default Unit creates the same number of threads as there
   are CPUs available.

#. `backlog`

   This option can be set under `/listeners/backlog`. This is a per-listener
   option that sets the the backlog parameter as passed to the listen(2)
   system-call, which defines the maximum length for the queue of pending
   connections for the socket.

   This is analogous to the `backlog` parameter of the `listen` directive in
   NGINX.

****************
unitctl CLI tool
****************

Chunked request body support


*************************************
Changes in behavior and other updates
*************************************

==========================================================================
Change 1
==========================================================================

Change 1 description.

=======================================================
Change 2
=======================================================

Change 2 description.

************
Wall of fame
************

Special Thanks to all external contributors helping us
making Unit better! With 1.33.0 we would like to send a shout out to:

- Alejandro Colomar
- Costas Drongos
- Gourav
- Remi Collet

Special thanks to Arjun for his fuzzing work.

**************
Full Changelog
**************

.. code-block:: none

  Changes with Unit 1.33.0                                         29 Aug 2024

    *) Feature: show list of loaded language modules in the /status
       endpoint.

    *) Feature: make the number of router threads configurable.

    *) Feature: make the listen(2) backlog configurable.

    *) Feature: add fuzzing via oss-fuzz.

    *) Feature: add Python application factory support.

    *) Feature: add chunked request body support.

    *) Feature: add "if" option to the "match" object.

    *) Feature: Unit ships with a new Rust based CLI application "unitctl".

    *) Change: under systemd unit runs in forking mode (once again).

    *) Change: if building with njs, version 0.8.3 or later is now required.

    *) Change: Unit now builds with -std=gnu11 (C11 with GNU extensions).

    *) Change: Unit now creates the full directory path for the PID file and
       control socket.

    *) Change: build system improvements, including pretty printing the make
       output and enabling various make variables to influence the build
       process (see: make help).

    *) Change: better detection of available runnable CPUs on Linux.

    *) Change: default listen(2) backlog on Linux now defaults to Kernel
       default.

    *) Bugfix: don't create the $runstatedir directory which triggered an
       Alpine packaging error.

    *) Bugfix: wasm-wasi-component application process hangs after receiving
       restart signal from the control endpoint.

    *) Bugfix: njs variables accessed with a JS template literal should not
       be cacheable.

    *) Bugfix: don't modify REQUEST_URI.

    *) Bugfix: properly handle deleting arrays of certificates.
