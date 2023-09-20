:orphan:

####################
Unit 1.28.0 Released
####################

We are happy to announce Unit 1.28! This release sets the first milestone for
observability:

- It is now possible to get basic information about connections, requests, and
  other per-application metrics

- All this is now available via our powerful RESTful API

In addition, we introduce new variables and the ability to use them to
customize the access log format. Besides the long-awaited statistics and
logging use cases, we also present:

-  Enhanced forward header handling with new configuration syntax and
   X-Forwarded-Proto support

-  Support for abstract UNIX domain sockets in listeners on Linux-like
   systems

-  Fixes for several community-reported bugs


**********************
Metrics and Statistics
**********************

With 1.28, the Unit API has a new endpoint available; the :samp:`/status`
endpoint is exposed at the root level, as with the :samp:`/config` and
:samp:`/certificates` endpoints:

.. code-block:: console

   curl --unix-socket /var/run/control.unit.sock http://localhost

.. code-block:: json

   {
       "config": {
           "listeners": {
           },

           "applications": {
           }
       },

       "status": {
           "connections": {
               "accepted": 0,
               "active": 0,
               "idle": 0,
               "closed": 0
           },

           "requests": {
               "total": 0
           },

           "applications": {}
       }
   }

The :samp:`status` object contains three nested objects:

- The :samp:`connections` object provides detailed information about the client
  connections to the Unit instance or, specifically, to its listeners.  Here,
  :samp:`accepted` and :samp:`closed` are total values accumulated over the
  instance's lifetime; restarting Unit resets the total values.

- In contrast, :samp:`active` and :samp:`idle` are spot values representing the
  number of active or idle requests at one of the listeners that Unit exposes.

The :samp:`requests` object holds the total number of requests to all exposed
listeners since the last restart.

.. note::

   Both :samp:`connections` and :samp:`requests` count requests to Unit's
   listeners, NOT the config API itself.

- The :samp:`applications` section follows the :samp:`/config/applications`
  tree in the API; again, there's no special setup required because Unit
  automatically maintains per-app metrics for all applications in
  :samp:`/config/applications`, and the apps' names identify them respectively.

Consider the following applications configuration as an example:

.. code-block:: json

   {
       "my-app":{
           "type": "external",
           "working_directory": "/www/chat",
           "executable": "bin/chat_app",
           "processes":{
               "max": 10,
               "spare": 5,
               "idle_timeout": 20
           }
       }
   }

The interesting part is the :samp:`processes` configuration. We defined a
maximum of 10 and a spare number of 5 processes; the :samp:`idle_timeout` is 20
seconds. After a couple of requests, let's look at the app statistics:

.. code-block:: json

   {
       "my-app":{
           "processes":{
               "running": 9,
               "starting": 0,
               "idle": 2
           },

           "requests":{
               "active": 9
           }
       }
   }

Knowing the process configuration of :samp:`my-app`, this is quite easy to
understand. Currently, there are 9 out of 10 total processes running, while 0
are currently starting. The two idles are inactive app processes that have not
reached the :samp:`idle_timeout` yet; these will be removed when the configured
timeout of 20 seconds elapses, so the number of running processes will drop to
7.

But what would the stats look like if the app gets no more requests or isn't
able to handle the incoming traffic with the minimum number of configured
processes?

.. code-block:: json

   {
       "my-app":{
           "processes":{
               "running": 5,
               "starting": 0,
               "idle": 0
           },
           "requests":{
               "active": 1
           }
       }
   }

Correct! The number of currently running processes matches the :samp:`spare`
configuration defined in :samp:`applications/my-app/processes/spare`.

So, with Unit 1.28, you now can see your basic workload and process statistics
for the Unit instance itself as well as individual applications. This is but a
first, very important step to increased visibility for us.


*******************************************
More Variables and Access Log Customization
*******************************************

Another noteworthy development is all about variables. First, 1.28.0 adds a
few, namely:

.. code-block:: none

   $remote_addr, $time_local, $request_line, $status,
   $body_bytes_sent, $header_referer, $header_user_agent

Most are self-explanatory but note that some are populated from the
response, such as :samp:`$status` or :samp:`$body_bytes_sent`. That comes in
handy with another new feature, the custom access log format:

.. code-block:: json

   {
       "access_log":{
           "path":"/var/log/unit/access.log",
           "format":"$remote_addr - - [$time_local] \"$request_line\" $status $body_bytes_sent \"$header_referer\" \"$header_user_agent\""
       }
   }

The :samp:`access_log` option can be set to an object that defines both the log
path and the entry structure, so you can go beyond the combined log format and
choose XML or JSON for your log if you like.

Finally, request arguments, cookies, and headers are now also exposed as
dynamic variables: for instance, a query string of :samp:`Type=car&Color=red`
results in two argument variables, :samp:`$arg_Type` and :samp:`$arg_Color`.


**********************************
X-Forwarded-\* Headers Replacement
**********************************

