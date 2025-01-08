.. |app| replace:: Express
.. |mod| replace:: Node.js

#######
Express
#######

To run apps built with the `Express <https://expressjs.com>`_ web framework
using Unit:

#. Install :ref:`Unit <installation-precomp-pkgs>` with the
   **unit-dev/unit-devel** package.  Next, :ref:`install
   <installation-nodejs-package>` Unit's **unit-http** package:

   .. code-block:: console

      # npm install -g --unsafe-perm unit-http

#. Create your app directory, `install
   <https://expressjs.com/en/starter/installing.html>`_ |app|, and link
   **unit-http**:

   .. code-block:: console

      $ mkdir -p :nxt_ph:`/path/to/app/ <Path to the application directory; use a real path in your configuration>`

   .. code-block:: console

      $ cd :nxt_ph:`/path/to/app/ <Path to the application directory; use a real path in your configuration>`

   .. code-block:: console

      $ npm install express --save

   .. code-block:: console

      # npm link unit-http

#. Create your Express `app
   <https://expressjs.com/en/starter/hello-world.html>`_; let's store it as
   **/path/to/app/app.js**.  First, initialize the directory:

   .. code-block:: console

      $ cd :nxt_ph:`/path/to/app/ <Path to the application directory; use a real path in your configuration>`

   .. code-block:: console

      $ npm init

   Next, add your application code:

   .. code-block:: javascript

      #!/usr/bin/env node

      const http = require('http')
      const express = require('express')
      const app = express()

      app.get('/', (req, res) => res.send('Hello, Express on Unit!'))

      http.createServer(app).listen()

   The file should be made executable so the application can run on Unit:

   .. code-block:: console

      $ chmod +x :nxt_ph:`app.js <Application file; use a real path in your configuration>`

#. .. include:: ../include/howto_change_ownership.rst

#. Next, :ref:`prepare <configuration-nodejs>` the |app| configuration for
   Unit:

   .. code-block:: json

      {
          "listeners": {
              "*:80": {
                  "pass": "applications/express"
              }
          },

          "applications": {
              "express": {
                  "type": "external",
                  "working_directory": ":nxt_ph:`/path/to/app/ <Needed to use the installed NPM modules; use a real path in your configuration>`",
                  "executable": ":nxt_hint:`/usr/bin/env <The external app type allows to run arbitrary executables, provided they establish communication with Unit>`",
                  ":nxt_hint:`arguments <The env executable runs Node.js, supplying Unit's loader module and your app code as arguments>`": [
                      "node",
                      "--loader",
                      "unit-http/loader.mjs",
                      "--require",
                      "unit-http/loader",
                      ":nxt_ph:`app.js <Basename of the application file; be sure to make it executable>`"
                  ]
              }
          }
      }

#. .. include:: ../include/howto_upload_config.rst

   After a successful update, your app should be available on the listener's IP
   address and port:

   .. image:: ../images/express.png
      :width: 100%
      :alt: Express on Unit - Welcome Screen
