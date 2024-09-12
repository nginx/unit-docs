.. |app| replace:: Responder
.. |mod| replace:: Python 3.6+
.. |app-pip-package| replace:: responder
.. |app-pip-link| replace:: PIP package
.. _app-pip-link: https://responder.kennethreitz.org/#installing-responder

#########
Responder
#########

To run apps built with the `Responder
<https://responder.kennethreitz.org/>`_ web framework using Unit:

#. .. include:: ../include/howto_install_unit.rst

#. .. include:: ../include/howto_install_venv.rst

#. Let's try a Unit-friendly version of a `tutorial app
   <https://responder.kennethreitz.org/quickstart.html#declare-a-web-service>`_,
   saving it as **/path/to/app/asgi.py**:

   .. code-block:: python

      import responder

      app = responder.API()

      @app.route("/")
      def hello_world(req, resp):
          resp.text = "Hello, World!"

      @app.route("/hello/{who}")
      def hello_to(req, resp, *, who):
          resp.text = f"Hello, {who}!"

   The **app.run()** call is omitted because **app** will be directly
   run by Unit as an ASGI `callable
   <https://github.com/kennethreitz/responder/blob/c6f3a7364cfa79805b0d51eea011fe34d9bd331a/responder/api.py#L501>`_.

#. .. include:: ../include/howto_change_ownership.rst

#. Next, :ref:`prepare <configuration-python>` the |app| configuration for
   Unit (use real values for **type**, **home**, and **path**):

   .. code-block:: json

      {
          "listeners": {
              "*:80": {
                  "pass": "applications/responder"
              }
          },

          "applications": {
              "responder": {
                  "type": "python 3.:nxt_ph:`Y <Must match language module version and virtual environment version>`",
                  "path": ":nxt_ph:`/path/to/app/ <Path to the ASGI module>`",
                  "home": ":nxt_ph:`/path/to/app/venv/ <Path to the virtual environment, if any>`",
                  "working_directory": ":nxt_ph:`/path/to/app/ <Path to the directory where Responder creates static_dir and templates_dir>`",
                  "module": ":nxt_hint:`asgi <ASGI module filename with extension omitted>`",
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


   .. code-block:: console

      $ curl http://localhost/hello/JohnDoe

            Hello, JohnDoe!

