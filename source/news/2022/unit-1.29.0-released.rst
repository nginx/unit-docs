:orphan:

####################
Unit 1.29.0 Released
####################


We are happy to announce Unit 1.29.0! This release enhances the configuration
experience when managing Unit and provides programmability within the
configuration.

- NGINX JavaScript (njs) is now built with official Unit packages, enabling
  JavaScript expressions within configuration values.

- First-time users benefit from a setup script that configures Unit with a
  helpful welcome page.

- A simple command-line curl(1) wrapper simplifies configuring a running
  instance in real time.

In addition, Unit's :ref:`isolation capabilities
<configuration-proc-mgmt-isolation>` have been extended so that each
application can run in a new or a pre-existing `Linux cgroup
<https://en.wikipedia.org/wiki/Cgroups>`__, but this is only a sampler of even
richer per-application observability.  Read on for full details of these
enhancements, smaller features, and bug fixes.


****************************
NGINX JavaScript Integration
****************************

NGINX JavaScript (njs) is a server-side JavaScript runtime, optimized for
ultra-fast initialization, with a virtual machine that lives and dies with each
request.  Originally designed for extending NGINX, the njs architecture lends
itself to integration, and now it also extends Unit!

This release brings the initial integration of the NGINX JavaScript engine to
Unit.  Future releases will extend these capabilities to enable more elaborate
uses.  With Unit 1.29.0, JavaScript template literals may be used in
configuration strings to execute JavaScript expressions.  A simple example is
to use the ternary operator to make a routing decision.

.. code-block:: console

   # curl --unix-socket /var/run/control.unit.sock http://localhost/config/routes

.. code-block:: json

   [
       {
           "action": {
               "pass": "`applications/${new Date().getHours() < 12 ? 'am' : 'pm'}`"
           }
       }
   ]

Here, requests are passed between different applications depending on the time
of day.  Note that a template literal is enclosed in backticks (:samp:`\`\``),
and :samp:`${}` encloses the JavaScript expression.  Template literals may be
used wherever Unit supports variables, and multiple expressions can appear in a
single template literal.

Also, this embedded JavaScript code can access various HTTP request properties:

- Scalars: :samp:`host`, :samp:`uri`, :samp:`remoteAddr`
- Objects: :samp:`args`, :samp:`cookies`, :samp:`headers`

Let's use these properties to redirect clients to the HTTPS login page if there
is no :samp:`session` cookie:

.. code-block:: console

   # curl --unix-socket /var/run/control.unit.sock http://localhost/config/routes/0

.. code-block:: json

   {
       "match": {
           "scheme": "http"
       },

       "action": {
           "return": 302,
           "location": "`https://${host}${cookies['session'] === undefined ? '/login' : uri}`"
       }
   }

More complex logic can be implemented using the `immediately invoked function
expressions <https://developer.mozilla.org/en-US/docs/Glossary/IIFE>`__ (IFFE)
in the template literal: an entire JavaScript function can be defined,
comprising multiple statements and local variables.  This defines a simple
key-value log format that parses a JSON Web Token (JWT) to extract the sub
claim:

.. code-block:: console

   # curl --unix-socket /var/run/control.unit.sock http://localhost/config/access_log

.. code-block:: json

   {
       "path": "/var/log/unit/access_kv.log",
       "format": "`timestamp=${new Date().toISOString()} ip=${remoteAddr} uri=${uri} sub=${(() => { var authz = headers['Authorization']; if (authz === undefined) { return '-'; } else { var parts = authz.slice(7).split('.').slice(0,2).map(v=>Buffer.from(v, 'base64url').toString()).map(JSON.parse); return parts[1].sub; } } )()}\n`"
   }

Embedding IFFE code in the configuration is extremely powerful, but is
typically long, difficult to read, and challenging to debug.  The `njs command
line utility <http://nginx.org/en/docs/njs/cli.html>`__ can be used to help
develop JavaScript expressions.

Future releases will support loading JavaScript modules into a separate storage
and later using module-based functions in the configuration.


*******************
Configuration Tools
*******************

This release introduces two new command-line tools to simplify Unit's installation and configuration.

setup-unit
##########

The :program:`setup-unit` tool automates configuring the software repository
prior to installing Unit.  It also verifies a fresh installation by configuring
and serving a "welcome" web page.  This takes some of the guesswork out of the
installation process for first-time users and guides them to their next steps.
Installing and running Unit on a typical Linux system is now as simple as this:

.. code-block:: console

   $ wget https://unit.nginx.org/_downloads/setup-unit && chmod +x setup-unit

.. code-block:: console

   # ./setup-unit repo-config

.. code-block:: console

   # apt install unit || yum install unit

.. code-block:: console

   # ./setup-unit welcome

The :program:`setup-unit` tool has other useful functions you can explore by
running :samp:`setup-unit --help`.

unitc
#####

