##############
Unit in Docker
##############

To run your apps in containerized Unit using the :ref:`images we provide
<installation-docker>`, you need at least to:

- Mount your application files to a directory in your container.
- Publish Unit's listener port to the host machine.

For example:

.. code-block:: console

   $ export UNIT=$(docker run -d \
                          --mount type=bind,src="$(pwd)",dst=/www \
                          -p 8080:8000 nginx/unit:latest)

The command mounts current host directory (where your app files are stored) to
the container's :file:`/www` directory and publishes the container's port
:samp:`8000` (that the listener will use) as port :samp:`8080` on the host,
saving the container ID in the :envvar:`UNIT` environment variable.

Next, you need to upload a configuration to Unit via the control socket:

.. code-block:: console

   $ docker exec -ti $UNIT curl -X PUT --data-binary @/www/config.json \
                                --unix-socket var/run/control.unit.sock http://localhost/config

This command assumes that your configuration is stored as :file:`config.json`
in the container-mounted directory on the host.  If it has a listener on port
:samp:`8000`, your app is now accessible at port :samp:`8080` of the host.  For
details of Unit configuration, see :ref:`configuration-mgmt`.

.. note::

   For app containerization examples, refer to our sample :download:`Go
   <../downloads/Dockerfile.go.txt>`, :download:`Java
   <../downloads/Dockerfile.java.txt>`, :download:`Node.js
   <../downloads/Dockerfile.nodejs.txt>`, :download:`Perl
   <../downloads/Dockerfile.perl.txt>`, :download:`PHP
   <../downloads/Dockerfile.php.txt>`, :download:`Python
   <../downloads/Dockerfile.python.txt>`, and :download:`Ruby
   <../downloads/Dockerfile.ruby.txt>` Dockerfiles; also, see a more
   elaborate discussion :ref:`below <docker-apps>`.

Now for a few detailed scenarios.

Running Apps in Containerized Unit
##################################

Suppose we have a web app with a few dependencies, say :doc:`Flask's <flask>`
official :samp:`hello world` app:

.. code-block:: console

   $ cd /path/to/app/
   $ mkdir webapp
   $ cat << EOF > webapp/app.py

       from flask import Flask
       app = Flask(__name__)
       application = app

       @app.route('/')
       def hello_world():
           return 'Hello, World!'
       EOF

However basic it is, there's already a dependency, so let's put it into a file
called :file:`requirements.txt`:

.. code-block:: none

   $ cat << EOF > requirements.txt

       flask
       EOF

Next, create a simple Unit :ref:`configuration <configuration-python>` for the
app:

.. code-block:: console

   $ mkdir config
   $ cat << EOF > config/config.json

       {
          "listeners":{
             "*:8000":{
                "pass":"applications/webapp"
             }
          },
          "applications":{
             "webapp":{
                "type":"python 3",
                "path":"/www/",
                "module":"app"
             }
          }
       }
       EOF

Finally, let's create :file:`log` and :file:`state` directories to store Unit
:ref:`log and state <installation-src-startup>` respectively:

.. code-block:: console

   $ mkdir log
   $ touch log/unit.log
   $ mkdir state

Our file structure so far:

.. code-block:: none

   /path/to/app
   ├── config
   │   └── config.json
   ├── log
   │   └── unit.log
   ├── requirements.txt
   ├── state
   └── webapp
       └── app.py

Everything is ready for a containerized Unit.  First, let's create a
:file:`Dockerfile` to install app prerequisites:

.. code-block:: docker

   FROM nginx/unit:latest
   COPY requirements.txt /config/requirements.txt
   RUN apt update && apt install -y python3-pip                               \
       && pip3 install -r /config/requirements.txt                            \
       && apt remove -y python3-pip                                           \
       && apt autoremove --purge -y                                           \
       && rm -rf /var/lib/apt/lists/* /etc/apt/sources.list.d/*.list


.. code-block:: console

   $ docker build --tag=unit-webapp .

Next, we start a container and map it to our directory structure:

.. code-block:: console

   $ export UNIT=$(docker run -d \
                          --mount type=bind,src="$(pwd)/config/",dst=/docker-entrypoint.d/  \
                          --mount type=bind,src="$(pwd)/log/unit.log",dst=/var/log/unit.log \
                          --mount type=bind,src="$(pwd)/state",dst=/var/lib/unit            \
                          --mount type=bind,src="$(pwd)/webapp",dst=/www                    \
                                      -p 8080:8000 unit-webapp)

.. note::

   With this mapping, Unit will store its state and log in your file structure,
   essentially making it portable.

We've mapped the source :file:`config/` to :file:`/docker-entrypoint.d/` in the
container; the official image :ref:`uploads <installation-docker-init>` any
:file:`.json` files found there into Unit's :samp:`config` section if the state
is empty.  Now we can test the app:

.. code-block:: console

   $ curl -X GET localhost:8080

       Hello, World!

To relocate the app in your filesystem, you only need to move the file
structure:

.. code-block:: console

   $ mv /path/to/app /new/path/to/app

To switch your app to another Unit image, prepare a corresponding
:file:`Dockerfile` first:

.. subs-code-block:: docker

   FROM nginx/unit:|version|-python3.7
   COPY requirements.txt /config/requirements.txt
   RUN apt update && apt install -y python3-pip    \
       && pip3 install -r /config/requirements.txt \
       && rm -rf /var/lib/apt/lists/*

.. code-block:: console

   $ docker build --tag=unit-pruned-webapp .

Run a container from the new image; Unit picks up the mapped state
automatically:

.. code-block:: console

   $ export UNIT=$(docker run -d \
                          --mount type=bind,src="$(pwd)/log/unit.log",dst=/var/log/unit.log \
                          --mount type=bind,src="$(pwd)/state",dst=/var/lib/unit \
                          --mount type=bind,src="$(pwd)/webapp",dst=/www \
                                      -p 8080:8000 unit-pruned-webapp)

.. _docker-apps:

Containerizing Apps
###################

Suppose you have a Unit-ready :doc:`Express <express>` app:

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

Its Unit configuration, stored as :file:`config.json`:

   .. code-block:: json

      {
          "listeners": {
              "*:8080": {
                  "pass": "applications/express"
              }
          },

          "applications": {
              "express": {
                  "type": "external",
                  "working_directory": "/www/",
                  "executable": "app.js"
              }
          }
      }

Resulting file structure:

.. code-block:: none

   myapp/
   ├── app.js
   └── config.json

Let's prepare a :file:`Dockerfile` to install and configure the app in an
image:

.. subs-code-block:: docker

   # keep our base image as small as possible
   FROM nginx/unit:|version|-minimal

   # same as "working_directory" in config.json
   COPY myapp/app.js /www/

   # add NGINX Unit and Node.js repos
   RUN apt update                                                             \
       && apt install -y apt-transport-https gnupg1                           \
       && curl https://nginx.org/keys/nginx_signing.key | apt-key add -       \
       && echo "deb https://packages.nginx.org/unit/debian/ stretch unit"     \
            > /etc/apt/sources.list.d/unit.list                               \
       && echo "deb-src https://packages.nginx.org/unit/debian/ stretch unit" \
            >> /etc/apt/sources.list.d/unit.list                              \
       && curl https://deb.nodesource.com/setup_12.x | bash -                 \
   # install build chain
       && apt update                                                          \
       && apt install -y build-essential nodejs unit-dev=$:nxt_term:`UNIT_VERSION <Makes sure the package version is the same as the base image version>`        \
   # add global dependencies
       && npm install -g --unsafe-perm unit-http                              \
   # add app dependencies locally
       && cd /www && npm link unit-http && npm install express                \
   # final cleanup
       && apt remove -y build-essential unit-dev apt-transport-https gnupg1   \
       && apt autoremove --purge -y                                           \
       && rm -rf /var/lib/apt/lists/* /etc/apt/sources.list.d/*.list

   # port used by the listener in config.json
   EXPOSE 8080

When you start a container based on this image, mount the :file:`config.json`
file to :ref:`initialize <installation-docker-init>` Unit's state:

.. code-block:: console

   $ docker build --tag=unit-expressapp .
   $ export UNIT=$(docker run -d --mount \
         type=bind,src="$(pwd)/myapp/config.json",dst=/docker-entrypoint.d/config.json \
         -p 8080:8080 unit-expressapp)
   $ curl -X GET localhost:8080

        Hello, Unit!

.. note::

   This mechanism allows to initialize Unit at container startup only if its
   state is empty; otherwise, the contents of :file:`/docker-entrypoint.d/` is
   ignored.  Continuing the previous sample:

   .. code-block:: console

      $ docker commit $UNIT unit-expressapp  # store non-empty Unit state in the image
      # cat << EOF > myapp/new-config.json   # let's attempt re-initialization
        ...
        EOF
      $ export UNIT=$(docker run -d --mount \
            type=bind,src="$(pwd)/myapp/new-config.json",dst=/docker-entrypoint.d/new-config.json \
            -p 8080:8080 unit-expressapp)

   Here, Unit *will not* pick up the :samp:`new-config.json` from the
   :file:`/docker-entrypoint.d/` directory when we run a container from the
   updated image because Unit's state was initialized and saved earlier.

To configure the app after startup, supply a file or an explicit snippet via
the :ref:`config API <configuration-mgmt>`:

.. code-block:: console

   $ cat << EOF > myapp/new-config.json
     ...
     EOF
   $ export UNIT=$(docker run -d --mount \
         type=bind,src="$(pwd)/myapp/new-config.json",dst=/cfg/new-config.json unit-expressapp)
   $ docker exec -ti $UNIT curl -X PUT --data-binary @/cfg/new-config.json \
         --unix-socket /var/run/control.unit.sock http://localhost/config
   $ docker exec -ti $UNIT curl -X PUT -d '"/www/newapp/"' --unix-socket \
         /var/run/control.unit.sock http://localhost/config/applications/express/working_directory

This approach is applicable to any Unit-supported apps with external
dependencies.
