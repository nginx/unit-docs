.. |app| replace:: Flask
.. |mod| replace:: Python 3
.. |app-pip-package| replace:: Flask
.. |app-pip-link| replace:: PIP package
.. _app-pip-link: https://flask.palletsprojects.com/en/1.1.x/installation/#install-flask

#####
Flask
#####

To run apps built with the `Flask
<https://flask.palletsprojects.com/en/1.1.x/>`_ web framework using Unit:

#. .. include:: ../include/howto_install_unit.rst

#. .. include:: ../include/howto_install_venv.rst

#. Let's try a basic version of the `quickstart app
   <https://flask.palletsprojects.com/en/1.1.x/quickstart/>`_,
   saving it as **/path/to/app/wsgi.py**:

   .. code-block:: python

      from flask import Flask
      :nxt_hint:`app <Callable name used in Unit's condfiguration>` = Flask(__name__)

      @app.route("/")
      def hello_world():
          return "Hello, World!"

#. .. include:: ../include/howto_change_ownership.rst

#. Next, :ref:`prepare <configuration-python>` the |app| configuration for
   Unit (use real values for **type**, **home**, and **path**):

   .. code-block:: json

      {
          "listeners": {
              "*:80": {
                  "pass": "applications/flask"
              }
          },

          "applications": {
              "flask": {
                  "type": "python 3.:nxt_ph:`Y <Must match language module version and virtual environment version>`",
                  "path": ":nxt_ph:`/path/to/app/ <Path to the WSGI module>`",
                  "home": ":nxt_ph:`/path/to/app/venv/ <Path to the virtual environment, if any>`",
                  "module": ":nxt_hint:`wsgi <WSGI module filename with extension omitted>`",
                  "callable": ":nxt_hint:`app <Name of the callable in the module to run>`"
              }
          }
      }

#. .. include:: ../include/howto_upload_config.rst

   After a successful update, your app should be available on the listener’s IP
   address and port:

   .. code-block:: console

      $ curl http://localhost

            Hello, World!
