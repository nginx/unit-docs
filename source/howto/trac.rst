####
Trac
####


.. warning::

  So far, Unit doesn't support handling the :samp:`REMOTE_USER` headers
  directly, so authentication should be implemented via external means.  For
  example, consider using `trac-oidc <https://pypi.org/project/trac-oidc/>`_ or
  `OAuth2Plugin <https://trac-hacks.org/wiki/OAuth2Plugin>`_.

To install and run the `Trac <https://trac.edgewall.org/>`_ issue tracking
system using Unit:

#. Install :ref:`Unit <installation-precomp-pkgs>` with a Python 2 language
   module.

   .. note::

      As of now, Trac `doesn't fully support
      <https://trac.edgewall.org/ticket/12130>`_ Python 3.  Mind that Python 2
      is officially deprecated.

#. Prepare and activate a `virtual environment
   <https://virtualenv.pypa.io/en/latest/>`_ to contain your installation
   (assuming :program:`virtualenv` is installed):

   .. code-block:: console

      $ mkdir /path/to/trac/
      $ cd /path/to/trac
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
      (env) # chown -R trac_user:trac_group /path/to/trac/

#. Unit :ref:`uses WSGI <configuration-python>` to run Python apps, so a
   `wrapper <https://trac.edgewall.org/wiki/1.3/TracModWSGI#Averybasicscript>`_
   script is required to run Trac as a Unit app; let's save it as
   :file:`/path/to/trac/trac_wsgi.py`.  Here, the :samp:`application` callable
   serves as the entry point for the app:

    .. code-block:: python

       import trac.web.main

       def application(environ, start_response):
           environ["trac.locale"] = "en_US.UTF8"
           return trac.web.main.dispatch_request(environ, start_response)

#. Finally, prepare and upload the :ref:`configuration <configuration-python>`
   to Unit (note the use of :samp:`home` and :samp:`environment`):

   .. code-block:: json

      {
          "listeners": {
              "*:80": {
                  "pass": "routes/trac"
              }
          },

          "routes": {
              "trac": [
                  {
                      "match": {
                          "uri": "/chrome/*"
                      },
                      "action": {
                          "share": "/path/to/trac/static/"
                      }
                  },
                  {
                      "action": {
                          "pass": "applications/trac"
                      }
                  }
              ]
          },

          "applications": {
              "trac": {
                  "type": "python 2",
                  "path": ":nxt_term:`/path/to/trac/ <Path to the WSGI file>`",
                  "home": ":nxt_term:`/path/to/trac/env/ <Path to the virtual environment where Trac is installed>`",
                  "user": "trac_user",
                  "module": ":nxt_term:`trac_wsgi <WSGI file basename>`",
                  "environment": {
                      "TRAC_ENV": ":nxt_term:`/path/to/trac/trac_env/ <Path to the Trac environment>`",
                      "PYTHON_EGG_CACHE": ":nxt_term:`/path/to/trac/trac_env/eggs/ <Path to the Python egg cache for Trac>`"
                  }
              }
          }
      }

   The route serves requests for static files in Trac's :file:`/chrome/`
   `hierarchy <https://trac.edgewall.org/wiki/TracDev/TracURLs>`_ from the
   :file:`static/` directory.

#. Upload the updated configuration.  Assuming the config above is saved as
   :file:`trac.json`:

   .. code-block:: console

      # curl -X PUT --data-binary @trac.json --unix-socket \
             /var/run/control.unit.sock http://localhost/config

   After a successful update, Trac should be available on the listener’s IP
   address and port:

   .. image:: ../images/trac.png
      :width: 100%
      :alt: Trac on Unit - New Ticket Screen
