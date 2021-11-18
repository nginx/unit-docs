.. |app| replace:: Django
.. |mod| replace:: Python 3

######
Django
######

To run apps based on the |app| `framework <https://www.djangoproject.com>`__
using Unit:

#. .. include:: ../include/howto_install_unit.rst

#. Install and configure the |app| `framework
   <https://www.djangoproject.com>`__.  The official docs `recommend
   <https://docs.djangoproject.com/en/stable/topics/install/#installing-an-official-release-with-pip>`_
   setting up a virtual environment; if you do, list it as :samp:`home` when
   configuring Unit later.  Here, it's :samp:`/path/to/venv/`.

#. Create a |app| `project
   <https://docs.djangoproject.com/en/stable/intro/tutorial01/>`_.  Here, we
   install it at :samp:`/path/to/app/`; use a real path in your configuration.
   The following steps assume your project uses `basic directory structure
   <https://docs.djangoproject.com/en/stable/ref/django-admin/#django-admin-startproject>`_:

   .. code-block:: none

      :nxt_ph:`/path/to/app/ <Project directory>`
      |-- manage.py
      |-- :nxt_hint:`django_app1/ <Individual app directory>`
      |   |-- ...
      |-- :nxt_hint:`django_app2/ <Individual app directory>`
      |   |-- ...
      |-- :nxt_hint:`project/ <Project subdirectory>`
      |   |-- ...
      |   |-- :nxt_hint:`asgi.py <ASGI application module>`
      |   `-- :nxt_hint:`wsgi.py <WSGI application module>`
      `-- :nxt_hint:`static/ <Static files subdirectory>`

#. .. include:: ../include/howto_change_ownership.rst

#. Next, prepare the |app| :ref:`configuration <configuration-python>` for
   Unit.  Here, the :file:`/path/to/app/` directory is stored in the
   :samp:`path` option; the virtual environment is :samp:`home`; the WSGI or
   ASGI module in the :file:`project/` subdirectory is `imported
   <https://docs.python.org/3/reference/import.html>`_ via :samp:`module`.  If
   you reorder your directories, :ref:`set up <configuration-python>`
   :samp:`path`, :samp:`home`, and :samp:`module` accordingly.

   You can also set up some environment variables that your project relies on,
   using the :samp:`environment` option.  Finally, if your project uses |app|'s
   `static files
   <https://docs.djangoproject.com/en/stable/howto/static-files/>`_, optionally
   add a :ref:`route <configuration-routes>` to :ref:`serve
   <configuration-static>` them with Unit.

   Here's an example (use real values for :samp:`share`, :samp:`path`,
   :samp:`environment`, :samp:`module`, and :samp:`home`):

   .. tabs::
      :prefix: interface

      .. tab:: WSGI

         .. code-block:: json

            {
                "listeners": {
                    "*:80": {
                        "pass": "routes"
                    }
                },

                "routes": [
                    {
                        "match": {
                            "uri": "/static/*"
                        },

                        "action": {
                            ":nxt_hint:`share <Serves static files>`": ":nxt_ph:`/path/to/app <Thus, URIs starting with /static/ are served from /path/to/app/static/>`$uri"
                        }
                    },
                    {
                        "action": {
                            "pass": "applications/django"
                        }
                    }
                ],

                "applications": {
                    "django": {
                        "type": "python :nxt_ph:`3.X <Must match language module version and virtual environment version>`",
                        "path": ":nxt_ph:`/path/to/app/ <Project directory; use a real path in your configuration>`",
                        "home": ":nxt_ph:`/path/to/venv/ <Virtual environment directory; use a real path in your configuration>`",
                        "module": ":nxt_ph:`project.wsgi <Note the qualified name of the WSGI module; use a real project directory name in your configuration>`",
                        ":nxt_hint:`environment <App-specific environment variables>`": {
                            "DJANGO_SETTINGS_MODULE": "project.settings",
                            "DB_ENGINE": "django.db.backends.postgresql",
                            "DB_NAME": "project",
                            "DB_HOST": "127.0.0.1",
                            "DB_PORT": "5432"
                        }
                    }
                }
            }

      .. tab:: ASGI

         .. note::

            ASGI requires Python 3.5+ and Django 3.0+.

         .. code-block:: json

            {
                "listeners": {
                    "*:80": {
                        "pass": "routes"
                    }
                },

                "routes": [
                    {
                        "match": {
                            "uri": "/static/*"
                        },

                        "action": {
                            ":nxt_hint:`share <Serves static files>`": ":nxt_ph:`/path/to/app <Thus, URIs starting with /static/ are served from /path/to/app/static/>`$uri"
                        }
                    },
                    {
                        "action": {
                            "pass": "applications/django"
                        }
                    }
                ],

                "applications": {
                    "django": {
                        "type": "python :nxt_ph:`3.X <Must match language module version and virtual environment version>`",
                        "path": ":nxt_ph:`/path/to/app/ <Project directory; use a real path in your configuration>`",
                        "home": ":nxt_ph:`/path/to/venv/ <Virtual environment directory; use a real path in your configuration>`",
                        "module": ":nxt_ph:`project.asgi <Note the qualified name of the ASGI module; use a real project directory name in your configuration>`",
                        ":nxt_hint:`environment <App-specific environment variables>`": {
                            "DJANGO_SETTINGS_MODULE": "project.settings",
                            "DB_ENGINE": "django.db.backends.postgresql",
                            "DB_NAME": "project",
                            "DB_HOST": "127.0.0.1",
                            "DB_PORT": "5432"
                        }
                    }
                }
            }

#. .. include:: ../include/howto_upload_config.rst

   After a successful update, your project and apps should be available on the
   listener's IP address and port:

   .. image:: ../images/django.png
      :width: 100%
      :alt: Django on Unit - Admin Login Screen
