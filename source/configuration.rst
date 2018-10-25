
#############
Configuration
#############

By default, the Unit API is available in the control socket file
**control.unit.sock**.

Applications
************

For each application, you use the API to define a JSON object in the
``applications`` section of the Unit configuration.  The JSON object defines
several characteristics of the application, including the language it's written
in, the number of application processes to run, the directory with the file or
files for the application, and parameters that vary by language.

This example runs 20 processes of the PHP application named **blogs** using the
files found in the **/www/blogs/scripts** directory.  The default launch file
when the URL doesn't specify the PHP file is **index.php**.

::

    {
        "blogs": {
            "type": "php",
            "processes": 20,
            "root": "/www/blogs/scripts",
            "index": "index.php"
        }
    }

.. _configuration-listeners:

Listeners
*********

For an application to be accessible via HTTP, you must define at least
one listener for it in the ``listeners`` section of the Unit configuration.
A listener is an IP address and port on which Unit listens for client requests
to a named application.  The IP address can be either a full address (for
example, ``127.0.0.1:8300``) or a wildcard (for example, ``*:8300``).

In this example, requests received on port 8300 are sent to the **blogs**
application::

    {
        "*:8300": {
            "application": "blogs"
        }
    }


For complete details about the JSON objects for each language, see
`Application Objects`_.

Minimum Configuration
*********************

In order to run an application, configuration must include at least one
listener and associated application, as in this example::

    {
        "listeners": {
            "*:8300": {
                "application": "blogs"
            }
        },

        "applications": {
            "blogs": {
                "type": "php",
                "processes": 20,
                "root": "/www/blogs/scripts",
                "index": "index.php"
            }
        }
    }

Creating Configuration Objects
******************************

To create a configuration object, specify the JSON data for it in the body of
a ``PUT`` request.  To reduce errors, it makes sense to write the JSON data in a
file and specify the file path with the ``-d`` option to the ``curl`` command.


Example: Create a Full Configuration
====================================

Create an initial configuration by uploading the contents of the **start.json**
file:

.. code-block:: none

    # curl -X PUT -d @/path/to/start.json  \
           --unix-socket /path/to/control.unit.sock http://localhost/config/


Example: Create an Application Object
=====================================

Create a new application object called **wiki** from the file **wiki.json**:

.. code-block:: none

    # curl -X PUT -d @/path/to/wiki.json  \
           --unix-socket /path/to/control.unit.sock http://localhost/config/applications/wiki


The contents of **wiki.json** are::

    {
        "type": "python",
        "processes": 10,
        "module": "wsgi",
        "user": "www-wiki",
        "group": "www-wiki",
        "path": "/www/wiki"
    }

Displaying Configuration Objects
********************************

To display a configuration object, append its path to the ``curl`` URL.

Example: Display the Full Configuration
=======================================

Display the complete configuration:

.. code-block:: none

    # curl --unix-socket /path/to/control.unit.sock http://localhost/config/
    {
        "listeners": {
            "*:8300": {
                "application": "blogs"
            }
        },

        "applications": {
            "blogs": {
                "type": "php",
                "user": "nobody",
                "group": "nobody",
                "root": "/www/blogs/scripts",
                "index": "index.php"
            }
        }
    }

Example: Display One Object
===========================

Display the data for the **wiki** application:

.. code-block:: none

    # curl --unix-socket /path/to/control.unit.sock http://localhost/config/applications/wiki
    {
        "type": "python",
        "processes": 10,
        "module": "wsgi",
        "user": "www",
        "group": "www",
        "path": "/www/wiki"
    }

Modifying Configuration Objects
*******************************

To change a configuration object, use the ``-d`` option to the ``curl`` command
to specify the object's JSON data in the body of a ``PUT`` request.

Example: Change the Application for a Listener
==============================================

Change the ``application`` object to **wiki-dev** for the listener on \*:8400:

.. code-block:: none

    # curl -X PUT -d '"wiki-dev"' --unix-socket /path/to/control.unit.sock  \
           'http://localhost/config/listeners/*:8400/application'
    {
        "success": "Reconfiguration done."
    }

Example: Change the File Path for an Application
================================================

