:orphan:

####################
Unit 1.25.0 Released
####################

Hi,

I'm glad to announce a new release of NGINX Unit.

This one is much awaited not only because the last one occurred quite some
time ago, but also because it contains some sought-after features that were
requested quite often.


*******************************************
Obtaining The Originating Client IP Address
*******************************************

When Unit operates behind a reverse proxy, it receives all incoming connections
from a proxy machine address.  As a result, the originating IP address of
a client cannot be determined from the IP protocol.  To overcome this, a
special HTTP request header field can be used to carry the client IP address
information over one to several proxies.  Such header fields are usually called
"X-Forwarded-For", but variations exist as well ("X-Real-IP", "X-Remote-Addr",
etc..).

Before, Unit could not use information from such header fields otherwise than
just pass them on "as is."  With this release, functionality similar to the
real-ip nginx module became available.  Now, in any listener object, you can
specify a :samp:`client_ip` option, configuring trusted proxy addresses and the
header field name, to obtain the client IP address:

.. code-block:: json

   {
       "listeners": {
           "*:80": {
               "client_ip": {
                   "header": "X-Forwarded-For",
                   "recursive": true,
                   "source": [
                       "10.0.0.0/8",
                       "150.172.238.0/24"
                   ]
               }
           }
       }
   }

Unit will use the address obtained from this header to the same effect as if a
direct connection was made from the client.  For instance, it will be reflected
in any logs, used for source address matching in routing, and provided to the
application via a relevant request environment (e. g.
:samp:`$_SERVER['REMOTE_ADDR']` in PHP).

See more details in the documentation:
https://unit.nginx.org/configuration/#originating-ip-identification


********************************************
Control API to Restart Application Processes
********************************************

Unit dynamic configuration is pretty smart and granular.  If it detects
no changes to an application during reconfiguration, it won't touch the
application's processes.  However, sometimes our users need to restart a
specific application, and the only good way to do that was to intentionally
introduce a change to the application's configuration.  Usually, a dummy
:samp:`environment` option was used for this:

.. code-block:: console

   curl -X PUT -d '"$RANDOM"' --unix-socket /var/run/control.unit.sock \
        /config/applications/<name>/environment/gen

While it worked well, the solution can't be called elegant; it was more like a
workaround.  But now, Unit has a special section in the control API that allows
restarting any configured application with a basic GET request:

.. code-block:: console

   curl --unix-socket /var/run/control.unit.sock \
        /control/applications/<name>/restart

See here for the details of app process management in Unit:
https://unit.nginx.org/configuration/#process-management


******************************
TLS Sessions Cache and Tickets
******************************

A full TLS handshake can be quite expensive; to save server resources and
reduce latency in subsequent client connections, two ways are commonly used:
TLS sessions cache and TLS session tickets.  The main difference between the
two is who stores the session information: the server (cache) or the client
(tickets).  Now, Unit allows you to configure either or both:

.. code-block:: json

   {
       "tls": {
           "certificate": "bundle",
           "session": {
               "cache_size": 10000,
               "timeout": 600,
               "tickets": true
           }
       }
   }

For tickets, it doesn't only allow enabling or disabling them; you can specify
shared ticket keys between multiple servers and rotate them.

See more sophisticated configurations in the docs:
https://unit.nginx.org/configuration/#ssl-tls-configuration

We will proceed to improve the client-side protocol support to be on par with
nginx in this regard or even go further.  To be specific, HTTP/2 and HTTP/3
are definitely on our shortlist.


****************************************
Ruby Process and Thread Start/Stop Hooks
****************************************

Earlier this year, one of our users opened a `feature request
<https://github.com/nginx/unit/issues/535>`__ on Unit's GitHub; we were asked
to support hooks to be triggered on process or thread start/stop, as does
another popular Ruby web server, `Puma <https://puma.io>`__.  These are usually
used to instantiate a database connection or to perform some other
initialization or cleanup work.

A few months later, we've fulfilled the request.  Here we go:
https://unit.nginx.org/configuration/#ruby

That's why I always ask you not to hesitate and instead open a feature request
for any crazy idea you may have on our GitHub issue tracker:
https://github.com/nginx/unit/issues

We'd like to hear from you, we'd like to know your cases, your issues, anything
you're struggling with or are missing and would want to see in Unit.

Sure, not all requests are handled fast.  There's plenty of them pending for
years already.  It's different case by case; sometimes, we're just busy with
other important tasks, sometimes the feature depends on other missing parts,
which also depend on other ones, and so on.  Sometimes, it just takes a while
to find a good solution, to design a good architecture, or to find a proper
method of configuring something.  Anyway, all your requests are collected and
carefully examined; perhaps, it's your idea that will be implemented next.
Please go and open a ticket if in doubt.

The full changelog for the release:

.. code-block:: none

   Changes with Unit 1.25.0                                         19 Aug 2021

       *) Feature: client IP address replacement from a specified HTTP header
          field.

       *) Feature: TLS sessions cache.

       *) Feature: TLS session tickets.

       *) Feature: application restart control.

       *) Feature: process and thread lifecycle hooks in Ruby.

       *) Bugfix: the router process could crash on TLS connection open when
          multiple listeners with TLS certificates were configured; the bug had
          appeared in 1.23.0.

       *) Bugfix: TLS connections were rejected for configurations with
          multiple certificate bundles in a listener if the client did not use
          SNI.

       *) Bugfix: the router process could crash with frequent multithreaded
          application reconfiguration.

       *) Bugfix: compatibility issues with some Python ASGI apps, notably
          based on the Starlette framework.

       *) Bugfix: a descriptor and memory leak occurred in the router process
          when an app process stopped or crashed.

       *) Bugfix: the controller or router process could crash if the
          configuration contained a full-form IPv6 in a listener address.

       *) Bugfix: the router process crashed when a request was passed to an
          empty "routes" or "upstreams" using a variable "pass" option.

       *) Bugfix: the router process crashed while matching a request to an
          empty array of source or destination address patterns.


In the meantime, there are several other features currently at different stages
of development and implementation:

- Variable support in the static file serving options
- Custom variables from regexp captures in the "match" object
- Simple request rewrites using variables
- More variables to access request and connection information
- A statistics API
- Unit CLI utility tool
- App prototype processes to reduce memory usage, share the PHP opcache,
  and improve the handling of apps isolation
- `njs <https://nginx.org/en/docs/njs/index.html>`__ integration
- .NET Core language module prototype

Some of them bound to appear in the next release.  Stay tuned!

wbr, Valentin V. Bartenev
