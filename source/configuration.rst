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

To run an application in Unit, first set up an :ref:`application
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
members <https://tools.ietf.org/html/rfc8259#section-4>`_ or indexes of its
`array elements <https://tools.ietf.org/html/rfc8259#section-5>`_.

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
configuration; if there's none, nothing is done. For example, you can't restart
an updated app by uploading the same configuration it already has.

.. note::

   While we're working on handy app reload control, there's a workaround to
   forcefully restart an app in Unit by updating an :ref:`environment
   <configuration-apps-common>` variable.  First, check whether the app has an
   :samp:`environment` object:

   .. code-block:: console

      # curl --unix-socket /path/to/control.unit.sock \
             http://localhost/config/applications/app/environment

            {
                "error": "Value doesn't exist."
            }

   Here, it doesn't, so you can safely add a new variable with a
   shell-interpolated value:

   .. code-block:: console

      # curl -X PUT -d '{"APPGEN":"'$(date +"%s")'"}' --unix-socket \
             /path/to/control.unit.sock http://localhost/config/applications/app/environment

   Otherwise, take care and target the individual variable to avoid overwriting
   the entire :samp:`environment`:

   .. code-block:: console

      # curl -X PUT -d '"'$(date +"%s")'"' --unix-socket \
             /path/to/control.unit.sock http://localhost/config/applications/app/environment/APPGEN

   To make Unit reload the app, repeat the :samp:`PUT` command,
   updating the :samp:`APPGEN` variable.


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


.. _configuration-listeners:

*********
Listeners
*********

To start accepting requests, add a listener object in the
:samp:`config/listeners` API section.  The object's name uniquely combines a
host IP address and a port that Unit binds to; a wildcard matches any host IPs.

.. note::

   On Linux-based systems, wildcard listeners can't overlap with other
   listeners on the same port due to kernel-imposed limitations.  For example,
   :samp:`*:8080` conflicts with :samp:`127.0.0.1:8080`; in partcular, this
   also means you can't directly reconfigure a listener on :samp:`*:8080` to
   use :samp:`127.0.0.1:8080` or vice versa without deleting it first.

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
        - :ref:`Target <configuration-php-targets>` in a PHP application:
          :samp:`applications/my_php_app/section`
        - :ref:`Route <configuration-routes>`: :samp:`routes/route66`,
          :samp:`routes`
        - :ref:`Upstream <configuration-upstreams>`: :samp:`upstreams/rr-lb`

        .. note::

           The value is :ref:`variable <configuration-variables>`-interpolated;
           if it matches no configuration entities after interpolation, a 404
           "Not Found" response is returned.

    * - :samp:`tls`
      - SSL/TLS configuration object.  Its only option, :samp:`certificate`,
        enables secure communication via the listener; it must name a
        certificate chain that you have :ref:`configured <configuration-ssl>`
        earlier.

Here, a local listener accepts requests at port 8300 and passes them to the
:samp:`blogs` app :ref:`target <configuration-php-targets>` identified by the
:samp:`uri` :ref:`variable <configuration-variables>`.  The wildcard listener
on port 8400 is protected by the :samp:`blogs-cert` :ref:`certificate bundle
<configuration-ssl>` and relays requests at any host IPs to the :samp:`main`
:ref:`route <configuration-routes>`:

.. code-block:: json

    {
        "127.0.0.1:8300": {
            "pass": "applications/blogs$uri"
        },

        "*:8400": {
            "pass": "routes/main",
            "tls": {
                "certificate": "blogs-cert"
            }
        }
    }

Also, the :samp:`pass` values can be `percent encoded
<https://tools.ietf.org/html/rfc3986#section-2.1>`_.  For example, you can
escape slashes in entity names:

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


.. _configuration-routes:

******
Routes
******

The :samp:`config/routes` configuration entity defines internal request
routing, receiving requests via :ref:`listeners <configuration-listeners>` and
filtering them through :ref:`sets of conditions
<configuration-routes-matching>` to be processed by :ref:`apps
<configuration-applications>`, :ref:`proxied <configuration-routes-proxy>` to
external servers or :ref:`load-balanced <configuration-upstreams>` between
them, served with :ref:`static content <configuration-static>`, :ref:`answered
<configuration-routes-return>` with arbitrary status codes, or :ref:`redirected
<configuration-routes-location>`.

