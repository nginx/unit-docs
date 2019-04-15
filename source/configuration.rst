
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
available via the :ref:`control socket <installation-startup>` at
:samp:`http://localhost/`:

.. code-block:: console

   # cat << EOF > config.json

       >{
       >    "type": "php",
       >    "root": "/www/blogs/scripts"
       >}
       > EOF

   # curl -X PUT --data-binary @config.json --unix-socket \
          /path/to/control.unit.sock http://localhost/config/applications/blogs/

       {
	       "success": "Reconfiguration done."
       }

Unit starts the application process.  Next, reference the application object
from a :ref:`listener <configuration-listeners>` object, comprising an IP (or a
wildcard to match any IPs) and a port number, in the :samp:`config/listeners`
section of the API:

.. code-block:: console

   # cat << EOF > config.json

       > {
       >     "pass": "applications/blogs"
       > }
       > EOF

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

================
Creating Objects
================

To create a configuration object, specify the JSON data for it in the body of a
:samp:`PUT` request.  To reduce errors, it makes sense to write the JSON data
in a file and specify the file path with the :option:`!-d` option to the
:program:`curl` command.

Create an initial configuration by uploading the contents of the
:file:`start.json` file:

.. code-block:: console

   # curl -X PUT -d @/path/to/start.json  \
          --unix-socket /path/to/control.unit.sock http://localhost/config/

Create a new application object called :samp:`wiki` from the file
:file:`wiki.json`:

.. code-block:: console

   # curl -X PUT -d @/path/to/wiki.json  \
          --unix-socket /path/to/control.unit.sock http://localhost/config/applications/wiki

The contents of :file:`wiki.json` are:

.. code-block:: json

   {
       "type": "python",
       "processes": 10,
       "module": "wsgi",
       "user": "www-wiki",
       "group": "www-wiki",
       "path": "/www/wiki"
   }

==================
Displaying Objects
==================

To display a configuration object, append its path to the :samp:`curl` URL.

Display the complete configuration:

.. code-block:: console

   # curl --unix-socket /path/to/control.unit.sock http://localhost/config/

       {
           "listeners": {
               "*:8300": {
                   "pass": applications/blogs"
               }
           },

           "applications": {
               "blogs": {
                   "type": "php",
                   "user": "nobody",
                   "group": "nobody",
                   "root": "/www/blogs/scripts/"
               }
           }
       }

Display the data for the :samp:`wiki` application:

.. code-block:: console

   # curl --unix-socket /path/to/control.unit.sock \
          http://localhost/config/applications/wiki

       {
           "type": "python",
           "processes": 10,
           "module": "wsgi",
           "user": "www",
           "group": "www",
           "path": "/www/wiki"
       }

=================
Modifying Objects
=================

To change a configuration object, use the :option:`!-d` option to the
:program:`curl` command to specify the object's JSON data in the body of a
:samp:`PUT` request.

Change the :samp:`application` object to :samp:`wiki-dev` for the listener on
:samp:`\*:8400`:

.. code-block:: console

   # curl -X PUT -d '"wiki-dev"' --unix-socket /path/to/control.unit.sock  \
          'http://localhost/config/listeners/*:8400/application'

       {
           "success": "Reconfiguration done."
       }

Change the :samp:`root` object for the :samp:`blogs` application to
:file:`/www/blogs-dev/scripts`:

.. code-block:: console

   # curl -X PUT -d '"/www/blogs-dev/scripts"'  \
          --unix-socket /path/to/control.unit.sock  \
          http://localhost/config/applications/blogs/root

       {
           "success": "Reconfiguration done."
       }

================
Deleting Objects
================

To delete a configuration object, make a :samp:`DELETE` request and append the
object's path to the :program:`curl` URL.

Delete the listener on :samp:`\*:8400`:

.. code-block:: console

   # curl -X DELETE --unix-socket /path/to/control.unit.sock  \
          'http://localhost/config/listeners/*:8400'

       {
           "success": "Reconfiguration done."
       }

.. _configuration-listeners:

*********
Listeners
*********

