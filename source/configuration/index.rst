.. meta::
   :og:description: Create and maintain a working configuration using
                  listeners, routes, apps, and upstreams.

.. include:: ../include/replace.rst

#############
Configuration
#############

The **/config** section of the
:ref:`control API <configuration-api>`
handles Unit's general configuration with entities such as
:ref:`listeners <configuration-listeners>`,
:ref:`routes <configuration-routes>`,
:ref:`applications <configuration-applications>`,
or
:ref:`upstreams <configuration-upstreams>`.

.. _configuration-listeners:

*********
Listeners
*********

To accept requests,
add a listener object in the **config/listeners** API section;
the object's name can be:

- A unique IP socket:
  **127.0.0.1:80**, **[::1]:8080**

- A wildcard that matches any host IPs on the port:
  ***:80**

- On Linux-based systems,
   `abstract UNIX sockets <https://man7.org/linux/man-pages/man7/unix.7.html>`__
   can be used as well:
   **unix:@abstract_socket**.

.. note::

   Also on Linux-based systems,
   wildcard listeners can't overlap with other listeners
   on the same port
   due to rules imposed by the kernel.
   For example, ***:8080** conflicts with **127.0.0.1:8080**;
   in particular,
   this means ***:8080** can't be *immediately* replaced
   by **127.0.0.1:8080**
   (or vice versa)
   without deleting it first.

Unit dispatches the requests it receives
to destinations referenced by listeners.
You can plug several listeners into one destination
or use a single listener
and hot-swap it between multiple destinations.

Available listener options:

.. list-table::
    :header-rows: 1

    * - Option
      - Description

    * - **pass** (required)
      - Destination to which the listener passes incoming requests.
        Possible alternatives:

        - :ref:`Application <configuration-applications>`:
          **applications/qwk2mart**

        - :ref:`PHP target <configuration-php-targets>`
          or
          :ref:`Python target <configuration-python-targets>`:
          **applications/myapp/section**

        - :ref:`Route <configuration-routes>`:
          **routes/route66**, **routes**

        - :ref:`Upstream <configuration-upstreams>`:
          **upstreams/rr-lb**

        The value is
        :ref:`variable <configuration-variables>`
        -interpolated;
        if it matches no configuration entities after interpolation,
        a 404 "Not Found" response is returned.

    * - **forwarded**
      - Object;
        configures client IP address and protocol
        :ref:`replacement <configuration-listeners-forwarded>`.

    * - **tls**
      - Object;
        defines SSL/TLS
        :ref:`settings <configuration-listeners-ssl>`.

    * - **backlog**
      - Integer;
        controls the 'backlog' parameter to the *listen(2)* system-call.
        This essentially limits the number of pending connections waiting
        to be accepted.

        The default varies by system.

        On Linux, FreeBSD, OpenBSD and macOS the default is **-1** which
        means use the OS default. For example. on Linux since 5.4, this is
        **4096** (previously **128**) and on FreeBSD it's **128**.

        On other systems the default is **511**.

        NOTE: Whatever limit you set here will be limited by the OS
        system-wide sysctl. For example. on Linux that is
        **net.core.somaxconn** and on BSD it's **kern.ipc.somaxconn**

        *(since 1.33.0)*

Here, a local listener accepts requests at port 8300
and passes them to the **blogs** app
:ref:`target <configuration-php-targets>`
identified by the **uri**
:ref:`variable <configuration-variables>`.
The wildcard listener on port 8400
relays requests at any host IPs
to the **main**
:ref:`route
<configuration-routes>`:

.. code-block:: json

    {
        "127.0.0.1:8300": {
            "pass": "applications/blogs$uri"
        },

        "*:8400": {
            "pass": "routes/main"
        }
    }

Also, **pass** values can be
`percent encoded
<https://datatracker.ietf.org/doc/html/rfc3986#section-2.1>`__.
For example, you can escape slashes in entity names:

.. code-block:: json

   {
       "listeners": {
            "*:80": {
                "pass": "routes/slashes%2Fin%2Froute%2Fname"
            }
       },

       "routes": {
            "slashes/in/route/name": []
       }
   }

.. _configuration-listeners-ssl:

=====================
SSL/TLS configuration
=====================

The **tls** object provides the following options:

.. list-table::
   :header-rows: 1

   * - Option
     - Description

   * - **certificate** (required)
     - String or an array of strings;
       refers to one or more
       :ref:`certificate bundles <configuration-ssl>`
       uploaded earlier,
       enabling secure communication via the listener.

   * - **conf_commands**
     - Object;
       defines the OpenSSL
       `configuration commands
       <https://www.openssl.org/docs/manmaster/man3/SSL_CONF_cmd.html>`__
       to be set for the listener.

       To have this option,
       Unit must be built and run with OpenSSL 1.0.2+:

       .. code-block:: console

          $ openssl version

                OpenSSL 1.1.1d  10 Sep 2019

       Also, make sure your OpenSSL version supports the commands
       set by this option.

   * - **session**
     - Object; configures the TLS session cache and tickets
       for the listener.

To use a certificate bundle you
:ref:`uploaded <configuration-ssl>`
earlier,
name it in the **certificate** option of the **tls** object:

.. code-block:: json

   {
       "listeners": {
           "127.0.0.1:443": {
               "pass": "applications/wsgi-app",
               "tls": {
                   "certificate": ":nxt_hint:`bundle <Certificate bundle name>`"
               }
           }
       }
   }

.. nxt_details:: Configuring multiple bundles
   :hash: conf-bundles

   Since version 1.23.0,
   Unit supports configuring
   `Server Name Indication (SNI)
   <https://datatracker.ietf.org/doc/html/rfc6066#section-3>`__
   on a listener
   by supplying an array of certificate bundle names
   for the **certificate** option value:

   .. code-block:: json

      {
          "*:443": {
              "pass": "routes",
              "tls": {
                  "certificate": [
                      "bundleA",
                      "bundleB",
                      "bundleC"
                  ]
              }
          }
      }

   - If the connecting client sends a server name,
     Unit responds with the matching certificate bundle.
   - If the name matches several bundles,
     exact matches have priority over wildcards;
     if this doesn't help, the one listed first is used.
   - If there's no match or no server name was sent, Unit uses
     the first bundle on the list.

To set custom OpenSSL
`configuration commands
<https://www.openssl.org/docs/manmaster/man3/SSL_CONF_cmd.html>`__
for a listener,
use the **conf_commands** object in **tls**:

.. code-block:: json

   {
       "tls": {
           "certificate": ":nxt_hint:`bundle <Certificate bundle name>`",
           "conf_commands": {
               "ciphersuites": ":nxt_hint:`TLS_AES_128_GCM_SHA256:TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256 <Mandatory cipher suites as per RFC8446, section 9.1>`",
               "minprotocol": "TLSv1.3"
           }
       }
   }

.. _configuration-listeners-ssl-sessions:

The **session** object in **tls**
configures the session settings of the listener:

.. list-table::
   :header-rows: 1

   * - Option
     - Description

   * - **cache_size**
     - Integer;
       sets the number of sessions in the TLS session cache.

       The default is **0**
       (caching is disabled).

   * - **tickets**
     - Boolean, string, or an array of strings;
       configures TLS session tickets.

       The default is **false**
       (tickets are disabled).

   * - **timeout**
     - Integer;
       sets the session timeout for the TLS session cache.

       When a new session is created,
       its lifetime derives from current time and **timeout**.
       If a cached session is requested past its lifetime,
       it is not reused.

       The default is **300**
       (5 minutes).

Example:

.. code-block:: json

   {
       "tls": {
           "certificate": ":nxt_hint:`bundle <Certificate bundle name>`",
           "session": {
               "cache_size": 10240,
               "timeout": 60,
               "tickets": [
                   "k5qMHi7IMC7ktrPY3lZ+sL0Zm8oC0yz6re+y/zCj0H0/sGZ7yPBwGcb77i5vw6vCx8vsQDyuvmFb6PZbf03Auj/cs5IHDTYkKIcfbwz6zSU=",
                   "3Cy+xMFsCjAek3TvXQNmCyfXCnFNAcAOyH5xtEaxvrvyyCS8PJnjOiq2t4Rtf/Gq",
                   "8dUI0x3LRnxfN0miaYla46LFslJJiBDNdFiPJdqr37mYQVIzOWr+ROhyb1hpmg/QCM2qkIEWJfrJX3I+rwm0t0p4EGdEVOXQj7Z8vHFcbiA="
               ]
           }
       }
   }

The **tickets** option works as follows:

- Boolean values enable or disable session tickets;
  with **true**, a random session ticket key is used:

  .. code-block:: json

     {
         "session": {
             "tickets": :nxt_hint:`true <Enables session tickets>`
         }
     }

- A string enables tickets
  and explicitly sets the session ticket key:

  .. code-block:: json

     {
         "session": {
             ":nxt_hint:`tickets <Enables session tickets, sets a single session ticket key>`": "IAMkP16P8OBuqsijSDGKTpmxrzfFNPP4EdRovXH2mqstXsodPC6MqIce5NlMzHLP"
         }
     }

  This enables ticket reuse in scenarios
  where the key is shared between individual servers.

  .. nxt_details:: Shared key rotation
     :hash: key-rotation

     If multiple Unit instances need to recognize tickets
     issued by each other
     (for example, when running behind a load balancer),
     they should share session ticket keys.

     For example,
     consider three SSH-enabled servers named **unit*.example.com**,
     with Unit installed and identical ***:443** listeners configured.
     To configure a single set of three initial keys on each server:

     .. code-block:: shell

        SERVERS="unit1.example.com
        unit2.example.com
        unit3.example.com"

        KEY1=$(openssl rand -base64 48)
        KEY2=$(openssl rand -base64 48)
        KEY3=$(openssl rand -base64 48)

        for SRV in $SERVERS; do
            ssh :nxt_hint:`root <Assuming Unit runs as root on each server>`@$SRV  \
                curl -X PUT -d '["$KEY1", "$KEY2", "$KEY3"]' --unix-socket :nxt_ph:`/path/to/control.unit.sock <Path to the remote control socket>`  \
                    'http://localhost/config/listeners/*:443/tls/session/tickets/'
        done

     To add a new key on each server:

     .. code-block:: shell

        NEWKEY=$(openssl rand -base64 48)

        for SRV in $SERVERS; do
            ssh :nxt_hint:`root <Assuming Unit runs as root on each server>`@$SRV  \
                curl -X POST -d '\"$NEWKEY\"' --unix-socket :nxt_ph:`/path/to/control.unit.sock <Path to the remote control socket>`  \
                    'http://localhost/config/listeners/*:443/tls/session/tickets/'"
        done

     To delete the oldest key after adding the new one:

     .. code-block:: shell

        for SRV in $SERVERS; do
            ssh :nxt_hint:`root <Assuming Unit runs as root on each server>`@$SRV  \
                curl -X DELETE --unix-socket :nxt_ph:`/path/to/control.unit.sock <Path to the remote control socket>`  \
                    'http://localhost/config/listeners/*:443/tls/session/tickets/0'
        done

     This scheme enables safely sharing session ticket keys
     between individual Unit instances.

  Unit supports AES256 (80-byte keys) or AES128 (48-byte keys);
  the bytes should be encoded in Base64:

  .. code-block:: console

     $ openssl rand -base64 48

           LoYjFVxpUFFOj4TzGkr5MsSIRMjhuh8RCsVvtIJiQ12FGhn0nhvvQsEND1+OugQ7

  .. code-block:: console

     $ openssl rand -base64 80

           GQczhdXawyhTrWrtOXI7l3YYUY98PrFYzjGhBbiQsAWgaxm+mbkm4MmZZpDw0tkK
           YTqYWxofDtDC4VBznbBwTJTCgYkJXknJc4Gk2zqD1YA=

- An array of strings just like the one above:

  .. code-block:: json

     {
         "session": {
             ":nxt_hint:`tickets <Enables session tickets, sets two session ticket keys>`": [
                 "IAMkP16P8OBuqsijSDGKTpmxrzfFNPP4EdRovXH2mqstXsodPC6MqIce5NlMzHLP",
                 "Ax4bv/JvMWoQG+BfH0feeM9Qb32wSaVVKOj1+1hmyU8ORMPHnf3Tio8gLkqm2ifC"
             ]
         }
     }

  Unit uses these keys to decrypt the tickets submitted by clients
  who want to recover their session state;
  the last key is always used to create new session tickets
  and update the tickets created earlier.

  .. note::

     An empty array effectively disables session tickets,
     same as setting **tickets** to **false**.

.. _configuration-listeners-forwarded:

=======================
IP, protocol forwarding
=======================

Unit enables the **X-Forwarded-*** header fields
with the **forwarded** object and its options:

.. list-table::
    :header-rows: 1

    * - Option
      - Description

    * - **source** (required)
      - String or an array of strings;
        defines
        :ref:`address-based patterns
        <configuration-routes-matching-patterns>`
        for trusted addresses.
        Replacement occurs only if the source IP of the request is a
        :ref:`match <configuration-routes-matching-resolution>`.

        A special case here is the **"unix"** string;
        it matches *any* UNIX domain sockets.

    * - **client_ip**
      - String;
        names the HTTP header fields to expect in the request.
        They should use the
        `X-Forwarded-For
        <https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Forwarded-For>`__
        format where the value is a comma- or space-separated list
        of IPv4s or IPv6s.

    * - **protocol**
      - String;
        defines the relevant HTTP header field to look for in the request.
        Unit expects it to follow the
        `X-Forwarded-Proto
        <https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Forwarded-Proto>`__
        notation,
        with the field value itself
        being **http**, **https**, or **on**.

    * - **recursive**
      - Boolean;
        controls how the **client_ip** fields are traversed.

        The default is **false**
        (no recursion).

.. note::

   Besides **source**,
   the **forwarded** object must specify
   **client_ip**, **protocol**, or both.

.. warning::

   Before version 1.28.0,
   Unit provided the **client_ip** object
   that evolved into **forwarded**:

   .. list-table::
       :header-rows: 1

       * - **client_ip** (pre-1.28.0)
         - **forwarded** (post-1.28.0)

       * - **header**
         - **client_ip**

       * - **recursive**
         - **recursive**

       * - **source**
         - **source**

       * - N/A
         - **protocol**

   This old syntax still works but will be eventually deprecated,
   though not earlier than version 1.30.0.


When **forwarded** is set,
Unit respects the appropriate header fields
only if the immediate source IP of the request
:ref:`matches <configuration-routes-matching-resolution>`
the **source** option.
Mind that it can use not only subnets but any
:ref:`address-based patterns <configuration-routes-matching-patterns>`:

.. code-block:: json

   {
       "forwarded": {
           "client_ip": "X-Forwarded-For",
           "source": [
               ":nxt_hint:`198.51.100.1-198.51.100.254 <Ranges can be specified explicitly>`",
               ":nxt_hint:`!198.51.100.128/26 <Negation rejects any addresses originating here>`",
               ":nxt_hint:`203.0.113.195 <Individual addresses are supported as well>`"
           ]
       }
   }

.. _configuration-listeners-xfp:

Overwriting protocol scheme
***************************

The **protocol** option enables overwriting
the incoming request's protocol scheme
based on the header field it specifies.
Consider the following **forwarded** configuration:

.. code-block:: json

   {
       "forwarded": {
           "protocol": "X-Forwarded-Proto",
           "source": [
               "192.0.2.0/24",
               "198.51.100.0/24"
           ]
       }
   }

Suppose a request arrives with the following header field:

.. code-block:: none

   X-Forwarded-Proto: https

If the source IP of the request matches **source**,
Unit handles this request as an **https** one.

.. _configuration-listeners-xff:

Originating IP identification
*****************************

Unit also supports identifying the clients' originating IPs
with the **client_ip** option:

.. code-block:: json

   {
       "forwarded": {
           "client_ip": "X-Forwarded-For",
           "recursive": false,
           "source": [
               "192.0.2.0/24",
               "198.51.100.0/24"
           ]
       }
   }

