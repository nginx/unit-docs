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

      $ cd :nxt_ph:`/path/to/app/ <Path to the application directory; use a real path in your configuration>`
      $ :nxt_hint:`python --version <Make sure your virtual environment version matches the module version>`
            Python :nxt_hint:`X.Y.Z <Major version, minor version, and revision number>`
      $ python -m venv :nxt_hint:`venv <Arbitrary name of the virtual environment>`
      $ source :nxt_hint:`venv <Name of the virtual environment from the previous command>`/bin/activate
      $ pip install |app-pip-package|
      $ deactivate

   .. warning::

      Create your virtual environment with a Python version that matches the
      language module from Step |_| 1 up to the minor number (**X.Y** in
      this example).  Also, the app **type** in Step |_| 5 must
      :ref:`resolve <configuration-apps-common>` to a similarly matching
      version; Unit doesn't infer it from the environment.

#. Let's try an updated version of the `quickstart app
   <https://bottlepy.org/docs/dev/tutorial.html#the-default-application>`_,
   saving it as **/path/to/app/wsgi.py**:

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
   Unit (use real values for **type**, **home**, and **path**):

   .. code-block:: json

      {
          "listeners": {
              "*:80": {
                  "pass": "applications/bottle"
              }
          },

          "applications": {
              "bottle": {
                  "type": "python :nxt_ph:`X.Y <Must match language module version and virtual environment version>`",
                  "path": ":nxt_ph:`/path/to/app/ <Path to the WSGI module; use a real path in your configuration>`",
                  "home": ":nxt_ph:`/path/to/app/venv/ <Path to the virtual environment, if any; use a real path in your configuration>`",
                  "module": ":nxt_hint:`wsgi <WSGI module basename with extension omitted>`",
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
