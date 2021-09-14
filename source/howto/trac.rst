.. |app| replace:: Trac
.. |mod| replace:: Python 2

####
Trac
####

.. warning::

  So far, Unit doesn't support handling the :samp:`REMOTE_USER` headers
  directly, so authentication should be implemented via external means.  For
  example, consider using `trac-oidc <https://pypi.org/project/trac-oidc/>`_ or
  `OAuth2Plugin <https://trac-hacks.org/wiki/OAuth2Plugin>`_.

To run the `Trac <https://trac.edgewall.org>`_ issue tracking system using
Unit:

#. .. include:: ../include/howto_install_unit.rst

   .. note::

      As of now, Trac `doesn't fully support
      <https://trac.edgewall.org/ticket/12130>`_ Python 3.  Mind that Python 2
      is officially deprecated.

#. Prepare and activate a `virtual environment
   <https://virtualenv.pypa.io/en/latest/>`_ to contain your installation
   (assuming :program:`virtualenv` is installed):

   .. code-block:: console

      $ mkdir /path/to/app/
      $ cd /path/to/app/
      $ virtualenv env
      $ source env/bin/activate

#. Next, `install Trac <https://trac.edgewall.org/wiki/TracInstall>`_ and its
   optional dependencies, then initialize a `Trac environment
   <https://trac.edgewall.org/wiki/TracEnvironment>`_ and deploy static files:

   .. code-block:: console

      (env) $ pip install Trac
      (env) $ pip install babel docutils genshi \
                          pygments pytz textile             # optional dependencies
      (env) $ mkdir static/                                 # will store Trac's /chrome/ tree
      (env) $ mkdir trac_env/
      (env) $ trac-admin trac_env/ initenv                  # initialize Trac environment
      (env) $ trac-admin trac_env/ deploy static/           # extract Trac's static files
      (env) $ mv static/htdocs static/chrome                # align static file paths
      (env) $ rm -rf static/cgi-bin/                        # remove unneeded files

#. Unit :ref:`uses WSGI <configuration-python>` to run Python apps, so a
   `wrapper <https://trac.edgewall.org/wiki/1.3/TracModWSGI#Averybasicscript>`_
   script is required to run Trac as a Unit app; let's save it as
   :file:`/path/to/app/trac_wsgi.py`.  Here, the :samp:`application` callable
   serves as the entry point for the app:

    .. code-block:: python

       import trac.web.main

       def application(environ, start_response):
           environ["trac.locale"] = "en_US.UTF8"
           return trac.web.main.dispatch_request(environ, start_response)

#. .. include:: ../include/howto_change_ownership.rst

#. Next, :ref:`prepare <configuration-python>` the |app| configuration for Unit
   (use real values for :samp:`share`, :samp:`path`, :samp:`home`,
   :samp:`module`, :samp:`TRAC_ENV`, and :samp:`PYTHON_EGG_CACHE`):

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
                      "uri": "/chrome/*"
                  },
                  "action": {
                      ":nxt_hint:`share <Serves matching static files>`": ":nxt_ph:`/path/to/app/static/ <Use a real path in your configuration>`"
                  }
              },
              {
                  "action": {
                      "pass": "applications/trac"
                  }
              }
          ],

          "applications": {
              "trac": {
                  "type": "python 2",
                  "path": ":nxt_ph:`/path/to/app/ <Path to the WSGI file>`",
                  "home": ":nxt_ph:`/path/to/app/env/ <Path to the virtual environment where Trac is installed>`",
                  "module": ":nxt_hint:`trac_wsgi <WSGI wrapper file basename from Step 4>`",
                  "environment": {
                      "TRAC_ENV": ":nxt_ph:`/path/to/app/trac_env/ <Path to the Trac environment>`",
                      "PYTHON_EGG_CACHE": ":nxt_ph:`/path/to/app/trac_env/eggs/ <Path to the Python egg cache for Trac>`"
                  }
              }
          }
      }

   The route serves requests for static files in Trac's :file:`/chrome/`
   `hierarchy <https://trac.edgewall.org/wiki/TracDev/TracURLs>`_ from the
   :file:`static/` directory.

#. .. include:: ../include/howto_upload_config.rst

   After a successful update, |app| should be available on the listener’s IP
   address and port:

   .. image:: ../images/trac.png
      :width: 100%
      :alt: Trac on Unit - New Ticket Screen