Suppose a request arrives with the following header fields:

.. code-block:: none

   X-Forwarded-For: 192.0.2.18
   X-Forwarded-For: 203.0.113.195, 198.51.100.178

If **recursive** is set to **false**
(default),
Unit chooses the *rightmost* address of the *last* field
named in **client_ip**
as the originating IP of the request.
In the example,
it's set to 198.51.100.178 for requests from 192.0.2.0/24 or 198.51.100.0/24.

If **recursive** is set to **true**,
Unit inspects all **client_ip** fields in reverse order.
Each is traversed from right to left
until the first non-trusted address;
if found, it's chosen as the originating IP.
In the previous example with **"recursive": true**,
the client IP would be set to 203.0.113.195
because 198.51.100.178 is also trusted;
this simplifies working behind multiple reverse proxies.


.. _configuration-routes:

******
Routes
******

The **config/routes** configuration entity
defines internal request routing.
It receives requests
from :ref:`listeners <configuration-listeners>`
and filters them through
:ref:`sets of conditions <configuration-routes-matching>`
to be processed by
:ref:`apps <configuration-applications>`,
:ref:`proxied <configuration-proxy>`
to external servers or
:ref:`load-balanced <configuration-upstreams>`
between them,
served with
:ref:`static content <configuration-static>`,
:ref:`answered <configuration-return>`
with arbitrary status codes, or
:ref:`redirected <configuration-return>`.

In its simplest form,
**routes** is an array
that defines a single route:

.. code-block:: json

   {
        "listeners": {
            "*:8300": {
                "pass": "routes"
            }
        },

        ":nxt_hint:`routes <Array-mode routes, simply referred to as 'routes'>`": [
            ":nxt_ph:`... <Any acceptable route array may go here; see the 'Route Steps' section for details>`"
        ]
   }

Another form is an object
with one or more named route arrays as members:

.. code-block:: json

   {
        "listeners": {
            "*:8300": {
                "pass": "routes/main"
            }
        },

        "routes": {
            ":nxt_hint:`main <Named route, referred to as 'routes/main'>`": [
                ":nxt_ph:`... <Any acceptable route array may go here; see the 'Route Steps' section for details>`"
            ],

            ":nxt_hint:`route66 <Named route, referred to as 'routes/route66'>`": [
                ":nxt_ph:`... <Any acceptable route array may go here; see the 'Route Steps' section for details>`"
            ]
        }
   }


.. _configuration-routes-step:

===========
Route steps
===========

A
:ref:`route <configuration-routes>`
array contains step objects as elements;
they accept the following options:

.. list-table::
   :header-rows: 1

   * - Option
     - Description

   * - **action** (required)
     - Object;
       defines how matching requests are
       :ref:`handled <configuration-routes-action>`.

   * - **match**
     - Object;
       defines the step's
       :ref:`conditions <configuration-routes-matching>`
       to be matched.

A request passed to a route traverses its steps sequentially:

- If all **match** conditions in a step are met,
  the traversal ends
  and the step's **action** is performed.

- If a step's condition isn't met,
  Unit proceeds to the next step of the route.

- If no steps of the route match,
  a 404 "Not Found" response is returned.

.. warning::

  If a step omits the **match** option,
  its **action** occurs automatically.
  Thus, use no more than one such step per route,
  always placing it last to avoid potential routing issues.