In its simplest form, :samp:`routes` can be a single route array:

.. code-block:: json

   {
        "listeners": {
            "*:8300": {
                "pass": "routes"
            }
        },

        "routes": [ "simply referred to as routes" ]
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
            "main": [ "named route, qualified name: routes/main" ],
            "route66": [ "named route, qualified name: routes/route66" ]
        }
   }

===========
Route Steps
===========

A route array contains step objects as elements; they accept the following
options:

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
                      "share": "/www/static_version/"
                  }
              }
          ]
      }

   This route passes all requests to the :samp:`/php/` subsection of the
   :samp:`example.com` website via HTTPS to the :samp:`php_version` app.  All
   other requests are served with static content from the
   :samp:`/www/static_version` directory.  If there's no matching content. Unit
   returns a 404 response code.

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
                          "share": "/www/static/"
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
   :samp:`/www/static/` directory.  If none of the steps matches, a 404
   response code is returned.


.. _configuration-routes-matching:

===================
Matching Conditions
===================

Conditions in a :samp:`match` object define patterns to be compared to the
requests' properties:

.. list-table::
   :header-rows: 1

   * - Property
     - Patterns Are Matched Against
     - Case |-| :nxt_term:`Sensitive <For arguments, cookies, and headers, this relates to property names and values; for other properties, case sensitivity affects only values>`
   * - :samp:`arguments`

     - Parameter arguments supplied with the request's target `query
       <https://tools.ietf.org/html/rfc3986#section-3.4>`_.  In argument names
       and values, plus signs (:samp:`+`) are replaced with spaces.

     - Yes

   * - :samp:`cookies`

     - Cookies supplied with the request.

     - Yes

   * - :samp:`destination`

     - Target IP address and optional port of the request.

     - No

   * - :samp:`headers`

     - `Header fields <https://tools.ietf.org/html/rfc7230#section-3.2>`_
       supplied with the request.

     - No

   * - :samp:`host`

     - :samp:`Host` `header field
       <https://tools.ietf.org/html/rfc7230#section-5.4>`_, converted to lower
       case and normalized by removing the port number and the trailing period
       (if any).

     - No

   * - :samp:`method`

     - Method from the `request line
       <https://tools.ietf.org/html/rfc7231#section-4>`_, converted to upper
       case.

     - No

   * - :samp:`scheme`

     - URI `scheme
       <https://www.iana.org/assignments/uri-schemes/uri-schemes.xhtml>`_.
       Currently, only :samp:`http` and :samp:`https` are supported.

     - No

   * - :samp:`source`

     - Source IP address and optional port of the request.

     - No

   * - :samp:`uri`

     - Request target `path
       <https://tools.ietf.org/html/rfc7230#section-5.3>`_, normalized by
       removing the query part, resolving relative path references ("." and
       ".."), and collapsing adjacent slashes.

     - Yes

.. nxt_details:: Percent Encoding In Arguments and URIs

   Names and values in :samp:`arguments` and values in :samp:`uri` additionally
   support `percent encoding
   <https://tools.ietf.org/html/rfc3986#section-2.1>`_.  Thus, you can escape
   characters which have special meaning in routing (:samp:`!` is :samp:`%21`,
   :samp:`*` is :samp:`%2A`, :samp:`%` is :samp:`%25`), or even target
   individual bytes.  For example, to select an entire class of diacritic
   characters such as Ö or Å by their starting byte :samp:`0xC3` in UTF-8:

   .. code-block:: json

      {
          "match": {
              "arguments": {
                  "word": "*%C3*"
              }
          },

          "action": {
              "pass": "..."
          }
      }

   This requires mentioning that actual arguments and URIs passed with requests
   are percent *decoded*: Unit interpolates all percent-encoded entities in
   these properties.  Thus, the following configuration:

   .. code-block:: json

      {
          "routes": [
              {
                  "match": {
                      "uri": "/:nxt_term:`static files <Note the unencoded space>`/*"
                  },

                  "action": {
                      "share": "/www/data/"
                  }
              }
          ]
      }

   Matches this percent-encoded request:

   .. subs-code-block:: console

      $ curl http://127.0.0.1/static%20files/test.txt -v

            > GET /static%20files/test.txt HTTP/1.1
            ...
            < HTTP/1.1 200 OK
            ...


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
           "pass": "..."
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
           "pass": "..."
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
           "pass": "..."
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
           "pass": "..."
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
              "pass": "..."
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
              "pass": "..."
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
regexes modify this behavior:

