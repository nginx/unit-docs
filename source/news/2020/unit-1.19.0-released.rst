:orphan:

####################
Unit 1.19.0 Released
####################

Hi,

I'm always happy to announce a new release of NGINX Unit, but this one's BIG.
Besides the varied features and bugfixes, some breakthrough improvements were
made under the hood.

As you may know, Unit uses an advanced architecture that relies on dedicated
processes to serve different roles in request processing.  The process that
handles client connections is the router.  It uses asynchronous threads (one
per CPU core) to accept new connections and send or receive data over already
established connections in a non-blocking manner.  For security and scalability,
all applications run as separate processes over which you have a degree of
control: https://unit.nginx.org/configuration/#process-management

To talk to application processes, relay requests for actual processing,
and obtain their responses, the router process uses an elaborate mechanism
of inter-process communication (IPC) based on shared memory segments.
The general idea is to avoid copying data between processes and minimize
overhead, potentially achieving almost zero-latency application interaction.

Our first implementation of this protocol used a complex algorithm to
distribute requests between processes, heavily utilizing Unix socket pairs
to pass synchronization control messages.  In practice, this turned out
rather sub-optimal due to lots of extra syscalls and overt complexity.
Also, the push semantics became a serious limitation that prevented us
from efficiently handling asynchronous applications.

Thus, we stepped back a bit at the end of the last year to meticulously
reconsider our approach to IPC, and now this tremendous work finally sees
the light of day with the release of Unit version 1.19.0.  Maintaining the
progress achieved while working with shared memory segments, the protocol now
is enhanced to bring the number of syscalls almost to zero under heavy load.
We have also changed the request distribution semantics.  Now, instead of
pushing requests to application processes using a complex router process
algorithm, we make application processes pull requests out of a shared
queue anytime they're ready.  This enables implementing async interfaces
in applications in the most effective manner.

Relying on this new approach to IPC, we shall be able to improve the
performance of Go and Node.js modules in the upcoming releases, also
introducing multithreading and new interfaces, such as ASGI in Python.

We are obsessed over performance and will continue optimizing Unit to
make it the best and brightest in every aspect.

As for the other features of the release, there's an improvement in proxying:
now it speaks HTTP/1.1 and accepts chunked responses from backends.

Moreover, request matching rules were also upgraded to enable more complex
wildcard patterns like :samp:`*/some/*/path/*.php*`.

Finally, we have introduced our first configuration variables.  They are
a small bunch at the moment, but that's to change.  In a while, variables
shall be sufficiently diversified and will be available in more and more
options.

.. code-block:: none

   Changes with Unit 1.19.0                                         13 Aug 2020

       *) Feature: reworked IPC between the router process and the applications
          to lower latencies, increase performance, and improve scalability.

       *) Feature: support for an arbitrary number of wildcards in route
          matching patterns.

       *) Feature: chunked transfer encoding in proxy responses.

       *) Feature: basic variables support in the "pass" option.

       *) Feature: compatibility with PHP 8 Beta 1. Thanks to Remi Collet.

       *) Bugfix: the router process could crash while passing requests to an
          application under high load.

       *) Bugfix: a number of language modules failed to build on some systems;
          the bug had appeared in 1.18.0.

       *) Bugfix: time in error log messages from PHP applications could lag.

       *) Bugfix: reconfiguration requests could hang if an application had
          failed to start; the bug had appeared in 1.18.0.

       *) Bugfix: memory leak during reconfiguration.

       *) Bugfix: the daemon didn't start without language modules; the bug had
          appeared in 1.18.0.

       *) Bugfix: the router process could crash at exit.

       *) Bugfix: Node.js applications could crash at exit.

       *) Bugfix: the Ruby module could be linked against a wrong library
          version.


Also, official packages for Fedora 32 are available now:
https://unit.nginx.org/installation/#fedora

And if you'd like to know more about the features introduced recently in
the previous release, see the blog posts:

- `NGINX Unit 1.18.0 Adds Filesystem Isolation and Other Enhancements
  <https://www.nginx.com/blog/nginx-unit-1-18-0-now-available/>`__

- `Filesystem Isolation in NGINX Unit
  <https://www.nginx.com/blog/filesystem-isolation-nginx-unit/>`__

Stay tuned!

wbr, Valentin V. Bartenev