For an application to be accessible via HTTP, you must define at least one
listener for it in the :samp:`listeners` section of the Unit configuration.  A
listener is an IP address and port on which Unit listens for client requests to
a named application.  The IP address can be either a full address (for example,
:samp:`127.0.0.1:8300`) or a wildcard (for example, :samp:`*:8300`).

.. list-table::
    :header-rows: 1

    * - Option
      - Description

    * - :samp:`application` (deprecated)
      - App name: :samp:`"application": "qwk2mart"`.  Mutually exclusive with
        :samp:`pass`.

        .. warning::

           This option is deprecated.  Please update your configurations to use
           :samp:`pass` instead.

    * - :samp:`pass` (required)
      - Qualified app or route name: :samp:`"pass": "routes/route66"`,
        :samp:`"pass": "applications/qwk2mart"`.  Mutually exclusive with
        :samp:`application`.

    * - :samp:`tls`
      - SSL/TLS configuration.  Set its only option, :samp:`certificate`, to
        enable secure communication via the listener.  The value must reference
        a certificate chain that you have uploaded earlier.  For details, see
        :ref:`configuration-ssl`.

In this example, requests received on port 8300 are sent to the :samp:`blogs`
application:

.. code-block:: json

   {
       "pass": "applications/blogs",
       "tls": {
           "certificate": "blogs-cert"
       }
   }

.. _configuration-routes:

******
Routes
******

Unit configuration offers a :samp:`routes` object to enable elaborate internal
routing between listeners and apps.  Listeners :samp:`pass` requests to routes
or directly to apps.  Requests are matched against route step conditions; a
request fully matching a step's condition is passed to the app or the route
that the step specifies.

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

============
Route Object
============

A route array contains step objects as elements; a request passed to a route
traverses them sequentially.

Steps have the following options:

