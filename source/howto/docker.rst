:orphan:

##############
Unit in Docker
##############

To run your apps in containerized Unit using the :ref:`images we provide
<installation-docker>`, you need at least to:

- Mount your application files to a directory in your container.
- Publish Unit's listener port to the host machine.

For example:

.. code-block:: console

   $ export UNIT=$(docker run --rm -d -v $(pwd):/www -p 8080:8000 nginx/unit:latest)

The command mounts current host directory (where your app files are stored)
to the container's :file:`/www` directory and publishes the container's port
:samp:`8000` (that the listener will use) as port :samp:`8080` on the host,
storing the container ID in the :samp:`UNIT` environment variable.

Next, you need to upload your configuration to Unit via the control socket:

.. code-block:: console

   $ docker exec -ti $UNIT curl -X PUT -d @/www/config.json --unix-socket
                                /var/run/control.unit.sock http://localhost/config

This command assumes that your configuration listens on port 8000 and is stored
as :file:`config.json` in the container-mounted directory on the host.  As a
result, this makes your app accessible at port :samp:`8080` of the host.  For
details of Unit configuration, see :ref:`configuration-mgmt`.