When passing an incoming request to a Unit language module, we build an
internal context to store all information related to the request, including the
client's IP and the protocol used (plain-text HTTP or encrypted HTTPS).  When
there is no caching layer or reverse proxy in front of Unit, this
information stays correct (as it's included in the request), but that
changes when a proxy or a cache stands between the client and Unit.

In that case, the client's IP will always be the IP address of the proxy/cache
server, and the same applies to the protocol. If the connection from the client
to this server uses HTTPS, but it's HTTP all the way to Unit, we have to tell
the app: "Hey, the protocol we use to talk to the client is actually HTTPS.
Keep this in mind when building links and routes internally." That's where the
:samp:`X-Forwarded-*` `header fields
<https://www.rfc-editor.org/rfc/rfc7239.html>`__ come into play.

To extend Unit's capabilities, we've added support for protocol replacement in
version 1.28; now you can configure client IPs and protocol replacement in your
listeners' configuration:

.. code-block:: json

    {
        "listeners":{
            "*:80":{
                "pass":"routes/my-app",
                "forwarded":{
                    "client_ip":"X-Forwarded-For",
                    "protocol":"X-Forwarded-Proto",
                    "recursive":false,
                    "source":[
                        "198.51.100.1-198.51.100.254",
                        "!198.51.100.128/26",
                        "203.0.113.195"
                    ]
                }
            }
        },

        "routes":{
            "my-app":[
                {
                    "action":{
                        "return":200
                    }
                }
            ]
        },

        "applications":{}
    }

The configuration above shows the **new syntax** to configure the replacement;
the old :samp:`client_ip` syntax will still work but is now deprecated and will
be removed in a future release (no sooner than version 1.30).

We have wrapped :samp:`client_ip` and :samp:`protocol` in a new object, while
the :samp:`recursive` and :samp:`source` options stay the same; the IPs in
:samp:`source` are now valid for all replacements in :samp:`forwarded`.

Another use case for header replacement was prompted by a community-reported
issue; now, we have enhanced the support for header replacement in combination
with UNIX domain sockets:

.. code-block:: json

   {
       "listeners":{
           "unix:@socket":{
               "pass":"routes/my-app",
               "forwarded":{
                   "client_ip":"X-Forwarded-For",
                   "protocol":"X-Forwarded-Proto",
                   "recursive":false,
                   "source":[
                       "unix",
                       "198.51.100.1"
                   ]
               }
           }
       },

       "routes":{
           "my-app":[
               {
                   "action":{
                       "return":200
                   }
               }
           ]
       },

       "applications":{}
   }

The :samp:`source` can include :samp:`unix` to trigger replacement if the
request was made via a socket, like this:

.. code-block:: console

   curl -H "X-Forwarded-For: 192.168.10.100" --abtract-unix-socket socket http://localhost

Are you intrigued by the whole socket listener thing here?  Read on!


****************************
Abstract UNIX Domain Sockets
****************************

To put it simply, using traditional UNIX sockets with Unit listeners has a few
trade-offs that we weren't ready to accept. Still, there's a viable option for
Linux-like systems, namely, the abstract UNIX sockets!  They aren't tied to the
file system, so they don't carry the overhead of handling the socket files. In
turn, this places them quite nicely for use with Unit listeners, so here we
are:

.. code-block:: json

   {
       "listeners": {
           "unix:@socket": {
               "pass": "routes/sockets"
           },

           "unix:@/test/123": {
               "pass": "routes/sockets"
           }
    },

    "routes": {
        "sockets": [
            {
                "action": {
                    "return": 200
                }
            }
        ]
    },

    "applications": {}
   }

Unlike file-based UNIX sockets, abstract sockets are automatically
cleaned up by the Linux kernel when nobody is using them. If you find
yourself with untidy UNIX sockets on the filesystem then give abstract
sockets a try, but note that this is a Linux-only feature (does not work
on BSD systems).


**************
Full Changelog
**************

.. code-block:: none

   Changes with Unit 1.28.0                                         13 Sep 2022

       *) Change: increased the applications' startup timeout.

       *) Change: disallowed abstract Unix domain socket syntax in non-Linux
          systems.

       *) Feature: basic statistics API.

       *) Feature: customizable access log format.

       *) Feature: more HTTP variables support.

       *) Feature: forwarded header to replace client address and protocol.

       *) Feature: ability to get dynamic variables.

       *) Feature: support for abstract Unix sockets.

       *) Feature: support for Unix sockets in address matching.

       *) Feature: the $dollar variable translates to a literal "$" during
          variable substitution.

       *) Bugfix: router process could crash if index file didn't contain an
          extension.

       *) Bugfix: force SCRIPT_NAME in Ruby to always be an empty string.

       *) Bugfix: when isolated PID numbers reach the prototype process host
          PID, the prototype crashed.

       *) Bugfix: the Ruby application process could crash on SIGTERM.

       *) Bugfix: the Ruby application process could crash on SIGINT.

       *) Bugfix: mutex leak in the C API.


****************
Platform Updates
****************

Docker Images
*************

-  The Unit JSC11 image is now based on :samp:`eclipse-temurin` instead of
   :samp:`openjdk`

-  Go version bump: 1.18 → 1.19

-  Perl version bump: 5.34 → 5.36

Wbr, Timo & the Unit team