.. nxt_details:: Ad-Hoc examples
   :hash: conf-route-examples

   A basic one:

   .. code-block:: json

      {
          "routes": [
              {
                  "match": {
                      "host": "example.com",
                      "scheme": "https",
                      "uri": "/php/*"
                  },

                  "action": {
                      "pass": "applications/php_version"
                  }
              },
              {
                  "action": {
                      "share": "/www/static_version$uri"
                  }
              }
          ]
      }

   This route passes all HTTPS requests
   to the **/php/** subsection of the **example.com** website
   to the **php_version** app.
   All other requests are served with static content
   from the **/www/static_version/** directory.
   If there's no matching content,
   a 404 "Not Found" response is returned.

   A more elaborate example with chained routes and proxying:

   .. code-block:: json

      {
          "routes": {
              "main": [
                  {
                      "match": {
                          "scheme": "http"
                      },

                      "action": {
                          "pass": "routes/http_site"
                      }
                  },
                  {
                      "match": {
                          "host": "blog.example.com"
                      },

                      "action": {
                          "pass": "applications/blog"
                      }
                  },
                  {
                      "match": {
                          "uri": [
                              "*.css",
                              "*.jpg",
                              "*.js"
                          ]
                      },

                      "action": {
                          "share": "/www/static$uri"
                      }
                  }
              ],

              "http_site": [
                  {
                      "match": {
                          "uri": "/v2_site/*"
                      },

                      "action": {
                          "pass": "applications/v2_site"
                      }
                  },
                  {
                      "action": {
                          "proxy": "http://127.0.0.1:9000"
                      }
                  }
              ]
          }
      }

   Here, a route called **main** is explicitly defined,
   so **routes** is an object instead of an array.
   The first step of the route passes all HTTP requests
   to the **http_site** app.
   The second step passes all requests
   that target **blog.example.com**
   to the **blog** app.
   The final step serves requests for certain file types
   from the **/www/static/** directory.
   If no steps match,
   a 404 "Not Found" response is returned.


.. _configuration-routes-matching:

===================
Matching conditions
===================

Conditions in a
:ref:`route step <configuration-routes-step>`'s
**match** object
define patterns to be compared to the request's properties:

.. list-table::
   :header-rows: 1

   * - Property
     - Patterns Are Matched Against
     - Case |-| :nxt_hint:`Sensitive <For arguments, cookies, and headers, this
       relates to property names and values; for other properties, case
       sensitivity affects only values>`

   * - **arguments**
     - Arguments supplied with the request's
       `query string
       <https://datatracker.ietf.org/doc/html/rfc3986#section-3.4>`__;
       these names and value pairs are
       `percent decoded
       <https://datatracker.ietf.org/doc/html/rfc3986#section-2.1>`__,
       with plus signs
       (**+**)
       replaced by spaces.
     - Yes

   * - **cookies**
     - Cookies supplied with the request.
     - Yes

   * - **destination**
     - Target IP address and optional port of the request.
     - No

   * - **headers**
     - `Header fields
       <https://datatracker.ietf.org/doc/html/rfc9110#section-6.3>`__
       supplied with the request.
     - No

   * - **host**
     - **Host**
       `header field
       <https://datatracker.ietf.org/doc/html/rfc9110#section-7.2>`__,
       converted to lower case and normalized
       by removing the port number and the trailing period
       (if any).
     - No

   * - **method**
     - `Method <https://datatracker.ietf.org/doc/html/rfc7231#section-4>`__
       from the request line,
       uppercased.
     - No

   * - **query**
     - `Query string
       <https://datatracker.ietf.org/doc/html/rfc3986#section-3.4>`__,
       `percent decoded
       <https://datatracker.ietf.org/doc/html/rfc3986#section-2.1>`__,
       with plus signs
       (**+**)
       replaced by spaces.
     - Yes

   * - **scheme**
     - URI
       `scheme
       <https://www.iana.org/assignments/uri-schemes/uri-schemes.xhtml>`__.
       Accepts only two patterns,
       either **http** or **https**.
     - No

   * - **source**
     - Source IP address and optional port of the request.
     - No

   * - **uri**
     - `Request target
       <https://datatracker.ietf.org/doc/html/rfc9110#target.resource>`__,
       `percent decoded
       <https://datatracker.ietf.org/doc/html/rfc3986#section-2.1>`__
       and normalized
       by removing the
       `query string
       <https://datatracker.ietf.org/doc/html/rfc3986#section-3.4>`__
       and resolving
       `relative references
       <https://datatracker.ietf.org/doc/html/rfc3986#section-4.2>`__
       ("." and "..", "//").
     - Yes

.. nxt_details:: Arguments vs. query
   :hash: args-vs-query

   Both **arguments** and **query** operate on the query string,
   but **query** is matched against the entire string
   whereas **arguments** considers only the key-value pairs
   such as **key1=4861&key2=a4f3**.

   Use **arguments** to define conditions
   based on key-value pairs in the query string:

   .. code-block:: json

      "arguments": {
         "key1": "4861",
         "key2": "a4f3"
      }

   Argument order is irrelevant:
   **key1=4861&key2=a4f3** and **key2=a4f3&key1=4861**
   are considered the same.
   Also, multiple occurrences of an argument must all match,
   so **key=4861&key=a4f3** matches this:

   .. code-block:: json

      "arguments":{
          "key": "*"
      }

   But not this:

   .. code-block:: json

      "arguments":{
          "key": "a*"
      }

   To the contrary,
   use **query**
   if your conditions concern query strings
   but don't rely on key-value pairs:

   .. code-block:: json

      "query": [
          "utf8",
          "utf16"
      ]

   This only matches query strings
   of the form
   **https://example.com?utf8** or **https://example.com?utf16**.


.. _configuration-routes-matching-resolution:

Match resolution
****************

To be a match,
the property must meet two requirements:

- If there are patterns without negation
  (the **!** prefix),
  at least one of them matches the property value.

- No negated patterns match the property value.

.. nxt_details:: Formal explanation
   :hash: pattern-set-theory

   This logic can be described with set operations.
   Suppose set *U* comprises all possible values of a property;
   set *P* comprises strings that match any patterns without negation;
   set *N* comprises strings that match any negation-based patterns.
   In this scheme,
   the matching set is:

   | *U* ∩ *P* \\ *N* if *P* ≠ ∅
   | *U* \\ *N* if *P* = ∅

Here, the URI of the request must fit **pattern3**,
but must not match **pattern1** or **pattern2**:

.. code-block:: json

   {
       "match": {
           "uri": [
               "!pattern1",
               "!pattern2",
               "pattern3"
           ]
       },

       "action": {
           "pass": ":nxt_ph:`... <Any acceptable 'pass' value may go here; see the 'Listeners' section for details>`"
       }
   }

Additionally, special matching logic applies to
**arguments**, **cookies**, and **headers**.
Each of these can be either
a single object that lists custom-named properties and their patterns
or an array of such objects.

To match a single object,
the request must match *all* properties named in the object.
To match an object array,
it's enough to match *any* single one of its item objects.
The following condition matches only
if the request arguments include **arg1** and **arg2**,
and both match their patterns:

.. code-block:: json

   {
       "match": {
           "arguments": {
               "arg1": "pattern",
               "arg2": "pattern"
           }
       },

       "action": {
           "pass": ":nxt_ph:`... <Any acceptable 'pass' value may go here; see the 'Listeners' section for details>`"
       }
   }

With an object array,
the condition matches
if the request's arguments include
**arg1** or **arg2**
(or both)
that matches the respective pattern:

.. code-block:: json

   {
       "match": {
           "arguments": [
               {
                   "arg1": "pattern"
               },
               {
                   "arg2": "pattern"
               }
           ]
       },

       "action": {
           "pass": ":nxt_ph:`... <Any acceptable 'pass' value may go here; see the 'Listeners' section for details>`"
       }
   }

The following example combines all matching types.
Here, **host**, **method**, **uri**,
**arg1** *and* **arg2**,
either **cookie1** or **cookie2**,
and either **header1** or **header2** *and* **header3**
must be matched
for the **action** to be taken
(**host & method & uri & arg1 & arg2 & (cookie1 | cookie2)
& (header1 | (header2 & header3))**):

.. code-block:: json

   {
       "match": {
           "host": "pattern",
           "method": "!pattern",
           "uri": [
               "pattern",
               "!pattern"
           ],

           "arguments": {
               "arg1": "pattern",
               "arg2": "!pattern"
           },

           "cookies": [
               {
                   "cookie1": "pattern",
               },
               {
                   "cookie2": "pattern",
               }
           ],

           "headers": [
               {
                   "header1": "pattern",
               },
               {
                   "header2": "pattern",
                   "header3": "pattern"
               }
           ]
       },

       "action": {
           "pass": ":nxt_ph:`... <Any acceptable 'pass' value may go here; see the 'Listeners' section for details>`"
       }
   }

.. nxt_details:: Object pattern examples
   :hash: conf-obj-pattern-examples

   This requires **mode=strict**
   and any **access** argument other than **access=full**
   in the URI query:

   .. code-block:: json

      {
          "match": {
              "arguments": {
                  "mode": "strict",
                  "access": "!full"
              }
          },

          "action": {
              "pass": ":nxt_ph:`... <Any acceptable 'pass' value may go here; see the 'Listeners' section for details>`"
          }
      }

   This matches requests that
   either use **gzip** and identify as **Mozilla/5.0**
   or list **curl** as the user agent:

   .. code-block:: json

      {
          "match": {
              "headers": [
                  {
                      "Accept-Encoding": "*gzip*",
                      "User-Agent": "Mozilla/5.0*"
                  },
                  {
                      "User-Agent": "curl*"
                  }
              ]
          },

          "action": {
              "pass": ":nxt_ph:`... <Any acceptable 'pass' value may go here; see the 'Listeners' section for details>`"
          }
      }


.. _configuration-routes-matching-patterns:

Pattern syntax
**************

Individual patterns can be
address-based
(**source** and **destination**)
or string-based
(other properties).

String-based patterns must match the property to a character;
wildcards or
:nxt_hint:`regexes <Available only if Unit was built with PCRE support enabled,
which is the default for the official packages>`
modify this behavior:

- A wildcard pattern may contain any combination of wildcards
  (*****),
  each standing for an arbitrary number of characters:
  **How*s*that*to*you**.

.. _configuration-routes-matching-patterns-regex:

- A regex pattern starts with a tilde
  (**~**):
  **~^\\d+\\.\\d+\\.\\d+\\.\\d+**
  (escaping backslashes is a
  `JSON requirement <https://www.json.org/json-en.html>`_).
  The regexes are
  `PCRE <https://www.pcre.org/current/doc/html/pcre2syntax.html>`_-flavored.

.. nxt_details:: Percent encoding in arguments, query, and URI patterns
   :hash: percent-encoding

   Argument names, non-regex string patterns in **arguments**,
   **query**, and **uri** can be
   `percent encoded
   <https://datatracker.ietf.org/doc/html/rfc3986#section-2.1>`__
   to mask special characters
   (**!** is **%21**, **~** is **%7E**,
   ***** is **%2A**, **%** is **%25**)
   or even target single bytes.
   For example, you can select diacritics such as Ö or Å
   by their starting byte **0xC3** in UTF-8:

   .. code-block:: json

      {
          "match": {
              "arguments": {
                  "word": "*%C3*"
              }
          },

          "action": {
              "pass": ":nxt_ph:`... <Any acceptable 'pass' value may go here; see the 'Listeners' section for details>`"
          }
      }

   Unit decodes such strings
   and matches them against respective request entities,
   decoding these as well:

   .. code-block:: json

      {
          "routes": [
              {
                  "match": {
                      "query": ":nxt_ph:`%7E <Tilde>`fuzzy word search"
                  },

                  "action": {
                      "return": 200
                  }
              }
          ]
      }

   This condition matches the following percent-encoded request:

   .. subs-code-block:: console

      $ curl http://127.0.0.1/?~fuzzy:nxt_ph:`%20 <Space>`word:nxt_ph:`%20 <Space>`search -v

            > GET /?~fuzzy%20word%20search HTTP/1.1
            ...
            < HTTP/1.1 200 OK
            ...

   Note that the encoded spaces
   (**%20**)
   in the request
   match their unencoded counterparts in the pattern;
   vice versa, the encoded tilde
   (**%7E**)
   in the condition matches **~** in the request.


.. nxt_details:: String pattern examples
   :hash: conf-str-pattern-examples

   A regular expression that matches any **.php** files
   in the **/data/www/** directory and its subdirectories.
   Note the backslashes;
   escaping is a JSON-specific requirement:

   .. code-block:: json

      {
          "match": {
              "uri": "~^/data/www/.*\\.php(/.*)?$"
          },

          "action": {
              "pass": ":nxt_ph:`... <Any acceptable 'pass' value may go here; see the 'Listeners' section for details>`"
          }
      }

   Only subdomains of **example.com** match:

   .. code-block:: json

      {
          "match": {
              "host": "*.example.com"
          },

          "action": {
              "pass": ":nxt_ph:`... <Any acceptable 'pass' value may go here; see the 'Listeners' section for details>`"
          }
      }

   Only requests for **.php** files
   located in **/admin/**'s subdirectories
   match:

   .. code-block:: json

      {
          "match": {
              "uri": "/admin/*/*.php"
          },

          "action": {
              "pass": ":nxt_ph:`... <Any acceptable 'pass' value may go here; see the 'Listeners' section for details>`"
          }
      }

   Here, any **eu-** subdomains of **example.com** match
   except **eu-5.example.com**:

   .. code-block:: json

      {
          "match": {
              "host": [
                  "eu-*.example.com",
                  "!eu-5.example.com"
              ]
          },

          "action": {
              "pass": ":nxt_ph:`... <Any acceptable 'pass' value may go here; see the 'Listeners' section for details>`"
          }
      }

   Any methods match
   except **HEAD** and **GET**:

   .. code-block:: json

      {
          "match": {
              "method": [
                  "!HEAD",
                  "!GET"
              ]
          },

          "action": {
              "pass": ":nxt_ph:`... <Any acceptable 'pass' value may go here; see the 'Listeners' section for details>`"
          }
      }

   You can also combine certain special characters in a pattern.
   Here, any URIs match
   except the ones containing **/api/**:

   .. code-block:: json

      {
          "match": {
              "uri": "!*/api/*"
          },

          "action": {
              "pass": ":nxt_ph:`... <Any acceptable 'pass' value may go here; see the 'Listeners' section for details>`"
          }
      }

   Here, URIs of any articles
   that don't look like **YYYY-MM-DD** dates
   match.
   Again, note the backslashes;
   they are a JSON requirement:

   .. code-block:: json

      {
          "match": {
              "uri": [
                  "/articles/*",
                  "!~/articles/\\d{4}-\\d{2}-\\d{2}"
              ]
          },

          "action": {
              "pass": ":nxt_ph:`... <Any acceptable 'pass' value may go here; see the 'Listeners' section for details>`"
          }
      }

Address-based patterns define individual IPv4
(dot-decimal or
`CIDR
<https://datatracker.ietf.org/doc/html/rfc4632>`__),
IPv6 (hexadecimal or
`CIDR
<https://datatracker.ietf.org/doc/html/rfc4291#section-2.3>`__),
or any
`UNIX domain socket <https://en.wikipedia.org/wiki/Unix_domain_socket>`__
addresses
that must exactly match the property;
wildcards and ranges modify this behavior:

- Wildcards
  (*****)
  can only match arbitrary IPs
  (***:<port>**).

- Ranges
  (**-**)
  work with both IPs
  (in respective notation)
  and ports
  (**<start_port>-<end_port>**).

.. nxt_details:: Address-based allow-deny lists
   :hash: allow-deny

   Addresses come in handy
   when implementing an allow-deny mechanism
   with routes,
   for instance:

   .. code-block:: json

      "routes": [
          {
              "match": {
                  "source": [
                      "!192.168.1.1",
                      "!10.1.1.0/16",
                      "192.168.1.0/24",
                      "2001:0db8::/32"
                  ]
              },

              "action": {
                  "share": "/www/data$uri"
              }
          }
      ]

   See
   :ref:`here <configuration-routes-matching-resolution>`
   for details of pattern resolution order;
   this corresponds to the following :program:`nginx` directive:

   .. code-block:: nginx

      location / {
          deny  10.1.1.0/16;
          deny  192.168.1.1;
          allow 192.168.1.0/24;
          allow 2001:0db8::/32;
          deny  all;

          root /www/data;
      }

.. nxt_details::  Address pattern examples
   :hash: conf-addr-pattern-examples

   This uses IPv4-based matching with wildcards and ranges:

   .. code-block:: json

      {
          "match": {
              "source": [
                  "192.0.2.1-192.0.2.200",
                  "198.51.100.1-198.51.100.200:8000",
                  "203.0.113.1-203.0.113.200:8080-8090",
                  "*:80"
              ],

              "destination": [
                  "192.0.2.0/24",
                  "198.51.100.0/24:8000",
                  "203.0.113.0/24:8080-8090",
                  "*:80"
              ]
          },

          "action": {
              "pass": ":nxt_ph:`... <Any acceptable 'pass' value may go here; see the 'Listeners' section for details>`"
          }
      }

   This uses IPv6-based matching with wildcards and ranges:

   .. code-block:: json

      {
          "match": {
              "source": [
                   "2001:0db8::-2001:0db8:aaa9:ffff:ffff:ffff:ffff:ffff",
                   "[2001:0db8:aaaa::-2001:0db8:bbbb::]:8000",
                   "[2001:0db8:bbbb::1-2001:0db8:cccc::]:8080-8090",
                   "*:80"
              ],

              "destination": [
                   "2001:0db8:cccd::/48",
                   "[2001:0db8:ccce::/48]:8000",
                   "[2001:0db8:ccce:ffff::/64]:8080-8090",
                   "*:80"
              ]
          },

          "action": {
              "pass": ":nxt_ph:`... <Any acceptable 'pass' value may go here; see the 'Listeners' section for details>`"
          }
      }

   This matches any of the listed IPv4 or IPv6 addresses:

   .. code-block:: json

      {
          "match": {
              "destination": [
                  "127.0.0.1",
                  "192.168.0.1",
                  "::1",
                  "2001:0db8:1::c0a8:1"
              ]
          },

          "action": {
              "pass": ":nxt_ph:`... <Any acceptable 'pass' value may go here; see the 'Listeners' section for details>`"
          }
      }

   Here, any IPs from the range match
   except **192.0.2.9**:

   .. code-block:: json

      {
          "match": {
              "source": [
                  "192.0.2.1-192.0.2.10",
                  "!192.0.2.9"
              ]
          },

          "action": {
              "pass": ":nxt_ph:`... <Any acceptable 'pass' value may go here; see the 'Listeners' section for details>`"
          }
      }

   This matches any IPs but limits the acceptable ports:

   .. code-block:: json

      {
          "match": {
              "source": [
                  "*:80",
                  "*:443",
                  "*:8000-8080"
              ]
          },

          "action": {
              "pass": ":nxt_ph:`... <Any acceptable 'pass' value may go here; see the 'Listeners' section for details>`"
          }
      }

   This matches any UNIX domain sockets:

   .. code-block:: json

      {
          "match": {
              "source": "unix"
          },

          "action": {
              "pass": ":nxt_ph:`... <Any acceptable 'pass' value may go here; see the 'Listeners' section for details>`"
          }
      }



.. _configuration-routes-action:

================
Handling actions
================

If a request matches all
:ref:`conditions <configuration-routes-matching>`
of a route step
or the step itself omits the **match** object,
Unit handles the request with the respective **action**.
The mutually exclusive **action** types are:

.. list-table::
   :header-rows: 1

   * - Option
     - Description
     - Details

   * - **pass**
     - Destination for the request,
       identical to a listener's **pass** option.
     - :ref:`configuration-listeners`

   * - **proxy**
     - Socket address of an HTTP server
       to where the request is proxied.
     - :ref:`configuration-proxy`

   * - **return**
     - HTTP status code
       with a context-dependent redirect location.
     - :ref:`configuration-return`

   * - **share**
     - File paths that serve the request with static content.
     - :ref:`configuration-static`

An additional option is applicable to any of these actions:

.. list-table::
   :header-rows: 1

   * - Option
     - Description
     - Details

   * - **response_headers**
     - Updates the header fields
       of the upcoming response.
     - :ref:`configuration-response-headers`

   * - **rewrite**
     - Updated the request URI,
       preserving the query string.
     - :ref:`configuration-rewrite`

An example:

.. code-block:: json

   {
       "routes": [
           {
               "match": {
                   "uri": [
                       "/v1/*",
                       "/v2/*"
                   ]
               },

               "action": {
                   "rewrite": "/app/$uri",
                   "pass": "applications/app"
               }
           },
           {
               "match": {
                   "uri": "~\\.jpe?g$"
               },

               "action": {
                   "share": [
                       "/var/www/static$uri",
                       "/var/www/static/assets$uri"
                    ],

                   "fallback": {
                        "pass": "upstreams/cdn"
                   }
               }
           },
           {
               "match": {
                   "uri": "/proxy/*"
               },

               "action": {
                   "proxy": "http://192.168.0.100:80"
               }
           },
           {
               "match": {
                   "uri": "/return/*"
               },

               "action": {
                   "return": 301,
                   "location": "https://www.example.com"
               }
           }
       ]
   }


.. _configuration-variables:
.. _configuration-variables-native:

*********
Variables
*********

Some options in Unit configuration
allow the use of
:ref:`variables <configuration-variables-native>`
whose values are calculated at runtime.
There's a number of built-in variables available:

.. list-table::
   :header-rows: 1

   * - Variable
     - Description

   * - **arg_***, **cookie_***, **header_***
     - Variables that store
       :ref:`request arguments, cookies, and header fields
       <configuration-routes-matching>`,
       such as **arg_queryTimeout**,
       **cookie_sessionId**,
       or **header_Accept_Encoding**.
       The names of the **header_*** variables are case insensitive.

   * - **body_bytes_sent**
     - Number of bytes sent in the response body.

   * - **dollar**
     - Literal dollar sign (**$**),
       used for escaping.

   * - **header_referer**
     - Contents of the **Referer** request
       `header field
       <https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Referer>`__.

   * - **header_user_agent**
     - Contents of the **User-Agent** request
       `header field
       <https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/User-Agent>`__.

   * - **host**
     - **Host**
       `header field
       <https://datatracker.ietf.org/doc/html/rfc9110#section-7.2>`__,
       converted to lower case and normalized
       by removing the port number
       and the trailing period (if any).

   * - **method**
     - `Method <https://datatracker.ietf.org/doc/html/rfc7231#section-4>`__
       from the request line.

   * - **remote_addr**
     - Remote IP address of the request.

   * - **request_id**
     - Contains a string generated with random data. Can be used as a unique
       request identifier.

   * - **request_line**
     - Entire
       `request line
       <https://datatracker.ietf.org/doc/html/rfc9112#section-3>`__.

   * - **request_time**
     - Request processing time in milliseconds,
       formatted as follows:
       **1.234**.

   * - **request_uri**
     - Request target
       `path
       <https://datatracker.ietf.org/doc/html/rfc3986#section-3.3>`__
       *including* the
       `query
       <https://datatracker.ietf.org/doc/html/rfc3986#section-3.4>`__,
       normalized by resolving relative path references
       ("." and "..")
       and collapsing adjacent slashes.

   * - **response_header_***
     - Variables that store
       :ref:`response header fields
       <configuration-response-headers>`,
       such as **response_header_content_type**.
       The names of these variables are case insensitive.

   * - **status**
     - HTTP
       `status code
       <https://datatracker.ietf.org/doc/html/rfc7231#section-6>`__
       of the response.

   * - **time_local**
     - Local time,
       formatted as follows:
       **31/Dec/1986:19:40:00 +0300**.

   * - **uri**
     - Request target
       `path
       <https://datatracker.ietf.org/doc/html/rfc3986#section-3.3>`__
       *without* the `query
       <https://datatracker.ietf.org/doc/html/rfc3986#section-3.4>`__
       part,
       normalized by resolving relative path references
       ("." and "..")
       and collapsing adjacent slashes.
       The value is
       `percent decoded
       <https://datatracker.ietf.org/doc/html/rfc3986#section-2.1>`__:
       Unit interpolates all percent-encoded entities
       in the request target
       `path
       <https://datatracker.ietf.org/doc/html/rfc3986#section-3.3>`__.


These variables can be used with:

- **pass** in
  :ref:`listeners <configuration-listeners>`
  and
  :ref:`actions <configuration-routes-action>`
  to choose between routes, applications, app targets, or upstreams.

- **rewrite** in
  :ref:`actions <configuration-routes-action>`
  to enable :ref:`URI rewriting <configuration-rewrite>`.

- **share** and **chroot** in
  :ref:`actions <configuration-routes-action>`
  to control
  :ref:`static content serving <configuration-static>`.

- **location** in **return**
  :ref:`actions <configuration-return>`
  to enable HTTP redirects.

- **format** in the
  :ref:`access log <configuration-access-log>`
  to customize Unit's log output.


To reference a variable,
prefix its name with the dollar sign character
(**$**),
optionally enclosing the name in curly brackets
(**{}**)
to separate it from adjacent text
or enhance visibility.
Variable names can contain letters and underscores
(**_**),
so use the brackets
if the variable is immediately followed by such characters:

.. code-block:: json

   {
       "listeners": {
           "*:80": {
               "pass": "routes/:nxt_hint:`${method} <The method variable is thus separated from the '_route' postfix>`_route"
           }
       },

       "routes": {
           "GET_route": [
               {
                   "action": {
                       "return": 201
                   }
               }
           ],

           "PUT_route": [
               {
                   "action": {
                       "return": 202
                   }
               }
           ],

           "POST_route": [
               {
                   "action": {
                       "return": 203
                   }
               }
           ]
       }
   }

To reference an **arg_***,
**cookie_***,
or **header_*** variable,
add the name you need to the prefix.
A query string of **Type=car&Color=red**
yields two variables,
**$arg_Type** and **$arg_Color**;
Unit additionally normalizes capitalization and hyphenation
in header field names,
so the **Accept-Encoding** header field
can also be referred to as **$header_Accept_Encoding**,
**$header_accept-encoding**,
or **$header_accept_encoding**.

.. note::

   With multiple argument instances
   (think **Color=Red&Color=Blue**),
   the rightmost one is used (**Blue**).

At runtime,
variables expand into dynamically computed values
(at your risk!).
The previous example targets an entire set of routes,
picking individual ones by HTTP verbs
from the incoming requests:

.. code-block:: console

   $ curl -i -X GET http://localhost

       HTTP/1.1 201 Created

.. code-block:: console

   $ curl -i -X PUT http://localhost

       HTTP/1.1 202 Accepted

.. code-block:: console

   $ curl -i -X POST http://localhost

       HTTP/1.1 203 Non-Authoritative Information

.. code-block:: console

   $ curl -i --head http://localhost  # Bumpy ride ahead, no route defined

       HTTP/1.1 404 Not Found

If you reference a non-existing variable,
it is considered empty.

.. nxt_details:: Examples
   :hash: variables-examples

   This configuration selects the static file location
   based on the requested hostname;
   if nothing's found,
   it attempts to retrieve the requested file
   from a common storage:

   .. code-block:: json

      {
          "listeners": {
              "*:80": {
                  "pass": "routes"
              }
          },

          "routes": [
              {
                  "action": {
                      "share": [
                          "/www/$host:nxt_hint:`$uri <Note that the $uri variable value always includes a starting slash>`",
                          "/www/storage:nxt_hint:`$uri <Note that the $uri variable value always includes a starting slash>`"
                      ]
                  }
              }
          ]
      }

   Another use case is employing the URI
   to choose between applications:

   .. code-block:: json

      {
          "listeners": {
              "*:80": {
                  "pass": "applications:nxt_hint:`$uri <Note that the $uri variable value always includes a starting slash>`"
              }
          },

          "applications": {
              "blog": {
                  "root": "/path/to/blog_app/",
                  "script": "index.php"
              },

              "sandbox": {
                  "type": "php",
                  "root": "/path/to/sandbox_app/",
                  "script": "index.php"
              }
          }
      }

   This way, requests are routed between applications by their target URIs:

   .. code-block:: console

         $ curl http://localhost/blog     # Targets the 'blog' app

   .. code-block:: console

         $ curl http://localhost/sandbox  # Targets the 'sandbox' app

   A different approach puts the **Host** header field
   received from the client
   to the same use:

   .. code-block:: json

      {
          "listeners": {
              "*:80": {
                  "pass": "applications/$host"
              }
          },

          "applications": {
              "localhost": {
                  "root": "/path/to/admin_section/",
                  "script": "index.php"
              },

              "www.example.com": {
                  "type": "php",
                  "root": "/path/to/public_app/",
                  "script": "index.php"
              }
          }
      }

   You can use multiple variables in a string,
   repeating and placing them arbitrarily.
   This configuration picks an app target
   (supported for
   :ref:`PHP <configuration-php-targets>`
   and
   :ref:`Python
   <configuration-python-targets>`
   apps)
   based on the requested hostname and URI:

   .. code-block:: json

      {
          "listeners": {
              "*:80": {
                  "pass": "applications/app_$host:nxt_hint:`$uri <Note that the $uri value doesn't include the request's query part>`"
              }
          }
      }

   At runtime,
   a request for **example.com/myapp**
   is passed to **applications/app_example.com/myapp**.

   To select a share directory
   based on an **app_session** cookie:

   .. code-block:: json

      {
          "action": {
              "share": "/data/www/$cookie_app_session"
          }
      }

   Here, if **$uri** in **share** resolves to a directory,
   the choice of an index file to be served
   is dictated by **index**:

   .. code-block:: json

      {
          "action": {
              "share": "/www/data:nxt_hint:`$uri <Note that the $uri variable value always includes a starting slash>`",
              "index": "index.htm"
          }
      }

   Here, a redirect uses the **$request_uri** variable value
   to relay the request,
   *including* the query part,
   to the same website over HTTPS:

   .. code-block:: json

      {
          "action": {
              "return": 301,
              "location": "https://$host$request_uri"
          }
      }


.. _configuration-rewrite:

***********
URI rewrite
***********

All route step
:ref:`actions <configuration-routes-action>`
support the **rewrite** option
that updates the URI of the incoming request
before the action is applied.
It does not affect the
`query
<https://datatracker.ietf.org/doc/html/rfc3986#section-3.4>`__
but changes the
**uri** and
**$request_uri**
:ref:`variables <configuration-variables>`.

This **match**-less action
prefixes the request URI with **/v1**
and returns it to routing:

