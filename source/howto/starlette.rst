.. |app| replace:: Starlette
.. |mod| replace:: Python 3.5+
.. |app-pip-package| replace:: 'starlette[full]'
.. |app-pip-link| replace:: PIP package
.. _app-pip-link: https://www.starlette.io/#installation

#########
Starlette
#########

To run apps built with the `Starlette <https://www.starlette.io>`_ web
framework using Unit:

#. .. include:: ../include/howto_install_unit.rst

#. .. include:: ../include/howto_install_venv.rst

#. Let's try a version of a `tutorial app
   <https://www.starlette.io/applications/>`_,
   saving it as :file:`/path/to/app/asgi.py`:

   .. code-block:: python

      from starlette.applications import Starlette
      from starlette.responses import PlainTextResponse
      from starlette.routing import Route, Mount, WebSocketRoute


      def homepage(request):
          return PlainTextResponse('Hello, world!')

      def user_me(request):
          username = "John Doe"
          return PlainTextResponse('Hello, %s!' % username)

      def user(request):
          username = request.path_params['username']
          return PlainTextResponse('Hello, %s!' % username)

      async def websocket_endpoint(websocket):
          await websocket.accept()
          await websocket.send_text('Hello, websocket!')
          await websocket.close()

      def startup():
          print('Ready to go')


      routes = [
          Route('/', homepage),
          Route('/user/me', user_me),
          Route('/user/{username}', user),
          WebSocketRoute('/ws', websocket_endpoint)
      ]

      app = Starlette(debug=True, routes=routes, on_startup=[startup])

   .. note::

      This sample omits the static route because Unit's quite :ref:`capable
      <configuration-static>` of serving static files itself if needed.

#. .. include:: ../include/howto_change_ownership.rst

#. Next, :ref:`prepare <configuration-python>` the |app| configuration for Unit
   (use real values for :samp:`type`, :samp:`home`, and :samp:`path`), adding a
   :ref:`route <configuration-routes>` to serve static content:

   .. code-block:: json

      {
          "listeners": {
              "*:80": {
                  "pass": "routes"
              }
          },

          "routes": [
              {
                  "match": {
                      "uri": "/static/*"
                  },

                  "action": {
                      ":nxt_hint:`share <Serves static files>`": ":nxt_ph:`/path/to/app <Thus, URIs starting with /static/ are served from /path/to/app/static/; use a real path in your configuration>`$uri"
                  }
              },

              {
                  "action": {
                      "pass": "applications/starlette"
                  }
              }
          ],

          "applications": {
              "starlette": {
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

            Hello, world!

      $ curl http://localhost/user/me

            Hello, John Doe!

      $ wscat -c ws://localhost/ws

            Connected (press CTRL+C to quit)
            < Hello, websocket!
            Disconnected (code: 1000, reason: "")