.. list-table::
   :header-rows: 1

   * - Option
     - Description

   * - :samp:`match`
     - Object that defines the step condition.

       - If the request fits the :samp:`match` condition, the step's
         :samp:`pass` is followed.

       - If the request doesn't match a step, Unit proceeds to the next
         step of the route.

       - If the request doesn't match any steps, a 404 "Not Found" response is
         returned.

       See :ref:`below <configuration-routes-cond>` for condition matching
       details.

   * - :samp:`action`/:samp:`pass` (required)
     - Route's destination; identical to :samp:`pass` in a :ref:`listener
       <configuration-listeners>`.  If you omit :samp:`match`, requests are
       passed unconditionally; to avoid issues, use no more than one such step
       per route, placing it last.

An example:

.. code-block:: json

   {
       "routes": [
           {
               "match": {
                   "host": "example.com",
                   "uri": "/admin/*"
               },

               "action": {
                   "pass": "applications/php5_app"
                }
           },
           {
               "action": {
                   "pass": "applications/php7_app"
                }
           }
        ]
   }

A more elaborate example with chained routes:

.. code-block:: json

   {
       "routes": {
           "main": [
               {
                   "match": {
                       "host": [ "www.example.com", "example.com" ]
                   },

                   "action": {
                       "pass": "routes/site"
                   }
               },
               {
                   "match": {
                       "host": "blog.example.com"
                   },

                   "action": {
                       "pass": "applications/blog"
                   }
               }
           ],

           "site": [ "..." ]
       }
   }

.. _configuration-routes-cond:

==================
Condition Matching
==================

The :samp:`match` condition in a step comprises request property names and
corresponding patterns:

.. code-block:: json

   {
       "match": {
           "request_property1": "pattern",
           "request_property2": ["pattern", "pattern", "..." ]
       },

       "action": {
           "pass": "..."
        }
   }

To fit a step's condition, the request must match all properties listed in it.
Available options:

.. list-table::
   :header-rows: 1

   * - Option
     - Description

   * - :samp:`host`
     - Request host from the :samp:`Host` header field without port number,
       normalized by removing the trailing period (if any); case-insensitive.

   * - :samp:`method`
     - Request method from the request line; case-insensitive.

   * - :samp:`uri`
     - Request URI path without arguments, normalized by decoding the "%XX"
       sequences, resolving relative path references ("." and ".."), and
       compressing adjacent slashes into one; case-sensitive.

Patterns must be exact matches; they also support wildcards (:samp:`*`) and
negations (:samp:`!`):

- A wildcard matches zero or more arbitrary characters; pattern can start with
  it, end with it, or both.

- A negation restricts specific patterns; pattern can only start with it.

To be a match against the patterns listed in a condition, the property must
meet two requirements:

- If there are patterns without negation, at least one of them matches.

- No negation-based patterns match.

.. note::

   This type of matching can be explained with set operations.  Suppose set *U*
   comprises all possible values of a property; set *P* comprises strings that
   match any patterns without negation; set *N* comprises strings that match
   any negation-based patterns.  In this scheme, the matching set will be:

   | *U* ∩ *P* \\ *N* if *P* ≠ ∅
   | *U* \\ *N* if *P* = ∅

A few examples:

.. code-block:: json

   {
       "host": "*.example.com"
   }

Only subdomains of :samp:`example.com` will match.

.. code-block:: json

   {
       "host": ["*.example.com", "!www.example.com"]
   }

Here, any subdomains of :samp:`example.com` will match except
:samp:`www.example.com`.

.. code-block:: json

   {
       "method": ["!HEAD", "!GET"]
   }

Any methods will match except :samp:`HEAD` and :samp:`GET`.

You can also combine special characters in a pattern:

.. code-block:: json

   {
       "uri": "!*/api/*"
   }

Here, any URIs will match except ones containing :samp:`/api/`.

If all properties match or you omit the condition, Unit routes the request
where :samp:`pass` points to:

.. code-block:: json

   {
       "match": {
           "host": [ "*.example.com", "!php7.example.com" ],
           "uri": [ "/admin/*", "/store/*" ],
           "method": "POST"
       },

       "action": {
           "pass": "applications/php5_app"
        }
   }

Here, all :samp:`POST` requests for URIs prefixed with :samp:`/admin/` or
:samp:`/store/` within any subdomains of :samp:`example.com` (except
:samp:`php7`) are routed to :samp:`php5_app`.

.. _configuration-applications:

************
Applications
************

Each app that Unit runs is defined as an object in the
:samp:`config/applications` section of the control API; it lists the app's
language and settings, its runtime limits, process model, and various
language-specific options.

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

Each application object has a number of common options that can be specified
for any application regardless of its type:

.. list-table::
    :header-rows: 1

    * - Option
      - Description

    * - :samp:`type` (required)
      - Type of the application: :samp:`external` (Go and Node.js),
        :samp:`java`, :samp:`perl`, :samp:`php`, :samp:`python`, or
        :samp:`ruby`.

        Except with :samp:`external`, you can detail the runtime version:
        :samp:`"type": "python 3"`, :samp:`"type": "python 3.4"`, or even
        :samp:`"type": "python 3.4.9rc1"`.  Unit searches its modules and uses
        the latest matching one, reporting an error if none match.

        For example, if you have installed only one PHP 7 module, 7.1.9, it
        will match :samp:`"php"`, :samp:`"php 7"`, :samp:`"php 7.1"`, and
        :samp:`"php 7.1.9"`.  If you install two PHP modules, 7.0.2 and 7.0.23,
        and prefer to use 7.0.2, set :samp:`"type": "php 7.0.2"`.  If you
        supply :samp:`"php 7"`, PHP 7.0.23 will be used as the latest version
        available.

    * - :samp:`limits`
      - An object that accepts two integer options, :samp:`timeout` and
        :samp:`requests`.  Their values restrict the life cycle of an
        application process.  For details, see
        :ref:`configuration-proc-mgmt-lmts`.

    * - :samp:`processes`
      - An integer or an object.  Integer value configures a static number of
        application processes.  Object accepts dynamic process management
        options: :samp:`max`, :samp:`spare`, and :samp:`idle_timeout`.  For
        details, see :ref:`configuration-proc-mgmt-prcs`.

        The default value is 1.

    * - :samp:`working_directory`
      - Working directory for the application.
        If not specified, the working directory of Unit daemon is used.

    * - :samp:`user`
      - Username that runs the app process.
        If not specified, :samp:`nobody` is used.

    * - :samp:`group`
      - Group name that runs the app process.
        If not specified, user's primary group is used.

    * - :samp:`environment`
      - Environment variables to be used by the application.

Example:

.. code-block:: json

   {
       "type": "python 3.6",
       "processes": 16,
       "working_directory": "/www/python-apps",
       "path": "blog",
       "module": "blog.wsgi",
       "user": "blog",
       "group": "blog",
       "limits": {
           "timeout": 10,
           "requests": 1000
       },

       "environment": {
           "DJANGO_SETTINGS_MODULE": "blog.settings.prod",
           "DB_ENGINE": "django.db.backends.postgresql",
           "DB_NAME": "blog",
           "DB_HOST": "127.0.0.1",
           "DB_PORT": "5432"
       }
   }

Depending on the :samp:`type` of the application, you may need to configure a
number of additional options.  In the example above, Python-specific options
:samp:`path` and :samp:`module` are used.

=============================
Process Management and Limits
=============================

Application process behavior in Unit is described by two configuration options,
:samp:`limits` and :samp:`processes`.

.. _configuration-proc-mgmt-lmts:

Request Limits
**************

The :samp:`limits` object has two options:

 .. list-table::
    :header-rows: 1

    * - Option
      - Description

    * - :samp:`timeout`
      - Request timeout in seconds.  If an application process exceeds this
        limit while processing a request, Unit terminates the process and
        returns an HTTP error to the client.

    * - :samp:`requests`
      - Maximum number of requests Unit allows an application process to serve.
        If this limit is reached, Unit terminates and restarts the application
        process.  This allows to mitigate application memory leaks or other
        issues that may accumulate over time.

.. _configuration-proc-mgmt-prcs:

Process Management
******************

The :samp:`processes` option offers choice between static and dynamic process
management model.  If you provide an integer value, Unit immediately launches
the given number of application processes and maintains them statically without
scaling.

Unit also supports a dynamic prefork model for :samp:`processes` that is
enabled and configured with the following parameters:

.. list-table::
    :header-rows: 1

    * - Option
      - Description

    * - :samp:`max`
      - Maximum number of application processes that Unit will maintain
        (busy and idle).

        The default value is 1.

    * - :samp:`spare`
      - Minimum number of idle processes that Unit will reserve for the
        application when possible.  When Unit starts an application,
        :samp:`spare` idle processes are launched.  As requests arrive, Unit
        assigns them to existing idle processes and forks new idle ones to
        maintain the :samp:`spare` level if :samp:`max` permits.  When
        processes complete requests and turn idle, Unit terminates extra ones
        after a timeout.

        The default value is 0.  The value of :samp:`spare` cannot exceed
        :samp:`max`.


    * - :samp:`idle_timeout`
      - Number of seconds for Unit to wait before it terminates an extra idle
        process, when the count of idle processes exceeds :samp:`spare`.

        The default value is 15.

If :samp:`processes` is omitted entirely, Unit creates 1 static process.  If
an empty object is provided: :samp:`"processes": {}`, dynamic behavior with
default parameter values is assumed.

In the following example, Unit tries to keep 5 idle processes, no more than 10
processes in total, and terminates extra idle processes after 20 seconds of
inactivity:

.. code-block:: json

   {
       "max": 10,
       "spare": 5,
       "idle_timeout": 20
   }

.. _configuration-external:

=======================
Go/Node.js Applications
=======================

To run your Go or Node.js applications in Unit, you need to configure
them `and` modify their source code as suggested below.  Let's start with the
application configuration:

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

Modifying Go Sources
********************

In the :samp:`import` section, reference the :samp:`"nginx/unit"` package that
you have installed earlier:

.. code-block:: go

   import (
       ...
       "nginx/unit"
       ...
   )

In the :samp:`main()` function, replace the :samp:`http.ListenandServe` call
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

.. _configuration-external-nodejs:

Modifying Node.js Sources
*************************

First, you need to have the :program:`unit-http` package :ref:`installed
<installation-nodejs-package>`.  If it's global, symlink it in your project
directory:

.. code-block:: console

   # npm link unit-http

Do the same if you move a Unit-hosted application to a new system where
:program:`unit-http` is installed globally.

Next, use :samp:`unit-http` instead of :samp:`http` in your code:

.. code-block:: javascript

   var http = require('unit-http');

.. _configuration-java:

================
Java Application
================

.. list-table::
    :header-rows: 1

    * - Object
      - Description

    * - :samp:`classpath`
      - Array of paths to your app's required libraries (may point to
        directories or :file:`.jar` files).

    * - :samp:`options`
      - Array of strings defining JVM runtime options.

    * - :samp:`webapp` (required)
      - Pathname of the application's packaged or unpackaged :file:`.war` file.

Example:

.. code-block:: json

   {
       "type": "java",
       "classpath": ["/www/qwk2mart/lib/qwk2mart-2.0.0.jar"],
       "options": ["-Dlog_path=/var/log/qwk2mart.log"],
       "webapp": "/www/qwk2mart/qwk2mart.war"
   }

================
Perl Application
================

.. list-table::
    :header-rows: 1

    * - Option
      - Description

    * - :samp:`script` (required)
      - PSGI script path.

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

.. _configuration-php:

===============
PHP Application
===============

.. list-table::
    :header-rows: 1

    * - Option
      - Description

    * - :samp:`index`
      - Filename appended to any URI paths ending with a slash; applies if
        :samp:`script` is omitted.

        Default value is :samp:`index.php`.

    * - :samp:`options`
      - Object that defines :file:`php.ini` location and options.  For details,
        see below.

    * - :samp:`root` (required)
      - Base directory of your PHP app's file structure.  All URI paths are
        relative to this value.

    * - :samp:`script`
      - Filename of a PHP script; if set, Unit uses this script to serve any
        requests to this application.  Relative to :samp:`root`.

The :samp:`index` and :samp:`script` options enable two modes of operation:

- If :samp:`script` is set, all requests to the application are handled by
  the script you provide.

- Otherwise, the requests are served according to their URI paths; if script
  name is omitted, :samp:`index` is used.

You can customize :file:`php.ini` via the :samp:`options` object:

.. list-table::
    :header-rows: 1

    * - Option
      - Description

    * - :samp:`file`
      - Pathname of the :file:`php.ini` file.

    * - :samp:`admin`, :samp:`user`
      - Objects with `PHP configuration directives
        <http://php.net/manual/en/ini.list.php>`_.  Directives in :samp:`admin`
        are set in :samp:`PHP_INI_SYSTEM` mode; it means that your application
        can't alter them.  Directives in :samp:`user` are set in
        :samp:`PHP_INI_USER` mode; your application is allowed to `update them
        <http://php.net/manual/en/function.ini-set.php>`_ in runtime.