.. code-block:: json

   {
       "action": {
           "rewrite": "/v1$uri",
           "pass": "routes"
       }
   }


.. warning::

   Avoid infinite loops
   when you  **pass** requests
   back to **routes**.

This action
normalizes the request URI
and passes it to an application:

.. code-block:: json

   {
       "match": {
           "uri": [
               "/fancyAppA",
               "/fancyAppB"
           ]
       },

       "action": {
           "rewrite": "/commonBackend",
           "pass": "applications/backend"
       }
   }

.. _configuration-response-headers:

****************
Response headers
****************

All route step
:ref:`actions <configuration-routes-action>`
support the **response_headers** option
that updates the header fields of Unit's response
before the action is taken:

.. code-block:: json

   {
       "action": {
           "share": "/www/static/$uri",
           "response_headers": {
               "Cache-Control": "max-age=60, s-maxage=120",
               "CDN-Cache-Control": "max-age=600"
           }
       }
   }

This works only for the **2XX** and **3XX** responses;
also, **Date**, **Server**, and **Content-Length** can't be set.

The option sets given string values
for the header fields of the response
that Unit will send for the specific request:

- If there's no header field associated with the name
  (regardless of the case),
  the value is set.

- If a header field with this name is already set, its value is updated.

- If **null** is supplied for the value, the header field is *deleted*.

If the action is taken and Unit issues a response,
it sends the header fields *this specific* action specifies.
Only the last action
along the entire routing path of a request
affects the resulting response headers.

The values support
:ref:`variables <configuration-variables>`
and
:doc:`template literals <../scripting>`,
which enables arbitrary runtime logic:

.. code-block:: json

   "response_headers": {
       "Content-Language": "`${ uri.startsWith('/uk') ? 'en-GB' : 'en-US' }`"
   }

Finally, there are the **response_header_*** variables
that evaluate to the header field values set with the response
(by the app, upstream, or Unit itself;
the latter is the case with
**$response_header_connection**,
**$response_header_content_length**,
and **$response_header_transfer_encoding**).

One use is to update the headers in the final response;
this extends the **Content-Type** issued by the app:

.. code-block:: json

   "action": {
       "pass": "applications/converter",
           "response_headers": {
               "Content-Type": "${response_header_content_type};charset=iso-8859-1"
           }
       }
   }

Alternatively, they will come in handy with
:ref:`custom log formatting <configuration-access-log>`.


.. _configuration-return:

****************************
Instant responses, redirects
****************************

You can use route step
:ref:`actions <configuration-routes-action>`
to instantly handle certain conditions
with arbitrary
`HTTP status codes
<https://datatracker.ietf.org/doc/html/rfc7231#section-6>`__:

.. code-block:: json

   {
       "match": {
           "uri": "/admin_console/*"
       },

       "action": {
           "return": 403
       }
   }

The **return** action provides the following options:

.. list-table::

   * - **return** (required)
     - Integer (000–999);
       defines the HTTP response status code
       to be returned.

   * - **location**
     - String URI;
       used if the **return** value implies redirection.

Use the codes according to their intended
`semantics
<https://datatracker.ietf.org/doc/html/rfc7231#section-6>`__;
if you use custom codes,
make sure that user agents can understand them.

If you specify a redirect code (3xx),
supply the destination
using the **location** option
alongside **return**:

.. code-block:: json

   {
       "action": {
           "return": 301,
           "location": "https://www.example.com"
       }
   }

Besides enriching the response semantics,
**return** simplifies :ref:`allow-deny lists <allow-deny>`:
instead of guarding each action with a filter,
add
:ref:`conditions <configuration-routes-matching>`
to deny unwanted requests as early as possible,
for example:

.. code-block:: json

    "routes": [
        {
            "match": {
                "scheme": "http"
            },

            "action": {
                "return": 403
            }
        },
        {
            "match": {
                "source": [
                    "!192.168.1.1",
                    "!10.1.1.0/16",
                    "192.168.1.0/24",
                    "2001:0db8::/32"
                ]
            },

            "action": {
                "return": 403
            }
        }
    ]


.. _configuration-static:

************
Static files
************

Unit is capable of acting as a standalone web server,
efficiently serving static files
from the local file system;
to use the feature,
list the file paths
in the **share** option
of a route step
:ref:`action
<configuration-routes-action>`.

A **share**-based action provides the following options:

.. list-table::

   * - **share** (required)
     - String or an array of strings;
       lists file paths that are tried
       until a file is found.
       When no file is found,
       **fallback** is used if set.

       The value is
       :ref:`variable <configuration-variables>`-interpolated.

   * - **index**
     - Filename;
       tried if **share** is a directory.
       When no file is found,
       **fallback** is used if set.

       The default is **index.html**.

   * - **fallback**
     - Action-like :ref:`object <configuration-fallback>`;
       used if the request
       can't be served by **share** or **index**.

   * - **types**
     - :ref:`Array <configuration-share-mime>`
       of
       `MIME type
       <https://www.iana.org/assignments/media-types/media-types.xhtml>`__
       patterns;
       used to filter the shared files.

   * - **chroot**
     - Directory pathname that
       :ref:`restricts <configuration-share-path>`
       the shareable paths.

       The value is
       :ref:`variable <configuration-variables>`-interpolated.

   * - **follow_symlinks**, **traverse_mounts**
     - Booleans;
       turn on and off symbolic link and mount point
       :ref:`resolution <configuration-share-resolution>`
       respectively;
       if **chroot** is set,
       they only
       :ref:`affect <configuration-share-path>`
       the insides of **chroot**.

       The default for both options is **true**
       (resolve links and mounts).

.. note::

   To serve the files,
   Unit's router process must be able to access them;
   thus, the account this process runs as
   must have proper permissions
   :ref:`assigned <security-apps>`.
   When Unit is installed from the
   :ref:`official packages
   <installation-precomp-pkgs>`,
   the process runs as **unit:unit**;
   for details of other installation methods,
   see :doc:`../installation`.

Consider the following configuration:

.. code-block:: json

   {
       "listeners": {
           "*:80": {
               "pass": "routes"
           }
        },

       "routes": [
           {
               "action": {
                   "share": "/www/static/$uri"
               }
           }
       ]
   }

It uses
:ref:`variable interpolation <configuration-variables>`:
Unit replaces the **$uri** reference
with its current value
and tries the resulting path.
If this doesn't yield a servable file,
a 404 "Not Found" response is returned.

.. warning::

   Before version 1.26.0,
   Unit used **share** as the document root.
   This was changed for flexibility,
   so now **share** must resolve to specific files.
   A common solution is
   to append **$uri** to your document root.

   Pre-1.26,
   the snippet above would've looked like this:

   .. code-block:: json

      "action": {
          "share": "/www/static/"
      }

   Mind that URI paths always start with a slash,
   so there's no need to separate the directory
   from **$uri**;
   even if you do, Unit compacts adjacent slashes
   during path resolution,
   so there won't be an issue.

If **share** is an array,
its items are searched in order of appearance
until a servable file is found:

.. code-block:: json

   "share": [
       "/www/$host$uri",
       "/www/error_pages/not_found.html"
   ]

This snippet tries a **$host**-based directory first;
if a suitable file isn't found there,
the **not_found.html** file is tried.
If neither is accessible,
a 404 "Not Found" response is returned.

Finally, if a file path points to a directory,
Unit attempts to serve an **index**-indicated file from it.
Suppose we have the following directory structure
and share configuration:

.. code-block:: none

   /www/static/
   ├── ...
   └──default.html

.. code-block:: json

   "action": {
       "share": "/www/static$uri",
       "index": "default.html"
   }

The following request returns **default.html**
even though the file isn't named explicitly:

.. subs-code-block:: console

   $ curl http://localhost/ -v

    ...
    < HTTP/1.1 200 OK
    < Last-Modified: Fri, 20 Sep 2021 04:14:43 GMT
    < ETag: "5d66459d-d"
    < Content-Type: text/html
    < Server: Unit/|version|
    ...

.. note::

   Unit's ETag response header fields
   use the **MTIME-FILESIZE** format,
   where **MTIME** stands for file modification timestamp
   and **FILESIZE** stands for file size in bytes,
   both in hexadecimal.


.. _configuration-share-mime:

==============
MIME filtering
==============

To filter the files a **share** serves
by their
`MIME types <https://www.iana.org/assignments/media-types/media-types.xhtml>`__,
define a **types** array of string patterns.
They work like
:ref:`route patterns
<configuration-routes-matching-patterns>`
but are compared to the MIME type of each file;
the request is served only if it's a
:ref:`match
<configuration-routes-matching-resolution>`:

.. code-block:: json

   {
       "share": "/www/data/static$uri",
       "types": [
           "!text/javascript",
           "!text/css",
           "text/*",
           "~video/3gpp2?"
       ]
   }

This sample configuration blocks JS and CSS files with
:ref:`negation <configuration-routes-matching-resolution>`
but allows all other text-based MIME types with a
:ref:`wildcard pattern <configuration-routes-matching-patterns>`.
Additionally, the **.3gpp** and **.3gpp2** file types
are allowed by a
:ref:`regex pattern <configuration-routes-matching-patterns>`.

If no MIME types match the request, a 403 "Forbidden" response is
returned. You can pair that behavior with a
:ref:`fallback <configuration-fallback>` option that will be called
when a 40x response would be returned.

.. code-block:: json

    {
        "share": "/www/data/static$uri",
        "types": ["image/*", "font/*", "text/*"],
        "response_headers": {
            "Cache-Control": "max-age=1209600"
        },
        "fallback": {
            "share": "/www/data/static$uri",
        }
    }

Here, all requests to images, fonts, and any text-based files will have
a cache control header added to the response. Any other requests will still
serve the files, but this time without the header. This is useful
for serving common web page resources that do not change; web browsers
and proxies are informed that this content should be cached.

If the MIME type of a requested file isn't recognized,
it's considered empty
(**""**).
Thus, the **"!"** pattern
("deny empty strings")
can be used to restrict all file types
:ref:`unknown <configuration-mime>`
to Unit:

.. code-block:: json

   {
       "share": "/www/data/known-types-only$uri",
       "types": [
           "!"
       ]
   }

If a share path specifies only the directory name,
Unit *doesn't* apply MIME filtering.


.. _configuration-share-path:

=================
Path restrictions
=================

.. note::

   To have these options,
   Unit must be built and run
   on a system with Linux kernel version 5.6+.

The **chroot** option confines the path resolution
within a share to a certain directory.
First, it affects symbolic links:
any attempts to go up the directory tree
with relative symlinks like **../../var/log**
stop at the **chroot** directory,
and absolute symlinks are treated as relative
to this directory to avoid breaking out:

.. code-block:: json

   {
       "action": {
           "share": "/www/data$uri",
           "chroot": ":nxt_hint:`/www/data/ <Now, any paths accessible via the share are confined to this directory>`"
       }
   }

Here, a request for **/log**
initially resolves to **/www/data/log**;
however, if that's an absolute symlink to **/var/log/app.log**,
the resulting path is **/www/data/var/log/app.log**.

Another effect is that any requests
for paths that resolve outside the **chroot** directory
are forbidden:

.. code-block:: json

   {
       "action": {
           "share": "/www$uri",
           "chroot": ":nxt_hint:`/www/data/ <Now, any paths accessible via the share are confined to this directory>`"
       }
   }

Here, a request for **/index.xml**
elicits a 403 "Forbidden" response
because it resolves to **/www/index.xml**,
which is outside **chroot**.

.. _configuration-share-resolution:

The **follow_symlinks** and **traverse_mounts** options
disable resolution of symlinks and traversal of mount points
when set to **false**
(both default to **true**):

.. code-block:: json

   {
       "action": {
           "share": "/www/$host/static$uri",
           "follow_symlinks": :nxt_hint:`false <Disables symlink traversal>`,
           "traverse_mounts": :nxt_hint:`false <Disables mount point traversal>`
       }
   }

Here, any symlink or mount point in the entire **share** path
results in a 403 "Forbidden" response.

With **chroot** set,
**follow_symlinks** and **traverse_mounts**
only affect portions of the path *after* **chroot**:

.. code-block:: json

   {
       "action": {
           "share": "/www/$host/static$uri",
           "chroot": "/www/$host/",
           "follow_symlinks": false,
           "traverse_mounts": false
       }
   }

Here, **www/** and interpolated **$host**
can be symlinks or mount points,
but any symlinks and mount points beyond them,
including the **static/** portion,
won't be resolved.

.. nxt_details:: Details
   :hash: chroot-details

   Suppose you want to serve files from a share
   that itself includes a symlink
   (let's assume **$host** always resolves to **localhost**
   and make it a symlink in our example)
   but disable any symlinks inside the share.

   Initial configuration:

   .. code-block:: json

      {
          "action": {
              "share": "/www/$host/static$uri",
              "chroot": ":nxt_hint:`/www/$host/ <Now, any paths accessible via the share are confined to this directory>`"
          }
      }

   Create a symlink to **/www/localhost/static/index.html**:

   .. code-block:: console

      $ mkdir -p /www/localhost/static/ && cd /www/localhost/static/

   .. code-block:: console

      $ cat > index.html << EOF

            > index.html
            > EOF

   .. code-block:: console

      $ ln -s index.html /www/localhost/static/symlink

   If symlink resolution is enabled
   (with or without **chroot**),
   a request that targets the symlink works:

   .. code-block:: console

      $ curl http://localhost/index.html

            index.html

   .. code-block:: console

      $ curl http://localhost/symlink

            index.html

   Now set **follow_symlinks** to **false**:

   .. code-block:: json

      {
          "action": {
              "share": "/www/$host/static$uri",
              "chroot": ":nxt_hint:`/www/$host/ <Now, any paths accessible via the share are confined to this directory>`",
              "follow_symlinks": false
          }
      }

   The symlink request is forbidden,
   which is presumably the desired effect:

   .. code-block:: console

      $ curl http://localhost/index.html

            index.html

   .. code-block:: console

      $ curl http://localhost/symlink

            <!DOCTYPE html><title>Error 403</title><p>Error 403.

   Lastly, what difference does **chroot** make?
   To see, remove it:

   .. code-block:: json

      {
          "action": {
              "share": "/www/$host/static$uri",
              "follow_symlinks": false
          }
      }

   Now, **"follow_symlinks": false** affects the entire share,
   and **localhost** is a symlink,
   so it's forbidden:

   .. code-block:: console

      $ curl http://localhost/index.html

            <!DOCTYPE html><title>Error 403</title><p>Error 403.


