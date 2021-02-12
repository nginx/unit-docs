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
   saving it as :file:`/path/to/app/wsgi.py`:

   .. code-block:: python

      from flask import Flask
      :nxt_hint:`application <Callable name expected by Unit>` = Flask(__name__)

      @application.route("/")
      def hello_world():
          return "Hello, World!"

#. .. include:: ../include/howto_change_ownership.rst

#. Next, :ref:`prepare <configuration-python>` the |app| configuration for
   Unit:

   .. code-block:: json

      {
          "listeners": {
              "*:80": {
                  "pass": "applications/flask"
              }
          },

          "applications": {
              "flask": {
                  "type": ":nxt_hint:`python 3.x <Must match language module version and virtual environment version>`",
                  "path": ":nxt_ph:`/path/to/app/ <Path to the WSGI module>`",
                  "home": ":nxt_ph:`/path/to/app/venv/ <Path to the virtual environment, if any>`",
                  "module": ":nxt_hint:`wsgi <WSGI module filename with extension omitted>`"
              }
          }
      }

#. .. include:: ../include/howto_upload_config.rst

   After a successful update, your app should be available on the listener’s IP
   address and port:

   .. code-block:: console

      $ curl http://localhost

            Hello, World!
