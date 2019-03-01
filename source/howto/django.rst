###########
Django Apps
###########

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

      project/
      |-- manage.py
      |-- app1/
      |   |-- ...
      |-- app2/
      |   |-- ...
      `-- project/
          |-- ...
          `-- wsgi.py

   Edit the JSON file, adding a :ref:`listener <configuration-listeners>` in
   :samp:`listeners` and pointing it to your project's :file:`wsgi.py` file in
   :samp:`applications`.  Your project and apps will run on the listener's IP
   and port at their respective URL paths.  If you use a `virtual environment
   <https://docs.djangoproject.com/en/stable/intro/contributing/#getting-a-copy-of-django-s-development-version>`_
   for your project, reference it as :samp:`home` within your app definition
   object.

   .. code-block:: json

      {
          "listeners": {
              "127.0.0.1:8080": {
                  "action": {
                      "pass": "applications/django_project"
                  }
              }
          },

          "applications": {
              "django_project": {
                  "type": "python 3",
                  "path": "/home/django/project/",
                  "home": "/home/django/venv/",
                  "module": "project.wsgi"
              }
          }
      }

   Here, the top-level :file:`project` directory becomes :samp:`path`; its
   child :file:`project` and the :file:`wsgi.py` in it are `imported
   <https://docs.python.org/3/reference/import.html>`_ via :samp:`module`.  If
   you reorder your directories, :ref:`set up <configuration-python>`
   :samp:`path` and :samp:`module` accordingly.

#. Upload the updated configuration:

   .. code-block:: console

      # curl -X PUT --data-binary @config.json --unix-socket \
             /path/to/control.unit.sock http://localhost/config

   After a successful update, your project and apps should be available
   on the listener's IP address and port:

   .. code-block:: console

      # curl 127.0.0.1:8080/admin/
      # curl 127.0.0.1:8080/app1/