.. _configuration-fallback:

===============
Fallback action
===============

Finally, within an **action**,
you can supply a **fallback** option
beside a **share**.
It specifies the
:ref:`action <configuration-routes-action>`
to be taken
if the requested file can't be served
from the **share** path:

.. code-block:: json

   {
       "share": "/www/data/static$uri",
       "fallback": {
           "pass": "applications/php"
       }
   }

Serving a file can be impossible for different reasons, such as:

- The request's HTTP method isn't **GET** or **HEAD**.

- The file's MIME type doesn't match the **types**
  :ref:`array <configuration-share-mime>`.

- The file isn't found at the **share** path.

- The router process has
  :ref:`insufficient permissions <security-apps>`
  to access the file or an underlying directory.

In the previous example,
an attempt to serve the requested file
from the **/www/data/static/** directory
is made first.
Only if the file can't be served,
the request is passed to the **php** application.

If the **fallback** itself is a **share**,
it can also contain a nested **fallback**:

.. code-block:: json

   {
       "share": "/www/data/static$uri",
       "fallback": {
           "share": "/www/cache$uri",
           "chroot": "/www/",
           "fallback": {
               "proxy": "http://127.0.0.1:9000"
           }
       }
   }

The first **share** tries to serve the request
from **/www/data/static/**;
on failure, the second **share** tries the **/www/cache/** path
with **chroot** enabled.
If both attempts fail,
the request is proxied elsewhere.

.. nxt_details:: Examples
   :hash: conf-variable-examples

   One common use case that this feature enables
   is the separation of requests
   for static and dynamic content
   into independent routes.
   The following example relays all requests
   that target **.php** files
   to an application
   and uses a catch-all static **share**
   with a **fallback**:

   .. code-block:: json

      {
          "routes": [
              {
                  "match": {
                      "uri": "*.php"
                  },

                  "action": {
                      "pass": "applications/php-app"
                  }
              },
              {
                  "action": {
                      "share": "/www/php-app/assets/files$uri",
                      "fallback": {
                          "proxy": "http://127.0.0.1:9000"
                      }
                  }
              }

          ],

          "applications": {
              "php-app": {
                  "type": "php",
                  "root": "/www/php-app/scripts/"
              }
          }
      }

   You can reverse this scheme for apps
   that avoid filenames in dynamic URIs,
   listing all types of static content
   to be served from a **share**
   in a **match** condition
   and adding an unconditional application path:

   .. code-block:: json

      {
          "routes": [
              {
                  "match": {
                      "uri": [
                          "*.css",
                          "*.ico",
                          "*.jpg",
                          "*.js",
                          "*.png",
                          "*.xml"
                      ]
                  },

                  "action": {
                      "share": "/www/php-app/assets/files$uri",
                      "fallback": {
                          "proxy": "http://127.0.0.1:9000"
                      }
                  }
              },
              {
                  "action": {
                      "pass": "applications/php-app"
                  }
              }

          ],

          "applications": {
              "php-app": {
                  "type": "php",
                  "root": "/www/php-app/scripts/"
              }
          }
      }

   If image files should be served locally
   and other proxied,
   use the **types** array
   in the first route step:

   .. code-block:: json

      {
          "match": {
              "uri": [
                  "*.css",
                  "*.ico",
                  "*.jpg",
                  "*.js",
                  "*.png",
                  "*.xml"
              ]
          },

          "action": {
              "share": "/www/php-app/assets/files$uri",
              "types": [
                  "image/*"
              ],

              "fallback": {
                  "proxy": "http://127.0.0.1:9000"
              }
          }
      }

   Another way to combine
   **share**, **types**, and **fallback**
   is exemplified by the following compact pattern:

   .. code-block:: json

      {
          "share": "/www/php-app/assets/files$uri",
          "types": [
              "!application/x-httpd-php"
          ],

          "fallback": {
              "pass": "applications/php-app"
          }
      }

   It forwards explicit requests for PHP files
   to the app
   while serving all other types of files
   from the share;
   note that a **match** object
   isn't needed here to achieve this effect.


.. _configuration-proxy:

********
Proxying
********

Unit's routes support HTTP proxying
to socket addresses
using the **proxy** option
of a route step
:ref:`action <configuration-routes-action>`:

.. code-block:: json

   {
       "routes": [
           {
               "match": {
                   "uri": "/ipv4/*"
               },

               "action": {
                   "proxy": ":nxt_hint:`http://127.0.0.1:8080 <Note that the http:// scheme is required>`"
               }
           },
           {
               "match": {
                   "uri": "/ipv6/*"
               },

               "action": {
                   "proxy": ":nxt_hint:`http://[::1]:8080 <Note that the http:// scheme is required>`"
               }
           },
           {
               "match": {
                   "uri": "/unix/*"
               },

               "action": {
                   "proxy": ":nxt_hint:`http://unix:/path/to/unix.sock <Note that the http:// scheme is required, followed by the unix: prefix>`"
               }
           }
       ]
   }

As the example suggests,
you can use UNIX, IPv4, and IPv6 socket addresses
for proxy destinations.

.. note::

   The HTTPS scheme is not supported yet.


.. _configuration-upstreams:

==============
Load balancing
==============

Besides proxying requests to individual servers,
Unit can also relay incoming requests to *upstreams*.
An upstream is a group of servers
that comprise a single logical entity
and may be used as a **pass** destination
for incoming requests in a
:ref:`listener <configuration-listeners>`
or a
:ref:`route <configuration-routes>`.

Upstreams are defined
in the eponymous **/config/upstreams** section of the API:

.. code-block:: json

   {
       "listeners": {
           "*:80": {
               "pass": "upstreams/rr-lb"
           }
       },

       "upstreams": {
           ":nxt_hint:`rr-lb <Upstream object>`": {
               ":nxt_hint:`servers <Lists individual servers as object-valued options>`": {
                   ":nxt_hint:`192.168.0.100:8080 <Empty object needed due to JSON requirements>`": {},
                   "192.168.0.101:8080": {
                       "weight": 0.5
                   }
               }
           }
       }
   }

An upstream must define a **servers** object
that lists socket addresses
as server object names.
Unit dispatches requests between the upstream's servers
in a round-robin fashion,
acting as a load balancer.
Each server object can set a numeric **weight**
to adjust the share of requests
it receives via the upstream.
In the above example,
**192.168.0.100:8080** receives twice as many requests
as **192.168.0.101:8080**.

Weights can be specified as integers or fractions
in decimal or scientific notation:

.. code-block:: json

   {
       "servers": {
           "192.168.0.100:8080": {
               ":nxt_hint:`weight <All three values are equal>`": 1e1
           },

           "192.168.0.101:8080": {
               ":nxt_hint:`weight <All three values are equal>`": 10.0
           },

           "192.168.0.102:8080": {
               ":nxt_hint:`weight <All three values are equal>`": 10
           }
       }
   }

The maximum weight is **1000000**,
the minimum is **0**
(such servers receive no requests);
the default is **1**.


.. _configuration-applications:

************
Applications
************

Each app that Unit runs
is defined as an object
in the **/config/applications** section of the control API;
it lists the app's language and settings,
its runtime limits,
process model,
and various language-specific options.

.. note::

   Our official
   :ref:`language-specific packages <installation-precomp-pkgs>`
   include end-to-end examples of application configuration,
   available for your reference at
   **/usr/share/doc/<module name>/examples/**
   after package installation.

Here, Unit runs 20 processes of a PHP app called **blogs**,
stored in the **/www/blogs/scripts/** directory:

.. code-block:: json

   {
       "blogs": {
           "type": "php",
           "processes": 20,
           "root": "/www/blogs/scripts/"
       }
   }

.. _configuration-apps-common:

App objects have a number of options
shared between all application languages:

.. list-table::
    :header-rows: 1

    * - Option
      - Description

    * - **type** (required)
      - Application type:
        **external**
        (Go and Node.js),
        **java**,
        **perl**,
        **php**,
        **python**,
        **ruby**,
        or **wasm**
        (WebAssembly).

        Except for **external** and **wasm**,
        you can detail the runtime version:
        **"type": "python 3"**,
        **"type": "python 3.4"**,
        or even
        **"type": "python 3.4.9rc1"**.
        Unit searches its modules
        and uses the latest matching one,
        reporting an error if none match.

        For example, if you have only one PHP module,
        7.1.9,
        it matches **"php"**,
        **"php 7"**,
        **"php 7.1"**,
        and **"php 7.1.9"**.
        If you have modules for versions 7.0.2 and 7.0.23,
        set **"type": "php 7.0.2"** to specify the former;
        otherwise, PHP |_| 7.0.23 will be used.

    * - **environment**
      - String-valued object;
        environment variables to be passed to the app.

    * - **group**
      - String;
        group name that runs the
        :ref:`app process <sec-processes>`.

        The default is the **user**'s primary group.

    * - **isolation**
      - Object; manages the isolation
        of an application process.
        For details, see
        :ref:`here <configuration-proc-mgmt-isolation>`.

    * - **limits**
      - Object; accepts two integer options,
        **timeout** and **requests**.
        Their values govern the life cycle of an application process.
        For details, see
        :ref:`here <configuration-proc-mgmt-lmts>`.

    * - **processes**
      - Integer or object;
        integer sets a static number of app processes,
        and object options **max**,
        **spare**,
        and **idle_timeout**
        enable dynamic management.
        For details, see
        :ref:`here <configuration-proc-mgmt-prcs>`.

        The default is 1.

    * - **stderr**, **stdout**
      - Strings;
        filenames where Unit redirects the application's output.

        The default when running *with* **--no-daemon** is to send
        *stdout* to the *console* and *stderr* to Unit's *log*.

        The default when running *without* **--no-daemon** is to send
        *stdout* to */dev/null* and *stderr* to Unit's *log*.

        These options have *no* effect when running with **--no-daemon**.

    * - **user**
      - String;
        username that runs the
        :ref:`app process <sec-processes>`.

        The default is the username configured at
        :ref:`build time <source-config-src>`
        or at
        :ref:`startup <source-startup>`.

    * - **working_directory**
      - String;
        the app's working directory.

        The default is
        the working directory
        of Unit's
        :ref:`main process <sec-processes>`.

Also, you need to set **type**-specific options
to run the app.
This
:ref:`Python app <configuration-python>`
sets **path** and **module**:

.. code-block:: json

   {
       "type": "python 3.6",
       "processes": 16,
       "working_directory": "/www/python-apps",
       "path": "blog",
       "module": "blog.wsgi",
       "user": "blog",
       "group": "blog",
       "environment": {
           "DJANGO_SETTINGS_MODULE": "blog.settings.prod",
           "DB_ENGINE": "django.db.backends.postgresql",
           "DB_NAME": "blog",
           "DB_HOST": "127.0.0.1",
           "DB_PORT": "5432"
       }
   }


.. _configuration-proc-mgmt:

==================
Process management
==================

Unit has three per-app options
that control how the app's processes behave:
**isolation**, **limits**, and **processes**.
Also, you can **GET**
the **/control/applications/** section of the API
to restart an app:

.. code-block:: console

   # curl -X GET --unix-socket :nxt_ph:`/path/to/control.unit.sock <Path to Unit's control socket in your installation>`  \
         http://localhost/control/applications/:nxt_ph:`app_name <Your application's name as defined in the /config/applications/ section>`/restart

Unit handles the rollover gracefully,
allowing the old processes
to deal with existing requests
and starting a new set of processes
(as defined by the **processes**
:ref:`option <configuration-proc-mgmt-prcs>`)
to accept new requests.

.. _configuration-proc-mgmt-isolation:

Process isolation
*****************

You can use
`namespace <https://man7.org/linux/man-pages/man7/namespaces.7.html>`__
and
`file system <https://man7.org/linux/man-pages/man2/chroot.2.html>`__
isolation for your apps
if Unit's underlying OS supports them:

.. code-block:: console

   $ ls /proc/self/ns/

       cgroup :nxt_hint:`mnt <The mount namespace>` :nxt_hint:`net <The network namespace>` pid ... :nxt_hint:`user <The credential namespace>` :nxt_hint:`uts <The uname namespace>`

The **isolation** application option
has the following members:

.. list-table::
   :header-rows: 1

   * - Option
     - Description

   * - **automount**
     - Object;
       controls mount behavior
       if **rootfs** is enabled.
       By default, Unit automatically mounts the
       :ref:`language runtime dependencies <conf-rootfs>`,
       a
       `procfs
       <https://man7.org/linux/man-pages/man5/procfs.5.html>`__
       at **/proc/**,
       and a
       `tmpfs
       <https://man7.org/linux/man-pages/man5/tmpfs.5.html>`__ at **/tmp/**,
       but you can disable any of these default mounts:

       .. code-block:: json

          {
              "isolation": {
                  "automount": {
                      "language_deps": false,
                      "procfs": false,
                      "tmpfs": false
                  }
              }
          }

   * - **cgroup**
     - Object;
       defines the app's
       :ref:`cgroup <conf-app-cgroup>`.

       .. list-table::
          :header-rows: 1

          * - Option
            - Description

          * - **path** (required)
            - String;
              configures absolute or relative path of the app
              in the
              `cgroups v2 hierarchy
              <https://man7.org/linux/man-pages/man7/cgroups.7.html#CGROUPS_VERSION_2>`__.
              The limits trickle down the hierarchy,
              so child cgroups can't exceed parental thresholds.

   * - **gidmap**
     - Same as **uidmap**,
       but configures group IDs instead of user IDs.

   * - **namespaces**
     - Object; configures
       `namespace <https://man7.org/linux/man-pages/man7/namespaces.7.html>`__
       isolation scheme for the application.

       Available options
       (system-dependent;
       check your OS manual for guidance):

       .. list-table::

          * - **cgroup**
            - Creates a new
              `cgroup
              <https://man7.org/linux/man-pages/man7/cgroup_namespaces.7.html>`__
              namespace for the app.

          * - **credential**
            - Creates a new
              `user
              <https://man7.org/linux/man-pages/man7/user_namespaces.7.html>`__
              namespace for the app.

          * - **mount**
            - Creates a new
              `mount
              <https://man7.org/linux/man-pages/man7/mount_namespaces.7.html>`__
              namespace for the app.

          * - **network**
            - Creates a new
              `network
              <https://man7.org/linux/man-pages/man7/network_namespaces.7.html>`__
              namespace for the app.

          * - **pid**
            - Creates a new
              `PID
              <https://man7.org/linux/man-pages/man7/pid_namespaces.7.html>`__
              namespace for the app.

          * - **uname**
            - Creates a new
              `UTS
              <https://man7.org/linux/man-pages/man7/namespaces.7.html>`__
              namespace for the app.

       All options listed above are Boolean;
       to isolate the app,
       set the corresponding namespace option to **true**;
       to disable isolation,
       set the option to **false**
       (default).

   * - **rootfs**
     - String; pathname of the directory
       to be used as the new
       :ref:`file system root
       <conf-rootfs>`
       for the app.

   * - **uidmap**
     - Array of user ID
       :ref:`mapping objects <conf-uidgid-mapping>`;
       each array item must define the following:

       .. list-table::

          * - **container**
            - Integer;
              starts the user ID mapping range
              in the app's namespace.

          * - **host**
            - Integer;
              starts the user ID mapping range
              in the OS namespace.

          * - **size**
            - Integer;
              size of the ID range
              in both namespaces.

A sample **isolation** object
that enables all namespaces
and sets mappings for user and group IDs:

.. code-block:: json

    {
        "namespaces": {
            "cgroup": true,
            "credential": true,
            "mount": true,
            "network": true,
            "pid": true,
            "uname": true
        },

        "cgroup": {
            "path": "/unit/appcgroup"
        },

        "uidmap": [
            {
                "host": 1000,
                "container": 0,
                "size": 1000
            }
        ],

        "gidmap": [
            {
                "host": 1000,
                "container": 0,
                "size": 1000
            }
        ]
    }


.. _conf-app-cgroup:

Using control groups
====================

A control group (cgroup) commands
the use of computational resources
by a group of processes
in a unified hierarchy.
Cgroups are defined
by their *paths*
in the cgroups file system.

The **cgroup** object
defines the cgroup
for a Unit app;
its **path** option
can set an absolute
(starting with **/**)
or a relative value.
If the path doesn't exist
in the cgroups file system,
Unit creates it.