Change the ``root`` object for the **blogs** application to
**/www/blogs-dev/scripts**:

.. code-block:: none

    # curl -X PUT -d '"/www/blogs-dev/scripts"'  \
           --unix-socket /path/to/control.unit.sock  \
           http://localhost/config/applications/blogs/root
    {
        "success": "Reconfiguration done."
    }

Deleting Configuration Objects
******************************

To delete a configuration object, make a ``DELETE`` request and append the
object's path to the ``curl`` URL.

Example: Delete a Listener
==========================

Delete the listener on \*:8400:

.. code-block:: none

    # curl -X DELETE --unix-socket /path/to/control.unit.sock  \
           'http://localhost/config/listeners/*:8400'
    {
        "success": "Reconfiguration done."
    }

.. _configuration-stngs:

Settings Object
***************

Unit has a global ``settings`` configuration object that stores instance-wide
preferences.  Its ``http`` option fine-tunes the handling of HTTP requests from
the clients:

.. list-table::
    :header-rows: 1

    * - Option
      - Description

    * - ``header_read_timeout`` (optional)
      - Maximum number of seconds to read the header of a client's request.
        If Unit doesn't receive the entire header from the client within this
        interval, it responds with a 408 Request Timeout error.

        The default value is 30.

    * - ``body_read_timeout`` (optional)
      - Maximum number of seconds to read data from the body of a client's
        request.  It limits the interval between consecutive read operations,
        not the time to read the entire body.  If Unit doesn't receive any
        data from the client within this interval, it responds with a 408
        Request Timeout error.

        The default value is 30.

    * - ``send_timeout`` (optional)
      - Maximum number of seconds to transmit data in the response to a client.
        It limits the interval between consecutive transmissions, not the
        entire response transmission.  If the client doesn't receive any data
        within this interval, Unit closes the connection.

        The default value is 30.

    * - ``idle_timeout`` (optional)
      - Maximum number of seconds between requests in a keep-alive connection.
        If no new requests arrive within this interval, Unit responds with a
        408 Request Timeout error and closes the connection.

        The default value is 180.

    * - ``max_body_size`` (optional)
      - Maximum number of bytes in the body of a client's request.  If the body
        size exceeds this value, Unit responds with a 413 Payload Too Large
        error and closes the connection.

        The default value is 8388608 (8 MB).

Example::

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

Listener Objects
****************

.. list-table::
    :header-rows: 1

    * - Object
      - Description

    * - ``application``
      - Application name.

    * - :samp:`tls` (optional)
      - SSL/TLS configuration.  Set its only option, :samp:`certificate`, to
        enable secure communication via the listener.  The value must reference
        a certificate chain that you have uploaded earlier.  For details, see
        :ref:`configuration-ssl`.

Example:

.. code-block:: json

    {
        "application": "blogs",
        "tls": {
            "certificate": "blogs-cert"
        }
    }

Application Objects
*******************

Each application object has a number of common options that can be specified
for any application regardless of its type.

The common options are follows:

.. list-table::
    :header-rows: 1

    * - Object
      - Description

    * - ``type``
      - Type of the application: ``external`` (Go and Node.js), ``perl``,
        ``php``, ``python``, or ``ruby``.

        Except with ``external``, you can detail the runtime version: ``"type":
        "python 3"``, ``"type": "python 3.4"``, or even ``"type": "python
        3.4.9rc1"``.  Unit searches its modules and uses the latest matching
        one, reporting an error if none match.

        For example, if you have installed only one PHP 7 module, 7.1.9,
        it will match ``"php"``, ``"php 7"``, ``"php 7.1"``, and
        ``"php 7.1.9"``.  If you install two PHP modules, 7.0.2 and 7.0.23,
        and prefer to use 7.0.2, set ``"type": "php 7.0.2"``.  If you supply
        ``"php 7"``, PHP 7.0.23 will be used as the latest version available.

    * - ``limits`` (optional)
      - An object that accepts two integer options, ``timeout`` and
        ``requests``.  Their values restrict the life cycle of an application
        process.  For details, see :ref:`configuration-proc-mgmt-lmts`.

    * - ``processes`` (optional)
      - An integer or an object.  Integer value configures a static number
        of application processes.  Object accepts dynamic process management
        settings: ``max``, ``spare``, and ``idle_timeout``.  For details, see
        :ref:`configuration-proc-mgmt-prcs`.

        The default value is 1.

    * - ``working_directory`` (optional)
      - Working directory for the application.
        If not specified, the working directory of Unit daemon is used.

    * - ``user`` (optional)
      - Username that runs the app process.
        If not specified, ``nobody`` is used.

    * - ``group`` (optional)
      - Group name that runs the app process.
        If not specified, user's primary group is used.

    * - ``environment`` (optional)
      - Environment variables to be used by the application.

