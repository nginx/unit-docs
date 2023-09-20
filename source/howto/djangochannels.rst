.. |app| replace:: Django Channels
.. |mod| replace:: Python 3.6+

###############
Django Channels
###############

To run Django apps using the |app| `framework
<https://channels.readthedocs.io/en/stable/>`__ with Unit:

#. .. include:: ../include/howto_install_unit.rst

#. Install and configure the Django 3.0+ `framework
   <https://www.djangoproject.com>`__.  The official docs `recommend
   <https://docs.djangoproject.com/en/stable/topics/install/#installing-an-official-release-with-pip>`_
   setting up a virtual environment; if you do, list it as :samp:`home` when
   configuring Unit later.  Here, it's :samp:`/path/to/venv/`.

#. Install |app| in your virtual environment:

    .. code-block:: console

       $ cd :nxt_ph:`/path/to/venv/ <Path to the virtual environment; use a real path in your configuration>`
       $ source bin/activate
       $ pip install channels
       $ deactivate

#. Create a Django project.  Here, we'll use the `tutorial chat app
   <https://channels.readthedocs.io/en/stable/tutorial/part_1.html#tutorial-part-1-basic-setup>`_,
   installing it at :samp:`/path/to/app/`; use a real path in your
   configuration.  The following steps assume your project uses `basic
   directory structure
   <https://docs.djangoproject.com/en/stable/ref/django-admin/#django-admin-startproject>`_:

   .. code-block:: none

      :nxt_ph:`/path/to/app/ <Project directory>`
      |-- manage.py
      |-- :nxt_hint:`chat/ <Individual app directory>`
      |   |-- ...
      |-- :nxt_hint:`mysite/ <Project subdirectory>`
      |   |-- ...
      |   `-- :nxt_hint:`asgi.py <ASGI application module>`
      `-- :nxt_hint:`static/ <Static files subdirectory>`

#. .. include:: ../include/howto_change_ownership.rst

#. Integrate |app| into your project according to the official `Channels guide
   <https://channels.readthedocs.io/en/stable/tutorial/part_1.html#integrate-the-channels-library>`_.

#. Next, create the |app| :ref:`configuration <configuration-python>` for
   Unit.  Here, the :file:`/path/to/app/` directory is stored in the
   :samp:`path` option; the virtual environment is :samp:`home`; the ASGI
   module in the :file:`mysite/` subdirectory is `imported
   <https://docs.python.org/3/reference/import.html>`_ via :samp:`module`.  If
   you reorder your directories, :ref:`set up <configuration-python>`
   :samp:`path`, :samp:`home`, and :samp:`module` accordingly.

   You can also set up some environment variables that your project relies on,
   using the :samp:`environment` option.  Finally, if your project uses
   Django's `static files
   <https://docs.djangoproject.com/en/stable/howto/static-files/>`_, optionally
   add a :ref:`route <configuration-routes>` to :ref:`serve
   <configuration-static>` them with Unit.

   Here's an example (use real values for :samp:`share`, :samp:`path`,
   :samp:`environment`, :samp:`module`, and :samp:`home`):

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
                      ":nxt_hint:`share <Serves static files>`": ":nxt_ph:`/path/to/app <Thus, URIs starting with /static/ are served from /path/to/app/static/; use a real path in your configuration>`$uri"
                  }
              },
              {
                  "action": {
                      "pass": "applications/djangochannels"
                  }
              }
          ],

          "applications": {
              "djangochannels": {
                  "type": "python :nxt_ph:`3.X <Must match language module version and virtual environment version>`",
                  "path": ":nxt_ph:`/path/to/app/ <Project directory; use a real path in your configuration>`",
                  "home": ":nxt_ph:`/path/to/venv/ <Virtual environment directory; use a real path in your configuration>`",
                  "module": ":nxt_ph:`mysite.asgi <Note the qualified name of the ASGI module; use a real site directory name in your configuration>`",
                  ":nxt_hint:`environment <App-specific environment variables>`": {
                      "DJANGO_SETTINGS_MODULE": "mysite.settings"
                  }
              }
          }
      }

#. .. include:: ../include/howto_upload_config.rst

   After a successful update, your project and apps (here, a chat) run on
   the listener's IP address and port:

   .. image:: ../images/djangochannels.png
      :width: 100%
      :alt: Django Channels on Unit - Tutorial App Screen
