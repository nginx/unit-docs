.. meta::
   :og:description: Create and maintain a working configuration using certificates, listeners, routes, apps, and upstreams.

.. include:: include/replace.rst

#############
Configuration
#############

.. _configuration-quickstart:

***********
Quick Start
***********

To run an application on Unit, first set up an :ref:`application
<configuration-applications>` object.  Let's store it in a file to :samp:`PUT`
it into the :samp:`config/applications` section of Unit's control API,
available via the :ref:`control socket <installation-src-startup>` at
:samp:`http://localhost/`:

.. code-block:: console

   $ cat << EOF > config.json

       {
           "type": "php",
           "root": "/www/blogs/scripts"
       }
       EOF

   # curl -X PUT --data-binary @config.json --unix-socket \
          /path/to/control.unit.sock http://localhost/config/applications/blogs

       {
           "success": "Reconfiguration done."
       }

Unit starts the application process.  Next, reference the application object
from a :ref:`listener <configuration-listeners>` object, comprising an IP (or a
wildcard to match any IPs) and a port number, in the :samp:`config/listeners`
section of the API:

.. code-block:: console

   $ cat << EOF > config.json

       {
           "pass": "applications/blogs"
       }
       EOF

   # curl -X PUT --data-binary @config.json --unix-socket \
          /path/to/control.unit.sock http://localhost/config/listeners/127.0.0.1:8300

       {
           "success": "Reconfiguration done."
       }

Unit accepts requests at the specified IP and port, passing them to the
application process.  Your app works!

Finally, check the resulting configuration:

.. code-block:: console

   # curl --unix-socket /path/to/control.unit.sock http://localhost/config/

       {
           "listeners": {
               "127.0.0.1:8300": {
                   "pass": "applications/blogs"
               }
           },

           "applications": {
               "blogs": {
                   "type": "php",
                   "root": "/www/blogs/scripts/"
               }
           }
       }

You can upload the entire configuration at once or update it in portions.  For
details of configuration techniques, see :ref:`below <configuration-mgmt>`.
For a full configuration sample, see :ref:`here <configuration-full-example>`.


.. _configuration-mgmt:

************************
Configuration Management
************************

Unit's configuration is JSON-based, accessed via the :ref:`control socket
<installation-src-startup>`, and entirely manageable over HTTP.

.. note::

   Here, we use :program:`curl` to query Unit's control API, prefixing URIs
   with :samp:`http://localhost` as expected by this utility.  You can use any
   tool capable of making HTTP requests; also, the hostname is irrelevant for
   Unit.

To address parts of the configuration, query the control socket over HTTP; URI
path segments of your requests to the API must be names of its `JSON object
members <https://datatracker.ietf.org/doc/html/rfc8259#section-4>`_ or indexes
of its `array elements
<https://datatracker.ietf.org/doc/html/rfc8259#section-5>`_.

You can manipulate the API with the following HTTP methods:

.. list-table::
   :header-rows: 1

   * - Method
     - Action

   * - :samp:`GET`
     - Returns the entity at the request URI as a JSON value in the HTTP
       response body.

   * - :samp:`POST`
     - Updates the *array* at the request URI, appending the JSON value
       from the HTTP request body.

   * - :samp:`PUT`
     - Replaces the entity at the request URI and returns status message in the
       HTTP response body.

   * - :samp:`DELETE`
     - Deletes the entity at the request URI and returns status message in the
       HTTP response body.

Before a change, Unit evaluates the difference it causes in the entire
configuration; if there's none, nothing is done.  For example, you can't
:ref:`restart <configuration-proc-mgmt>` an updated app by uploading the same
configuration it already has.

Unit performs actual reconfiguration steps as gracefully as possible: running
tasks expire naturally, connections are properly closed, processes end
smoothly.

Any type of update can be done with different URIs, provided you supply the
right JSON:

.. code-block:: console

   # curl -X PUT -d '{ "pass": "applications/blogs" }' --unix-socket \
          /path/to/control.unit.sock http://localhost/config/listeners/127.0.0.1:8300

   # curl -X PUT -d '"applications/blogs"' --unix-socket /path/to/control.unit.sock \
          http://localhost/config/listeners/127.0.0.1:8300/pass

However, mind that the first command replaces the *entire* listener, dropping
any other options you could have configured, whereas the second one replaces
only the :samp:`pass` value and leaves other options intact.

.. nxt_details:: Examples

   To minimize typos and effort, avoid embedding JSON payload in your commands;
   instead, consider storing your configuration snippets for review and reuse.
   Suppose you save your application object as :file:`wiki.json`:

   .. code-block:: json

      {
          "type": "python",
          "module": "wsgi",
          "user": "www-wiki",
          "group": "www-wiki",
          "path": "/www/wiki/"
      }

   Use it to set up an application called :samp:`wiki-prod`:

   .. code-block:: console

      # curl -X PUT --data-binary @/path/to/wiki.json \
             --unix-socket /path/to/control.unit.sock http://localhost/config/applications/wiki-prod

   Use it again to set up a development version of the same app called
   :samp:`wiki-dev`:

   .. code-block:: console

      # curl -X PUT --data-binary @/path/to/wiki.json \
             --unix-socket /path/to/control.unit.sock http://localhost/config/applications/wiki-dev

   Toggle the :samp:`wiki-dev` app to another source code directory:

   .. code-block:: console

      # curl -X PUT -d '"/www/wiki-dev/"' \
             --unix-socket /path/to/control.unit.sock http://localhost/config/applications/wiki-dev/path

   Next, boost the process count for the production app to warm it up a bit:

   .. code-block:: console

      # curl -X PUT -d '5' \
             --unix-socket /path/to/control.unit.sock http://localhost/config/applications/wiki-prod/processes

   Add a listener for the :samp:`wiki-prod` app to accept requests at all host
   IPs:

   .. code-block:: console

      # curl -X PUT -d '{ "pass": "applications/wiki-prod" }' \
             --unix-socket /path/to/control.unit.sock 'http://localhost/config/listeners/*:8400'

   Plug the :samp:`wiki-dev` app into the listener to test it:

   .. code-block:: console

      # curl -X PUT -d '"applications/wiki-dev"' --unix-socket /path/to/control.unit.sock \
             'http://localhost/config/listeners/*:8400/pass'

   Then rewire the listener, adding a URI-based route to the development
   version of the app:

   .. code-block:: console

      $ cat << EOF > config.json

          [
              {
                  "match": {
                      "uri": "/dev/*"
                  },

                  "action": {
                      "pass": "applications/wiki-dev"
                  }
              }
          ]
          EOF

      # curl -X PUT --data-binary @config.json --unix-socket \
             /path/to/control.unit.sock http://localhost/config/routes

      # curl -X PUT -d '"routes"' --unix-socket \
             /path/to/control.unit.sock 'http://localhost/config/listeners/*:8400/pass'

   Next, let's change the :samp:`wiki-dev`'s URI prefix in the :samp:`routes`
   array using its index (0):

   .. code-block:: console

      # curl -X PUT -d '"/development/*"' --unix-socket=/path/to/control.unit.sock \
             http://localhost/config/routes/0/match/uri

   Let's add a route to the prod app: :samp:`POST` always adds to the array
   end, so there's no need for an index:

   .. code-block:: console

      # curl -X POST -d '{"match": {"uri": "/production/*"}, \
             "action": {"pass": "applications/wiki-prod"}}'  \
             --unix-socket=/path/to/control.unit.sock        \
             http://localhost/config/routes/

   Otherwise, use :samp:`PUT` with the array's last index (0 in our sample)
   *plus one* to add the new item at the end:

   .. code-block:: console

      # curl -X PUT -d '{"match": {"uri": "/production/*"}, \
             "action": {"pass": "applications/wiki-prod"}}' \
             --unix-socket=/path/to/control.unit.sock       \
             http://localhost/config/routes/1/

   To get the complete :samp:`config` section:

   .. code-block:: console

      # curl --unix-socket /path/to/control.unit.sock http://localhost/config/

          {
              "listeners": {
                  "*:8400": {
                      "pass": "routes"
                  }
              },

              "applications": {
                  "wiki-dev": {
                      "type": "python",
                      "module": "wsgi",
                      "user": "www-wiki",
                      "group": "www-wiki",
                      "path": "/www/wiki-dev/"
                  },

                  "wiki-prod": {
                      "type": "python",
                      "processes": 5,
                      "module": "wsgi",
                      "user": "www-wiki",
                      "group": "www-wiki",
                      "path": "/www/wiki/"
                  }
              },

              "routes": [
                  {
                      "match": {
                          "uri": "/development/*"
                      },

                      "action": {
                          "pass": "applications/wiki-dev"
                      }
                  },
                  {
                      "action": {
                          "pass": "applications/wiki-prod"
                      }
                  }
              ]
          }

   To obtain the :samp:`wiki-dev` application object:

   .. code-block:: console

      # curl --unix-socket /path/to/control.unit.sock \
             http://localhost/config/applications/wiki-dev

          {
              "type": "python",
              "module": "wsgi",
              "user": "www-wiki",
              "group": "www-wiki",
              "path": "/www/wiki-dev/"
          }

   You can save JSON returned by such requests as :file:`.json` files for
   update or review:

   .. code-block:: console

      # curl --unix-socket /path/to/control.unit.sock \
             http://localhost/config/ > config.json

   To drop the listener on :samp:`\*:8400`:

   .. code-block:: console

      # curl -X DELETE --unix-socket /path/to/control.unit.sock \
             'http://localhost/config/listeners/*:8400'

   Mind that you can't delete objects that other objects rely on, such as a
   route still referenced by a listener:

   .. code-block:: console

      # curl -X DELETE --unix-socket /var/run/unit/control.sock \
              http://localhost/config/routes

           {
               "error": "Invalid configuration.",
               "detail": "Request \"pass\" points to invalid location \"routes\"."
           }

.. nxt_details:: Replicating Unit Configurations

   Although Unit is fully dynamic, sometimes you just want to copy an existing
   setup without the need for subsequent meddling.  Unit's :ref:`state
   directories <installation-config-src-state>` are interchangeable, provided
   they are used by the same version of Unit that created them, so you can use
   a shortcut to replicate a Unit instance.

   .. warning::

      Unit's state can change its structure between versions and shouldn't be
      edited by external means.

   On the machine where the *reference* Unit instance runs, find out
   where the state is stored:

   .. code-block:: console

      $ unitd -h

            --state DIRECTORY    set state directory name
                                 default: ":nxt_ph:`/path/to/reference/unit/state <The value we're looking for>`"

   Double-check that the state location isn't overridden at startup:

   .. subs-code-block:: console

      $ ps ax | grep unitd
            ...
            unit: main v|version| [unitd --state :nxt_ph:`/runtime/path/to/reference/unit/state <The runtime value overrides the default>` ... ]

   Repeat these commands on the second machine to see where the target instance
   stores its state.

   Stop both Unit instances, for example:

   .. code-block:: console

      # systemctl stop unit

   .. note::

      Different stop and start commands may be needed if you use a
      :ref:`non-official <installation-community-repos>` installation
      method.

   Copy the reference state directory to the target state directory by
   arbitrary means; make sure to include subdirectories and hidden files.
   Finally, restart both Unit instances:

   .. code-block:: console

      # systemctl restart unit

   .. note::

      If you run your Unit instances manually, :option:`!--state` can be
      used to set the state directory at :ref:`startup
      <installation-src-startup>`.

   After the restart, the target instance picks up the configuration you've
   copied to the state directory.


.. _configuration-listeners:

*********
Listeners
*********

To start accepting requests, add a listener object in the
:samp:`config/listeners` API section.  The object's name uniquely combines a
host IP address and a port that Unit binds to; a wildcard matches any host IPs.

.. note::

   On Linux-based systems, wildcard listeners can't overlap with other
   listeners on the same port due to kernel-imposed rules.  For example,
   :samp:`*:8080` conflicts with :samp:`127.0.0.1:8080`; this means a listener
   can't be directly reconfigured from :samp:`*:8080` to :samp:`127.0.0.1:8080`
   or vice versa without deleting it first.

Unit dispatches the requests it receives to destinations referenced by
listeners.  You can plug several listeners into one destination or use a
single listener and hot-swap it between multiple destinations.

Available listener options:

.. list-table::
    :header-rows: 1

    * - Option
      - Description

    * - :samp:`pass`
      - Destination to which the listener passes incoming requests.  Possible
        alternatives:

        - :ref:`Application <configuration-applications>`:
          :samp:`applications/qwk2mart`

        - :ref:`PHP <configuration-php-targets>` or :ref:`Python
          <configuration-python-targets>` app target:
          :samp:`applications/myapp/section`

        - :ref:`Route <configuration-routes>`: :samp:`routes/route66`,
          :samp:`routes`

        - :ref:`Upstream <configuration-upstreams>`: :samp:`upstreams/rr-lb`

        .. note::

           The value is :ref:`variable <configuration-variables>`-interpolated;
           if it matches no configuration entities after interpolation, a 404
           "Not Found" response is returned.

    * - :samp:`tls`
      - Object, defines SSL/TLS :ref:`settings
        <configuration-listeners-ssl>`.

    * - :samp:`client_ip`
      - Object, configures client IP address :ref:`replacement
        <configuration-listeners-xff>`.


Here, a local listener accepts requests at port 8300 and passes them to the
:samp:`blogs` app :ref:`target <configuration-php-targets>` identified by the
:samp:`uri` :ref:`variable <configuration-variables>`.  The wildcard listener
on port 8400 relays requests at any host IPs to the :samp:`main` :ref:`route
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

Also, :samp:`pass` values can be `percent encoded
<https://datatracker.ietf.org/doc/html/rfc3986#section-2.1>`_.  For example,
you can escape slashes in entity names:

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
SSL/TLS Configuration
=====================

The :samp:`tls` object provides the following options:

.. list-table::
   :header-rows: 1

   * - Option
     - Description

   * - :samp:`certificate` (required)
     - String or string array, refers to one or more certificate bundles you
       have :ref:`uploaded <configuration-ssl>` earlier, enabling secure
       communication via the listener.

   * - :samp:`conf_commands`
     - Object, defines the SSL `configuration commands
       <https://www.openssl.org/docs/manmaster/man3/SSL_CONF_cmd.html>`__ to
       be set for the listener.

       To provide this option, Unit must be built and run on a system with
       OpenSSL 1.0.2+:

       .. code-block:: console

          $ openssl version

                OpenSSL 1.1.1d  10 Sep 2019

   * - :samp:`session`
     - Object, configures the TLS session cache and tickets for the listener.

To use a certificate bundle you've :ref:`uploaded <configuration-ssl>` earlier,
name it in the :samp:`certificate` option of the :samp:`tls` object:

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

.. nxt_details:: Configuring Multiple Bundles

   Since version 1.23.0, Unit supports configuring `Server Name Indication
   (SNI) <https://datatracker.ietf.org/doc/html/rfc6066#section-3>`__ on a
   listener by supplying an array of certificate bundle names for the
   :samp:`certificate` option value:

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

   If the connecting client sends a server name, Unit responds with the
   matching certificate bundle.  If the name matches several bundles, exact
   matches trump wildcards; if ambiguity remains, the one listed first is used.
   If there's no match or no server name was sent, Unit uses the first bundle
   on the list.

To set custom OpenSSL `configuration commands
<https://www.openssl.org/docs/manmaster/man3/SSL_CONF_cmd.html>`__ for a
listener, use the :samp:`conf_commands` object in :samp:`tls`:

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

The :samp:`session` object in :samp:`tls` configures the session settings of
the listener:

.. list-table::
   :header-rows: 1

   * - Option
     - Description

   * - :samp:`cache_size`
     - Integer, sets the number of sessions in the TLS session cache.

       The default is :samp:`0` (caching is disabled).

   * - :samp:`timeout`
     - Integer, sets the session timeout for the TLS session cache.

       When a new session is created, it is assigned a lifetime based on its
       creation time and current timeout value.  If a cached session is
       requested past its lifetime, it is not reused.

       The default is :samp:`300` (5 minutes).

   * - :samp:`tickets`
     - Boolean, string, or an array of strings; configures TLS session tickets.

       The default is :samp:`false` (tickets are disabled).

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

The :samp:`tickets` option works as follows:

- Boolean values enable or disable session tickets; when enabled, a random
  session ticket key is used:

  .. code-block:: json

     {
         "session": {
             "tickets": :nxt_hint:`true <Enables session tickets>`
         }
     }

- A string enables tickets and explicitly sets the session ticket key:

  .. code-block:: json

     {
         "session": {
             ":nxt_hint:`tickets <Enables session tickets, sets a single session ticket key>`": "IAMkP16P8OBuqsijSDGKTpmxrzfFNPP4EdRovXH2mqstXsodPC6MqIce5NlMzHLP"
         }
     }

  This can be employed to implement ticket reuse in scenarios where the key
  is shared between servers.

  Unit supports AES256 (80-byte keys) or AES128 (48-byte keys); the bytes
  should be encoded in Base64:

  .. code-block:: console

     $ openssl rand -base64 48

           LoYjFVxpUFFOj4TzGkr5MsSIRMjhuh8RCsVvtIJiQ12FGhn0nhvvQsEND1+OugQ7

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

  Unit uses these keys to decrypt the tickets submitted by clients who want to
  recover their session state; the last key is always used to create new
  session tickets and update the tickets created earlier.

  .. note::

     An empty array effectively disables session tickets, same as setting
     :samp:`tickets` to :samp:`false`.

.. _configuration-listeners-xff:

=============================
Originating IP Identification
=============================

Unit supports identification of the clients' originating IPs with the
:samp:`client_ip` object and its options:

.. list-table::
    :header-rows: 1

    * - Option
      - Description

    * - :samp:`header` (required)
      - String, defines the relevant HTTP header fields to expect in the
        request.  Unit expects them to follow the `X-Forwarded-For
        <https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Forwarded-For>`__
        notation with the field value being a comma- or space-separated list of
        IPv4 or IPv6 addresses.

    * - :samp:`source` (required)
      - String or array of strings, defines :ref:`address-based patterns
        <configuration-routes-matching-patterns>` for trusted addresses; the
        replacement occurs only if the source IP of the request is a
        :ref:`match <configuration-routes-matching-resolution>`.

    * - :samp:`recursive`
      - Boolean, controls how the header fields are traversed.

        The default value is :samp:`false` (no recursion).

Unit proceeds to inspect the :samp:`header` fields only if the source IP of the
request :ref:`matches <configuration-routes-matching-resolution>` the
:samp:`source` option.

Consider the following :samp:`client_ip` configuration:

.. code-block:: json

   {
       "client_ip": {
           "header": "X-Forwarded-For",
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

If :samp:`recursive` is set to :samp:`false` (default), Unit chooses the
*rightmost* address of the *last* :samp:`header` field as the originating IP.
In the example, it is set to 198.51.100.178 for requests from 192.0.2.0/24 or
198.51.100.0/24.

If :samp:`recursive` is set to :samp:`true`, Unit inspects all :samp:`header`
fields in reverse order.  Each is traversed from right to left until the first
non-trusted address; if found, it's chosen as the originating IP.  In the
example above with :samp:`"recursive": true`, the client IP would be set to
203.0.113.195 because 198.51.100.178 is also trusted; this simplifies working
behind multiple reverse proxies.

Finally, mind that :samp:`source` can use not only subnets but any
:ref:`address-based patterns <configuration-routes-matching-patterns>`:

.. code-block:: json

   {
       "client_ip": {
           "header": "X-Forwarded-For",
           "source": [
               ":nxt_hint:`198.51.100.1-198.51.100.254 <Ranges can be specified explicitly>`",
               ":nxt_hint:`!198.51.100.128/26 <Negation rejects any addresses originating here>`",
               ":nxt_hint:`203.0.113.195 <Individual addresses are supported as well>`"
           ]
       }
   }



.. _configuration-routes:

******
Routes
******

The :samp:`config/routes` configuration entity defines internal request
routing, receiving requests via :ref:`listeners <configuration-listeners>` and
filtering them through :ref:`sets of conditions
<configuration-routes-matching>` to be processed by :ref:`apps
<configuration-applications>`, :ref:`proxied <configuration-proxy>` to external
servers or :ref:`load-balanced <configuration-upstreams>` between them, served
with :ref:`static content <configuration-static>`, :ref:`answered
<configuration-return>` with arbitrary status codes, or :ref:`redirected
<configuration-return>`.

In its simplest form, :samp:`routes` can be a single route array:

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

Another form is an object with one or more named route arrays as members:

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
Route Steps
===========

A :ref:`route <configuration-routes>` array contains step objects as elements;
they accept the following options:

.. list-table::
   :header-rows: 1

   * - Option
     - Description

   * - :samp:`action` (required)
     - Object that defines how matching requests are :ref:`handled
       <configuration-routes-action>`.

   * - :samp:`match`
     - Object that defines the step's :ref:`conditions
       <configuration-routes-matching>` to be matched.

A request passed to a route traverses its steps sequentially:

- If all :samp:`match` conditions in a step are met, the step's :samp:`action`
  is performed.

- If a step's condition isn't met, Unit proceeds to the next step of the route.

- If no steps of the route match, a 404 "Not Found" response is returned.

.. warning::

  If a step omits the :samp:`match` option, its :samp:`action` is
  performed automatically.  Thus, use no more than one such step per
  route, always placing it last to avoid potential routing issues.

.. nxt_details:: Ad-Hoc Examples

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

   This route passes all requests to the :samp:`/php/` subsection of the
   :samp:`example.com` website via HTTPS to the :samp:`php_version` app.  All
   other requests are served with static content from the
   :samp:`/www/static_version/` directory.  If there's no matching content, a
   404 "Not Found" response is returned.

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

   Here, a route called :samp:`main` is explicitly defined, so :samp:`routes`
   is an object instead of an array.  The first step of the route passes all
   requests that arrive via HTTP to the :samp:`http_site` app.  The second step
   passes all requests that target :samp:`blog.example.com` to the :samp:`blog`
   app.  The final step serves requests for certain file types from the
   :samp:`/www/static/` directory.  If no steps match, a 404 "Not Found"
   response is returned.


.. _configuration-routes-matching:

===================
Matching Conditions
===================

Conditions in a :ref:`route step <configuration-routes-step>`'s :samp:`match`
object define patterns to be compared to the requests' properties:

.. list-table::
   :header-rows: 1

   * - Property
     - Patterns Are Matched Against
     - Case |-| :nxt_hint:`Sensitive <For arguments, cookies, and headers, this relates to property names and values; for other properties, case sensitivity affects only values>`

   * - :samp:`arguments`
     - Arguments supplied with the request's `query string
       <https://datatracker.ietf.org/doc/html/rfc3986#section-3.4>`__; these
       names and value pairs are `percent decoded
       <https://datatracker.ietf.org/doc/html/rfc3986#section-2.1>`__ with plus
       signs (:samp:`+`) replaced by spaces.
     - Yes

   * - :samp:`cookies`
     - Cookies supplied with the request.
     - Yes

   * - :samp:`destination`
     - Target IP address and optional port of the request.
     - No

   * - :samp:`headers`
     - `Header fields
       <https://datatracker.ietf.org/doc/html/rfc7230#section-3.2>`_ supplied
       with the request.
     - No

   * - :samp:`host`
     - :samp:`Host` `header field
       <https://datatracker.ietf.org/doc/html/rfc7230#section-5.4>`_, converted
       to lower case and normalized by removing the port number and the
       trailing period (if any).
     - No

   * - :samp:`method`
     - Method from the `request line
       <https://datatracker.ietf.org/doc/html/rfc7231#section-4>`_, converted
       to upper case.
     - No

   * - :samp:`query`
     - `Query string
       <https://datatracker.ietf.org/doc/html/rfc3986#section-3.4>`_, `percent
       decoded <https://datatracker.ietf.org/doc/html/rfc3986#section-2.1>`__
       with plus signs (:samp:`+`) replaced by spaces.
     - Yes

   * - :samp:`scheme`
     - URI `scheme
       <https://www.iana.org/assignments/uri-schemes/uri-schemes.xhtml>`_.
       Currently, only :samp:`http` and :samp:`https` are supported.
     - No

   * - :samp:`source`
     - Source IP address and optional port of the request.
     - No

   * - :samp:`uri`
     - `Request target
       <https://datatracker.ietf.org/doc/html/rfc7230#section-5.3>`_, `percent
       decoded <https://datatracker.ietf.org/doc/html/rfc3986#section-2.1>`__
       and normalized by removing the `query string
       <https://datatracker.ietf.org/doc/html/rfc3986#section-3.4>`__ and
       resolving `relative references
       <https://datatracker.ietf.org/doc/html/rfc3986#section-4.2>`__ ("." and
       "..", "//").
     - Yes

.. nxt_details:: Arguments vs. Query

   Both :samp:`arguments` and :samp:`query` operate on the query string, but
   :samp:`query` is matched against the entire string whereas :samp:`arguments`
   considers only the key-value pairs such as :samp:`key1=foo&key2=bar`.

   Use :samp:`arguments` to define conditions based on key-value pairs in the
   query string:

   .. code-block:: json

      "arguments": {
         "key1": "foo",
         "key2": "bar"
      }

   Argument order is irrelevant: :samp:`key1=foo&key2=bar` and
   :samp:`key2=bar&key1=foo` are considered the same.  Also, multiple
   occurences of an argument must all match, which means
   :samp:`key=foo&key=bar` matches this:

   .. code-block:: json

      "arguments":{
          "key": "*"
      }

   But not this:

   .. code-block:: json

      "arguments":{
          "key": "b*"
      }

   To the contrary, use :samp:`query` if your conditions concern query strings
   but don't rely on key-value pairs:

   .. code-block:: json

      "query": [
          "utf8",
          "utf16"
      ]

   This only matches query strings of the form
   :samp:`https://example.com?utf8` or :samp:`https://example.com?utf16`.


.. _configuration-routes-matching-resolution:

Match Resolution
****************

To be a match, the property must meet two requirements:

- If there are patterns without negation (the :samp:`!` prefix), at least one
  of them matches the property value.

- No negated patterns match the property value.

.. note::

   The :samp:`scheme` property accepts no patterns or arrays, but only two
   string values: :samp:`http` or :samp:`https`.

Here, the URI of the request must fit :samp:`pattern3`, but should not match
:samp:`pattern1` or :samp:`pattern2`.

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

.. nxt_details:: Formal Explanation

   This logic can be described with set operations.  Suppose set *U* comprises
   all possible values of a property; set *P* comprises strings that match any
   patterns without negation; set *N* comprises strings that match any
   negation-based patterns.  In this scheme, the matching set will be:

   | *U* ∩ *P* \\ *N* if *P* ≠ ∅
   | *U* \\ *N* if *P* = ∅

Additionally, special matching logic is used for :samp:`arguments`,
:samp:`cookies`, and :samp:`headers`. Each of these can be a single object that
lists custom-named properties and their patterns or an array of such objects.

To match a single object, the request must match *all* properties named in the
object.  To match an object array, it's enough to match *any* single one of its
item objects.  The following condition will match only if the request arguments
include both :samp:`arg1` and :samp:`arg2` and they match their patterns:

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

With an object array, the condition will match if the request's arguments
include either :samp:`arg1` or :samp:`arg2` (or maybe both) that matches the
respective pattern:

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

The following example combines all matching types.  Here, :samp:`host`,
:samp:`method`, :samp:`uri`, :samp:`arg1` *and* :samp:`arg2`, either
:samp:`cookie1` or :samp:`cookie2`, and either :samp:`header1` or
:samp:`header2` *and* :samp:`header3` must be matched for the :samp:`action` to
be taken (:samp:`host & method & uri & arg1 & arg2 & (cookie1 | cookie2) &
(header1 | (header2 & header3))`):

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

.. nxt_details:: Object Pattern Examples

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

   This requires :samp:`mode=strict` and any :samp:`access` argument other than
   :samp:`access=full` in the URI query.

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

   This matches requests that either use :samp:`gzip` and identify as
   :samp:`Mozilla/5.0` or list :samp:`curl` as the user agent.


.. _configuration-routes-matching-patterns:

Pattern Syntax
**************

Individual patterns can be address-based (:samp:`source` and
:samp:`destination`) or string-based (other properties).

String-based patterns must match the property to a character; wildcards or
:nxt_hint:`regexes <Available only if Unit was built with PCRE support enabled,
which is the default for the official packages>` modify this behavior:

- A wildcard pattern may contain any combination of wildcards (:samp:`*`), each
  standing for an arbitrary number of characters: :samp:`How*s*that*to*you`.

- A regex pattern starts with a tilde (:samp:`~`):
  :samp:`~^\\\\d+\\\\.\\\\d+\\\\.\\\\d+\\\\.\\\\d+` (escaping backslashes is a
  JSON `requirement <https://www.json.org/json-en.html>`_).  Regexes are `PCRE
  <https://www.pcre.org/current/doc/html/pcre2syntax.html>`_-flavored.

.. nxt_details:: Percent Encoding In Arguments, Query, and URI Patterns

   Argument names, non-regex string patterns in :samp:`arguments`,
   :samp:`query`, and :samp:`uri` can be `percent encoded
   <https://datatracker.ietf.org/doc/html/rfc3986#section-2.1>`_ to mask
   special characters (:samp:`!` is :samp:`%21`, :samp:`~` is :samp:`%7E`,
   :samp:`*` is :samp:`%2A`, :samp:`%` is :samp:`%25`) or even target single
   bytes.  For example, you can select diacritics such as Ö or Å by their
   starting byte :samp:`0xC3` in UTF-8:

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

   Unit decodes such strings and matches them against respective request
   entities, decoding these as well:

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

   Note that the encoded spaces (:samp:`%20`) in the request match their
   unencoded counterparts in the pattern; vice versa, the encoded tilde
   (:samp:`%7E`) in the condition matches :samp:`~` in the request.


.. nxt_details:: String Pattern Examples

   .. code-block:: json

      {
          "match": {
              "uri": "~^/data/www/.*\\.php(/.*)?$"
          },

          "action": {
              "pass": ":nxt_ph:`... <Any acceptable 'pass' value may go here; see the 'Listeners' section for details>`"
          }
      }

   A regular expression that matches any :file:`.php` files within the
   :file:`/data/www/` directory and its subdirectories.  Note the backslashes;
   escaping is a JSON-specific requirement.

   .. code-block:: json

      {
          "match": {
              "host": "*.example.com"
          },

          "action": {
              "pass": ":nxt_ph:`... <Any acceptable 'pass' value may go here; see the 'Listeners' section for details>`"
          }
      }

   Only subdomains of :samp:`example.com` will match.

   .. code-block:: json

      {
          "match": {
              "uri": "/admin/*/*.php"
          },

          "action": {
              "pass": ":nxt_ph:`... <Any acceptable 'pass' value may go here; see the 'Listeners' section for details>`"
          }
      }

   Only requests for :samp:`.php` files located in :file:`/admin/`'s
   subdirectories will match.

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

   Here, any :samp:`eu-` subdomains of :samp:`example.com` will match except
   :samp:`eu-5.example.com`.

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

   Any methods will match except :samp:`HEAD` and :samp:`GET`.

   You can also combine certain special characters in a pattern:

   .. code-block:: json

      {
          "match": {
              "uri": "!*/api/*"
          },

          "action": {
              "pass": ":nxt_ph:`... <Any acceptable 'pass' value may go here; see the 'Listeners' section for details>`"
          }
      }

   Here, any URIs will match except the ones containing :samp:`/api/`.

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

   Here, URIs of any articles that don't look like :samp:`YYYY-MM-DD` dates
   will match.  Again, note the backslashes; this is a JSON requirement.

Address-based patterns define individual IPv4 (dot-decimal or `CIDR
<https://datatracker.ietf.org/doc/html/rfc4632>`__) or IPv6 (hexadecimal or
`CIDR <https://datatracker.ietf.org/doc/html/rfc4291#section-2.3>`__) addresses
that must exactly match the property value; wildcards and ranges modify this
behavior:

- Wildcards (:samp:`*`) can only be used to match arbitrary IPs
  (:samp:`*:<port>`).

- Ranges (:samp:`-`) can used with both IPs (in respective notation) and ports
  (:samp:`<start_port>-<end_port>`).

.. nxt_details::  Address Pattern Examples

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

   This uses IPv4-based matching with wildcards and ranges.

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

   This uses IPv6-based matching with wildcards and ranges.

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

   This matches any of the listed IPv4 or IPv6 addresses.

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

   Here, any IPs from the range will match, except for :samp:`192.0.2.9`.

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

   This matches any IPs but limits the acceptable ports.


.. _configuration-routes-action:

================
Handling Actions
================

If a request matches all :ref:`conditions <configuration-routes-matching>` of a
route step or the step itself omits the :samp:`match` object, Unit handles the
request using the respective :samp:`action`.  The mutually exclusive
:samp:`action` types are:

.. list-table::
   :header-rows: 1

   * - Option
     - Description
     - Details

   * - :samp:`pass`
     - Destination for the request, identical to a listener's
       :samp:`pass` option.
     - :ref:`configuration-listeners`

   * - :samp:`proxy`
     - Socket address of an HTTP server where the request is proxied.
     - :ref:`configuration-proxy`

   * - :samp:`return`
     - HTTP status code with a context-dependent redirect location.
     - :ref:`configuration-return`

   * - :samp:`share`
     - File paths that serve the request with static content.
     - :ref:`configuration-static`

An example:

.. code-block:: json

   {
       "routes": [
           {
               "match": {
                   "uri": "/pass/*"
               },

               "action": {
                   "pass": "applications/app"
               }
           },
           {
               "match": {
                   "uri": "~\\.jpe?g$"
               },

               "action": {
                   "share": "/var/www/static$uri",
                   "fallback": {
                       "share": "/var/www/static/assets$uri",
                       "fallback": {
                            "pass": "upstreams/cdn"
                       }
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

*********
Variables
*********

Some options in Unit configuration allow the use of variables whose values are
set in runtime:

- :samp:`pass` in :ref:`listeners <configuration-listeners>` and
  :ref:`actions <configuration-routes-action>` to choose between routes,
  applications, app targets, or upstreams.

- :samp:`share` and :samp:`chroot` in :ref:`actions
  <configuration-routes-action>` to control :ref:`static content serving
  <configuration-static>`.

Available variables:

.. list-table::
   :header-rows: 1

   * - Variable
     - Description

   * - :samp:`host`
     - :samp:`Host`
       `header field
       <https://datatracker.ietf.org/doc/html/rfc7230#section-5.4>`_ in
       lowercase, without the port number and the trailing period (if any).

   * - :samp:`method`
     - Method from the `request
       line <https://datatracker.ietf.org/doc/html/rfc7231#section-4>`_.

   * - :samp:`uri`
     - Request target `path
       <https://datatracker.ietf.org/doc/html/rfc7230#section-5.3>`_ without
       the query part, normalized by resolving relative path references ("."
       and "..") and collapsing adjacent slashes.  The value is `percent
       decoded <https://datatracker.ietf.org/doc/html/rfc3986#section-2.1>`_:
       Unit interpolates all percent-encoded entities in the request target
       `path <https://datatracker.ietf.org/doc/html/rfc7230#section-5.3>`_.

To reference a variable, prefix its name with the dollar sign character
(:samp:`$`), optionally enclosing the name in curly brackets (:samp:`{}`) to
separate it from adjacent text or enhance visibility.  Variable names can
contain letters and underscores (:samp:`_`), so use the brackets if the
variable is immediately followed by these characters:

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

At runtime, variables are replaced by dynamically computed values (at your
risk!).  For example, the listener above targets an entire set of routes,
picking individual ones by HTTP verbs that the incoming requests use:

.. code-block:: console

   $ curl -i -X GET http://localhost

       HTTP/1.1 201 Created

   $ curl -i -X PUT http://localhost

       HTTP/1.1 202 Accepted

   $ curl -i -X POST http://localhost

       HTTP/1.1 203 Non-Authoritative Information

   $ curl -i --head http://localhost  # Bumpy ride ahead, no route defined

       HTTP/1.1 404 Not Found

Another obvious usage is employing the URI to choose between applications:

.. code-block:: json

   {
       "listeners": {
           "*:80": {
               "pass": ":nxt_hint:`applications$uri <Note that the $uri variable value always includes a starting slash>`"
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

This way, we can route requests to applications by request target URIs.  A
different approach can route requests between applications by the :samp:`Host`
header field received from the client:

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

You can combine variables as you see fit, repeating them or placing them in
arbitrary order.  This configuration picks application targets by their names
and request methods:

.. code-block:: json

   {
       "listeners": {
           "*:80": {
               "pass": "applications/app${uri}_${method}"
           }
       }
   }


.. _configuration-return:

****************************
Instant Responses, Redirects
****************************

You can use route step :ref:`actions <configuration-routes-action>` to
instantly respond to certain conditions with arbitrary HTTP `status codes
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

The :samp:`return` action provides the following options:

.. list-table::

   * - :samp:`return` (required)
     - Integer (000-999), defines the HTTP response status code to be returned.

   * - :samp:`location`
     - URI, required if the :samp:`return` value implies redirection.

It is recommended to use the codes according to their `semantics
<https://datatracker.ietf.org/doc/html/rfc7231#section-6>`_; if you use custom
codes, make sure that user agents can understand them.

If you specify a redirect code (3xx), supply the destination using the
:samp:`location` option alongside :samp:`return`:

.. code-block:: json

   {
       "action": {
           "return": 301,
           "location": "https://www.example.com"
       }
   }


.. _configuration-static:

************
Static Files
************

Unit is capable of acting as a standalone web server, efficiently serving
static files from the local file system; to use the feature, list the file
paths in the :samp:`share` option of a route step :ref:`action
<configuration-routes-action>`.

A :samp:`share`-based action provides the following options:

.. list-table::

   * - :samp:`share` (required)
     - String or array of strings, listing file paths that are tried until a
       file is found; if it's not, :samp:`fallback` is used if set.

       The value is :ref:`variable <configuration-variables>`-interpolated.

   * - :samp:`fallback`
     - Action-like :ref:`object <configuration-fallback>`, used if the
       request can't be served by the :samp:`share`.

   * - :samp:`types`
     - Array of :ref:`MIME type <configuration-share-mime>` patterns, used
       to filter the shared files.

   * - :samp:`chroot`
     - Directory pathname that :ref:`restricts <configuration-share-path>`
       the shareable paths.

       The value is :ref:`variable <configuration-variables>`-interpolated.

   * - :samp:`follow_symlinks`, :samp:`traverse_mounts`
     - Booleans, enable or disable symbolic link and mount point
       :ref:`resolution <configuration-share-resolution>` respectively; if
       :samp:`chroot` is set, they only :ref:`affect <configuration-share-path>`
       the insides of :samp:`chroot`.

       The default for both options is :samp:`true` (resolve links and mounts).

.. note::

   To serve the files, Unit's router process must be able to access them; thus,
   the account this process runs as must have proper permissions :ref:`assigned
   <security-apps>`.  When Unit is installed from the :ref:`official packages
   <installation-precomp-pkgs>`, the process runs as :samp:`unit:unit`; for
   details of other installation methods, see :doc:`installation`.

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

It uses :ref:`variable interpolation <configuration-variables>`: Unit replaces
the :samp:`$uri` reference with its current value and tries the resulting path.
If it doesn't yield a servable file, a 404 "Not Found" response is returned.

.. warning::

   Before version 1.26.0, Unit used :samp:`share` as the document root.  This
   was changed for flexibility, so now :samp:`share` must resolve to specific
   files.  A common solution is to append :samp:`$uri` to your document root.

   In fact, if you update an existing Unit instance to 1.26+, its shares are
   automatically amended in this manner.  Pre-1.26, the snippet above would've
   looked like this:

   .. code-block:: json

      "action": {
          "share": "/www/static/"
      }

   Mind that URI paths always start with a slash, so there's no need to
   separate the directory from :samp:`$uri`; even if you do, Unit compacts
   adjacent slashes during path resolution, so there won't be an issue.

If :samp:`share` is an array, its items are searched in order of appearance
until a servable file is found:

.. code-block:: json

   "share": [
       "/www/$host$uri",
       "/www/global_static$uri",
   ]

This tries a :samp:`$host`-based directory first; if a suitable file isn't
found there, the search continues in :file:`/www/global_static/`.  If it also
fails, a 404 "Not Found" response is returned.

Finally, if a file path points to a directory, Unit attempts to serve an
:file:`index.html` file from it.  Suppose we have the following directory
structure and share configuration:

.. code-block:: none

   /www/static/
   ├── ...
   └──index.html

.. code-block:: json

   "action": {
       "share": "/www/static$uri"
   }

The following request returns :file:`index.html` even though the file isn't
named explicitly:

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

   Unit's ETag response header fields use the :samp:`MTIME-FILESIZE` format,
   where :samp:`MTIME` stands for file modification timestamp and
   :samp:`FILESIZE` stands for file size in bytes, both in hexadecimal.


.. _configuration-share-mime:

==============
MIME Filtering
==============

To filter the files a :samp:`share` serves by their :ref:`MIME types
<configuration-mime>`, define a :samp:`types` array of string patterns.
They work like :ref:`route patterns <configuration-routes-matching-patterns>`
but are matched to the MIME type of each file; the request is served only if
it's a :ref:`match <configuration-routes-matching-resolution>`:

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

This sample configuration blocks JS and CSS files with :ref:`negation
<configuration-routes-matching-resolution>` but allows all other text-based
MIME types with a :ref:`wildcard pattern
<configuration-routes-matching-patterns>`. Additionally, the :file:`.3gpp` and
:file:`.3gpp2` file types are allowed by a :ref:`regex pattern
<configuration-routes-matching-patterns>`.

If the MIME type of a requested file isn't recognized, it is considered empty
(:samp:`""`).  Thus, the :samp:`"!"` pattern ("deny empty strings") can be used
to restrict all file types :ref:`unknown <configuration-mime>` to Unit:

.. code-block:: json

   {
       "share": "/www/data/known-types-only$uri",
       "types": [
           "!"
       ]
   }

If a share path specifies only the directory name, Unit *doesn't* apply
:ref:`MIME filtering <configuration-share-mime>`.


.. _configuration-share-path:

=================
Path Restrictions
=================

.. note::

   To provide these options, Unit must be built and run on a system with Linux
   kernel version 5.6+.

The :samp:`chroot` option confines the path resolution within a share to a
certain directory.  First, it affects symbolic links: any attempts to go up the
directory tree with relative symlinks like :samp:`../../var/log` stop at the
:samp:`chroot` directory, and absolute symlinks are treated as relative to this
directory to avoid breaking out:

.. code-block:: json

   {
       "action": {
           "share": "/www/data$uri",
           "chroot": ":nxt_hint:`/www/data/ <Now, any paths accessible via the share are confined to this directory>`"
       }
   }

Here, a request for :file:`/log` initially resolves to :file:`/www/data/log`;
however, if that's an absolute symlink to :file:`/var/log/app.log`, the
resulting path is :file:`/www/data/var/log/app.log`.

Another effect is that any requests for paths that resolve outside the
:samp:`chroot` directory are forbidden:

.. code-block:: json

   {
       "action": {
           "share": "/www$uri",
           "chroot": ":nxt_hint:`/www/data/ <Now, any paths accessible via the share are confined to this directory>`"
       }
  }

Here, a request for :samp:`/index.xml` elicits a 403 "Forbidden" response
because it resolves to :samp:`/www/index.xml`, which is outside :samp:`chroot`.

.. _configuration-share-resolution:

The :samp:`follow_symlinks` and :samp:`traverse_mounts` options disable
resolution of symlinks and traversal of mount points when set to :samp:`false`
(both default to :samp:`true`):

.. code-block:: json

   {
       "action": {
           "share": "/www/$host/static$uri",
           "follow_symlinks": :nxt_hint:`false <Disables symlink traversal>`,
           "traverse_mounts": :nxt_hint:`false <Disables mount point traversal>`
       }
   }

Here, any symlink or mount point in the entire :samp:`share` path will result
in a 403 "Forbidden" response.

With :samp:`chroot` set, :samp:`follow_symlinks` and :samp:`traverse_mounts`
only affect portions of the path after :samp:`chroot`:

.. code-block:: json

   {
       "action": {
           "share": "/www/$host/static$uri",
           "chroot": "/www/$host/",
           "follow_symlinks": false,
           "traverse_mounts": false
       }
   }

Here, :file:`www/` and interpolated :samp:`$host` can be symlinks or mount
points, but any symlinks and mount points beyond them, including the
:file:`static/` portion, won't be resolved.

.. nxt_details:: Details

   Suppose you want to serve files from a share that itself includes a symlink
   (let's assume :samp:`$host` always resolves to :samp:`localhost` and make it
   a symlink in our example) but disable any symlinks inside the share.

   Initial configuration:

   .. code-block:: json

      {
          "action": {
              "share": "/www/$host/static$uri",
              "chroot": ":nxt_hint:`/www/$host/ <Now, any paths accessible via the share are confined to this directory>`"
          }
      }

   Create a symlink to :file:`/www/localhost/static/index.html`:

   .. code-block:: console

      $ mkdir -p /www/localhost/static/ && cd /www/localhost/static/
      $ cat > index.html << EOF

            > index.html
            > EOF

      $ ln -s index.html /www/localhost/static/symlink

   If symlink resolution is enabled (with or without :samp:`chroot`), a request
   that targets the symlink works:

   .. code-block:: console

      $ curl http://localhost/index.html

            index.html

      $ curl http://localhost/symlink

            index.html

   Now set :samp:`follow_symlinks` to :samp:`false`:

   .. code-block:: json

      {
          "action": {
              "share": "/www/$host/static$uri",
              "chroot": ":nxt_hint:`/www/$host/ <Now, any paths accessible via the share are confined to this directory>`",
              "follow_symlinks": false
          }
      }

   The symlink request is forbidden, which is presumably the desired effect:

   .. code-block:: console

      $ curl http://localhost/index.html

            index.html

      $ curl http://localhost/symlink

            <!DOCTYPE html><title>Error 403</title><p>Error 403.

   Lastly, what difference does :samp:`chroot` make?  To see, remove it:

   .. code-block:: json

      {
          "action": {
              "share": "/www/$host/static$uri",
              "follow_symlinks": false
          }
      }

   Now, :samp:`"follow_symlinks": false` affects the entire share, and
   :samp:`localhost` is a symlink, so it's forbidden:

   .. code-block:: console

      $ curl http://localhost/index.html

            <!DOCTYPE html><title>Error 403</title><p>Error 403.


.. _configuration-fallback:

===============
Fallback Action
===============

Finally, within an :samp:`action`, you can supply a :samp:`fallback` option
beside a :samp:`share`.  It specifies the :ref:`action
<configuration-routes-action>` to be taken if the requested file can't be
served from the :samp:`share` path:

.. code-block:: json

   {
       "share": "/www/data/static$uri",
       "fallback": {
           "pass": "applications/php"
       }
   }

Serving a file can be impossible for different reasons, such as:

- The request's HTTP method isn't :samp:`GET` or :samp:`HEAD`.

- The file's :ref:`MIME type <configuration-share-mime>` doesn't match the
  :samp:`types` array.

- The file isn't found at the :samp:`share` path.

- The router process has :ref:`insufficient permissions <security-apps>` to
  access the file or an underlying directory.

In the example above, an attempt to serve the requested file from the
:samp:`/www/data/static/` directory is made first.  Only if the file can't be
served, the request is passed to the :samp:`php` application.

If the :samp:`fallback` itself is a :samp:`share`, it can also contain a nested
:samp:`fallback`:

.. code-block:: json

   {
       "share": "/www/data/static$uri",
       "fallback": {
           "share": "/www/data/cache$uri",
           "fallback": {
               "proxy": "http://127.0.0.1:9000"
           }
       }
   }

First, this configuration tries to serve the request from the
:file:`/www/data/static/` directory; on failure, it queries the
:file:`/www/data/cache/` path.  Only if both attempts fail, the request is
proxied to an external server.

.. nxt_details:: Examples

   One common use case that this feature enables is the separation of requests
   for static and dynamic content into independent routes.  The following
   example relays all requests that target :file:`.php` files to an application
   and uses a catch-all static :samp:`share` with a :samp:`fallback`:

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

   You can reverse this scheme for apps that avoid filenames in dynamic URIs,
   listing all types of static content to be served from a :samp:`share` in a
   :samp:`match` condition and adding an unconditional application path:

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

   If image files should be served locally and other proxied, use the
   :samp:`types` array in the first route step:

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

   Another way to combine :samp:`share`, :samp:`types`, and :samp:`fallback` is
   exemplified by the following compact pattern:

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

   It forwards explicit requests for PHP files to the app while serving all
   other types of files from the share; note that a :samp:`match` object isn't
   needed here to achieve this effect.


.. _configuration-proxy:

********
Proxying
********

Unit's routes support HTTP proxying to socket addresses using the :samp:`proxy`
option of a route step :ref:`action <configuration-routes-action>`:

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

As the example above suggests, you can use Unix, IPv4, and IPv6 socket
addresses for proxy destinations.

.. note::

   The HTTPS scheme is not supported yet.


.. _configuration-upstreams:

==============
Load Balancing
==============

Besides proxying requests to individual servers, Unit can also relay incoming
requests to *upstreams*.  An upstream is a group of servers that comprise a
single logical entity and may be used as a :samp:`pass` destination for
incoming requests in a :ref:`listener <configuration-listeners>` or a
:ref:`route <configuration-routes>`.

Upstreams are defined in the eponymous :samp:`config/upstreams` section of the
API:

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

An upstream must define a :samp:`servers` object that lists socket addresses as
server object names.  Unit dispatches requests between the upstream's servers
in a round-robin fashion, acting as a load balancer.  Each server object can
set a numeric :samp:`weight` to adjust the share of requests it receives via
the upstream.  In the above example, :samp:`192.168.0.100:8080` receives twice
as many requests as :samp:`192.168.0.101:8080`.

Weights can be specified as integers or fractions in decimal or scientific
notation:

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

The maximum weight is :samp:`1000000`, the minimum is :samp:`0` (such servers
receive no requests), the default is :samp:`1`.


.. _configuration-applications:

************
Applications
************

Each app that Unit runs is defined as an object in the
:samp:`config/applications` section of the control API; it lists the app's
language and settings, its runtime limits, process model, and various
language-specific options.

.. note::

   Our official :ref:`language support packages <installation-precomp-pkgs>`
   include end-to-end examples of application configuration, available for your
   reference at :file:`/usr/share/doc/<module name>/examples/` after package
   installation.

Here, Unit runs 20 processes of a PHP app called :samp:`blogs`, stored in
the :file:`/www/blogs/scripts/` directory:

.. code-block:: json

   {
       "blogs": {
           "type": "php",
           "processes": 20,
           "root": "/www/blogs/scripts/"
       }
   }

.. _configuration-apps-common:

App objects have a number of options shared between all application languages:

.. list-table::
    :header-rows: 1

    * - Option
      - Description

    * - :samp:`type` (required)
      - Application type: :samp:`external` (Go and Node.js), :samp:`java`,
        :samp:`perl`, :samp:`php`, :samp:`python`, or :samp:`ruby`.

        Except with :samp:`external`, you can detail the runtime version:
        :samp:`"type": "python 3"`, :samp:`"type": "python 3.4"`, or even
        :samp:`"type": "python 3.4.9rc1"`.  Unit searches its modules and uses
        the latest matching one, reporting an error if none match.

        For example, if you have only one PHP module, 7.1.9, it matches
        :samp:`"php"`, :samp:`"php 7"`, :samp:`"php 7.1"`, and :samp:`"php
        7.1.9"`.  If you have modules for versions 7.0.2 and 7.0.23, set
        :samp:`"type": "php 7.0.2"` to specify the former; otherwise, PHP |_|
        7.0.23 will be used.

    * - :samp:`limits`
      - Object that accepts two integer options, :samp:`timeout` and
        :samp:`requests`.  Their values govern the life cycle of an
        application process.  For details, see
        :ref:`here <configuration-proc-mgmt-lmts>`.

    * - :samp:`processes`
      - Integer or object.  Integer sets a static number of app processes;
        object options :samp:`max`, :samp:`spare`, and :samp:`idle_timeout`
        enable dynamic management.  For details, see :ref:`here
        <configuration-proc-mgmt-prcs>`.

        The default value is 1.

    * - :samp:`working_directory`
      - The app's working directory.  If not set, the Unit daemon's working
        directory is used.

    * - :samp:`user`
      - Username that runs the app process.  If not set, the username
        configured at :ref:`build time <installation-config-src>` or :ref:`at
        startup <installation-src-startup>` to run Unit's non-privileged
        :ref:`processes <security-apps>` is used.

    * - :samp:`group`
      - Group name that runs the app process.  If not set, the :samp:`user`'s
        primary group is used.

    * - :samp:`environment`
      - Environment variables to be passed to the application.

Also, you need to set :samp:`type`-specific :ref:`options
<configuration-languages>` to run the app.  This :ref:`Python app
<configuration-python>` uses :samp:`path` and :samp:`module`:

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
Process Management
==================

Unit has three per-app options that control how the app's processes behave:
:samp:`isolation`, :samp:`limits`, and :samp:`processes`.  Also, you can send a
:samp:`GET` request to the :samp:`/control/applications/` API section to
restart an app:

.. code-block:: console

   # curl -X GET --unix-socket :nxt_ph:`/path/to/control.unit.sock <Path to Unit's control socket in your installation>`  \
         http://localhost/control/applications/:nxt_ph:`app_name <Your application's name as defined in the /config/applications/ section>`/restart

Unit handles the rollover gracefully, allowing the old processes to deal with
the existing requests and starting a new set of processes (as defined by the
:samp:`processes` :ref:`option <configuration-proc-mgmt-prcs>`) to accept new
requests.

.. _configuration-proc-mgmt-isolation:

Process Isolation
*****************

You can use `namespace
<https://man7.org/linux/man-pages/man7/namespaces.7.html>`_ and `file system
<https://man7.org/linux/man-pages/man2/chroot.2.html>`_ isolation for your apps
if Unit's underlying OS supports them:

.. code-block:: console

   $ ls /proc/self/ns/

       cgroup :nxt_hint:`mnt <The mount namespace>` :nxt_hint:`net <The network namespace>` pid ... :nxt_hint:`user <The credential namespace>` :nxt_hint:`uts <The uname namespace>`

The :samp:`isolation` application option has the following members:

.. list-table::
   :header-rows: 1

   * - Option
     - Description

   * - :samp:`namespaces`
     - Object that configures namespace isolation scheme for the application.

       Available options (system-dependent; check your OS manual for guidance):

       .. list-table::

          * - :samp:`cgroup`
            - Creates a new `cgroup
              <https://man7.org/linux/man-pages/man7/cgroup_namespaces.7.html>`_
              namespace for the app.

          * - :samp:`credential`
            - Creates a new `user
              <https://man7.org/linux/man-pages/man7/user_namespaces.7.html>`_
              namespace for the app.

          * - :samp:`mount`
            - Creates a new `mount
              <https://man7.org/linux/man-pages/man7/mount_namespaces.7.html>`_
              namespace for the app.

          * - :samp:`network`
            - Creates a new `network
              <https://man7.org/linux/man-pages/man7/network_namespaces.7.html>`_
              namespace for the app.

          * - :samp:`pid`
            - Creates a new `PID
              <https://man7.org/linux/man-pages/man7/pid_namespaces.7.html>`_
              namespace for the app.

          * - :samp:`uname`
            - Creates a new `UTS
              <https://man7.org/linux/man-pages/man7/namespaces.7.html>`_
              namespace for the app.

       All options listed above are Boolean; to isolate the app, set the
       corresponding namespace option to :samp:`true`; to disable isolation,
       set the option to :samp:`false` (default).

   * - :samp:`uidmap`
     - Array of `ID mapping
       <https://man7.org/linux/man-pages/man7/user_namespaces.7.html>`_
       objects; each array item must define the following:

       .. list-table::

          * - :samp:`container`
            - Integer that starts the user ID mapping range in the app's
              namespace.

          * - :samp:`host`
            - Integer that starts the user ID mapping range in the OS
              namespace.

          * - :samp:`size`
            - Integer size of the ID range in both namespaces.

   * - :samp:`gidmap`
     - Same as :samp:`uidmap`, but configures group IDs instead of user IDs.

   * - :samp:`rootfs`
     - Pathname of the directory to be used as the new `file system root
       <https://man7.org/linux/man-pages/man2/chroot.2.html>`_ for the app.

   * - :samp:`automount`
     - Object that controls mount behavior if :samp:`rootfs` is enabled.  By
       default, Unit automatically mounts the :ref:`language runtime
       dependencies <configuration-lang-runtime>`, a `procfs
       <https://man7.org/linux/man-pages/man5/procfs.5.html>`_ at
       :file:`/proc/`, and a `tmpfs
       <https://man7.org/linux/man-pages/man5/tmpfs.5.html>`_ at :file:`/tmp/`,
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

A sample :samp:`isolation` object that enables all namespaces and sets mappings
for user and group IDs:

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

.. nxt_details:: Using Uidmap And Gidmap

   The :samp:`uidmap` and :samp:`gidmap` options are available only if the
   underlying OS supports user namespaces.

   If :samp:`uidmap` is omitted but :samp:`credential` isolation is enabled,
   the effective UID (EUID) of the application process in the host namespace is
   mapped to the same UID in the container namespace; the same applies to
   :samp:`gidmap` and GID, respectively.  This means that the configuration
   below:

   .. code-block:: json

      {
          "user": "some_user",
          "namespaces": {
              "credential": true
          }
      }

   Is equivalent to the following (assuming :samp:`some_user`'s EUID and EGID
   are both equal to 1000):

   .. code-block:: json

      {
          "user": "some_user",
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


.. _configuration-rootfs:

The :samp:`rootfs` option confines the app to the directory you provide, making
it the new file system root.  To use it, your app should have the corresponding
privilege (effectively, run as :samp:`root` in most cases).

The root directory is changed before the language module starts the
app, so any path options for the app should be relative to the new root.
Note the :samp:`path` and :samp:`home` settings:

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


.. _configuration-lang-runtime:

Unit mounts language-specific files and directories to the new root so the app
stays operational:

.. list-table::
   :header-rows: 1

   * - Language
     - Language-Specific Mounts

   * - Java
     - - JVM's :file:`libc.so` directory

       - Java module's :ref:`home <installation-modules-java>` directory

   * - Python
     - Python's :samp:`sys.path` `directories
       <https://docs.python.org/3/library/sys.html#sys.path>`__

   * - Ruby
     - - Ruby's header, interpreter, and library `directories
         <https://idiosyncratic-ruby.com/42-ruby-config.html>`__:
         :samp:`rubyarchhdrdir`, :samp:`rubyhdrdir`, :samp:`rubylibdir`,
         :samp:`rubylibprefix`, :samp:`sitedir`, and :samp:`topdir`

       - Ruby's gem installation directory (:samp:`gem env gemdir`)

       - Ruby's entire gem path list (:samp:`gem env gempath`)


.. _configuration-proc-mgmt-lmts:

Request Limits
**************

The :samp:`limits` object controls request handling by the app process and has
two integer options:

.. list-table::
   :header-rows: 1

   * - Option
     - Description

   * - :samp:`timeout`
     - Request timeout in seconds.  If an app process exceeds this limit while
       handling a request, Unit alerts it to cancel the request and returns an
       HTTP error to the client.

   * - :samp:`requests`
     - Maximum number of requests Unit allows an app process to serve.  If the
       limit is reached, the process is restarted; this helps to mitigate
       possible memory leaks or other cumulative issues.

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

Application Processes
*********************

The :samp:`processes` option offers a choice between static and dynamic process
management.  If you set it to an integer, Unit immediately launches the given
number of app processes and keeps them without scaling.

To enable a dynamic prefork model for your app, supply a :samp:`processes`
object with the following options:

.. list-table::
    :header-rows: 1

    * - Option
      - Description

    * - :samp:`max`
      - Maximum number of application processes that Unit will maintain
        (busy and idle).

        The default value is 1.

    * - :samp:`spare`
      - Minimum number of idle processes that Unit tries to reserve for an app.
        When the app is started, :samp:`spare` idle processes are launched;
        Unit assigns incoming requests to existing idle processes, forking new
        idles to maintain the :samp:`spare` level if :samp:`max` allows.  As
        processes complete requests and turn idle, Unit terminates extra ones
        after :samp:`idle_timeout`.

    * - :samp:`idle_timeout`
      - Time in seconds that Unit waits before terminating an idle process
        which exceeds :samp:`spare`.

If :samp:`processes` is omitted entirely, Unit creates 1 static process.  If
an empty object is provided: :samp:`"processes": {}`, dynamic behavior with
default option values is assumed.

Here, Unit allows 10 processes maximum, keeps 5 idles, and terminates extra
idles after 20 seconds:

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

To run your Go apps on Unit, you need to configure them `and` modify their
source code as suggested below.  Let's start with the app configuration;
besides :ref:`common options <configuration-apps-common>`, you have:

.. list-table::
    :header-rows: 1

    * - Option
      - Description

    * - :samp:`executable` (required)
      - Pathname of the application, absolute or relative to
        :samp:`working_directory`.

    * - :samp:`arguments`
      - Command line arguments to be passed to the application.
        The example below is equivalent to
        :samp:`/www/chat/bin/chat_app --tmp-files /tmp/go-cache`.

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

Before applying the configuration, update the application source code.  In the
:samp:`import` section, reference the :samp:`unit.nginx.org/go` package that
you :ref:`installed <installation-precomp-pkgs>` or :ref:`built
<installation-modules-go>` earlier:

.. code-block:: go

   import (
       ...
       "unit.nginx.org/go"
       ...
   )

.. note::

   The package is required only to build the app; there's no need to
   install it in the target environment.

In the :samp:`main()` function, replace the :samp:`http.ListenAndServe` call
with :samp:`unit.ListenAndServe`:

.. code-block:: go

   func main() {
       ...
       http.HandleFunc("/", handler)
       ...
       //http.ListenAndServe(":8080", nil)
       unit.ListenAndServe(":8080", nil)
       ...
   }

Next, create a `Go module <https://go.dev/blog/using-go-modules>`__ and
build your application:

.. code-block:: console

   $ go mod init :nxt_ph:`example.com/app <Module designation>`

         go: creating new go.mod: module example.com/app

   $ go build -o :nxt_ph:`app <Executable name>` :nxt_ph:`app.go <Application source code>`

         go: finding unit.nginx.org latest

This links the :program:`unit-http` module to your app and adds it as a
dependency to your :file:`go.mod`.  The resulting executable works as follows:

- When you run it standalone, the :samp:`unit.ListenAndServe` call falls
  back to :samp:`http` functionality.

- When Unit runs it, :samp:`unit.ListenAndServe` communicates with Unit's
  router process directly, ignoring the address supplied as its first
  argument and relying on the :ref:`listener's settings
  <configuration-listeners>` instead.

If you update Unit later, update the Go package as well according to your
:ref:`installation method <installation-go-package>`.  You'll also need to
rebuild your app with the updated package.

.. note::

   For Go-based examples, see our :doc:`howto/grafana` howto or a basic
   :ref:`sample <sample-go>`.


.. _configuration-java:

====
Java
====

First, make sure to install Unit along with the :ref:`Java language module
<installation-precomp-pkgs>`.

Besides :ref:`common options <configuration-apps-common>`, you have the
following:

.. list-table::
    :header-rows: 1

    * - Option
      - Description

    * - :samp:`webapp` (required)
      - Pathname of the application's packaged or unpackaged :file:`.war` file.

    * - :samp:`classpath`
      - Array of paths to your app's required libraries (may list directories
        or :file:`.jar` files).

    * - :samp:`options`
      - Array of strings defining JVM runtime options.

    * - :samp:`threads`
      - Integer that sets the number of worker threads per app process.  When
        started, each app process creates a corresponding number of threads to
        handle requests.

        The default value is :samp:`1`.

    * - :samp:`thread_stack_size`
      - Integer that defines the stack size of a worker thread (in bytes,
        multiple of memory page size; the minimum value is usually architecture
        specific).

        The default value is system dependent and can be set with
        :program:`ulimit -s <SIZE_KB>`.

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

   For Java-based examples, see our :doc:`howto/jira`, :doc:`howto/opengrok`,
   and :doc:`howto/springboot` howtos or a basic :ref:`sample <sample-java>`.


.. _configuration-nodejs:

=======
Node.js
=======

First, you need to have the :program:`unit-http` module :ref:`installed
<installation-nodejs-package>`.  If it's global, symlink it in your
project directory:

.. code-block:: console

   # npm link unit-http

Do the same if you move a Unit-hosted app to a new system where
:program:`unit-http` is installed globally.  Also, if you update Unit later,
update the Node.js module as well according to your :ref:`installation method
<installation-nodejs-package>`.

Next, to run your Node.js apps on Unit, you need to configure them.  Besides
:ref:`common options <configuration-apps-common>`, you have:

.. list-table::
    :header-rows: 1

    * - Option
      - Description

    * - :samp:`executable` (required)
      - Pathname of the application, absolute or relative to
        :samp:`working_directory`.

        Supply your :file:`.js` pathname here and start the file itself
        with a proper shebang:

        .. code-block:: javascript

           #!/usr/bin/env node

        .. note::

           Make sure to :command:`chmod +x` the file you list here so Unit can
           start it.

    * - :samp:`arguments`
      - Command line arguments to be passed to the application.
        The example below is equivalent to
        :samp:`/www/apps/node-app/app.js --tmp-files /tmp/node-cache`.

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

You can run Node.js apps without altering their code, using a loader module we
provide with :program:`unit-http`.  Apply the following app configuration,
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

The loader overrides the :samp:`http` and :samp:`websocket` modules with their
Unit-aware versions and starts the app.

You can also run your Node.js apps without the loader by updating the
application source code.  For that, use :samp:`unit-http` instead of
:samp:`http` in your code:

.. code-block:: javascript

   var http = require('unit-http');

To use the WebSocket protocol, your app only needs to replace the default
:samp:`websocket`:

.. code-block:: javascript

  var webSocketServer = require('unit-http/websocket').server;

.. note::

   For Node.js-based examples, see our :doc:`howto/express`, :doc:`howto/koa`,
   and :ref:`Docker <docker-apps>` howtos or a basic :ref:`sample
   <sample-nodejs>`.


.. _configuration-perl:

====
Perl
====

First, make sure to install Unit along with the :ref:`Perl language module
<installation-precomp-pkgs>`.

Besides :ref:`common options <configuration-apps-common>`, you have the
following:

.. list-table::
    :header-rows: 1

    * - Option
      - Description

    * - :samp:`script` (required)
      - PSGI script path.

    * - :samp:`threads`
      - Integer that sets the number of worker threads per app process.  When
        started, each app process creates a corresponding number of threads to
        handle requests.

        The default value is :samp:`1`.

    * - :samp:`thread_stack_size`
      - Integer that defines the stack size of a worker thread (in bytes,
        multiple of memory page size; the minimum value is usually architecture
        specific).

        The default value is system dependent and can be set with
        :program:`ulimit -s <SIZE_KB>`.

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

   For Perl-based examples of Perl, see our :doc:`howto/bugzilla` and
   :doc:`howto/catalyst` howtos or a basic :ref:`sample <sample-perl>`.

.. _configuration-php:

===
PHP
===

First, make sure to install Unit along with the :ref:`PHP language module
<installation-precomp-pkgs>`.

Besides :ref:`common options <configuration-apps-common>`, you have the
following:

.. list-table::
    :header-rows: 1

    * - Option
      - Description

    * - :samp:`root` (required)
      - Base directory of your PHP app's file structure.  All URI paths are
        relative to this value.

    * - :samp:`index`
      - Filename appended to any URI paths ending with a slash; applies if
        :samp:`script` is omitted.

        The default value is :samp:`index.php`.

    * - :samp:`options`
      - Object that :ref:`defines <configuration-php-options>` the
        :file:`php.ini` location and options.

    * - :samp:`targets`
      - Object that defines application sections with :ref:`custom
        <configuration-php-targets>` :samp:`root`, :samp:`script`, and
        :samp:`index` values.

    * - :samp:`script`
      - Filename of a :samp:`root`-based PHP script that Unit uses to serve all
        requests to the app.

The :samp:`index` and :samp:`script` options enable two modes of operation:

- If :samp:`script` is set, all requests to the application are handled by
  the script you provide.

- Otherwise, the requests are served according to their URI paths; if script
  name is omitted, :samp:`index` is used.

.. _configuration-php-options:

You can customize :file:`php.ini` via the :samp:`options` object:

.. list-table::
    :header-rows: 1

    * - Option
      - Description

    * - :samp:`file`
      - Pathname of the :file:`php.ini` file with `PHP configuration directives
        <https://www.php.net/manual/en/ini.list.php>`_.

    * - :samp:`admin`, :samp:`user`
      - Objects for extra directives.  Values in :samp:`admin` are set in
        :samp:`PHP_INI_SYSTEM` mode, so the app can't alter them; :samp:`user`
        values are set in :samp:`PHP_INI_USER` mode and may `be updated
        <https://www.php.net/manual/en/function.ini-set.php>`_ in runtime.

Directives from :file:`php.ini` are overridden by settings supplied in
:samp:`admin` and :samp:`user` objects.

.. note::

   Values in :samp:`options` must be strings (for example,
   :samp:`"max_file_uploads": "4"`, not :samp:`"max_file_uploads": 4`); for
   boolean flags, use :samp:`"0"` and :samp:`"1"` only.  For details about
   :samp:`PHP_INI_*` modes, see the `PHP docs
   <https://www.php.net/manual/en/configuration.changes.modes.php>`_.

.. note::

   Unit implements the :samp:`fastcgi_finish_request()` `function
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
               "variables_order": "EGPCS",
               "expose_php": "0"
           },

           "user": {
               "display_errors": "0"
           }
       }
   }

.. _configuration-php-targets:

Targets
*******

You can configure up to 254 individual entry points for a single PHP
application:

.. code-block:: json

   {
       "applications": {
           "php-app": {
               "type": "php",
               "targets": {
                   "foo": {
                       "script": "foo.php",
                       "root": "/www/apps/php-app/foo/"
                   },

                   "bar": {
                       "script": "bar.php",
                       "root": "/www/apps/php-app/bar/"
                   }
               }
           }
       }
   }

Each target is an object that specifies :samp:`root` and optionally
:samp:`index` or :samp:`script` just like a common application does.  Targets
can be used by the :samp:`pass` options in listeners and routes to serve
requests:

.. code-block:: json

   {
       "listeners": {
           "127.0.0.1:8080": {
               "pass": "applications/php-app/foo"
           },

           "127.0.0.1:80": {
               "pass": "routes"
           }
       },

       "routes": [
           {
               "match": {
                   "uri": "/bar"
               },

               "action": {
                   "pass": "applications/php-app/bar"
               }
           }
       ]
   }

App-wide settings (:samp:`isolation`, :samp:`limits`, :samp:`options`,
:samp:`processes`) are shared by all targets within the app.

.. warning::

   If you specify :samp:`targets`, there should be no :samp:`root`,
   :samp:`index`, or :samp:`script` defined at the application level.

.. note::

   For PHP-based examples, see our :doc:`howto/cakephp`,
   :doc:`howto/codeigniter`, :doc:`howto/dokuwiki`, :doc:`howto/drupal`,
   :doc:`howto/laravel`, :doc:`howto/lumen`, :doc:`howto/matomo`,
   :doc:`howto/mediawiki`, :doc:`howto/modx`, :doc:`howto/nextcloud`,
   :doc:`howto/phpbb`, :doc:`howto/symfony`, :doc:`howto/wordpress`, and
   :doc:`howto/yii` howtos or a basic :ref:`sample <sample-php>`.


.. _configuration-python:

======
Python
======

First, make sure to install Unit along with the :ref:`Python language module
<installation-precomp-pkgs>`.

Besides :ref:`common options <configuration-apps-common>`, you have the
following:

.. list-table::
    :header-rows: 1

    * - Option
      - Description

    * - :samp:`module` (required)
      - Application module name.  The :samp:`module` itself is `imported
        <https://docs.python.org/3/reference/import.html>`_ just like in
        Python.

    * - :samp:`callable`
      - Name of the callable in :samp:`module` that Unit uses to run the app.

        The default value is :samp:`application`.

    * - :samp:`home`
      - Path to the app's `virtual environment <https://packaging.python.org/
        tutorials/installing-packages/#creating-virtual-environments>`_.
        Absolute or relative to :samp:`working_directory`.

        .. note::

           The Python version used to run the app depends on :samp:`type`; for
           performance, Unit doesn't use the command-line interpreter from the
           virtual environment.

    * - :samp:`path`
      - String or array of strings that represent additional Python module
        lookup paths; these values are prepended to :samp:`sys.path`.

    * - :samp:`protocol`
      - Hint to tell Unit that the app uses a certain interface; can be
        :samp:`asgi` or :samp:`wsgi`.

    * - :samp:`targets`
      - Object that defines application sections with :ref:`custom
        <configuration-python-targets>` :samp:`module` and :samp:`callable`
        values.

    * - :samp:`threads`
      - Integer that sets the number of worker threads per app process.  When
        started, each app process creates a corresponding number of threads to
        handle requests.

        The default value is :samp:`1`.

    * - :samp:`thread_stack_size`
      - Integer that defines the stack size of a worker thread (in bytes,
        multiple of memory page size; the minimum value is usually architecture
        specific).

        The default value is system dependent and can be set with
        :program:`ulimit -s <SIZE_KB>`.

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
       "user": "www",
       "group": "www"
   }

This snippet runs the :samp:`app` callable from the
:file:`/www/store/cart/run.py` module with :file:`/www/store/cart/` as the
working directory and :file:`/www/store/.virtualenv/` as the virtual
environment; the :samp:`path` value accommodates for situations when some
modules of the application are imported from outside the :file:`cart/`
subdirectory.

.. _configuration-python-asgi:

You can provide the callable in two forms.  The first one uses WSGI (`PEP 333
<https://www.python.org/dev/peps/pep-0333/>`_ or `PEP 3333
<https://www.python.org/dev/peps/pep-3333/>`_):

.. code-block:: python

   def application(environ, start_response):
       start_response('200 OK', [('Content-Type', 'text/plain')])
       yield b'Hello, WSGI\n'

The second one, supported for Python 3.5+, uses `ASGI
<https://asgi.readthedocs.io/en/latest/>`__:

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

   Legacy `two-callable
   <https://asgi.readthedocs.io/en/latest/specs/main.html#legacy-applications>`_
   ASGI 2.0 applications were not supported prior to Unit 1.21.0.

Choose either one according to your needs; Unit will attempt to infer your
choice automatically.  If automatic inference fails, use the :samp:`protocol`
option to name the interface explicitly.

.. _configuration-python-targets:

Targets
*******

You can configure up to 254 individual entry points for a single Python
application:

.. code-block:: json

   {
       "applications": {
           "python-app": {
               "type": "python",
               "path": "/www/apps/python-app/",
               "targets": {
                   "foo": {
                       "module": "foo.wsgi",
                       "callable": "foo"
                   },

                   "bar": {
                       "module": "bar.wsgi",
                       "callable": "bar"
                   }
               }
           }
       }
   }

Each target is an object that specifies :samp:`module` and optionally
:samp:`callable` just like a common application does.  Targets can be used by
the :samp:`pass` options in listeners and routes to serve requests:

.. code-block:: json

   {
       "listeners": {
           "127.0.0.1:8080": {
               "pass": "applications/python-app/foo"
           },

           "127.0.0.1:80": {
               "pass": "routes"
           }
       },

       "routes": [
           {
               "match": {
                   "uri": "/bar"
               },

               "action": {
                   "pass": "applications/python-app/bar"
               }
           }
       ]
   }

The :samp:`home`, :samp:`path`, :samp:`protocol`, :samp:`threads`, and
:samp:`thread_stack_size` settings are shared by all targets in the app.

.. warning::

   If you specify :samp:`targets`, there should be no :samp:`module` or
   :samp:`callable` defined at the application level.  Moreover, you can't
   combine WSGI and ASGI targets within a single app.

.. note::

   For Python-based examples, see our :doc:`howto/bottle`,
   :doc:`howto/datasette`, :doc:`howto/django`, :doc:`howto/djangochannels`,
   :doc:`howto/fastapi`, :doc:`howto/flask`, :doc:`howto/guillotina`,
   :doc:`howto/mercurial`, :doc:`howto/moin`, :doc:`howto/plone`,
   :doc:`howto/pyramid`, :doc:`howto/quart`, :doc:`howto/responder`,
   :doc:`howto/reviewboard`, :doc:`howto/sanic`, :doc:`howto/starlette`,
   :doc:`howto/trac`, and :doc:`howto/zope` howtos or a basic :ref:`sample
   <sample-python>`.


.. _configuration-ruby:

====
Ruby
====

First, make sure to install Unit along with the :ref:`Ruby language module
<installation-precomp-pkgs>`.

.. note::

   Unit uses the `Rack <https://rack.github.io>`_ interface to run Ruby
   scripts; you need to have it installed as well:

   .. code-block:: console

      $ gem install rack

Besides :ref:`common options <configuration-apps-common>`, you have the
following:

.. list-table::
    :header-rows: 1

    * - Option
      - Description

    * - :samp:`script` (required)
      - Rack script pathname, including the :file:`.ru` extension:
        :file:`/www/rubyapp/script.ru`.

    * - :samp:`threads`
      - Integer that sets the number of worker threads per app process.  When
        started, each app process creates a corresponding number of threads to
        handle requests.

        The default value is :samp:`1`.

    * - :samp:`hooks`
      - Pathname of the :file:`.rb` file defining the event hooks to be
        called during the app's lifecycle.

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

The :samp:`hooks` script is evaluated when the application starts.  If set, it
can define blocks of Ruby code named :samp:`on_worker_boot`,
:samp:`on_worker_shutdown`, :samp:`on_thread_boot`, or
:samp:`on_thread_shutdown`.  If provided, these blocks are called at the
respective points of the application's lifecycle, for example:

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

Use these hooks to add custom runtime logic to your application.

.. note::

   For Ruby-based examples, see our :doc:`howto/rails` and :doc:`howto/redmine`
   howtos or a basic :ref:`sample <sample-ruby>`.


.. _configuration-stngs:

********
Settings
********

Unit has a global :samp:`settings` configuration object that stores
instance-wide preferences.  Its :samp:`http` option fine-tunes the handling of
HTTP requests from the clients:

.. list-table::
    :header-rows: 1

    * - Option
      - Description

    * - :samp:`header_read_timeout`
      - Maximum number of seconds to read the header of a client's request.
        If Unit doesn't receive the entire header from the client within this
        interval, it responds with a 408 Request Timeout error.

        The default value is 30.

    * - :samp:`body_read_timeout`
      - Maximum number of seconds to read data from the body of a client's
        request.  It limits the interval between consecutive read operations,
        not the time to read the entire body.  If Unit doesn't receive any
        data from the client within this interval, it responds with a 408
        Request Timeout error.

        The default value is 30.

    * - :samp:`send_timeout`
      - Maximum number of seconds to transmit data in the response to a client.
        It limits the interval between consecutive transmissions, not the
        entire response transmission.  If the client doesn't receive any data
        within this interval, Unit closes the connection.

        The default value is 30.

    * - :samp:`idle_timeout`
      - Maximum number of seconds between requests in a keep-alive connection.
        If no new requests arrive within this interval, Unit responds with a
        408 Request Timeout error and closes the connection.

        The default value is 180.

    * - :samp:`max_body_size`
      - Maximum number of bytes in the body of a client's request.  If the body
        size exceeds this value, Unit responds with a 413 Payload Too Large
        error and closes the connection.

        The default value is 8388608 (8 MB).

    * - :samp:`static`
      - Object that configures static asset handling, containing a single
        object named :samp:`mime_types`.  In turn, :samp:`mime_types`
        defines specific MIME types as options.  An option's value can be a
        string or an array of strings; each string must specify a filename
        extension or a specific filename that is included in the MIME type.

    * - :samp:`discard_unsafe_fields`
      - Controls the parsing mode of header field names.  If set to
        :samp:`true`, Unit only processes headers with names consisting of
        alphanumeric characters and hyphens (:samp:`-`); otherwise, all valid
        `RFC 7230 <https://datatracker.ietf.org/doc/html/rfc7230#section-3.2>`_
        header fields are processed.

        The default value is :samp:`true`.

Example:

.. code-block:: json

   {
       "settings": {
           "http": {
               "header_read_timeout": 10,
               "body_read_timeout": 10,
               "send_timeout": 10,
               "idle_timeout": 120,
               "max_body_size": 6291456,
               "static": {
                   "mime_types": {
                       "text/plain": [
                           ".log",
                           "README",
                           "CHANGES"
                       ]
                   }
               },

               "discard_unsafe_fields": false
           }
       }
   }

.. _configuration-mime:

.. note::

   Built-in support for MIME types includes :file:`.aac`, :file:`.apng`,
   :file:`.atom`, :file:`.avi`, :file:`.avif`, :file:`avifs`, :file:`.bin`,
   :file:`.css`, :file:`.deb`, :file:`.dll`, :file:`.exe`, :file:`.flac`,
   :file:`.gif`, :file:`.htm`, :file:`.html`, :file:`.ico`, :file:`.img`,
   :file:`.iso`, :file:`.jpeg`, :file:`.jpg`, :file:`.js`, :file:`.json`,
   :file:`.md`, :file:`.mid`, :file:`.midi`, :file:`.mp3`, :file:`.mp4`,
   :file:`.mpeg`, :file:`.mpg`, :file:`.msi`, :file:`.ogg`, :file:`.otf`,
   :file:`.pdf`, :file:`.php`, :file:`.png`, :file:`.rpm`, :file:`.rss`,
   :file:`.rst`, :file:`.svg`, :file:`.ttf`, :file:`.txt`, :file:`.wav`,
   :file:`.webm`, :file:`.webp`, :file:`.woff2`, :file:`.woff`, :file:`.xml`,
   and :file:`.zip`.  Built-ins can be overridden, and new types can be added:

   .. code-block:: console

      # curl -X PUT -d '{"text/x-code": [".c", ".h"]}' /path/to/control.unit.sock \
             http://localhost/config/settings/http/static/mime_types
      {
             "success": "Reconfiguration done."
      }


.. _configuration-access-log:

**********
Access Log
**********

To enable access logging, specify the log file path in the :samp:`access_log`
option of the :samp:`config` object.

In the example below, all requests will be logged to
:file:`/var/log/access.log`:

.. code-block:: console

   # curl -X PUT -d '"/var/log/access.log"' \
          --unix-socket /path/to/control.unit.sock \
          http://localhost/config/access_log

       {
           "success": "Reconfiguration done."
       }

The log is written in the Combined Log Format.  Example of a log line:

.. code-block:: none

   127.0.0.1 - - [21/Oct/2015:16:29:00 -0700] "GET / HTTP/1.1" 200 6022 "http://example.com/links.html" "Godzilla/5.0 (X11; Minix i286) Firefox/42"


.. _configuration-ssl:

**********************
Certificate Management
**********************

To set up SSL/TLS access for your application, upload a :file:`.pem` file
containing your certificate chain and private key to Unit.  Next, reference the
uploaded bundle in the listener's configuration.  After that, the listener's
application becomes accessible via SSL/TLS.

.. note::

   For the details of certificate issuance and renewal in Unit, see an
   example in :doc:`howto/certbot`.

First, create a :file:`.pem` file with your certificate chain and private key:

.. code-block:: console

   $ cat :nxt_ph:`cert.pem <Leaf certificate file>` :nxt_ph:`ca.pem <CA certificate file>` :nxt_ph:`key.pem <Private key file>` > :nxt_ph:`bundle.pem <Arbitrary certificate bundle's filename>`

Usually, your website's certificate (optionally followed by the intermediate CA
certificate) is enough to build a certificate chain.  If you add more
certificates to your chain, order them leaf to root.

Upload the resulting bundle file to Unit's certificate storage under a suitable
name (in this case, :samp:`bundle`):

.. code-block:: console

   # curl -X PUT --data-binary @:nxt_ph:`bundle.pem <Certificate bundle's filename>` --unix-socket \
          /path/to/control.unit.sock http://localhost/certificates/:nxt_ph:`bundle <Certificate bundle name in Unit's configuration>`

       {
           "success": "Certificate chain uploaded."
       }

.. warning::

   Don't use :option:`!-d` for file upload with :program:`curl`; this option
   damages :file:`.pem` files.  Use the :option:`!--data-binary` option when
   uploading file-based data to avoid data corruption.

Internally, Unit stores the uploaded certificate bundles along with other
configuration data in its :file:`state` subdirectory; Unit's control API maps
them to a separate configuration section, aptly named :samp:`certificates`:

.. code-block:: json

   {
       "certificates": {
           ":nxt_ph:`bundle <Certificate bundle name>`": {
               "key": "RSA (4096 bits)",
               "chain": [
                   {
                       "subject": {
                           "common_name": "example.com",
                           "alt_names": [
                               "example.com",
                               "www.example.com"
                           ],

                           "country": "US",
                           "state_or_province": "CA",
                           "organization": "Acme, Inc."
                       },

                       "issuer": {
                           "common_name": "intermediate.ca.example.com",
                           "country": "US",
                           "state_or_province": "CA",
                           "organization": "Acme Certification Authority"
                       },

                       "validity": {
                           "since": "Sep 18 19:46:19 2018 GMT",
                           "until": "Jun 15 19:46:19 2021 GMT"
                       }
                   },
                   {
                       "subject": {
                           "common_name": "intermediate.ca.example.com",
                           "country": "US",
                           "state_or_province": "CA",
                           "organization": "Acme Certification Authority"
                       },

                       "issuer": {
                           "common_name": "root.ca.example.com",
                           "country": "US",
                           "state_or_province": "CA",
                           "organization": "Acme Root Certification Authority"
                       },

                       "validity": {
                           "since": "Feb 22 22:45:55 2016 GMT",
                           "until": "Feb 21 22:45:55 2019 GMT"
                       }
                   }
               ]
           }
       }
   }

.. note::

   You can access individual certificates in your chain, as well as specific
   alternative names, by their indexes:

   .. code-block:: console

      # curl -X GET --unix-socket /path/to/control.unit.sock \
             http://localhost/certificates/:nxt_hint:`bundle <Certificate bundle name>`/chain/0/
      # curl -X GET --unix-socket /path/to/control.unit.sock \
             http://localhost/certificates/:nxt_hint:`bundle <Certificate bundle name>`/chain/0/subject/alt_names/0/

Next, :ref:`add <configuration-listeners>` the uploaded bundle to a listener;
the resulting control API configuration may look like this:

.. code-block:: json

   {
       "certificates": {
           ":nxt_ph:`bundle <Certificate bundle name>`": {
               "key": "<key type>",
               "chain": [
                   "<certificate chain, omitted for brevity>"
               ]
           }
       },

       "config": {
           "listeners": {
               "*:443": {
                   "pass": "applications/wsgi-app",
                   "tls": {
                       "certificate": ":nxt_ph:`bundle <Certificate bundle name>`"
                   }
               }
           },

           "applications": {
               "wsgi-app": {
                   "type": "python",
                   "module": "wsgi",
                   "path": "/usr/www/wsgi-app/"
               }
           }
       }
   }

Now you're solid; the application is accessible via SSL/TLS:

.. code-block:: console

   $ curl -v :nxt_hint:`https://127.0.0.1 <Port 443 is conventionally used for HTTPS connections>`
       ...
       * TLSv1.2 (OUT), TLS handshake, Client hello (1):
       * TLSv1.2 (IN), TLS handshake, Server hello (2):
       * TLSv1.2 (IN), TLS handshake, Certificate (11):
       * TLSv1.2 (IN), TLS handshake, Server finished (14):
       * TLSv1.2 (OUT), TLS handshake, Client key exchange (16):
       * TLSv1.2 (OUT), TLS change cipher, Client hello (1):
       * TLSv1.2 (OUT), TLS handshake, Finished (20):
       * TLSv1.2 (IN), TLS change cipher, Client hello (1):
       * TLSv1.2 (IN), TLS handshake, Finished (20):
       * SSL connection using TLSv1.2 / AES256-GCM-SHA384
       ...

Finally, you can :samp:`DELETE` a certificate bundle that you don't need
anymore from the storage:

.. code-block:: console

   # curl -X DELETE --unix-socket /path/to/control.unit.sock \
          http://localhost/certificates/:nxt_hint:`bundle <Certificate bundle name>`

       {
           "success": "Certificate deleted."
       }

.. note::

   You can't delete certificate bundles still referenced in your
   configuration, overwrite existing bundles using :samp:`PUT`, or (obviously)
   delete non-existent ones.


.. _configuration-full-example:

************
Full Example
************

.. code-block:: json

   {
       "certificates": {
           "example.com": {
               "key": "RSA (4096 bits)",
               "chain": [
                   {
                       "subject": {
                           "common_name": "example.com",
                           "alt_names": [
                               "example.com",
                               "www.example.com"
                           ],

                           "country": "US",
                           "state_or_province": "CA",
                           "organization": "Acme, Inc."
                       },

                       "issuer": {
                           "common_name": "intermediate.ca.example.com",
                           "country": "US",
                           "state_or_province": "CA",
                           "organization": "Acme Certification Authority"
                       },

                       "validity": {
                           "since": "Sep 18 19:46:19 2018 GMT",
                           "until": "Jun 15 19:46:19 2021 GMT"
                       }
                   },
                   {
                       "subject": {
                           "common_name": "intermediate.ca.example.com",
                           "country": "US",
                           "state_or_province": "CA",
                           "organization": "Acme Certification Authority"
                       },

                       "issuer": {
                           "common_name": "root.ca.example.com",
                           "country": "US",
                           "state_or_province": "CA",
                           "organization": "Acme Root Certification Authority"
                       },

                       "validity": {
                           "since": "Feb 22 22:45:55 2016 GMT",
                           "until": "Feb 21 22:45:55 2019 GMT"
                       }
                   }
               ]
           },

           "example.org": {
               "key": "RSA (4096 bits)",
               "chain": [
                   {
                       "subject": {
                           "common_name": "example.org",
                           "alt_names": [
                               "example.org",
                               "www.example.org"
                           ],

                           "country": "US",
                           "state_or_province": "CA",
                           "organization": "Acme, Inc."
                       },

                       "issuer": {
                           "common_name": "intermediate.ca.example.org",
                           "country": "US",
                           "state_or_province": "CA",
                           "organization": "Acme Certification Authority"
                       },

                       "validity": {
                           "since": "Sep 18 19:46:19 2018 GMT",
                           "until": "Jun 15 19:46:19 2021 GMT"
                       }
                   },
                   {
                       "subject": {
                           "common_name": "intermediate.ca.example.org",
                           "country": "US",
                           "state_or_province": "CA",
                           "organization": "Acme Certification Authority"
                       },

                       "issuer": {
                           "common_name": "root.ca.example.org",
                           "country": "US",
                           "state_or_province": "CA",
                           "organization": "Acme Root Certification Authority"
                       },

                       "validity": {
                           "since": "Feb 22 22:45:55 2016 GMT",
                           "until": "Feb 21 22:45:55 2019 GMT"
                       }
                   }
               ]
           }
       },

       "config": {
           "settings": {
               "http": {
                   "header_read_timeout": 10,
                   "body_read_timeout": 10,
                   "send_timeout": 10,
                   "idle_timeout": 120,
                   "max_body_size": 6291456,
                   "static": {
                       "mime_types": {
                           "text/plain": [
                                ".log",
                                "README",
                                "CHANGES"
                           ]
                       }
                   },

                   "discard_unsafe_fields": false
               }
           },

           "listeners": {
               "*:8000": {
                   "pass": "routes",
                   "tls": {
                       "certificate": [
                           "example.com",
                           "example.org"
                       ],

                       "conf_commands" : {
                            "ciphersuites": "TLS_CHACHA20_POLY1305_SHA256"
                       },

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
               },

               "127.0.0.1:8001": {
                   "pass": "applications/drive"
               },

               "*:8080": {
                   "pass": "upstreams/rr-lb",
                   "client_ip": {
                       "header": "X-Forwarded-For",
                       "source": [
                           "192.168.0.0.0/16"
                       ]
                   }
               }
           },

           "routes": [
               {
                   "match": {
                       "uri": "/admin/*",
                       "scheme": "https",
                       "arguments": {
                           "mode": "strict",
                           "access": "!raw"
                       },

                       "cookies": {
                           "user_role": "admin"
                       }
                   },

                   "action": {
                       "pass": "applications/cms"
                   }
               },
               {
                   "match": {
                       "host": "admin.emea-*.*.example.com",
                       "source": "*:8000-9000"
                   },

                   "action": {
                       "pass": "applications/blogs/admin"
                   }
               },
               {
                   "match": {
                       "host": [
                           "blog.example.com",
                           "blog.*.org"
                       ],

                       "source": "*:8000-9000"
                   },

                   "action": {
                       "pass": "applications/blogs/core"
                   }
               },
               {
                   "match": {
                       "host": "example.com",
                       "source": "127.0.0.1-127.0.0.254:8080-8090",
                       "uri": "/chat/*",
                       "query": [
                           "en-CA",
                           "en-IE",
                           "en-IN",
                           "en-UK",
                           "en-US"
                       ]
                   },

                   "action": {
                       "pass": "applications/chat"
                   }
               },
               {
                   "match": {
                       "host": "example.com",
                       "source": [
                           "198.51.100.0/24:8000",
                           "203.0.113.0/24:8080-8090"
                       ]
                   },

                   "action": {
                       "pass": "applications/store"
                   }
               },
               {
                   "match": {
                       "host": "extwiki.example.com"
                   },

                   "action": {
                       "pass": "applications/wiki/external"
                   }
               },
               {
                   "match": {
                       "host": "intwiki.example.com"
                   },

                   "action": {
                       "pass": "applications/wiki/internal"
                   }
               },
               {
                   "match": {
                        "uri": "/legacy/*"
                   },

                   "action": {
                       "return": 301,
                       "location": "https://legacy.example.com"
                   }
               },
               {
                   "match": {
                       "scheme": "http"
                   },

                   "action": {
                       "proxy": "http://127.0.0.1:8080"
                   }
               },
               {
                   "action": {
                       "share": [
                           "/www/$host$uri",
                           "/www/global_static$uri"
                       ],

                       "chroot": "/www/data/$host/",
                       "traverse_mounts": false,
                       "follow_symlinks": false,
                       "types": [
                           "image/*",
                           "video/*",
                           "application/json"
                       ],

                       "fallback": {
                           "proxy": "http://127.0.0.1:9000"
                       }
                   }
               }
           ],

           "applications": {
               "blogs": {
                   "type": "php",
                   "targets": {
                       "admin": {
                           "root": "/www/blogs/admin/",
                           "script": "index.php"
                       },

                       "core" : {
                           "root": "/www/blogs/scripts/"
                       }
                   },

                   "limits": {
                       "timeout": 10,
                       "requests": 1000
                   },

                   "options": {
                       "file": "/etc/php.ini",
                       "admin": {
                           "memory_limit": "256M",
                           "variables_order": "EGPCS",
                           "expose_php": "0"
                       },

                       "user": {
                           "display_errors": "0"
                       }
                   },

                   "processes": 4
               },

               "chat": {
                   "type": "external",
                   "executable": "bin/chat_app",
                   "group": "www-chat",
                   "user": "www-chat",
                   "working_directory": "/www/chat/",
                   "isolation": {
                       "namespaces": {
                           "cgroup": false,
                           "credential": true,
                           "mount": false,
                           "network": false,
                           "pid": false,
                           "uname": false
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
                       ],

                       "automount": {
                           "language_deps": false,
                           "procfs": false,
                           "tmpfs": false
                       }
                   }
               },

               "cms": {
                   "type": "ruby",
                   "script": "/www/cms/main.ru",
                   "working_directory": "/www/cms/",
                   "hooks": "hooks.rb"
               },

               "drive": {
                   "type": "perl",
                   "script": "app.psgi",
                   "threads": 2,
                   "thread_stack_size": 4096,
                   "working_directory": "/www/drive/",
                   "processes": {
                       "max": 10,
                       "spare": 5,
                       "idle_timeout": 20
                   }
               },

               "store": {
                   "type": "java",
                   "webapp": "/www/store/store.war",
                   "classpath": [
                       "/www/store/lib/store-2.0.0.jar"
                   ],

                   "options": [
                       "-Dlog_path=/var/log/store.log"
                   ]
               },

               "wiki": {
                   "type": "python",
                   "protocol": "asgi",
                   "targets": {
                       "internal": {
                           "module": "internal.asgi"
                       },

                       "external": {
                           "module": "external.asgi"
                       }
                   },

                   "environment": {
                       "DJANGO_SETTINGS_MODULE": "wiki.settings.prod",
                       "DB_ENGINE": "django.db.backends.postgresql",
                       "DB_NAME": "wiki",
                       "DB_HOST": "127.0.0.1",
                       "DB_PORT": "5432"
                   },

                   "path": "/www/wiki/",
                   "processes": 10
               }
           },

           "upstreams": {
               "rr-lb": {
                   "servers": {
                       "192.168.1.100:8080": {},
                       "192.168.1.101:8080": {
                           "weight": 2
                       }
                   }
               }
           },

           "access_log": "/var/log/access.log"
       }
   }
