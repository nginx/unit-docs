######
Django
######

To run your Django projects and apps in Unit:

#. :ref:`Install Unit <installation-precomp-pkgs>` with the appropriate Python
   language module version.

#. If you haven't already done so, `create your Django project and apps
   <https://docs.djangoproject.com/en/stable/intro/overview/>`_ where you
   usually store them.

#. .. include:: ../include/get-config.rst

   This creates a JSON file with Unit's current settings; update it with your
   project settings as follows.

   Suppose you use a `basic directory structure
   <https://docs.djangoproject.com/en/stable/ref/django-admin/#django-admin-startproject>`_
   for your Django project:

   .. code-block:: none

      /home/django/project/
      |-- manage.py
      |-- app1/
      |   |-- ...
      |-- app2/
      |   |-- ...
      `-- project/
          |-- ...
          |-- asgi.py
          `-- wsgi.py

   Edit the JSON, adding a :ref:`listener <configuration-listeners>` entry to
   point to a Unit :ref:`app <configuration-applications>` with your
   *project*'s WSGI or ASGI module; the project and its apps will run on the
   listener's IP and port.  If you use a `virtual environment
   <https://docs.djangoproject.com/en/stable/intro/contributing/#getting-a-copy-of-django-s-development-version>`_,
   reference it as :samp:`home`.  Also, you can set up some environment
   variables that your project relies on.  Finally, if your project uses
   Django's `static files
   <https://docs.djangoproject.com/en/stable/howto/static-files/>`_, optionally
   add a :ref:`route <configuration-routes>` to :ref:`serve
   <configuration-static>` them with Unit.

   .. tabs::
      :prefix: django

      .. tab:: WSGI

         Mind the :samp:`module` setting that references the
         :file:`project/wsgi.py` file.

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
                            "share": ":nxt_term:`/home/django/ <Thus, URIs starting with /static/ are served from /home/django/static/>`"
                        }
                    },
                    {
                        "action": {
                            "pass": "applications/django_project"
                        }
                    }
                ],

                "applications": {
                    "django_project": {
                        "type": "python 3",
                        "path": ":nxt_term:`/home/django/project/ <Project directory>`",
                        "home": ":nxt_term:`/home/django/venv/ <Virtual environment directory>`",
                        "module": ":nxt_term:`project.wsgi <Note the qualified name of the WSGI module>`",
                        "environment": {
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

         Mind the :samp:`module` setting that references the
         :file:`project/asgi.py` file.

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
                            "share": ":nxt_term:`/home/django/ <Thus, URIs starting with /static/ are served from /home/django/static/>`"
                        }
                    },
                    {
                        "action": {
                            "pass": "applications/django_project"
                        }
                    }
                ],

                "applications": {
                    "django_project": {
                        "type": "python 3",
                        "path": ":nxt_term:`/home/django/project/ <Project directory>`",
                        "home": ":nxt_term:`/home/django/venv/ <Virtual environment directory>`",
                        "module": ":nxt_term:`project.asgi <Note the qualified name of the ASGI module>`",
                        "environment": {
                            "DJANGO_SETTINGS_MODULE": "project.settings",
                            "DB_ENGINE": "django.db.backends.postgresql",
                            "DB_NAME": "project",
                            "DB_HOST": "127.0.0.1",
                            "DB_PORT": "5432"
                        }
                    }
                }
            }

   Here, the top-level :file:`project` directory becomes :samp:`path`; its
   child :file:`project` and the WSGI or ASGI module in it are `imported
   <https://docs.python.org/3/reference/import.html>`_ via :samp:`module`.  If
   you reorder your directories, :ref:`set up <configuration-python>`
   :samp:`path` and :samp:`module` accordingly.

#. Upload the updated configuration:

   .. code-block:: console

      # curl -X PUT --data-binary @config.json --unix-socket \
             /path/to/control.unit.sock http://localhost/config

   After a successful update, your project and apps should be available on the
   listener's IP address and port:

   .. code-block:: console

      $ curl localhost/admin/
      $ curl localhost/app1/
