.. |app| replace:: Express
.. |mod| replace:: Node.js

#######
Express
#######

To run apps built with the `Express <https://expressjs.com>`_ web framework
using Unit:

#. Install :ref:`Unit <installation-precomp-pkgs>` with the
   :samp:`unit-dev/unit-devel` package.  Next, :ref:`install
   <installation-nodejs-package>` Unit's :samp:`unit-http` package:

   .. code-block:: console

      # npm install -g --unsafe-perm unit-http

#. Create your app directory, `install
   <https://expressjs.com/en/starter/installing.html>`_ |app|, and link
   :samp:`unit-http`:

   .. code-block:: console

      $ mkdir -p :nxt_ph:`/path/to/app/ <Path to the application directory; use a real path in your configuration>`
      $ cd :nxt_ph:`/path/to/app/ <Path to the application directory; use a real path in your configuration>`
      $ npm init
      $ npm install express --save
      $ npm link unit-http

#. Create your Express `app
   <https://expressjs.com/en/starter/hello-world.html>`_; let's store it as
   :file:`/path/to/app/app.js`.  Unit requires it to be executable:

   .. code-block:: console

      $ touch :nxt_ph:`/path/to/app/app.js <Pathname of the application file; use a real path in your configuration>`
      $ chmod +x :nxt_ph:`/path/to/app/app.js <Pathname of the application file; use a real path in your configuration>`

   In the code, create a custom HTTP server (note :samp:`createServer`,
   :samp:`ServerResponse`, and :samp:`IncomingMessage`).  Also, mind that Unit
   needs a shebang to recognize the script:

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

   .. note::

      The same modifications apply if you use the `app generator
      <https://expressjs.com/en/starter/generator.html>`_ to create your
      :file:`app.js`:

      .. code-block:: javascript

         #!/usr/bin/env node

         const {
           createServer,
           IncomingMessage,
           ServerResponse,
         } = require('unit-http')

         require('http').ServerResponse = ServerResponse
         require('http').IncomingMessage = IncomingMessage

         // skipping generated code

         createServer(app).listen()

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
                  "executable": ":nxt_ph:`app.js <Basename of the application file; be sure to make it executable>`"
              }
          }
      }

#. .. include:: ../include/howto_upload_config.rst

   After a successful update, your app should be available on the listener's IP
   address and port:

   .. image:: ../images/express.png
      :width: 100%
      :alt: Express on Unit - Welcome Screen