Example::

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

Depending on the ``type`` of the application, you may need to configure
a number of additional options.
In the example above, Python-specific options ``path`` and ``module`` are used.

Process Management and Limits
=============================

Application process behavior in Unit is described by two configuration options,
``limits`` and ``processes``.

.. _configuration-proc-mgmt-lmts:

Request Limits
--------------

The ``limits`` object accepts two options:

 .. list-table::
    :header-rows: 1

    * - Option
      - Description

    * - ``timeout`` (optional)
      - Request timeout in seconds.  If an application process exceeds this
        limit while processing a request, Unit terminates the process and
        returns an HTTP error to the client.

    * - ``requests`` (optional)
      - Maximum number of requests Unit allows an application process to serve.
        If this limit is reached, Unit terminates and restarts the application
        process.  This allows to mitigate application memory leaks or other
        issues that may accumulate over time.

.. _configuration-proc-mgmt-prcs:

Process Management
------------------

The ``processes`` option offers choice between static and dynamic process
management model.  If you provide an integer value, Unit immediately launches
the given number of application processes and maintains them statically without
scaling.

Unit also supports a dynamic prefork model for ``processes`` that is
enabled and configured with the following parameters:

.. list-table::
    :header-rows: 1

    * - Option
      - Description

    * - ``max``
      - Maximum number of application processes that Unit will maintain
        (busy and idle).

        The default value is 1.

    * - ``spare``
      - Minimum number of idle processes that Unit will reserve for the
        application when possible.  When Unit starts an application, ``spare``
        idle processes are launched.  As requests arrive, Unit assigns them to
        existing idle processes and forks new idle ones to maintain the
        ``spare`` level if ``max`` permits.  When processes complete requests
        and turn idle, Unit terminates extra ones after a timeout.

        The default value is 0.  The value of ``spare`` cannot exceed ``max``.


    * - ``idle_timeout``
      - Number of seconds for Unit to wait before it terminates an extra idle
        process, when the count of idle processes exceeds ``spare``.

        The default value is 15.

If ``processes`` is omitted entirely, Unit creates 1 static process.  If empty
object is provided: ``"processes": {}``, dynamic behavior with default
parameter values is assumed.

In the following example, Unit tries to keep 5 idle processes, no more than 10
processes in total, and terminates extra idle processes after 20 seconds of
inactivity::

    {
        "max": 10,
        "spare": 5,
        "idle_timeout": 20
    }

.. _configuration-external:

Go/Node.js Applications
=======================

.. list-table::
    :header-rows: 1

    * - Object
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

Perl Application
================

.. list-table::
    :header-rows: 1

    * - Object
      - Description

    * - ``script``
      - PSGI script path.

Example::

    {
        "type": "perl",
        "script": "/www/bugtracker/app.psgi",
        "working_directory": "/www/bugtracker",
        "processes": 10,
        "user": "www",
        "group": "www"
    }

PHP Application
===============

.. list-table::
    :header-rows: 1

    * - Object
      - Description

    * - ``root``
      - Directory to search for PHP files.

    * - ``index``
      - Default launch file when the PHP file name is not specified in the URL.

    * - ``script`` (optional)
      - File that Unit runs for every URL, instead of searching for a file in
        the filesystem.  The location is relative to the root.

You can also customize :file:`php.ini` using the following options
(available in the :samp:`options` object):

.. list-table::
    :header-rows: 1

    * - Object
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
        "root": "/www/blogs/scripts",
        "index": "index.php",
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

Python Application
==================

