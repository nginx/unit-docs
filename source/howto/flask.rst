#####
Flask
#####

To run your Flask apps in Unit:

#. :ref:`Install Unit <installation-precomp-pkgs>` with the appropriate Python
   language module version.

#. If you haven’t already done so, create your `Flask app
   <https://flask.palletsprojects.com/en/1.1.x/quickstart/>`_, for example:

   .. code-block:: python

      from flask import Flask
      :nxt_term:`application <Callable name expected by Unit>` = Flask(__name__)

      @application.route("/")
      def hello_world():
          return "Hello, World!"

   Let's assume it's saved as :file:`/path/to/flask/flask_app/wsgi.py`.

   .. note::

      Mind that Unit will look for an :samp:`application` callable in the WSGI
      module.

#. .. include:: ../include/get-config.rst

   This creates a JSON file with Unit's current settings.  Edit the file,
   adding a :ref:`listener <configuration-listeners>` entry to point to a Unit
   :ref:`app <configuration-applications>` that references your application’s
   WSGI module as :samp:`module` and your `virtual environment
   <https://flask.palletsprojects.com/en/1.1.x/installation/#virtual-environments>`_
   as :samp:`home`:

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
                  "path": ":nxt_term:`/path/to/flask/flask_app/ <Path to the WSGI module>`",
                  "home": ":nxt_term:`/path/to/flask/venv/ <Path to the virtual environment, if any>`",
                  "module": ":nxt_term:`wsgi <WSGI module filename with extension omitted>`"
              }
          }
      }

   For details, see :ref:`Python app settings <configuration-python>`.

#. Upload the updated configuration:

   .. code-block:: console

      # curl -X PUT --data-binary @config.json --unix-socket \
             /path/to/control.unit.sock http://localhost/config

   After a successful update, your app should be available on the
   listener's IP address and port:

   .. code-block:: console

      $ curl http://127.0.0.1:8080/