- A wildcard pattern may contain any combination of wildcards (:samp:`*`), each
  standing for an arbitrary number of characters: :samp:`How*s*that*to*you`.

- A regex pattern starts with a tilde (:samp:`~`):
  :samp:`~^\\\\d+\\\\.\\\\d+\\\\.\\\\d+\\\\.\\\\d+` (escaping backslashes is a
  JSON `requirement <https://www.json.org/json-en.html>`_).  Regexes are `PCRE
  <https://www.pcre.org/current/doc/html/pcre2syntax.html>`_-flavored.

.. nxt_details:: String Pattern Examples

   .. code-block:: json

      {
          "match": {
              "uri": "~^/data/www/.*\\.php(/.*)?$"
          },

          "action": {
              "pass": "..."
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
              "pass": "..."
          }
      }

   Only subdomains of :samp:`example.com` will match.

   .. code-block:: json

      {
          "match": {
              "uri": "/admin/*/*.php"
          },

          "action": {
              "pass": "..."
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
              "pass": "..."
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
              "pass": "..."
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
              "pass": "..."
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
              "pass": "..."
          }
      }

   Here, URIs of any articles that don't look like :samp:`YYYY-MM-DD` dates
   will match.  Again, note the backslashes; this is a JSON requirement.

Address-based patterns define individual IPv4 (dot-decimal or `CIDR
<https://tools.ietf.org/html/rfc4632>`__) or IPv6 (hexadecimal or `CIDR
<https://tools.ietf.org/html/rfc4291#section-2.3>`__) addresses that must
exactly match the property value; wildcards and ranges modify this behavior:

- Wildcards (:samp:`*`) can only be used to match arbitrary IPs
  (:samp:`*:<port>`).

- Ranges (:samp:`-`) can used with both IPs (in respective notation) and ports
  (:samp:`<start_port>-<end_port>`).

.. nxt_details::  Address Pattern Examples

   .. code-block:: json

      {
          "match": {
              "source": [
                  "10.0.0.0-10.255.255.255",
                  "10.0.0.0-11.255.255.255:8000",
                  "8.0.0.0-11.255.255.255:8080-8090",
                  "*:80"
              ],

              "destination": [
                  "10.0.0.0/8",
                  "10.0.0.0/7:8000",
                  "10.0.0.0/6:8080-8090",
                  "*:80"
              ]
          },

          "action": {
              "pass": "..."
          }
      }

   This uses IPv4-based matching with wildcards and ranges.

   .. code-block:: json

      {
          "match": {
              "source": [
                   "2001::-200f:ffff:ffff:ffff:ffff:ffff:ffff:ffff",
                   "[fe08::-feff::]:8000",
                   "[fff0::-fff0::10]:8080-8090",
                   "*:80"
              ],

              "destination": [
                   "2001::/16",
                   "[0ff::/64]:8000",
                   "[fff0:abcd:ffff:ffff:ffff::/128]:8080-8090",
                   "*:80"
              ]
          },

          "action": {
              "pass": "..."
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
                  "2002:c0a8:0001::c0a8:0001"
              ]
          },

          "action": {
              "pass": "..."
          }
      }

   This matches any of the listed IPv4 or IPv6 addresses.

   .. code-block:: json

      {
          "match": {
              "source": [
                  "10.0.0.0-10.0.0.10",
                  "!10.0.0.9"
              ]
          },

          "action": {
              "pass": "..."
          }
      }

   Here, any IPs from the range will match, except for :samp:`10.0.0.9`.

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
              "pass": "..."
          }
      }

   This matches any IPs but limits the acceptable ports.


.. _configuration-routes-action:

================
Handling Actions
================

If a request matches all conditions of a route step, or the step itself omits
the :samp:`match` object, Unit handles the request using the respective
:samp:`action`.  Possible combinations of :samp:`action` options are:

.. list-table::

  * - :samp:`pass`
    - Route's destination upon a match, identical to :samp:`pass` in a
      listener.

      Read more: :ref:`configuration-listeners`.

  * - :samp:`share`, :samp:`fallback`
    - The :samp:`share` is a static pathname from where files are served upon a
      match. The optional :samp:`fallback` action (identical to
      :samp:`match/action`) is performed if the requested file isn't found or
      can't be accessed.  Thus, share-based :samp:`fallback` actions can be
      nested.

      Read more: :ref:`configuration-static`.

  * - :samp:`proxy`
    - Socket address of an HTTP server where the request is proxied upon a
      match.

      Read more: :ref:`configuration-routes-proxy`.

  * - :samp:`return`, :samp:`location`
    - The :samp:`return` value defines the HTTP response status `code
      <https://tools.ietf.org/html/rfc7231#section-6>`__ to be returned upon a
      match.  The :samp:`location` is required if the :samp:`return` value
      implies redirection (3xx).

      Read more: :ref:`configuration-routes-return`.

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
                   "share": "/var/www/static/",
                   "fallback": {
                       "share": "/var/www/static/assets",
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


.. _configuration-routes-return:

===============================
Instant Responses and Redirects
===============================

You can configure route actions to instantly respond to certain conditions with
arbitrary HTTP status codes:

.. code-block:: json

   {
       "match": {
           "uri": "/admin_console/*"
       },

       "action": {
           "return": 403
       }
   }

The :samp:`return` option accepts any integer values within the 000-999 range.
It is recommended to use the codes according to their `semantics
<https://tools.ietf.org/html/rfc7231#section-6>`_; if you use custom codes,
make sure user agents can understand them.

.. _configuration-routes-location:

If you specify a redirect code (3xx), supply the destination using the
:samp:`location` option alongside :samp:`return`:

.. code-block:: json

   {
       "action": {
           "return": 301,
           "location": "https://www.example.com"
       }
   }


.. _configuration-variables:

*********
Variables
*********

While configuring Unit, you can use built-in variables that are replaced by
dynamic values in runtime.  This enables flexible request processing, making
the configuration more compact and straightforward.

.. note::

   Currently, the only place where variables are recognized is the :samp:`pass`
   option in :ref:`listeners <configuration-listeners>` and :ref:`actions
   <configuration-routes-action>`.  This means you can use them to guide
   requests between sets of routes, applications, targets, or upstreams.

Available variables:

.. list-table::
   :header-rows: 1

   * - Variable
     - Description

   * - :samp:`host`
     - :samp:`Host`
       `header field <https://tools.ietf.org/html/rfc7230#section-5.4>`_ in
       lowercase, without the port number and the trailing period (if any).

   * - :samp:`method`
     - Method from the `request
       line <https://tools.ietf.org/html/rfc7231#section-4>`_.

   * - :samp:`uri`
     - Request target `path <https://tools.ietf.org/html/rfc7230#section-5.3>`_
       without the query part, normalized by resolving relative path
       references ("." and "..") and collapsing adjacent slashes.
       The value is `percent decoded
       <https://tools.ietf.org/html/rfc3986#section-2.1>`_: Unit interpolates
       all percent-encoded entities in the request target `path
       <https://tools.ietf.org/html/rfc7230#section-5.3>`_.

To reference a variable, prefix its name with the dollar sign character
(:samp:`$`), optionally enclosing the name in curly brackets (:samp:`{}`) to
separate it from adjacent text or enhance visibility.  Variable names can
contain letters and underscores (:samp:`_`), so use the brackets if the
variable is immediately followed by these characters:

.. code-block:: json

   {
       "listeners": {
           "*:80": {
               "pass": "routes/${method}_route"
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
               "pass": ":nxt_term:`applications$uri <Note that the $uri variable value always includes a starting slash>`"
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


.. _configuration-static:

************
Static Files
************

Unit is capable of acting as a standalone web server, serving requests for
static assets from directories you configure; to use the feature, supply the
directory path in the :samp:`share` option of a :ref:`route
<configuration-routes>` step:

.. code-block:: json

   {
       "listeners": {
           "127.0.0.1:8300": {
               "pass": "routes"
           }
        },

       "routes": [
           {
               "action": {
                   "share": "/www/data/static/"
                }
           }
       ]
   }

Suppose the :file:`/www/data/static/` directory has the following structure:

.. code-block:: none

   /www/data/static/
   ├── stylesheet.css
   ├── html
   │   └──index.html
   └── js files
       └──page.js

In the above configuration, you can request specific files by these URIs:

.. code-block:: console

   $ curl 127.0.0.1:8300/html/index.html
   $ curl 127.0.0.1:8300/stylesheet.css
   $ curl '127.0.0.1:8300/js files/page.js'

.. note::

   Unit supports encoded symbols in URIs as the last query above suggests.

If your query specifies only the directory name, Unit will attempt to serve
:file:`index.html` from this directory:

.. subs-code-block:: console

   $ curl -vL 127.0.0.1:8300/html/

    ...
    < HTTP/1.1 200 OK
    < Last-Modified: Fri, 20 Sep 2019 04:14:43 GMT
    < ETag: "5d66459d-d"
    < Content-Type: text/html
    < Server: Unit/|version|
    ...

.. note::

   Unit's ETag response header fields use the following format:
   :samp:`%MTIME_HEX%-%FILESIZE_HEX%`.

Unit maintains a number of :ref:`built-in MIME types <configuration-mime>` like
:samp:`text/plain` or :samp:`text/html`; also, you can add extra types and
override built-ins in the :samp:`/config/settings/http/static/mime_types`
section.

.. _configuration-fallback:

Finally, within an :samp:`action`, you can supply a :samp:`fallback` option
beside a :samp:`share`.  It specifies the :ref:`action
<configuration-routes-action>` to be taken if the requested file isn't found at
the :samp:`share` path:

.. code-block:: json

   {
       "share": "/data/www/",
       "fallback": {
           "pass": "applications/php"
       }
   }

In the example above, an attempt to serve the requested file from the
:samp:`/data/www/` directory is made first.  Only if there's no such file, the
request is passed to the :samp:`php` application.

If a :samp:`fallback` itself is a :samp:`share`, it can also contain a nested
:samp:`fallback`:

.. code-block:: json

   {
       "share": "/data/www/",
       "fallback": {
           "share": "/data/cache/",
           "fallback": {
               "proxy": "http://127.0.0.1:9000"
           }
       }
   }

First, this configuration tries to serve a file from the :file:`/data/www/`
directory; next, it queries the :file:`/data/cache/` path.  If both attempts
fail, the request is proxied to an external server.

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
                      "share": "/www/php-app/assets/files/",
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
                      "share": "/www/php-app/assets/files/",
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


.. _configuration-routes-proxy:

********
Proxying
********

Unit :ref:`routes <configuration-routes>` support HTTP proxying to socket
addresses using the :samp:`proxy` option of a step's :samp:`action`:

.. code-block:: json

   {
       "routes": [
           {
               "match": {
                   "uri": "/ipv4/*"
               },

               "action": {
                   "proxy": "http://127.0.0.1:8080"
               }
           },
           {
               "match": {
                   "uri": "/ipv6/*"
               },

               "action": {
                   "proxy": "http://[::1]:8090"
               }
           },
           {
               "match": {
                   "uri": "/unix/*"
               },

               "action": {
                   "proxy": ":nxt_term:`http://unix:/path/to/unix.sock <Note the http:// scheme is still required>`"
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
           ":nxt_term:`rr-lb <Upstream object>`": {
               ":nxt_term:`servers <Lists individual servers as object-valued options>`": {
                   ":nxt_term:`192.168.0.100:8080 <Empty object needed due to JSON requirements>`": { },
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
               ":nxt_term:`weight <All three values are equal>`": 1e1
           },
           "192.168.0.101:8080": {
               ":nxt_term:`weight <All three values are equal>`": 10.0
           },
           "192.168.0.102:8080": {
               ":nxt_term:`weight <All three values are equal>`": 10
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
        startup<installation-src-startup>` to run Unit's non-privileged processes
        is used.

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

==================
Process Management
==================

Unit supports three per-app options that control the app's processes:
:samp:`isolation`, :samp:`limits`, and :samp:`processes`.

.. _configuration-proc-mgmt-isolation:

Process Isolation
*****************

You can use `namespace
<https://man7.org/linux/man-pages/man7/namespaces.7.html>`_ and `file system
<https://man7.org/linux/man-pages/man2/chroot.2.html>`_ isolation for your apps
if Unit's underlying OS supports them:

.. code-block:: console

   $ ls /proc/self/ns/

       cgroup  ipc  mnt  net  pid  ...  user  uts

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
              <http://man7.org/linux/man-pages/man7/cgroup_namespaces.7.html>`_
              namespace for the app.

          * - :samp:`credential`
            - Creates a new `user
              <http://man7.org/linux/man-pages/man7/user_namespaces.7.html>`_
              namespace for the app.

          * - :samp:`mount`
            - Creates a new `mount
              <http://man7.org/linux/man-pages/man7/mount_namespaces.7.html>`_
              namespace for the app.

          * - :samp:`network`
            - Creates a new `network
              <http://man7.org/linux/man-pages/man7/network_namespaces.7.html>`_
              namespace for the app.

          * - :samp:`pid`
            - Creates a new `PID
              <http://man7.org/linux/man-pages/man7/pid_namespaces.7.html>`_
              namespace for the app.

          * - :samp:`uname`
            - Creates a new `UTS
              <http://man7.org/linux/man-pages/man7/namespaces.7.html>`_
              namespace for the app.

       All options listed above are Boolean; to isolate the app, set the
       corresponding namespace option to :samp:`true`; to disable isolation,
       set the option to :samp:`false` (default).

   * - :samp:`uidmap`
     - Array of `ID mapping
       <http://man7.org/linux/man-pages/man7/user_namespaces.7.html>`_ objects;
       each array item must define the following:

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
       "path": ":nxt_term:`/ <Without rootfs, this would be /var/app/sandbox/>`",
       "home": ":nxt_term:`/venv/ <Without rootfs, this would be /var/app/sandbox/venv/>`",
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

Process Management
******************

The :samp:`processes` option offers a choice between static and dynamic process
management.  If you set it to an integer, Unit immediately launches the given
number of app processes and keeps them without scaling.

To enable dynamic prefork model for your app, supply a :samp:`processes` object
with the following options:

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

.. _configuration-languages:
.. _configuration-external:

==========
Go/Node.js
==========

To run your Go or Node.js applications in Unit, you need to configure them
`and` modify their source code as suggested below.  Let's start with the app
configuration; besides :ref:`common options <configuration-apps-common>`, you
have the following:

.. list-table::
    :header-rows: 1

    * - Option
      - Description

    * - :samp:`executable` (required)
      - Pathname of the application, absolute or relative to
        :samp:`working_directory`.

        For Node.js, supply your :file:`.js` pathname and start the file itself
        with a proper shebang:

        .. code-block:: javascript

           #!/usr/bin/env node

        .. note::

           Make sure to :command:`chmod +x` the file you list here so Unit can
           start it.

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
       "arguments": ["--tmp-files", "/tmp/go-cache"]
   }

Before applying the configuration, update the application itself.

.. _configuration-external-go:

Go
**

In the :samp:`import` section, reference the :samp:`"unit.nginx.org/go"`
package that you have :ref:`installed <installation-precomp-pkgs>` or
:ref:`built <installation-modules-go>` earlier:

.. code-block:: go

   import (
       ...
       "unit.nginx.org/go"
       ...
   )

.. note::

   The package is required only to build the app; there's no need to install it
   in the target environment.

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

The resulting application works as follows:

- When you run it standalone, the :samp:`unit.ListenAndServe` call falls back
  to :samp:`http` functionality.
- When Unit runs it, :samp:`unit.ListenAndServe` communicates with Unit's
  router process directly, ignoring the address supplied as its first argument
  and relying on the :ref:`listener's settings <configuration-listeners>`
  instead.

.. note::

   For Go-based examples, see our :doc:`howto/grafana` howto or a basic
   :ref:`sample <sample-go>`.

.. _configuration-external-nodejs:

Node.js
*******

First, you need to have the :program:`unit-http` module :ref:`installed
<installation-nodejs-package>`.  If it's global, symlink it in your project
directory:

.. code-block:: console

   # npm link unit-http

Do the same if you move a Unit-hosted application to a new system where
:program:`unit-http` is installed globally.

Next, use :samp:`unit-http` instead of :samp:`http` in your code:

.. code-block:: javascript

   var http = require('unit-http');

Unit also supports the WebSocket protocol; your Node.js app only needs to
replace the default :samp:`websocket`:

.. code-block:: javascript

  var webSocketServer = require('unit-http/websocket').server;

.. note::

   For Node.js-based examples, see our :doc:`howto/express` and
   :ref:`Docker <docker-apps>` howtos or a basic :ref:`sample <sample-nodejs>`.

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
       "classpath": ["/www/qwk2mart/lib/qwk2mart-2.0.0.jar"],
       "options": ["-Dlog_path=/var/log/qwk2mart.log"],
       "webapp": "/www/qwk2mart/qwk2mart.war"
   }

.. note::

   For Java-based examples, see our :doc:`howto/jira` and :doc:`howto/opengrok`
   howtos or a basic :ref:`sample <sample-java>`.

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
        <https://php.net/manual/en/ini.list.php>`_.

    * - :samp:`admin`, :samp:`user`
      - Objects for extra directives.  Values in :samp:`admin` are set in
        :samp:`PHP_INI_SYSTEM` mode, so the app can't alter them; :samp:`user`
        values are set in :samp:`PHP_INI_USER` mode and may `be updated
        <https://php.net/manual/en/function.ini-set.php>`_ in runtime.

Directives from :file:`php.ini` are overridden by settings supplied in
:samp:`admin` and :samp:`user` objects.

.. note::

   Values in :samp:`options` must be strings (for example,
   :samp:`"max_file_uploads": "4"`, not :samp:`"max_file_uploads": 4`); for
   boolean flags, use :samp:`"0"` and :samp:`"1"` only.  For details about
   :samp:`PHP_INI_*` modes, see the `PHP docs
   <https://php.net/manual/en/configuration.changes.modes.php>`_.

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
           "php_app": {
               "type": "php",
               "targets": {
                   "phpinfo": {
                       "script": "phpinfo.php",
                       "root": "/www/data/admin/"
                   },

                   "hello": {
                       "script": "hello.php",
                       "root": "/www/data/test/"
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
               "pass": "applications/php_app/hello"
           },

           "127.0.0.1:80": {
               "pass": "routes"
           }
       },

       "routes": [
           {
               "match": {
                   "uri": "/info"
               },

               "action": {
                   "pass": "applications/php_app/phpinfo"
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
   :doc:`howto/codeigniter`, :doc:`howto/drupal`, :doc:`howto/laravel`,
   :doc:`howto/matomo`, :doc:`howto/mediawiki`, :doc:`howto/nextcloud`,
   :doc:`howto/phpbb`, :doc:`howto/symfony`,  :doc:`howto/wordpress`, and
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

           The Python version used to run the app depends on the :samp:`type`
           value; Unit ignores the command-line interpreter from the virtual
           environment for performance considerations.

    * - :samp:`path`
      - String or array of strings that represent additional Python module
        lookup paths; these values are prepended to :samp:`sys.path`.

    * - :samp:`protocol`
      - Hint to tell Unit that the app uses a certain interface; can be
        :samp:`asgi` or :samp:`wsgi`.

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
       "working_directory": "/www/store/",
       "path": "/www/store/cart/",
       "home": "/www/store/.virtualenv/",
       "module": "wsgi",
       "callable": "app",
       "user": "www",
       "group": "www"
   }

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

.. note::

   For Python-based examples, see our :doc:`howto/datasette`,
   :doc:`howto/django`, :doc:`howto/djangochannels`, :doc:`howto/fastapi`,
   :doc:`howto/flask`, :doc:`howto/guillotina`, :doc:`howto/mercurial`,
   :doc:`howto/moin`, :doc:`howto/pyramid`, :doc:`howto/quart`,
   :doc:`howto/responder`, :doc:`howto/reviewboard`, :doc:`howto/sanic`,
   :doc:`howto/starlette`, and :doc:`howto/trac` howtos or a basic :ref:`sample
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

Example:

.. code-block:: json

   {
       "type": "ruby",
       "processes": 5,
       "user": "www",
       "group": "www",
       "script": "/www/cms/config.ru"
   }

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
        `RFC 7230 <https://tools.ietf.org/html/rfc7230#section-3.2>`_ header
        fields are processed.

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
   :file:`.pdf`, :file:`.png`, :file:`.rpm`, :file:`.rss`, :file:`.rst`,
   :file:`.svg`, :file:`.ttf`, :file:`.txt`, :file:`.wav`, :file:`.webm`,
   :file:`.webp`, :file:`.woff2`, :file:`.woff`, :file:`.xml`, and
   :file:`.zip`.  Built-ins can be overridden, and new types can be added:

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

************************
SSL/TLS and Certificates
************************

To set up SSL/TLS access for your application, upload a :file:`.pem` file
containing your certificate chain and private key to Unit.  Next, reference the
uploaded bundle in the listener's configuration.  After that, the listener's
application becomes accessible via SSL/TLS.

.. note::

   For the details of certificate issuance and renewal in Unit, see an
   example in :doc:`howto/certbot`.

First, create a :file:`.pem` file with your certificate chain and private key:

.. code-block:: console

   $ cat cert.pem ca.pem key.pem > bundle.pem

.. note::

   Usually, your website's certificate (optionally followed by the
   intermediate CA certificate) is enough to build a certificate chain.  If
   you add more certificates to your chain, order them leaf to root.

Upload the resulting file to Unit's certificate storage under a suitable name:

.. code-block:: console

   # curl -X PUT --data-binary @bundle.pem --unix-socket \
          /path/to/control.unit.sock http://localhost/certificates/<bundle>

       {
           "success": "Certificate chain uploaded."
       }

.. warning::

   Don't use :option:`!-d` for file upload; this option damages :file:`.pem`
   files.  Use the :option:`!--data-binary` option when uploading file-based
   data with :program:`curl` to avoid data corruption.

Internally, Unit stores uploaded certificate bundles along with other
configuration data in its :file:`state` subdirectory; Unit's control API maps
them to a separate configuration section, aptly named :samp:`certificates`:

.. code-block:: json

   {
       "certificates": {
           "<bundle>": {
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
              http://localhost/certificates/<bundle>/chain/0/
       # curl -X GET --unix-socket /path/to/control.unit.sock \
              http://localhost/certificates/<bundle>/chain/0/subject/alt_names/0/

Next, add a :samp:`tls` object to the listener configuration, referencing the
uploaded bundle in :samp:`certificate`:

.. code-block:: json

   {
       "listeners": {
           "127.0.0.1:443": {
               "pass": "applications/wsgi-app",
               "tls": {
                   "certificate": "<bundle>"
               }
           }
       }
   }

The resulting control API configuration may look like this:

.. code-block:: json

   {
       "certificates": {
           "<bundle>": {
               "key": "<key type>",
               "chain": ["<certificate chain, omitted for brevity>"]
           }
       },

       "config": {
           "listeners": {
               "127.0.0.1:443": {
                   "pass": "applications/wsgi-app",
                   "tls": {
                       "certificate": "<bundle>"
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

Now you're solid.  The application is accessible via SSL/TLS:

.. code-block:: console

   $ curl -v https://127.0.0.1
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
          http://localhost/certificates/<bundle>

       {
           "success": "Certificate deleted."
       }

.. note::

   You can't delete certificate bundles still referenced in your
   configuration, overwrite existing bundles using :samp:`PUT`, or (obviously)
   delete non-existent ones.

Happy SSLing!

.. _configuration-full-example:

************
Full Example
************

.. code-block:: json

   {
       "certificates": {
           "bundle": {
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
                       "certificate": "bundle"
                   }
               },

               "127.0.0.1:8001": {
                   "pass": "applications/drive"
               },

               "*:8080": {
                   "pass": "upstreams/rr-lb"
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
                       "host": ["blog.example.com", "blog.*.org"],
                       "source": "*:8000-9000"
                   },

                   "action": {
                       "pass": "applications/blogs/core"
                   }
               },
               {
                   "match": {
                       "host": "example.com",
                       "source": "127.0.0.0-127.0.0.255:8080-8090",
                       "uri": "/chat/*"
                   },

                   "action": {
                       "pass": "applications/chat"
                   }
               },
               {
                   "match": {
                       "host": "example.com",
                       "source": [
                           "10.0.0.0/7:1000",
                           "10.0.0.0/32:8080-8090"
                       ]
                   },

                   "action": {
                       "pass": "applications/store"
                   }
               },
               {
                   "match": {
                       "host": "wiki.example.com"
                   },

                   "action": {
                       "pass": "applications/wiki"
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
                       "share": "/www/static/",
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
                   "working_directory": "/www/cms/"
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
                   "classpath": ["/www/store/lib/store-2.0.0.jar"],
                   "options": ["-Dlog_path=/var/log/store.log"]
               },

               "wiki": {
                   "type": "python",
                   "module": "asgi",
                   "protocol": "asgi",
                   "callable": "app",
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
                       "192.168.1.100:8080": { },
                       "192.168.1.101:8080": {
                           "weight": 2
                       }
                   }
               }
           },

           "access_log": "/var/log/access.log"
       }
   }