.. list-table::
    :header-rows: 1

    * - Object
      - Description

    * - ``module``
      - WSGI module name.

    * - ``path`` (optional)
      - Path to search for the WSGI module file.

    * - ``home`` (optional)
      - Path to Python `virtual environment <https://packaging.python.org/
        tutorials/installing-packages/#creating-virtual-environments>`_
        for the application.  You can set this value relative to the
        ``working_directory`` of the application.

        Note: The Python version used by Unit to run the application is
        controlled by the ``type`` of the application.  Unit doesn't use
        command line Python interpreter within the virtual environment due to
        performance considerations.

Example::

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

Ruby Application
==================

.. list-table::
    :header-rows: 1

    * - Object
      - Description

    * - ``script``
      - Rack script path.

Example::

    {
        "type": "ruby",
        "processes": 5,
        "user": "www",
        "group": "www",
        "script": "/www/cms/config.ru"
    }

Access log
**********

To configure access logging, use the ``access_log`` parameter in a configuration
object to specify the path to the log file.

In the example below, all requests will be logged to **/var/log/access.log**:

.. code-block:: none

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

SSL/TLS and Certificates
************************

To set up SSL/TLS access for your application, upload a :file:`.pem` file
containing your certificate chain and private key to Unit.  Next, reference the
uploaded bundle in the listener's configuration.  After that, the listener's
application becomes accessible via SSL/TLS.

First, create a :file:`.pem` file with your certificate chain and private key:

.. code-block:: none

    # cat cert.pem ca.pem key.pem > bundle.pem

.. note::

    Usually, your website's certificate (optionally followed by the
    intermediate CA certificate) is enough to build a certificate chain.  If
    you add more certificates to your chain, order them leaf to root.

Upload the resulting file to Unit's certificate storage under a suitable name:

.. code-block:: none

    # curl -X PUT --data-binary @bundle.pem 127.1:8443/certificates/<bundle>

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

    .. code-block:: none

     # curl -X GET 127.1:8443/certificates/<bundle>/chain/0/
     # curl -X GET 127.1:8443/certificates/<bundle>/chain/0/subject/alt_names/0/

Next, add a :samp:`tls` object to your listener configuration, referencing the
uploaded bundle's name in :samp:`certificate`:

.. code-block:: json

    {
        "listeners": {
            "127.0.0.1:8080": {
                "application": "wsgi-app",
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
                    "application": "wsgi-app",
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

.. code-block:: none

    # curl -v https://127.0.0.1:8080
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

.. code-block:: none

    # curl -X DELETE 127.1:8443/certificates/<bundle>

        {
            "success": "Certificate deleted."
        }

.. note::

    You can't delete certificate bundles still referenced in your
    configuration, overwrite existing bundles using :samp:`PUT`, or (obviously)
    delete non-existent ones.

Happy SSLing!

Full Example
************

::

    {
        "listeners": {
            "*:8300": {
                "application": "blogs"
            },

            "*:8400": {
                "application": "wiki"
            },

            "*:8500": {
                "application": "go_chat_app"
            },

            "127.0.0.1:8600": {
                "application": "bugtracker"
            },

            "127.0.0.1:8601": {
                "application": "cms"
            }
        },

        "applications": {
            "blogs": {
                "type": "php",
                "processes": 20,
                "root": "/www/blogs/scripts",
                "user": "www-blogs",
                "group": "www-blogs",
                "index": "index.php"
            },

            "wiki": {
                "type": "python",
                "processes": 10,
                "user": "www-wiki",
                "group": "www-wiki",
                "path": "/www/wiki",
                "module": "wsgi"
            },

            "go_chat_app": {
                "type": "go",
                "user": "www-chat",
                "group": "www-chat",
                "working_directory": "/www/chat",
                "executable": "bin/chat_app"
            },

            "bugtracker": {
                "type": "perl",
                "processes": 3,
                "user": "www",
                "group": "www",
                "working_directory": "/www/bugtracker",
                "script": "app.psgi"
            },

            "cms": {
                "type": "ruby",
                "processes": 5,
                "user": "www",
                "group": "www",
                "script": "/www/cms/config.ru"
            }
        },

        "access_log": "/var/log/access.log"
    }
