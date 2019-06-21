:orphan:

############
Express Apps
############

To run your `Express <https://expressjs.com>`_ apps in Unit:

#. :ref:`Install Unit <installation-precomp-pkgs>` with the appropriate Node.js
   language module version.

#. If you haven't already done so, `create your Express app
   <https://expressjs.com/en/starter/hello-world.html>`_ and store it as usual.

#. Next, you need to have the :program:`unit-http` package :ref:`installed
   <installation-nodejs-package>`.  If it's global, symlink it in your project
   directory:

   .. code-block:: console

      # npm link unit-http

#. In your app, create a custom HTTP server (note use of :samp:`createServer`,
   :samp:`ServerResponse`, and :samp:`IncomingMessage`):

   .. code-block:: javascript

      #!/usr/bin/env node

      const {
        createServer,
        IncomingMessage,
        ServerResponse,
      } = require('unit-http')

      require('http').ServerResponse = ServerResponse
      require('http').IncomingMessage = IncomingMessage

      const express = require('express')
      const app = express()

      app.get('/', (req, res) => res.send('Hello, Unit!'))

      createServer(app).listen()

#. .. include:: ../include/get-config.rst

   This creates a JSON file with Unit's current settings; update it with your
   project settings as follows.

#. Edit the JSON file, adding a :ref:`listener <configuration-listeners>` in
   :samp:`listeners` and pointing it to your app's :file:`.js` file in
   :samp:`applications`.  Your project and apps will run on the listener's IP
   and port at their respective URL paths.

   .. code-block:: json

      {
          "listeners": {
              "127.0.0.1:8080": {
                  "pass": "applications/express_app"
              }
          },

          "applications": {
              "express_app": {
                  "type": "external",
                  "working_directory": "/path/to/express/app/",
                  "executable": "app.js"
              }
          }
      }

#. Upload the updated configuration:

   .. code-block:: console

      # curl -X PUT --data-binary @config.json --unix-socket \
             /path/to/control.unit.sock http://localhost/config

   After a successful update, your app should be available on the listener's IP
   address and port:

   .. code-block:: console

      $ curl 127.0.0.1:8080/