Directives from :file:`php.ini` are applied first; next, :samp:`admin` and
:samp:`user` objects are applied.

.. note::

   Provide string values for any directives you specify in :samp:`options`
   (for example, :samp:`"max_file_uploads": "64"` instead of
   :samp:`"max_file_uploads": 64`).  For flags, use :samp:`"0"` and
   :samp:`"1"` only.  For more information about :samp:`PHP_INI_*` modes, see
   the `PHP documentation
   <http://php.net/manual/en/configuration.changes.modes.php>`_.

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

.. _configuration-python:

==================
Python Application
==================

.. list-table::
    :header-rows: 1

    * - Option
      - Description

    * - :samp:`module` (required)
      - `WSGI <https://www.python.org/dev/peps/pep-3333/>`_ module name.  To
        run the app, Unit looks for an :samp:`application` callable in the
        module you supply; the :samp:`module` itself is `imported
        <https://docs.python.org/3/reference/import.html>`_ just like in
        Python.

    * - :samp:`path`
      - Additional lookup path for Python modules; this string is inserted into
        :samp:`sys.path`.

    * - :samp:`home`
      - Path to Python `virtual environment <https://packaging.python.org/
        tutorials/installing-packages/#creating-virtual-environments>`_
        for the application.  You can set this value relative to the
        :samp:`working_directory` of the application.

        .. note::

           The Python version used by Unit to run the application is controlled
           by the :samp:`type` of the application.  Unit doesn't use command
           line Python interpreter within the virtual environment due to
           performance considerations.

