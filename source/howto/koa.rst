.. |app| replace:: Koa
.. |mod| replace:: Node.js

###
Koa
###

To run apps built with the `Koa <https://koajs.com>`_ web framework using Unit:

#. Install :ref:`Unit <installation-precomp-pkgs>` with the
   **unit-dev/unit-devel** package.  Next, :ref:`install
   <installation-nodejs-package>` Unit's **unit-http** package:

   .. code-block:: console

      # npm install -g --unsafe-perm unit-http

#. Create your app directory, `install <https://koajs.com/#introduction>`_
   |app|, and link **unit-http**:

   .. code-block:: console

      $ mkdir -p :nxt_ph:`/path/to/app/ <Path to the application directory; use a real path in your configuration>`

   .. code-block:: console

      $ cd :nxt_ph:`/path/to/app/ <Path to the application directory; use a real path in your configuration>`

   .. code-block:: console

      $ npm install koa

   .. code-block:: console

      # npm link unit-http

#. Let’s try a version of the `tutorial app
   <https://koajs.com/#application>`__, saving it as
   **/path/to/app/app.js**:

   .. code-block:: javascript

      const Koa = require('koa');
      const app = new Koa();

      // logger

      app.use(async (ctx, next) => {
        await next();
        const rt = ctx.response.get('X-Response-Time');
        console.log(`${ctx.method} ${ctx.url} - ${rt}`);
      });

      // x-response-time

      app.use(async (ctx, next) => {
        const start = Date.now();
        await next();
        const ms = Date.now() - start;
        ctx.set('X-Response-Time', `${ms}ms`);
      });

      // response

      app.use(async ctx => {
        ctx.body = 'Hello, Koa on Unit!';
      });

      app.listen();

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
                  "pass": "applications/koa"
              }
          },

          "applications": {
              "koa": {
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

   .. subs-code-block:: console

      $ curl http://localhost -v

            *   Trying 127.0.0.1:80...
            * TCP_NODELAY set
            * Connected to localhost (127.0.0.1) port 80 (#0)
            > GET / HTTP/1.1
            > Host: localhost
            > User-Agent: curl/7.68.0
            > Accept: */*
            >
            * Mark bundle as not supporting multiuse
            < HTTP/1.1 200 OK
            < Content-Type: text/plain; charset=utf-8
            < Content-Length: 11
            < X-Response-Time: 0ms
            < Server: Unit/|version|

            Hello, Koa on Unit!
