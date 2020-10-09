.. |app| replace:: Quart
.. |mod| replace:: Python 3.5+

#####
Quart
#####

To run apps built with the `Quart
<https://pgjones.gitlab.io/quart/index.html>`_ web framework using Unit:

#. .. include:: ../include/howto_install_unit.rst

#. Create a virtual environment to install |app|'s `PIP package
   <https://pgjones.gitlab.io/quart/tutorials/installation.html>`_:

   .. code-block:: console

      $ cd /path/to/app/
      $ python3 -m venv venv
      $ source venv/bin/activate
      $ pip install quart
      $ deactivate

#. Let's try a WebSocket-enabled version of a `tutorial app
   <https://pgjones.gitlab.io/quart/tutorials/deployment.html>`_,
   saving it as :file:`/path/to/app/asgi.py`:

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

#. Next, :ref:`put together <configuration-python>` the |app| configuration for
   Unit:

   .. code-block:: json

      {
          "listeners": {
              "*:80": {
                  "pass": "applications/quart_app"
              }
          },

          "applications": {
              "quart_app": {
                  "type": "python 3",
                  "user": ":nxt_term:`unit_user <User and group values must have access to path and home directories>`",
                  "group": "unit_group",
                  "path": ":nxt_term:`/path/to/app/ <Path to the ASGI module>`",
                  "home": ":nxt_term:`/path/to/app/venv/ <Path to the virtual environment, if any>`",
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

            <body><h1>Hello, World!</h1></body>

      $ wscat -c ws://localhost/ws

            < Hello, World!
            < Hello, World!
            < Hello, World!
            ...