Relative paths are implicitly placed
inside the cgroup of Unit's
:ref:`main process <sec-processes>`;
this setting effectively puts the app
to the **/<main Unit process cgroup>/production/app** cgroup:

.. code-block:: json

   {
       "isolation": {
           "cgroup": {
               "path": "production/app"
           }
       }
   }

An absolute pathname places the application
under a separate cgroup subtree;
this configuration puts the app under **/staging/app**:

.. code-block:: json

   {
       "isolation": {
           "cgroup": {
               "path": "/staging/app"
           }
       }
   }

A basic use case
would be to set a memory limit on a cgroup.
First,
find the cgroup mount point:

.. code-block:: console

   $ mount -l | grep cgroup

       cgroup2 on /sys/fs/cgroup type cgroup2 (rw,nosuid,nodev,noexec,relatime,nsdelegate,memory_recursiveprot)

Next, check the available controllers
and set the **memory.high** limit:

.. code-block:: console

   # cat /sys/fs/cgroup/:nxt_hint:`/staging/app <cgroup's path set in Unit configuration>`/cgroup.controllers

       cpuset cpu io memory pids

.. code-block:: console

   # echo 1G > /sys/fs/cgroup:nxt_hint:`/staging/app <cgroup's path set in Unit configuration>`/memory.high

For more details
and possible options,
refer to the
`admin guide
<https://docs.kernel.org/admin-guide/cgroup-v2.html>`__.

.. note::

   To avoid confusion,
   mind that the **namespaces/cgroups** option
   controls the application's cgroup *namespace*;
   instead, the **cgroup/path** option
   specifies the cgroup where Unit puts the application.


.. _conf-rootfs:

Changing root directory
=======================

The **rootfs** option confines the app
to the directory you provide,
making it the new
`file system root
<https://man7.org/linux/man-pages/man2/chroot.2.html>`__.
To use it,
your app should have the corresponding privilege
(effectively,
run as **root** in most cases).

The root directory is changed
before the language module starts the app,
so any path options for the app
should be relative to the new root.
Note the **path** and **home** settings:

.. code-block:: json

   {
       "type": "python 2.7",
       "path": ":nxt_hint:`/ <Without rootfs, this would be /var/app/sandbox/>`",
       "home": ":nxt_hint:`/venv/ <Without rootfs, this would be /var/app/sandbox/venv/>`",
       "module": "wsgi",
       "isolation": {
           "rootfs": "/var/app/sandbox/"
       }
   }

.. warning::

   When using **rootfs**
   with **credential** set to **true**:

   .. code-block:: json

      "isolation": {
          "rootfs": "/var/app/sandbox/",
          "namespaces": {
              "credential": true
          }
      }

   Ensure that the user the app *runs as*
   can access the **rootfs** directory.

Unit mounts language-specific files and directories
to the new root
so the app stays operational:

.. list-table::
   :header-rows: 1

   * - Language
     - Language-Specific Mounts

   * - Java
     - - JVM's **libc.so** directory

       - Java module's
         :ref:`home <howto/source-modules-java>`
         directory

   * - Python
     - Python's **sys.path**
       `directories
       <https://docs.python.org/3/library/sys.html#sys.path>`__

   * - Ruby
     - - Ruby's header, interpreter, and library
         `directories
         <https://idiosyncratic-ruby.com/42-ruby-config.html>`__:
         **rubyarchhdrdir**,
         **rubyhdrdir**,
         **rubylibdir**,
         **rubylibprefix**,
         **sitedir**,
         and **topdir**

       - Ruby's gem installation directory
         (**gem env gemdir**)

       - Ruby's entire gem path list
         (**gem env gempath**)


.. nxt_details:: Using "uidmap", "gidmap"
   :hash: conf-uidgid-mapping

   The **uidmap** and **gidmap** options
   are available only
   if the underlying OS supports
   `user namespaces
   <https://man7.org/linux/man-pages/man7/user_namespaces.7.html>`__.

   If **uidmap** is omitted but **credential** isolation is enabled,
   the effective UID (EUID) of the application process
   in the host namespace
   is mapped to the same UID
   in the container namespace;
   the same applies to **gidmap** and GID, respectively.
   This means that the configuration below:

   .. code-block:: json

      {
          "user": "some_user",
          "isolation": {
              "namespaces": {
                  "credential": true
              }
          }
      }

   Is equivalent to the following
   (assuming **some_user**'s EUID and EGID are both equal to 1000):

   .. code-block:: json

      {
          "user": "some_user",
          "isolation": {
              "namespaces": {
                  "credential": true
              },

              "uidmap": [
                  {
                      "host": "1000",
                      "container": "1000",
                      "size": 1
                  }
              ],

              "gidmap": [
                  {
                      "host": "1000",
                      "container": "1000",
                      "size": 1
                  }
              ]
          }
      }


.. _configuration-proc-mgmt-lmts:

Request limits
**************

The **limits** object
controls request handling by the app process
and has two integer options:

.. list-table::
   :header-rows: 1

   * - Option
     - Description

   * - **requests**
     - Integer;
       maximum number of requests
       an app process can serve.
       When the limit is reached,
       the process restarts;
       this mitigates possible memory leaks
       or other cumulative issues.

   * - **timeout**
     - Integer;
       request timeout in seconds.
       If an app process exceeds it
       while handling a request,
       Unit cancels the request
       and returns a 503 "Service Unavailable" response
       to the client.

       .. note::

          Now, Unit doesn't detect freezes,
          so the hanging process stays on
          the app's process pool.

Example:

.. code-block:: json

   {
       "type": "python",
       "working_directory": "/www/python-apps",
       "module": "blog.wsgi",
       "limits": {
           "timeout": 10,
           "requests": 1000
       }
   }

.. _configuration-proc-mgmt-prcs:

Application processes
*********************

The **processes** option
offers a choice
between static and dynamic process management.
If you set it to an integer,
Unit immediately launches the given number of app processes
and keeps them without scaling.

To enable a dynamic prefork model for your app,
supply a **processes** object with the following options:

.. list-table::
    :header-rows: 1

    * - Option
      - Description

    * - **idle_timeout**
      - Number of seconds
        Unit waits for
        before terminating an idle process
        that exceeds **spare**.

    * - **max**
      - Maximum number of application processes
        that Unit maintains
        (busy and idle).

        The default is 1.

    * - **spare**
      - Minimum number of idle processes
        that Unit tries to maintain for an app.
        When the app is started,
        **spare** idles are launched;
        Unit passes new requests to existing idles,
        forking new idles
        to keep the **spare** level
        if **max** allows.
        When busy processes complete their work
        and turn idle again,
        Unit terminates extra idles
        after **idle_timeout**.

If **processes** is omitted entirely,
Unit creates 1 static process.
If an empty object is provided: **"processes": {}**,
dynamic behavior
with default option values
is assumed.

Here, Unit allows 10 processes maximum,
keeps 5 idles,
and terminates extra idles after 20 seconds:

.. code-block:: json

   {
       "max": 10,
       "spare": 5,
       "idle_timeout": 20
   }

.. note::

   For details of manual application process restart, see
   :ref:`here <configuration-proc-mgmt>`.


.. _configuration-languages:
.. _configuration-go:

==
Go
==

To run a Go app on Unit,
modify its source
to make it Unit-aware
and rebuild the app.

.. nxt_details:: Updating Go apps to run on Unit
   :hash: updating-go-apps

   Unit uses
   `cgo <https://pkg.go.dev/cmd/cgo>`__
   to invoke C code from Go,
   so check the following prerequisites:

   - The :envvar:`CGO_ENABLED` variable is set to **1**:

     .. code-block:: console

        $ go env CGO_ENABLED

              0

     .. code-block:: console

        $ go env -w CGO_ENABLED=1

   - If you installed Unit from the
     :ref:`official packages <installation-precomp-pkgs>`,
     install the development package:

     .. tabs::
        :prefix: go-prereq

        .. tab:: Debian, Ubuntu

           .. code-block:: console

              # apt install unit-dev

        .. tab:: Amazon, Fedora, RHEL

           .. code-block:: console

              # yum install unit-devel

   - If you installed Unit from
     :doc:`source <../howto/source>`,
     install the include files and libraries:

     .. code-block:: console

        # make libunit-install

   In the **import** section,
   list the **unit.nginx.org/go** package:

   .. code-block:: go

      import (
          ...
          "unit.nginx.org/go"
          ...
      )

   Replace the **http.ListenAndServe** call
   with **unit.ListenAndServe**:

   .. code-block:: go

      func main() {
          ...
          http.HandleFunc("/", handler)
          ...
          // http.ListenAndServe(":8080", nil)
          unit.ListenAndServe(":8080", nil)
          ...
      }

   If you haven't done so yet,
   initialize the Go module for your app:

   .. code-block:: console

      $ go mod init :nxt_ph:`example.com/app <Arbitrary module designation>`

            go: creating new go.mod: module example.com/app

   Install the newly added dependency
   and build your application:

   .. subs-code-block:: console

      $ go get unit.nginx.org/go@|version|

            go: downloading unit.nginx.org

      $ go build -o :nxt_ph:`app <Executable name>` :nxt_ph:`app.go <Application source code>`

   If you update Unit to a newer version,
   repeat the two commands above
   to rebuild your app.

   The resulting executable works as follows:

   - When you run it standalone,
     the **unit.ListenAndServe** call
     falls back to **http** functionality.

   - When Unit runs it,
     **unit.ListenAndServe** directly communicates
     with Unit's router process,
     ignoring the address supplied as its first argument
     and relying on the
     :ref:`listener's settings <configuration-listeners>`
     instead.

Next, configure the app on Unit;
besides the
:ref:`common options <configuration-apps-common>`,
you have:

.. list-table::
    :header-rows: 1

    * - Option
      - Description

    * - **executable** (required)
      - String;
        pathname of the application,
        absolute or relative to **working_directory**.

    * - **arguments**
      - Array of strings;
        command-line arguments
        to be passed to the application.
        The example below is equivalent to
        **/www/chat/bin/chat_app --tmp-files /tmp/go-cache**.

Example:

.. code-block:: json

   {
       "type": "external",
       "working_directory": "/www/chat",
       "executable": "bin/chat_app",
       "user": "www-go",
       "group": "www-go",
       "arguments": [
           "--tmp-files",
           "/tmp/go-cache"
       ]
   }

.. note::

   For Go-based examples,
   see our
   :doc:`../howto/grafana`
   howto or a basic
   :ref:`sample <sample-go>`.


.. _configuration-java:

====
Java
====

First, make sure to install Unit
along with the
:ref:`Java language module
<installation-precomp-pkgs>`.

Besides the
:ref:`common options <configuration-apps-common>`,
you have:

.. list-table::
    :header-rows: 1

    * - Option
      - Description

    * - **webapp** (required)
      - String;
        pathname
        of the application's **.war** file
        (packaged or unpackaged).

    * - **classpath**
      - Array of strings;
        paths to your app's required libraries
        (may point to directories
        or individual **.jar** files).

    * - **options**
      - Array of strings;
        defines JVM runtime options.

        Unit itself
        exposes the **-Dnginx.unit.context.path** option
        that defaults to **/**;
        use it to customize the
        `context path
        <https://javaee.github.io/javaee-spec/javadocs/javax/servlet/ServletContext.html#getContextPath-->`__.

    * - **thread_stack_size**
      - Integer;
        stack size of a worker thread
        (in bytes,
        multiple of memory page size;
        the minimum value is usually architecture specific).

        The default is usually system dependent
        and can be set with :program:`ulimit -s <SIZE_KB>`.

    * - **threads**
      - Integer;
        number of worker threads
        per :ref:`app process <sec-processes>`.
        When started,
        each app process creates this number of threads
        to handle requests.

        The default is **1**.

Example:

.. code-block:: json

   {
       "type": "java",
       "classpath": [
           "/www/qwk2mart/lib/qwk2mart-2.0.0.jar"
       ],

       "options": [
           "-Dlog_path=/var/log/qwk2mart.log"
       ],

       "webapp": "/www/qwk2mart/qwk2mart.war"
   }

.. note::

   For Java-based examples,
   see our
   :doc:`../howto/jira`,
   :doc:`../howto/opengrok`,
   and
   :doc:`../howto/springboot`
   howtos or a basic
   :ref:`sample <sample-java>`.


.. _configuration-nodejs:

=======
Node.js
=======

First, you need to have the :program:`unit-http` module
:ref:`installed <installation-nodejs-package>`.
If it's global,
symlink it in your project directory:

.. code-block:: console

   # npm link unit-http

Do the same if you move a Unit-hosted app
to a new system
where :program:`unit-http` is installed globally.
Also, if you update Unit later,
update the Node.js module as well
according to your
:ref:`installation method <installation-nodejs-package>`.

Next, to run your Node.js apps on Unit,
you need to configure them.
Besides the
:ref:`common options <configuration-apps-common>`,
you have:

.. list-table::
    :header-rows: 1

    * - Option
      - Description

    * - **executable** (required)
      - String;
        pathname of the app,
        absolute or relative to **working_directory**.

        Supply your **.js** pathname here
        and start the file itself
        with a proper shebang:

        .. code-block:: javascript

           #!/usr/bin/env node

        .. note::

           Make sure to :command:`chmod +x`
           the file you list here
           so Unit can start it.

    * - **arguments**
      - Array of strings;
        command-line arguments
        to be passed to the app.
        The example below is equivalent to
        **/www/apps/node-app/app.js --tmp-files /tmp/node-cache**.

Example:

.. code-block:: json

   {
       "type": "external",
       "working_directory": "/www/app/node-app/",
       "executable": "app.js",
       "user": "www-node",
       "group": "www-node",
       "arguments": [
           "--tmp-files",
           "/tmp/node-cache"
       ]
   }

.. _configuration-nodejs-loader:

You can run Node.js apps without altering their code,
using a loader module
we provide with :program:`unit-http`.
Apply the following app configuration,
depending on your version of Node.js:

.. tabs::
   :prefix: nodejs

   .. tab:: 14.16.x and later

      .. code-block:: json

         {
             "type": "external",
             "executable": ":nxt_hint:`/usr/bin/env <The external app type allows to run arbitrary executables, provided they establish communication with Unit>`",
             "arguments": [
                 "node",
                 "--loader",
                 "unit-http/loader.mjs",
                 "--require",
                 "unit-http/loader",
                 ":nxt_ph:`app.js <Application script name>`"
             ]
         }


   .. tab:: 14.15.x and earlier

      .. code-block:: json

         {
             "type": "external",
             "executable": ":nxt_hint:`/usr/bin/env <The external app type allows to run arbitrary executables, provided they establish communication with Unit>`",
             "arguments": [
                 "node",
                 "--require",
                 "unit-http/loader",
                 ":nxt_ph:`app.js <Application script name>`"
             ]
         }

The loader overrides the **http** and **websocket** modules
with their Unit-aware versions
and starts the app.

You can also run your Node.js apps without the loader
by updating the application source code.
For that, use **unit-http** instead of **http** in your code:

.. code-block:: javascript

   var http = require('unit-http');

To use the WebSocket protocol,
your app only needs to replace the default **websocket**:

.. code-block:: javascript

  var webSocketServer = require('unit-http/websocket').server;

.. note::

   For Node.js-based examples,
   see our
   :doc:`../howto/apollo`,
   :doc:`../howto/express`,
   :doc:`../howto/koa`,
   and
   :ref:`Docker <docker-apps>`
   howtos or a basic
   :ref:`sample <sample-nodejs>`.


.. _configuration-perl:

====
Perl
====

First, make sure to install Unit along with the
:ref:`Perl language module <installation-precomp-pkgs>`.

Besides the
:ref:`common options <configuration-apps-common>`,
you have:

.. list-table::
    :header-rows: 1

    * - Option
      - Description

    * - **script** (required)
      - String;
        PSGI script path.

    * - **thread_stack_size**
      - Integer;
        stack size of a worker thread
        (in bytes,
        multiple of memory page size;
        the minimum value is usually architecture specific).

        The default is usually system dependent
        and can be set with :program:`ulimit -s <SIZE_KB>`.

    * - **threads**
      - Integer;
        number of worker threads
        per :ref:`app process <sec-processes>`.
        When started,
        each app process creates this number of threads
        to handle requests.

        The default is **1**.

Example:

.. code-block:: json

   {
       "type": "perl",
       "script": "/www/bugtracker/app.psgi",
       "working_directory": "/www/bugtracker",
       "processes": 10,
       "user": "www",
       "group": "www"
   }

.. note::

   For Perl-based examples of Perl,
   see our
   :doc:`../howto/bugzilla`
   and
   :doc:`../howto/catalyst`
   howtos or a basic
   :ref:`sample <sample-perl>`.

.. _configuration-php:

===
PHP
===

First, make sure to install Unit along with the
:ref:`PHP language module <installation-precomp-pkgs>`.

Besides the
:ref:`common options <configuration-apps-common>`, you have:

.. list-table::
    :header-rows: 1

    * - Option
      - Description

    * - **root** (required)
      - String;
        base directory
        of the app's file structure.
        All URI paths are relative to it.

    * - **index**
      - String;
        filename added to URI paths
        that point to directories
        if no **script** is set.

        The default is **index.php**.

    * - **options**
      - Object;
        :ref:`defines <configuration-php-options>`
        the **php.ini** location and options.

    * - **script**
      - String;
        filename of a **root**-based PHP script
        that serves all requests to the app.

    * - **targets**
      - Object;
        defines application sections with
        :ref:`custom <configuration-php-targets>`
        **root**, **script**, and **index** values.

The **index** and **script** options
enable two modes of operation:

- If **script** is set,
  all requests to the application are handled
  by the script you specify in this option.

- Otherwise, the requests are served
  according to their URI paths;
  if they point to directories,
  **index** is used.

.. _configuration-php-options:

You can customize **php.ini**
via the **options** object:

.. list-table::
    :header-rows: 1

    * - Option
      - Description

    * - **admin**, **user**
      - Objects for extra directives.
        Values in **admin** are set in **PHP_INI_SYSTEM** mode,
        so the app can't alter them;
        **user** values are set in **PHP_INI_USER** mode
        and can be
        `updated
        <https://www.php.net/manual/en/function.ini-set.php>`__
        at runtime.

        - The objects override the settings
          from any ***.ini** files

        - The **admin** object can only set what's
          `listed <https://www.php.net/manual/en/ini.list.php>`__
          as **PHP_INI_SYSTEM**;
          for other modes,
          set **user**

        - Neither **admin** nor **user**
          can set directives listed as
          `php.ini only <https://www.php.net/manual/en/ini.list.php>`__
          except for **disable_classes** and **disable_functions**

    * - **file**
      - String;
        pathname of the **php.ini** file with
        `PHP configuration directives
        <https://www.php.net/manual/en/ini.list.php>`__.

To load multiple **.ini** files,
use **environment** with :envvar:`PHP_INI_SCAN_DIR` to
`scan a custom directory
<https://www.php.net/manual/en/configuration.file.php>`__:

.. code-block:: json

  {
      "applications": {
          "hello-world": {
              "type": "php",
              "root": "/www/public/",
              "script": "index.php",
              "environment": {
                  "PHP_INI_SCAN_DIR": ":nxt_ph:`: <Path separator>`/tmp/php.inis/"
              }
          }
      }
  }

Mind that the colon that prefixes the value here is a path separator;
it causes PHP to scan the directory preconfigured with the
:option:`!--with-config-file-scan-dir` option,
which is usually **/etc/php.d/**,
and then the directory you set here, which is **/tmp/php.inis/**.
To skip the preconfigured directory, drop the **:** prefix.

.. note::

   Values in **options** must be strings
   (for example, **"max_file_uploads": "4"**,
   not **"max_file_uploads": 4**);
   for boolean flags,
   use **"0"** and **"1"** only.
   For details aof **PHP_INI_*** modes,
   see the
   `PHP docs
   <https://www.php.net/manual/en/configuration.changes.modes.php>`__.


.. note::

   Unit implements the **fastcgi_finish_request()** `function
   <https://www.php.net/manual/en/function.fastcgi-finish-request.php>`_ in a
   manner similar to PHP-FPM.

Example:

.. code-block:: json

   {
       "type": "php",
       "processes": 20,
       "root": "/www/blogs/scripts/",
       "user": "www-blogs",
       "group": "www-blogs",
       "options": {
           "file": "/etc/php.ini",
           "admin": {
               "memory_limit": "256M",
               "variables_order": "EGPCS"
           },

           "user": {
               "display_errors": "0"
           }
       }
   }

.. _configuration-php-targets:

Targets
*******

You can configure up to 254 individual entry points
for a single PHP app:

.. code-block:: json

   {
       "applications": {
           "php-app": {
               "type": "php",
               "targets": {
                   "front": {
                       "script": "front.php",
                       "root": "/www/apps/php-app/front/"
                   },

                   "back": {
                       "script": "back.php",
                       "root": "/www/apps/php-app/back/"
                   }
               }
           }
       }
   }

Each target is an object
that specifies **root**
and can define **index** or **script**
just like a regular app does.
Targets can be used by the **pass** options
in listeners and routes
to serve requests:

.. code-block:: json

   {
       "listeners": {
           "127.0.0.1:8080": {
               "pass": "applications/php-app/front"
           },

           "127.0.0.1:80": {
               "pass": "routes"
           }
       },

       "routes": [
           {
               "match": {
                   "uri": "/back"
               },

               "action": {
                   "pass": "applications/php-app/back"
               }
           }
       ]
   }

App-wide settings
(**isolation**, **limits**, **options**, **processes**)
are shared by all targets within the app.

.. warning::

   If you specify **targets**,
   there should be no **root**, **index**, or **script**
   defined at the app level.

.. note::

   For PHP-based examples,
   see our
   :doc:`../howto/cakephp`,
   :doc:`../howto/codeigniter`,
   :doc:`../howto/dokuwiki`,
   :doc:`../howto/drupal`,
   :doc:`../howto/laravel`,
   :doc:`../howto/lumen`,
   :doc:`../howto/matomo`,
   :doc:`../howto/mediawiki`,
   :doc:`../howto/modx`,
   :doc:`../howto/nextcloud`,
   :doc:`../howto/phpbb`,
   :doc:`../howto/phpmyadmin`,
   :doc:`../howto/roundcube`,
   :doc:`../howto/symfony`,
   :doc:`../howto/wordpress`,
   and
   :doc:`../howto/yii`
   howtos or a basic
   :ref:`sample <sample-php>`.


.. _configuration-python:

======
Python
======

First, make sure to install Unit along with the
:ref:`Python language module <installation-precomp-pkgs>`.

Besides the
:ref:`common options <configuration-apps-common>`,
you have:

.. list-table::
    :header-rows: 1

    * - Option
      - Description

    * - **module** (required)
      - String;
        app's module name.
        This module is
        `imported <https://docs.python.org/3/reference/import.html>`__
        by Unit
        the usual Python way.

    * - **callable**
      - String;
        name of the **module**-based callable
        that Unit runs as the app.

        The default is **application**.

    * - **factory**
      - Boolean:
        when enabled, Unit treats **callable** as a factory.

        The default is **false**.

        **Note:** Unit does *not* support passing arguments to factories.

        *(since 1.33.0)*

    * - **home**
      - String;
        path to the app's
        `virtual environment
        <https://packaging.python.org/en/latest/tutorials/installing-packages/#creating-virtual-environments>`__.
        Absolute or relative to **working_directory**.

        .. note::

           The Python version used to run the app
           is determined by **type**;
           for performance,
           Unit doesn't use the command-line interpreter
           from the virtual environment.

        .. nxt_details:: ImportError: No module named 'encodings'
           :hash: encodings-error

           Seeing this in Unit's
           :ref:`log <troubleshooting-log>`
           after you set up **home** for your app?
           This usually occurs
           if the interpreter can't use the virtual environment,
           possible reasons including:

           - Version mismatch
             between the **type** setting
             and the virtual environment;
             check the environment's version:

             .. code-block:: console

                $ source :nxt_ph:`/path/to/venv/ <Path to the virtual environment; use a real path in your commands>`bin/activate
                (venv) $ python --version

           - Unit's unprivileged user
             (usually **unit**)
             having no access to the environment's files;
             assign the necessary rights:

             .. code-block:: console

                # chown -R :nxt_hint:`unit:unit <User and group that Unit's router runs as by default>` :nxt_ph:`/path/to/venv/ <Path to the virtual environment; use a real path in your commands>`

    * - **path**
      - String or an array of strings;
        additional Python module lookup paths.
        These values are prepended to **sys.path**.

    * - **prefix**
      - String;
        **SCRIPT_NAME** context value for WSGI
        or the **root_path** context value for ASGI.
        Should start with a slash
        (**/**).

    * - **protocol**
      - String;
        hints Unit that the app uses a certain interface.
        Can be **asgi** or **wsgi**.

    * - **targets**
      - Object;
        app sections with
        :ref:`custom <configuration-python-targets>`
        **module** and **callable** values.

    * - **thread_stack_size**
      - Integer;
        stack size of a worker thread
        (in bytes,
        multiple of memory page size;
        the minimum value is usually architecture specific).

        The default is usually system dependent
        and can be set with :program:`ulimit -s <SIZE_KB>`.

    * - **threads**
      - Integer;
        number of worker threads
        per :ref:`app process <sec-processes>`.
        When started,
        each app process creates this number of threads
        to handle requests.

        The default is **1**.

