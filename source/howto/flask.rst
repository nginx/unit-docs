.. |app| replace:: Flask
.. |mod| replace:: Python 3

#####
Flask
#####

To run apps built with the `Flask
<https://flask.palletsprojects.com/en/1.1.x/>`_ web framework using Unit:

#. .. include:: ../include/howto_install_unit.rst

#. Create a virtual environment to install |app|'s `PIP package
   <https://flask.palletsprojects.com/en/1.1.x/installation/#install-flask>`_:

   .. code-block:: console

      $ cd /path/to/app/
      $ python3 -m venv venv
      $ venv/bin/activate
      $ pip install Flask
      $ deactivate

#. Let's try a basic version of the `quickstart app
   <https://flask.palletsprojects.com/en/1.1.x/quickstart/>`_,
   saving it as :file:`/path/to/app/wsgi.py`:

   .. code-block:: python

      from flask import Flask
      :nxt_term:`application <Callable name expected by Unit>` = Flask(__name__)

      @application.route("/")
      def hello_world():
          return "Hello, World!"

#. .. include:: ../include/howto_change_ownership.rst

#. Next, :ref:`put together <configuration-php>` the |app| configuration for
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
                  "type": "python 3",
                  "user": ":nxt_term:`app_user <User and group values must have access to path and home directories>`",
                  "group": "app_group",
                  "path": ":nxt_term:`/path/to/app/ <Path to the WSGI module>`",
                  "home": ":nxt_term:`/path/to/app/venv/ <Path to the virtual environment, if any>`",
                  "module": ":nxt_term:`wsgi <WSGI module filename with extension omitted>`"
              }
          }
      }

#. .. include:: ../include/howto_upload_config.rst

#. After a successful update, your app should be available on the listener’s IP
   address and port:

   .. code-block:: console

      $ curl http://localhost

            Hello, World!
