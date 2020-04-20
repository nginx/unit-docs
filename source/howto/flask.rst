:orphan:

#####
Flask
#####

To run your Flask apps in Unit:

#. :ref:`Install Unit <installation-precomp-pkgs>` with the appropriate Python
   language module version.

#. If you haven’t already done so, create your `Flask app
   <http://flask.pocoo.org/docs/1.0/quickstart/>`_.

#. .. include:: ../include/get-config.rst

   This creates a JSON file with Unit's current settings.  Edit the file,
   adding a :ref:`listener <configuration-listeners>` entry to point to a Unit
   :ref:`app <configuration-applications>` that references your application’s
   WSGI module as :samp:`module` and `virtual environment
   <http://flask.pocoo.org/docs/1.0/installation/#virtual-environments>`_ as
   :samp:`home`:

   .. code-block:: json

      {
          "listeners": {
              "*:8080": {
                  "pass": "applications/flask_app"
              }
          },

          "applications": {
              "flask_app": {
                  "type": "python 3",
                  "path": "/home/flask/flask_app/",
                  "home": "/home/flask/venv/",
                  "module": "wsgi"
              }
          }
      }

   .. note::

      Mind that Unit will look for an :samp:`application` callable in the WSGI
      module to run the app.

   For details, see :ref:`Python app settings <configuration-python>`.

#. Upload the updated configuration:

   .. code-block:: console

      # curl -X PUT --data-binary @config.json --unix-socket \
             /path/to/control.unit.sock http://localhost/config

   After a successful update, your app should be available on the
   listener's IP address and port:

   .. code-block:: console

      $ curl http://127.0.0.1:8080/