Example:

.. code-block:: json

   {
       "type": "python",
       "processes": 10,
       "working_directory": "/www/store/cart/",
       "path": ":nxt_hint:`/www/store/ <Added to sys.path for lookup; store the application module within this directory>`",
       "home": ":nxt_hint:`.virtualenv/ <Path where the virtual environment is located; here, it's relative to the working directory>`",
       "module": ":nxt_hint:`cart.run <Looks for a 'run.py' module in /www/store/cart/>`",
       "callable": "app",
       "prefix": ":nxt_hint:`/cart <Sets the SCRIPT_NAME or root_path context value>`",
       "user": "www",
       "group": "www"
   }

This snippet runs the **app** callable
from the **/www/store/cart/run.py** module
with **/www/store/cart/** as the working directory
and **/www/store/.virtualenv/** as the virtual environment;
the **path** value
accommodates for situations
when some modules of the app
are imported
from outside the **cart/** subdirectory.

.. _configuration-python-asgi:

You can provide the callable in two forms.
The first one uses WSGI
(`PEP 333 <https://peps.python.org/pep-0333/>`__
or `PEP 3333 <https://peps.python.org/pep-3333/>`__):

.. code-block:: python

   def application(environ, start_response):
       start_response('200 OK', [('Content-Type', 'text/plain')])
       yield b'Hello, WSGI\n'

The second one,
supported with Python 3.5+,
uses
`ASGI <https://asgi.readthedocs.io/en/latest/>`__:

.. code-block:: python

   async def application(scope, receive, send):

       await send({
           'type': 'http.response.start',
           'status': 200
       })

       await send({
           'type': 'http.response.body',
           'body': b'Hello, ASGI\n'
       })

.. note::

   Legacy
   `two-callable
   <https://asgi.readthedocs.io/en/latest/specs/main.html#legacy-applications>`_
   ASGI 2.0 applications
   were not supported prior to Unit 1.21.0.

Choose either one according to your needs;
Unit tries to infer your choice automatically.
If this inference fails,
use the **protocol** option
to set the interface explicitly.

.. note::

   The **prefix** option
   controls the **SCRIPT_NAME**
   (`WSGI <https://wsgi.readthedocs.io/en/latest/definitions.html>`__)
   or **root_path**
   (`ASGI
   <https://asgi.readthedocs.io/en/latest/specs/www.html#http-connection-scope>`__)
   setting in Python's context,
   allowing to route requests
   regardless of the app's factual path.

.. _configuration-python-targets:

Targets
*******

You can configure up to 254 individual entry points
for a single Python app:

.. code-block:: json

   {
       "applications": {
           "python-app": {
               "type": "python",
               "path": "/www/apps/python-app/",
               "targets": {
                   "front": {
                       "module": "front.wsgi",
                       "callable": "app"
                   },

                   "back": {
                       "module": "back.wsgi",
                       "callable": "app"
                   }
               }
           }
       }
   }

Each target is an object
that specifies **module**
and can also define **callable** and **prefix**
just like a regular app does.
Targets can be used by the **pass** options
in listeners and routes
to serve requests:

.. code-block:: json

   {
       "listeners": {
           "127.0.0.1:8080": {
               "pass": "applications/python-app/front"
           },

           "127.0.0.1:80": {
               "pass": "routes"
           }
       },

       "routes": [
           {
               "match": {
                   "uri": "/back"
               },

               "action": {
                   "pass": "applications/python-app/back"
               }
           }
       ]
   }

The **home**, **path**, **protocol**, **threads**, and
**thread_stack_size** settings
are shared by all targets in the app.

.. warning::

   If you specify **targets**,
   there should be no **module** or **callable**
   defined at the app level.
   Moreover, you can't combine WSGI and ASGI targets
   within a single app.

.. note::

   For Python-based examples,
   see our
   :doc:`../howto/bottle`,
   :doc:`../howto/datasette`,
   :doc:`../howto/django`,
   :doc:`../howto/djangochannels`,
   :doc:`../howto/falcon`,
   :doc:`../howto/fastapi`,
   :doc:`../howto/flask`,
   :doc:`../howto/guillotina`,
   :doc:`../howto/mailman`,
   :doc:`../howto/mercurial`,
   :doc:`../howto/moin`,
   :doc:`../howto/plone`,
   :doc:`../howto/pyramid`,
   :doc:`../howto/quart`,
   :doc:`../howto/responder`,
   :doc:`../howto/reviewboard`,
   :doc:`../howto/sanic`,
   :doc:`../howto/starlette`,
   :doc:`../howto/trac`,
   and
   :doc:`../howto/zope`
   howtos or a basic
   :ref:`sample <sample-python>`.


.. _configuration-ruby:

====
Ruby
====

First, make sure to install Unit along with the
:ref:`Ruby language module <installation-precomp-pkgs>`.

.. note::

   Unit uses the
   `Rack <https://rack.github.io>`__
   interface
   to run Ruby scripts;
   you need to have it installed as well:

   .. code-block:: console

      $ gem install rack

Besides the
:ref:`common options <configuration-apps-common>`,
you have:

.. list-table::
   :header-rows: 1

   * - Option
     - Description

   * - **script** (required)
     - String; rack script pathname, including the **.ru** extension,
       for instance: **/www/rubyapp/script.ru**.

   * - **hooks**
     - String; pathname of the **.rb** file setting the event hooks invoked
       during the app's lifecycle.

   * - **threads**
     - Integer; number of worker threads per
       :ref:`app process <sec-processes>`. When started, each app process
       creates this number of threads to handle requests. The default is **1**.

