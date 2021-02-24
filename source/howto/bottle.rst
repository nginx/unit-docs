.. include:: ../include/replace.rst

.. |app| replace:: Bottle
.. |mod| replace:: Python 2.7+
.. |app-pip-package| replace:: bottle
.. |app-pip-link| replace:: PIP package
.. _app-pip-link: https://bottlepy.org/docs/dev/tutorial.html#installation

######
Bottle
######

To run apps built with the `Bottle <https://bottlepy.org/docs/dev/>`_ web
framework using Unit:

#. .. include:: ../include/howto_install_unit.rst

#. Create a virtual environment to install |app|'s |app-pip-link|_, for
   instance:

   .. subs-code-block:: console

      $ cd /path/to/app/
      $ :nxt_hint:`python --version <Make sure your virtual environment version matches the module version>`
            Python x.y.z
      $ python -m venv venv
      $ source venv/bin/activate
      $ pip install |app-pip-package|
      $ deactivate

   .. warning::

      Create your virtual environment with a Python version that matches the
      language module from Step |_| 1 up to the minor number (:samp:`x.y` in
      this example).  Also, the app :samp:`type` in Step |_| 5 must
      :ref:`resolve <configuration-apps-common>` to a similarly matching
      version; Unit doesn't infer it from the environment.

#. Let's try an updated version of the `quickstart app
   <https://bottlepy.org/docs/dev/tutorial.html#the-default-application>`_,
   saving it as :file:`/path/to/app/wsgi.py`:

   .. code-block:: python

      from bottle import Bottle, template

      :nxt_hint:`app <Callable name used in Unit's configuration>` = Bottle()

      @app.route('/hello/<name>')
      def hello(name):
          return template('Hello, {{name}}!', name=name)

      # run(app, host='localhost', port=8080)

   Note that we’ve dropped the server code.

#. .. include:: ../include/howto_change_ownership.rst

#. Next, :ref:`prepare <configuration-python>` the |app| configuration for
   Unit:

   .. code-block:: json

      {
          "listeners": {
              "*:80": {
                  "pass": "applications/bottle"
              }
          },

          "applications": {
              "bottle": {
                  "type": ":nxt_hint:`python x.y <Must match language module version and virtual environment version>`",
                  "path": ":nxt_hint:`/path/to/app/ <Path to the WSGI module>`",
                  "home": ":nxt_hint:`/path/to/app/venv/ <Path to the virtual environment, if any>`",
                  "module": ":nxt_hint:`wsgi <WSGI module filename with extension omitted>`",
                  "callable": ":nxt_hint:`app <Name of the callable in the module to run>`"
              }
          }
      }

#. .. include:: ../include/howto_upload_config.rst

   After a successful update, your app should be available on the listener’s IP
   address and port:

   .. code-block:: console

      $ curl http://localhost/hello/Unit

            Hello, Unit!
