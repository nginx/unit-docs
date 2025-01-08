.. |app| replace:: Apollo
.. |mod| replace:: Node.js

######
Apollo
######

To run the `Apollo <https://www.apollographql.com>`_ GraphQL server
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

      $ npm install @apollo/server graphql

   .. code-block:: console

      # npm link unit-http

#. Create the `middleware
   <https://www.apollographql.com/docs/apollo-server/api/express-middleware/>`_
   module; let's store it as **/path/to/app/apollo.js**.
   First, initialize the directory:

   .. code-block:: console

      $ cd :nxt_ph:`/path/to/app/ <Path to the application directory; use a real path in your configuration>`

   .. code-block:: console

      $ npm init

   Next, add the following code:

   .. code-block:: javascript

      import { ApolloServer } from '@apollo/server';
      import { expressMiddleware } from '@apollo/server/express4';
      import { ApolloServerPluginDrainHttpServer } from '@apollo/server/plugin/drainHttpServer';
      import express from 'express';
      import http from 'http';
      import cors from 'cors';
      import bodyParser from 'body-parser';
      //import { typeDefs, resolvers } from './schema';

      const typeDefs = `#graphql
        type Query {
          hello: String
        }
      `;

      // A map of functions which return data for the schema.
      const resolvers = {
        Query: {
          hello: () => 'world',
        },
      };


      // Required logic for integrating with Express
      const app = express();
      // Our httpServer handles incoming requests to our Express app.
      // Below, we tell Apollo Server to "drain" this httpServer,
      // enabling our servers to shut down gracefully.
      const httpServer = http.createServer(app);

      // Same ApolloServer initialization as before, plus the drain plugin
      // for our httpServer.
      const server = new ApolloServer({
        typeDefs,
        resolvers,
        plugins: [ApolloServerPluginDrainHttpServer({ httpServer })],
      });
      // Ensure we wait for our server to start
      await server.start();

      // Set up our Express middleware to handle CORS, body parsing,
      // and our expressMiddleware function.
      app.use(
        '/',
        cors(),
        bodyParser.json(),
        // expressMiddleware accepts the same arguments:
        // an Apollo Server instance and optional configuration options
        expressMiddleware(server, {
          context: async ({ req }) => ({ token: req.headers.token }),
        }),
      );

      // Modified server startup; port number is overridden by Unit config
      await new Promise((resolve) => httpServer.listen({ port: 80 }, resolve));

   Make sure your **package.json** resembles this
   (mind **"type": "module"**):

   .. code-block:: json

      {
          "name": "unit-apollo",
          "version": "1.0.0",
          "description": "Running Apollo over Express on Unit",
          "main": "index.js",
          "type": "module",
          "scripts": {
              "test": "echo \"Error: no test specified\" && exit 1"
          },
          "author": "Unit Team",
          "license": "ISC",
          "dependencies": {
              "@apollo/server": "^4.7.5",
              "apollo-server": "^3.12.0",
              "body-parser": "^1.20.2",
              "cors": "^2.8.5",
              "express": "^4.18.2",
              "graphql": "^16.7.1",
              "unit-http": "^1.30.0"
          }
      }

#. .. include:: ../include/howto_change_ownership.rst

#. Next, :ref:`prepare <configuration-nodejs>` the |app| configuration for
   Unit:

   .. code-block:: json

      {
          "listeners": {
              "*:80": {
                  "pass": "applications/apollo"
              }
          },

          "applications": {
              "apollo": {
                  "type": "external",
                  "working_directory": ":nxt_ph:`/path/to/app/ <Needed to use the installed NPM modules; use a real path in your configuration>`",
                  "executable": ":nxt_hint:`/usr/bin/env <The external app type allows to run arbitrary executables, provided they establish communication with Unit>`",
                  ":nxt_hint:`arguments <The env executable runs Node.js, supplying Unit's loader module and your app code as arguments>`": [
                      "node",
                      "--loader",
                      "unit-http/loader.mjs",
                      "--require",
                      "unit-http/loader",
                      ":nxt_ph:`apollo.js <Basename of the application file; be sure to make it executable>`"
                  ]
              }
          }
      }

#. .. include:: ../include/howto_upload_config.rst

   After a successful update, your app should be available on the listener's IP
   address and port:

   .. image:: ../images/apollo.png
      :width: 100%
      :alt: Apollo on Unit