Example:

.. code-block:: json

   {
      "type": "ruby",
      "processes": 5,
      "user": "www",
      "group": "www",
      "script": "/www/cms/config.ru",
      "hooks": "hooks.rb"
   }

The **hooks** script
is evaluated when the app starts.
If set, it can define blocks of Ruby code named
**on_worker_boot**,
**on_worker_shutdown**,
**on_thread_boot**,
or **on_thread_shutdown**.
If provided,
these blocks are called
at the respective points
of the app's lifecycle,
for example:

.. code-block:: ruby

   @mutex = Mutex.new

   File.write("./hooks.#{Process.pid}", "hooks evaluated")
   # Runs once at app load.

   on_worker_boot do
      File.write("./worker_boot.#{Process.pid}", "worker boot")
   end
   # Runs at worker process boot.

   on_thread_boot do
      @mutex.synchronize do
         # Avoids a race condition that may crash the app.
         File.write("./thread_boot.#{Process.pid}.#{Thread.current.object_id}",
                     "thread boot")
      end
   end
   # Runs at worker thread boot.

   on_thread_shutdown do
       @mutex.synchronize do
           # Avoids a race condition that may crash the app.
           File.write("./thread_shutdown.#{Process.pid}.#{Thread.current.object_id}",
                      "thread shutdown")
       end
   end
   # Runs at worker thread shutdown.

   on_worker_shutdown do
       File.write("./worker_shutdown.#{Process.pid}", "worker shutdown")
   end
   # Runs at worker process shutdown.

Use these hooks
to add custom runtime logic
to your app.

.. note::

   For Ruby-based examples,
   see our
   :doc:`../howto/rails`
   and
   :doc:`../howto/redmine`
   howtos or a basic
   :ref:`sample <sample-ruby>`.


.. _configuration-wasm:

===========
WebAssembly
===========

.. tabs::
   :prefix: unit-wasm
   :toc:

   .. tab:: wasm-wasi-component

       First, make sure to install Unit along with the
       :ref:`WebAssembly language module <installation-precomp-pkgs>`.

       Besides the
       :ref:`common options <configuration-apps-common>`,
       you have:

       .. list-table::
          :header-rows: 1

          * - Option
            - Description
          * - **component** (required)
            - String; WebAssembly component pathname, including the **.wasm**
              extension, for instance: "/var/www/wasm/component.wasm"
          * - **access**
            - Object;  its only array member, **filesystem**, lists
              directories to which the application has access:

              .. code-block:: json

                  "access": {
                     "filesystem": [
                        "/tmp/",
                        "/var/tmp/"
                     ]
                  }

       Example:

       .. code-block:: json

          {
            "listeners": {
               "127.0.0.1:8080": {
                  "pass": "applications/wasm"
               }
            },
            "applications": {
               "wasm": {
                  "type": "wasm-wasi-component",
                  "component": "/var/www/app/component.wasm",
                  "access": {
                  "filesystem": [
                     "/tmp/",
                     "/var/tmp/"
                  ]
                  }
               }
            }
          }

       .. note::
          A good, first Rust-based project is available at
          `sunfishcode/hello-wasi-http <https://github.com/sunfishcode/hello-wasi-http>`__.
          It also includes all the important steps to get started with WebAssembly, WASI, and Rust.

   .. tab:: unit-wasm

       .. warning::
          The `unit-wasm` module is deprecated.
          We recommend using `wasm-wasi-component` instead, which supports
          WebAssembly Components using standard WASI 0.2 interfaces.
          The `wasm-wasi-component` module is available in Unit 1.32 and later.

       First, make sure to install Unit along with the
       :ref:`WebAssembly language module <installation-precomp-pkgs>`.

       Besides the
       :ref:`common options <configuration-apps-common>`,
       you have:

       .. list-table::
          :header-rows: 1

          * - Option
            - Description
          * - **module** (required)
            - String; WebAssembly module pathname, including the **.wasm** extension,
              for instance: **applications/wasmapp/module.wasm**.
          * - **request_handler** (required)
            - String; name of the request handler function. If you use Unit
              with the official :program:`unit-wasm` :ref:`package <installation-precomp-pkgs>`,
              the value is language specific; see the
              `SDK <https://github.com/nginx/unit-wasm/>`__ documentation for details.
              Otherwise, use the name of your custom implementation.

              The runtime calls this handler, providing the address of the
              shared memory block used to pass data in and out the app.
          * - **malloc_handler** (required)
            - String; name of the memory allocator function.  See note above regarding
              language-specific handlers in the official `unit-wasm` package.

              The runtime calls this handler at language module startup to allocate
              the shared memory block used to pass data in and out the app.
          * - **free_handler** (required)
            - String;  name of the memory deallocator function.  See note above regarding
              language-specific handlers in the official `unit-wasm` package.

              The runtime calls this handler at language module shutdown to free
              the shared memory block used to pass data in and out the app.
          * - **access**
            - Object;  its only array member, **filesystem**, lists directories
              the application can access:

              .. code-block:: json

                  "access": {
                     "filesystem": [
                        "/tmp/",
                        "/var/tmp/"
                     ]
                  }

          * - **module_init_handler**,
            - String;
              name of the module initilization function.
              If you use Unit with the official :program:`unit-wasm`
              :ref:`package <installation-precomp-pkgs>`,
              the value is language specific;
              see the `SDK <https://github.com/nginx/unit-wasm/>`__
              documentation for details.
              Otherwise, use the name of your custom implementation.

              It is invoked by the WebAssembly language module
              at language module startup,
              after the WebAssembly module was initialized.

          * - **module_end_handler**
            - String;
              name of the module finalization function.
              If you use Unit with the official :program:`unit-wasm`
              :ref:`package <installation-precomp-pkgs>`,
              the value is language specific;
              see the `SDK <https://github.com/nginx/unit-wasm/>`__
              documentation for details.
              Otherwise, use the name of your custom implementation.

              It is invoked by the WebAssembly language module
              at language module shutdown.

          * - **request_init_handler**
            - String;
              name of the request initialization function.
              If you use Unit with the official :program:`unit-wasm`
              :ref:`package <installation-precomp-pkgs>`,
              the value is language specific;
              see the `SDK <https://github.com/nginx/unit-wasm/>`__
              documentation for details.
              Otherwise, use the name of your custom implementation.

              It is invoked by the WebAssembly language module
              at the start of each request.

          * - **request_end_handler**
            - String;
              name of the request finalization function.
              If you use Unit with the official :program:`unit-wasm`
              :ref:`package <installation-precomp-pkgs>`,
              the value is language specific;
              see the `SDK <https://github.com/nginx/unit-wasm/>`__
              documentation for details.
              Otherwise, use the name of your custom implementation.

              It is invoked by the WebAssembly language module
              at the end of each request,
              when the headers and the request body were received.

          * - **response_end_handler**
            - String;
              name of the response finalization function.
              If you use Unit with the official :program:`unit-wasm`
              :ref:`package <installation-precomp-pkgs>`,
              the value is language specific;
              see the `SDK <https://github.com/nginx/unit-wasm/>`__
              documentation for details.
              Otherwise, use the name of your custom implementation.

              It is invoked by the WebAssembly language module
              at the end of each response,
              when the headers and the response body were sent.

       Example:

       .. code-block:: json

           {
               "type": "wasm",
               "module": "/www/webassembly/unitapp.wasm",
               "request_handler": "my_custom_request_handler",
               "malloc_handler": "my_custom_malloc_handler",
               "free_handler": "my_custom_free_handler",
               "access": {
                   "filesystem": [
                       "/tmp/",
                       "/var/tmp/"
                   ]
               },
               "module_init_handler": "my_custom_module_init_handler",
               "module_end_handler": "my_custom_module_end_handler",
               "request_init_handler": "my_custom_request_init_handler",
               "request_end_handler": "my_custom_request_end_handler",
               "response_end_handler": "my_custom_response_end_handler"
           }

       Use these handlers to add custom runtime logic to your app; for a detailed
       discussion of their usage and requirements, see the
       `SDK <https://github.com/nginx/unit-wasm/>`__ source code and documentation.

       .. note::

           For WASM-based examples, see our :ref:`Rust and C samples <sample-wasm>`.

.. _configuration-stngs:

********
Settings
********

Unit has a global **settings** configuration object
that stores instance-wide preferences.

.. list-table::
    :header-rows: 1

    * - Option
      - Description

    * - **listen_threads**
      - Integer;
        controls the number of router threads created to handle client
        connections. Each thread includes all the configured listeners.

        By default, we create as many threads as the number of CPUs that
        are available to run on.

        *(since 1.33.0)*

    * - **http**
      - Object;
        fine-tunes handling of HTTP requests
        from the clients.

    * - **js_module**
      - String or an array of strings;
        lists enabled
        :program:`njs`
        :doc:`modules <../scripting>`,
        uploaded
        via the :doc:`control API <../controlapi>`.

In turn, the **http** option exposes the following settings:

.. list-table::
    :header-rows: 1

    * - Option
      - Description

    * - **body_read_timeout**
      - Maximum number of seconds
        to read data from the body
        of a client's request.
        This is the interval
        between consecutive read operations,
        not the time to read the entire body.
        If Unit doesn't receive any data
        from the client
        within this interval,
        it returns a 408 "Request Timeout" response.

        The default is 30.

    * - **discard_unsafe_fields**
      - Boolean;
        controls header field name parsing.
        If it's set to **true**,
        Unit only processes header names
        made of alphanumeric characters and hyphens
        (see
        `RFC 9110
        <https://datatracker.ietf.org/doc/html/rfc9110#section-16.3.1-6>`__);
        otherwise,
        these characters are also permitted:
        **.!#$%&'*+^_`|~**.

        The default is **true**.

    * - **header_read_timeout**
      - Maximum number of seconds
        to read the header
        of a client's request.
        If Unit doesn't receive the entire header
        from the client
        within this interval,
        it returns a 408 "Request Timeout" response.

        The default is 30.

    * - **idle_timeout**
      - Maximum number of seconds
        between requests
        in a keep-alive connection.
        If no new requests
        arrive within this interval,
        Unit returns a 408 "Request Timeout" response
        and closes the connection.

        The default is 180.

    * - **log_route**
      - Boolean;
        enables or disables
        :ref:`router logging <troubleshooting-router-log>`.

        The default is **false** (disabled).

    * - **max_body_size**
      - Maximum number of bytes
        in the body of a client's request.
        If the body size exceeds this value,
        Unit returns a 413 "Payload Too Large" response
        and closes the connection.

        The default is 8388608 (8 MB).

    * - **send_timeout**
      - Maximum number of seconds
        to transmit data
        as a response to the client.
        This is the interval
        between consecutive transmissions,
        not the time for the entire response.
        If no data
        is sent to the client
        within this interval,
        Unit closes the connection.

        The default is 30.

    * - **server_version**
      - Boolean;
        if set to **false**,
        Unit omits version information
        in its **Server** response
        `header fields
        <https://datatracker.ietf.org/doc/html/rfc9110.html#section-10.2.4>`__.

        The default is **true**.

        *(since 1.30.0)*

    * - **static**
      - Object;
        configures static asset handling.
        Has a single object option named **mime_types**
        that defines specific
        `MIME types
        <https://www.iana.org/assignments/media-types/media-types.xhtml>`__
        as options.
        Their values
        can be strings or arrays of strings;
        each string must specify a filename extension
        or a specific filename
        that's included in the MIME type.
        You can override default MIME types
        or add new types:

        .. code-block:: console

           # curl -X PUT -d '{"text/x-code": [".c", ".h"]}' :nxt_ph:`/path/to/control.unit.sock <Path to Unit's control socket in your installation>` \
                  http://localhost/config/settings/http/static/mime_types
           {
                  "success": "Reconfiguration done."
           }

        .. _configuration-mime:

        Defaults:
        **.aac**, **.apng**, **.atom**,
        **.avi**, **.avif**, **avifs**, **.bin**, **.css**,
        **.deb**, **.dll**, **.exe**, **.flac**, **.gif**,
        **.htm**, **.html**, **.ico**, **.img**, **.iso**,
        **.jpeg**, **.jpg**, **.js**, **.json**, **.md**,
        **.mid**, **.midi**, **.mp3**, **.mp4**, **.mpeg**,
        **.mpg**, **.msi**, **.ogg**, **.otf**, **.pdf**,
        **.php**, **.png**, **.rpm**, **.rss**, **.rst**,
        **.svg**, **.ttf**, **.txt**, **.wav**, **.webm**,
        **.webp**, **.woff2**, **.woff**, **.xml**, and
        **.zip**.

.. _configuration-access-log:

**********
Access log
**********

To enable basic access logging,
specify the log file path
in the **access_log** option
of the **config** object.

In the example below,
all requests will be logged
to **/var/log/access.log**:

.. code-block:: console

   # curl -X PUT -d '"/var/log/access.log"' \
          --unix-socket :nxt_ph:`/path/to/control.unit.sock <Path to Unit's control socket in your installation>` \
          http://localhost/config/access_log

       {
           "success": "Reconfiguration done."
       }

By default, the log is written in the
`Combined Log Format
<https://httpd.apache.org/docs/2.2/logs.html#combined>`__.
Example of a CLF line:

.. code-block:: none

   127.0.0.1 - - [21/Oct/2015:16:29:00 -0700] "GET / HTTP/1.1" 200 6022 "http://example.com/links.html" "Godzilla/5.0 (X11; Minix i286) Firefox/42"

=====================
Custom log formatting
=====================

.. _custom-log-format:

The **access_log** option
can be also set to an object
to customize both the log path
and its format:

.. list-table::
    :header-rows: 1

    * - Option
      - Description

    * - **format**
      - String;
        sets the log format.
        Besides arbitrary text,
        can contain any
        :ref:`variables <configuration-variables>`
        Unit supports.

    * - **path**
      - String;
        pathname of the access log file.

Example:

.. code-block:: json

   {
       "access_log": {
           "path": "/var/log/unit/access.log",
           "format": "$remote_addr - - [$time_local] \"$request_line\" $status $body_bytes_sent \"$header_referer\" \"$header_user_agent\""
       }
   }

By a neat coincidence,
the above **format**
is the default setting.
Also, mind that the log entry
is formed *after* the request has been handled.

Besides
:ref:`built-in variables <configuration-variables-native>`,
you can use :program:`njs`
:doc:`templates <../scripting>`
to define the log format:

.. code-block:: json

   {
       "access_log": {
           "path": "/var/log/unit/basic_access.log",
           "format": "`${host + ': ' + uri}`"
       }
   }


======================
Conditional access log
======================

.. _conditional-access-log:

The **access_log** can be dynamically turned on and off by using the **if** option:

.. list-table::
    :header-rows: 1

    * - Option
      - Description

    * - **if**
      - if the value is empty, 0, false, null, or undefined,
        the logs will not be recorded.

This feature lets users set conditions to determine whether access logs are
recorded. The **if** option supports a string and JavaScript code.
If its value is empty, 0, false, null, or undefined, the logs will not be
recorded. And the '!' as a prefix inverses the condition.

Example without njs:

.. code-block:: json

   {
      "access_log": {
         "if": "$cookie_session",
         "path": "..."
      }
   }

All requests using a session cookie named **session** will be logged.

We can add ! to inverse the condition.

.. code-block:: json

   {
      "access_log": {
         "if": "!$cookie_session",
         "path": "..."
      }
   }

Now, all requests without a session cookie will be logged.

Example with njs and the use of a template literal:

.. code-block:: json

   {
      "access_log": {
         "if": "`${uri == '/health' ? false : true}`",
         "path": "..."
      }
   }