Example:

.. code-block:: json

   {
       "type": "python 3.6",
       "processes": 10,
       "working_directory": "/www/store/",
       "path": "/www/store/cart/",
       "home": "/www/store/.virtualenv/",
       "module": "wsgi",
       "user": "www",
       "group": "www"
   }

================
Ruby Application
================

.. list-table::
    :header-rows: 1

    * - Option
      - Description

    * - :samp:`script` (required)
      - Rack script path.

Example:

.. code-block:: json

   {
       "type": "ruby",
       "processes": 5,
       "user": "www",
       "group": "www",
       "script": "/www/cms/config.ru"
   }

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

Example:

.. code-block:: json

   {
       "settings": {
           "http": {
               "header_read_timeout": 10,
               "body_read_timeout": 10,
               "send_timeout": 10,
               "idle_timeout": 120,
               "max_body_size": 6291456
           }
       }
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

   # curl -X PUT -d '"/var/log/access.log"'  \
          --unix-socket /path/to/control.unit.sock  \
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

First, create a :file:`.pem` file with your certificate chain and private key:

.. code-block:: console

   $ cat cert.pem ca.pem key.pem > bundle.pem

.. note::

   Usually, your website's certificate (optionally followed by the
   intermediate CA certificate) is enough to build a certificate chain.  If
   you add more certificates to your chain, order them leaf to root.

