
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
a ``PUT`` request. To reduce errors, it makes sense to write the JSON data in a
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

Listener Objects
****************

.. list-table::
    :header-rows: 1

    * - Object
      - Description

    * - ``application``
      - Application name.

Example::

    {
        "application": "blogs"
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
      - Type of the application: ``go``, ``perl``, ``php``, ``python``,
        or ``ruby``.
        You can also define a specific version number of the interpreter
        that will be used to run the application.
        Valid version formats are ``MAJOR``, ``MAJOR.MINOR``, and
        ``MAJOR.MINOR.REVISION``.
        When one of the first two formats is used, Unit will use
        the latest ``MAJOR.MINOR.REVISION`` version found in existing modules.

    * - ``processes`` (optional)
      - Number of application processes.
        By default 1 process is used.
        Use the ``max`` and ``spare`` options to take advantage of
        the dynamic processes management feature.

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
        "processes": {
            "max": 3,
            "spare": 1
        },
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

Depending on the ``type`` of the application, you may need to configure
a number of additional options.
In the example above, Python-specific options ``path`` and ``module`` are used.

Go Application
==============

.. list-table::
    :header-rows: 1

    * - Object
      - Description

    * - ``executable``
      - Path to compiled application, absolute or relative
        to ``working_directory``.

    * - ``arguments`` (optional)
      - Command line arguments to be passed to the application.
        The example below is equivalent to
        ``/www/chat/bin/chat_app --tmp-files /tmp/go-cache``

Example::

    {
        "type": "go",
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

You can also customize php.ini using the following options
(available in the ``options`` object):

.. list-table::
    :header-rows: 1

    * - Object
      - Description

    * - ``file`` (optional)
      - Path to the php.ini file.

    * - ``admin`` and ``user`` (optional)
      - Hold the php.ini configuration options.
        Note that the configuration values must be defined as strings,
        even when they represent numbers.
        The ``user`` object allows ``ini_set()`` to override the options
        from within the application.

Example::

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

Example::

    {
        "type": "python",
        "processes": 10,
        "path": "/www/store/cart",
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