The :program:`unitc` tool provides a command-line interface as a wrapper for
:program:`curl(1)` for daily configuration and management of Unit instances.  It
aims to minimize typing effort and shield the users from exotic
:program:`curl(1)` options.  In most cases, you simply specify a URI within
Unit's control API, and :program:`unitc` executes the corresponding
:program:`curl(1)` command to read or modify the appropriate configuration
portion.  Unit's control socket is detected automatically, and the appropriate
HTTP method is used; several extra options cover advanced configuration and
remote instance management.  Here is a simple :program:`unitc` example that
reads and updates the entire configuration:

.. code-block:: console

   $ unitc /config

.. code-block:: console

   $ cat conf.json | unitc /config

You can find these tools and their corresponding documentation in the
:file:`tools/` directory of the Unit code repository at
https://github.com/nginx/unit/tree/master/tools.


***********************
Per-Application Cgroups
***********************

As we worked on Unit 1.28.0, our main goal was to extend support for any kind
of observability.  With 1.29.0, we add another important feature to this set.

.. note::

    Before we dive into the new syntax, let's distinguish the new feature from
    the already supported cgroup namespaces  that enable different per-process
    views of various system facets such as filesystem mounts, networking, or
    hostnames.  Instead, the new cgroup support for applications is based on a
    Linux kernel facility that puts processes together to perform tasks on the
    group as a whole (for example, to enforce resource limits or add hooks for
    observability frameworks).

There are two parts to cgroups in Linux: the core part of organizing processes
into a hierarchy, and the controllers responsible for enforcing resource
limits.

With Unit 1.29.0, we support the cgroup V2 API to provide the ability to place
each application into its own cgroup or have multiple applications in a single
cgroup.  The following configuration illustrates the newly added configuration
syntax:

.. code-block:: json

   "applications": {
       "cgroup-demo": {
           "type": "python",
           "path": "/path/to/app/dir",
           "module": "app",
           "isolation": {
               "cgroup": {
                   "path": "unit/cgroup-demo"
               }
           }
       }
   }

One thing to note about cgroups is that they are set up and controlled through
the cgroupfs pseudo-filesystem; you can use tools like systemd-cgls to get a
tree output of the control group content.

As mentioned initially, cgroups can be used for added application transparency
on Unit, giving system profiling solutions such as eBPF the ability to collect
detailed metrics per each application.  At this point, there is no simple
out-of-the-box solution to monitor and view the metrics that can be collected
from the applications in a single control group, but we are working to expand
in this direction to enable natively obtaining the performance data from
Unit-configured control groups.

Meanwhile, a variety of SDKs and tools can already be used to visualize the data.

- A great example, written in Go:
  https://github.com/cilium/ebpf/blob/master/examples/cgroup_skb/main.go

- If you prefer Rust, this SDK is the thing: https://github.com/aya-rs/aya


*************
New Variables
*************

With version 1.29.0, we also add a new variable: :samp:`$request_time` records
the number of seconds it took Unit to process the request.  The timer sets off
when the request reaches a Unit listener and stops when Unit sends the response
to the client.  Everything in between, e. g. in-app processing time, reading
static assets, or finding the correct route on Unit, adds to the timer.


***********************************
Version Updates in Language Modules
***********************************

Writing an application server for a single language is always challenging.  You
have to stay on top of the specifications, carefully monitoring the changes in
the underlying programming language.  Because Unit supports seven different
languages instead of just one, you can imagine the enormity of our task in this
respect.  However, we are not alone! A huge shout-out goes to all the community
members and supporters raising our awareness of language updates and version
bumps.  This kind of feedback is much appreciated and very important for us to
keep Unit compatible with the latest versions of all languages we support.  Due
to this effort, we are proud of these additions to the list of supported
languages:

- Python 3.11
- PHP 8.2
- Node.js 19.0
- Rack Version 3 in Ruby
- Java 19 (due to Ubuntu 22.10)

Can't say that loud enough—immense thanks to all who worked with us on these
enhancements!

**************
Full Changelog
**************

.. code-block:: none

   Changes with Unit 1.29.0                                         15 Dec 2022

       *) Change: removed $uri auto-append for "share" when loading
          configuration.

       *) Change: prefer system crypto policy instead of hardcoding a default.

       *) Feature: njs support with the basic syntax of JS template literals.

       *) Feature: support per-application cgroups on Linux.

       *) Feature: the $request_time variable contains the request processing
          time.

       *) Feature: "prefix" option in Python applications to set WSGI
          "SCRIPT_NAME" and ASGI root-path variables.

       *) Feature: compatibility with Python 3.11.

       *) Feature: compatibility with OpenSSL 3.

       *) Feature: compatibility with PHP 8.2.

       *) Feature: compatibility with Node.js 19.0.

       *) Feature: Ruby Rack v3 support.

       *) Bugfix: fix error in connection statistics when using proxy.

       *) Bugfix: fix HTTP cookie parsing when the value contains an equals
          sign.

       *) Bugfix: PHP directory URLs without a trailing '/' would give a 503
          error (fixed with a 301 re-direct).

       *) Bugfix: missing error checks in the C API.

       *) Bugfix: report the regex status in configure summary.


****************
Platform Updates
****************

- Added support for Ubuntu 22.10
- Added support for Fedora 37
