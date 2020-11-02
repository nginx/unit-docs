.. |app| replace:: Responder
.. |mod| replace:: Python 3.6+

#########
Responder
#########

To run apps built with the `Responder
<https://responder.kennethreitz.org/en/latest/#>`_ web framework using Unit:

#. .. include:: ../include/howto_install_unit.rst

#. Create a virtual environment to install |app|'s `PIP package
   <https://responder.kennethreitz.org/en/latest/#installing-responder>`_:

   .. code-block:: console

      $ cd /path/to/app/
      $ python3 -m venv venv
      $ source venv/bin/activate
      $ pip install responder
      $ deactivate

#. Let's try a Unit-friendly version of a `tutorial app
   <https://responder.kennethreitz.org/en/latest/quickstart.html#declare-a-web-service>`_,
   saving it as :file:`/path/to/app/asgi.py`:

   .. code-block:: python

      import responder

      app = responder.API()

      @app.route("/")
      def hello_world(req, resp):
          resp.text = "Hello, World!"

      @app.route("/hello/{who}")
      def hello_to(req, resp, *, who):
          resp.text = f"Hello, {who}!"

   The :samp:`app.run()` call is omitted because :samp:`app` will be directly
   run by Unit as an ASGI `callable
   <https://github.com/taoufik07/responder/blob/103816e27ae928d42ed850190472480124ba90e3/responder/api.py#L360>`_.

#. .. include:: ../include/howto_change_ownership.rst

#. Next, :ref:`put together <configuration-python>` the |app| configuration for
   Unit:

   .. code-block:: json

      {
          "listeners": {
              "*:80": {
                  "pass": "applications/responder"
              }
          },

          "applications": {
              "responder": {
                  "type": "python 3",
                  "user": ":nxt_term:`app_user <User and group values must have access to path, home, and working_directory>`",
                  "group": "app_group",
                  "path": ":nxt_term:`/path/to/app/ <Path to the ASGI module>`",
                  "home": ":nxt_term:`/path/to/app/venv/ <Path to the virtual environment, if any>`",
                  "working_directory": ":nxt_term:`/path/to/app/ <Path to the directory where Responder creates static_dir and templates_dir>`",
                  "module": ":nxt_term:`asgi <ASGI module filename with extension omitted>`",
                  "callable": ":nxt_term:`app <Name of the callable in the module to run>`"
              }
          }
      }

#. .. include:: ../include/howto_upload_config.rst

#. After a successful update, your app should be available on the listener’s IP
   address and port:

   .. code-block:: console

      $ curl http://localhost

            Hello, World!

      $ curl http://localhost/hello/JohnDoe

            Hello, JohnDoe!

