.. |app| replace:: Quart
.. |mod| replace:: Python 3.5+
.. |app-pip-package| replace:: quart
.. |app-pip-link| replace:: PIP package
.. _app-pip-link: https://pgjones.gitlab.io/quart/tutorials/installation.html

#####
Quart
#####

To run apps built with the `Quart
<https://pgjones.gitlab.io/quart/index.html>`_ web framework using Unit:

#. .. include:: ../include/howto_install_unit.rst

#. .. include:: ../include/howto_install_venv.rst

#. Let's try a WebSocket-enabled version of a `tutorial app
   <https://pgjones.gitlab.io/quart/tutorials/deployment.html>`_,
   saving it as **/path/to/app/asgi.py**:

   .. code-block:: python

      from quart import Quart, websocket

      app = Quart(__name__)

      @app.route('/')
      async def hello():
          return '<body><h1>Hello, World!</h1></body>'

      # Let's add WebSocket support to the app as well
      @app.websocket('/ws')
      async def ws():
          while True:
              await websocket.send('Hello, World!')

#. .. include:: ../include/howto_change_ownership.rst

#. Next, :ref:`prepare <configuration-python>` the |app| configuration for
   Unit (use real values for **type**, **home**, and **path**):

   .. code-block:: json

      {
          "listeners": {
              "*:80": {
                  "pass": "applications/quart"
              }
          },

          "applications": {
              "quart": {
                  "type": "python 3.:nxt_ph:`Y <Must match language module version and virtual environment version>`",
                  "path": ":nxt_ph:`/path/to/app/ <Path to the ASGI module>`",
                  "home": ":nxt_ph:`/path/to/app/venv/ <Path to the virtual environment, if any>`",
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

            <body><h1>Hello, World!</h1></body>


   .. code-block:: console

      $ wscat -c ws://localhost/ws

            < Hello, World!
            < Hello, World!
            < Hello, World!
            ...
