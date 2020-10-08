.. |app| replace:: Starlette
.. |mod| replace:: Python 3.5+

#########
Starlette
#########

To run apps built with the `Starlette <https://www.starlette.io>`_ web
framework using Unit:

#. .. include:: ../include/howto_install_unit.rst

#. Create a virtual environment to install |app|'s `PIP package
   <https://www.starlette.io/#installation>`_:

   .. code-block:: console

      $ cd /path/to/app/
      $ python3 -m venv venv
      $ source venv/bin/activate
      $ pip install starlette[full]
      $ deactivate

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

#. Next, :ref:`put together <configuration-python>` the |app| configuration for
   Unit, adding a :ref:`route <configuration-routes>` to serve static content:

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
                      "share": ":nxt_term:`/path/to/app/ <Thus, URIs starting with /static/ are served from /path/to/app/static/>`"
                  }
              },

              {
                  "action": {
                      "pass": "applications/starlette_app"
                  }
              }
          ],

          "applications": {
              "starlette_app": {
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

            Hello, world!

      $ curl http://localhost/user/me

            Hello, John Doe!

      $ wscat -c ws://localhost/ws

            Connected (press CTRL+C to quit)
            < Hello, websocket!
            Disconnected (code: 1000, reason: "")
