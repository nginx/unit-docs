:orphan:

.. include:: ../include/replace.rst

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

   $ docker exec -ti $UNIT curl -X PUT -d @/www/config.json --unix-socket
                                /var/run/control.unit.sock http://localhost/config

This command assumes that your configuration is stored as :file:`config.json`
in the container-mounted directory on the host.  If it has a listener on port
:samp:`8000`, your app is now accessible at port :samp:`8080` of the host.  For
details of Unit configuration, see :ref:`configuration-mgmt`.

Now for a few detailed scenarios.

Running Apps in Containerized Unit
##################################

Suppose we have a web app with a few dependencies, say :doc:`Flask's <flask>`
official :samp:`hello world` app:

.. code-block:: console

   $ cd /path/to/app/
   $ mkdir webapp
   $ cat << EOF > webapp/app.py

       > from flask import Flask
       > app = Flask(__name__)
       >
       > @app.route('/')
       > def hello_world():
       >     return 'Hello, World!'
       > EOF

However basic it is, there's already a dependency, so let's put it into a file
called :file:`requirements.txt`:

.. code-block:: none

   $ mkdir config
   $ cat << EOF > config/requirements.txt

       > flask
       > EOF

Next, create a simple Unit :ref:`configuration <configuration-python>` for the
app:

.. code-block:: console

   # cat << EOF > config/config.json

       > {
       >    "listeners":{
       >       "*:8000":{
       >          "pass":"applications/webapp"
       >       }
       >    },
       >    "applications":{
       >       "webapp":{
       >          "type":"python 3",
       >          "path":"/www/",
       >          "module":"app"
       >       }
       >    }
       > }
       > EOF

Finally, let's create :file:`log` and :file:`state` directories to store Unit
:ref:`log and state<installation-startup>` respectively:

.. code-block:: console

   $ mkdir log
   $ touch log/unit.log
   $ mkdir state

Our file structure so far:

.. code-block:: none

   /path/to/app
   ├── config
   │   ├── config.json
   │   └── requirements.txt
   ├── log
   │   └── unit.log
   ├── state
   └── webapp
       └── app.py

Everything is ready for a containerized Unit.  First, let's create a
:file:`Dockerfile` to install app prerequisites:

.. code-block:: docker

   FROM nginx/unit:latest
   COPY config/requirements.txt /config/requirements.txt
   RUN apt update && apt -y install python3-pip && \
       pip3 install -r /config/requirements.txt && \
       rm -rf /var/lib/apt/lists/*

.. code-block:: console

   $ docker build --tag=unit-webapp .

Next, we start a container and map it to our directory structure:

.. code-block:: console

   $ export UNIT=$(docker run -d \
                          --mount type=bind,src="$(pwd)/config/config.json",dst=/config/config.json \
                          --mount type=bind,src="$(pwd)/log/unit.log",dst=/var/log/unit.log \
                          --mount type=bind,src="$(pwd)/state",dst=/var/lib/unit \
                          --mount type=bind,src="$(pwd)/webapp",dst=/www \
                                      -p 8080:8000 unit-webapp)

.. note::

   With this mapping, Unit will store its state and log in your file structure,
   essentially making it portable.

Now we can configure the app in Unit:

.. code-block:: console

   $ docker exec -ti $UNIT curl -X PUT -d @/config/config.json --unix-socket \
                                /var/run/control.unit.sock http://localhost/config

       {
           "success": "Reconfiguration done."
       }

Finally, let's test the app:

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

   FROM nginx/unit:|version|-python3.5
   COPY config/requirements.txt /config/requirements.txt
   RUN apt update && apt -y install python3-pip && \
       pip3 install -r /config/requirements.txt && \
       rm -rf /var/lib/apt/lists/*

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