Upload the resulting file to Unit's certificate storage under a suitable name:

.. code-block:: console

   # curl -X PUT --data-binary @bundle.pem --unix-socket /path/to/control.unit.sock \
          http://localhost/certificates/<bundle>

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
                   },
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

Next, add a :samp:`tls` object to your listener configuration, referencing the
uploaded bundle's name in :samp:`certificate`:

.. code-block:: json

   {
       "listeners": {
           "127.0.0.1:8080": {
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
               "127.0.0.1:8080": {
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

   $ curl -v https://127.0.0.1:8080
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
                   "max_body_size": 6291456
               }
           },

           "listeners": {
               "*:8300": {
                   "pass": "applications/blogs",
                   "tls": {
                       "certificate": "bundle"
                   }
               },

               "*:8400": {
                   "pass": "applications/wiki"
               },

               "*:8500": {
                   "pass": "applications/go_chat_app"
               },

               "127.0.0.1:8600": {
                   "pass": "applications/bugtracker"
               },

               "127.0.0.1:8601": {
                   "pass": "routes/cms"
               },

               "*:8700": {
                   "pass": "applications/qwk2mart"
               }
           },

           "routes" {
               "cms": [
                   {
                       "match": {
                           "uri": "!/admin/*"
                       },
                       "action": {
                           "pass": "applications/cms_main"
                       }
                   },

                   {
                       "action": {
                           "pass": "applications/cms_admin"
                       }
                   }
               ]
           },

           "applications": {
               "blogs": {
                   "type": "php",
                   "processes": 20,
                   "root": "/www/blogs/scripts/",
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
                   }
               },

               "wiki": {
                   "type": "python",
                   "processes": 10,
                   "path": "/www/wiki",
                   "module": "wsgi",
                   "environment": {
                       "DJANGO_SETTINGS_MODULE": "blog.settings.prod",
                       "DB_ENGINE": "django.db.backends.postgresql",
                       "DB_NAME": "blog",
                       "DB_HOST": "127.0.0.1",
                       "DB_PORT": "5432"
                   }
               },

               "go_chat_app": {
                   "type": "external",
                   "user": "www-chat",
                   "group": "www-chat",
                   "working_directory": "/www/chat",
                   "executable": "bin/chat_app"
               },

               "bugtracker": {
                   "type": "perl",
                   "processes": {
                       "max": 10,
                       "spare": 5,
                       "idle_timeout": 20
                   },

                   "working_directory": "/www/bugtracker",
                   "script": "app.psgi"
               },

               "cms_main": {
                   "type": "ruby",
                   "processes": 5,
                   "script": "/www/cms/main.ru"
               },

               "cms_admin": {
                   "type": "ruby",
                   "processes": 1,
                   "script": "/www/cms/admin.ru"
               },

               "qwk2mart": {
                   "type": "java",
                   "classpath": ["/www/qwk2mart/lib/qwk2mart-2.0.0.jar"],
                   "options": ["-Dlog_path=/var/log/qwk2mart.log"],
                   "webapp": "/www/qwk2mart/qwk2mart.war"
               }
           },

           "access_log": "/var/log/access.log"
       }
   }
