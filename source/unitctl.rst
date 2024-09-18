 .. meta::
   :og:description: Learn how to use the Unit CLI.

.. include:: include/replace.rst
.. _unitctl:

#############
CLI (unitctl)
#############

.. note::

   **unitctl** is currently being provided as a "Technical Preview". We welcome
   feedback and suggestions for this early access version. It is provided to test
   its features and should not be used in production environments.

Unit provides a `Rust SDK <https://github.com/nginx/unit/tree/master/tools/unitctl>`_
to interact with its :ref:`control API <source-startup>`, and a command line
interface (unitctl) that exposes the functionality provided by the SDK.

This CLI is a multi-purpose tool that allows you to deploy, manage, and configure
Unit in your environment.

*****************
Download binaries
*****************

Unitctl binaries are available for Linux (ARM64 and X64) and macOS systems.

Download the latest binaries from the `Unit GitHub releases page
<https://github.com/nginx/unit/releases>`_.

*****************
Build from source
*****************

To build unitctl from source, follow the instructions in the `unitctl repository
<https://github.com/nginx/unit/tree/master/tools/unitctl>`_.

*************
Using unitctl
*************

The unitctl CLI offers several commands to interact with Unit. Here are the available commands:

.. list-table::
   :header-rows: 1

   * - Command
     - Description

   * - **instances**
     - List all running Unit processes

   * - **apps**
     - List and restart active applications

   * - **edit**
     - Open the current Unit configuration in the default system editor

   * - **export**
     - Export the current Unit configuration (excluding certificates) to a
       tarball

   * - **import**
     - Import Unit configuration from a directory

   * - **execute**
     - Send a raw JSON payload to Unit

   * - **status**
     - Get the current status of Unit

   * - **listeners**
     - List all active listeners

   * - **help**
     - Display help information for commands and options

There are also a number of options that you can use with the unitctl CLI:

.. list-table::
   :header-rows: 1

   * - Option
     - Description

   * - **-s, --control-socket-address <CONTROL_SOCKET_ADDRESS>**
     - Specify a path (unix:/var/run/unit/control.sock), TCP addres with port
       (127.0.0.1:80), or URL for Unit's control socket

   * - **-w, --wait-timeout-seconds <WAIT_TIMEOUT_SECONDS>**
     - Specify the timeout in seconds for the control socket to become available

   * - **-t, --wait-max-tries <WAIT_MAX_TRIES>**
     - Specify the maximum number of tries to connect to the control socket when
       waiting (default: 3)

   * - **-h, --help**
     - Display help information for commands and options

   * - **-v, --version**
     - Display the version of the unitctl CLI

+++++++++++++++++++++++++++++++++
List and create instances of Unit
+++++++++++++++++++++++++++++++++

The **instances** command lets you list all running Unit processes and
deploy new instances of Unit.

The **instances** command has the following option:

.. list-table::
   :header-rows: 1

   * - Option
     - Description

   * - **new**
     - Deploy a new instance of Unit

Running unitcl with the **instances** command shows output similar to this:

.. code-block:: console

   $ unitctl instances
   No socket path provided - attempting to detect from running instance
   unitd instance [pid: 79489, version: 1.32.0]:
      Executable: /opt/unit/sbin/unitd
      API control unix socket: unix:/opt/unit/control.unit.sock
      Child processes ids: 79489, 79489
      Runtime flags: --no-daemon
      Configure options: --prefix=/opt/unit --user=myUser --group=myGroup --openssl

You can use the **new** option with three arguments to deploy a new instance of Unit:

1. **Control API path**: A file path for a Unix socket or a TCP address with port.

   - If you specify a directory, the Unit container will mount it to **/var/run** internally.
     The control socket and pid file are accessible from the host. Example: **/tmp/2**.
   - If you specify a TCP address, the Unit container will listen on this
     address and port. Example: **127.0.0.1:7171**.

2. **Application path**. The Unit container will mount this path in read-only mode
   to **/www** internally. This setup allows you to configure the Unit
   container to expose an application stored on the host. Example: **$(pwd)**.

3. **Image tag**: Unitctl will deploy this image, enabling you use custom
   images. For example: **unit:wasm**.

.. code-block:: console

   $ unitctl instances new /tmp/2 $(pwd) 'unit:wasm'
   Pulling and starting a container from unit:wasm
   Will mount /tmp/2 to /var/run for socket access
   Will READ ONLY mount /home/user/unitctl to /www for application access
   Note: Container will be on host network

After the deployment is complete, you will have one Unit container running on the
host network.

+++++++++++++++++++++++++++++
List and restart running apps
+++++++++++++++++++++++++++++

The **apps** command lets you list and restart active applications.

Options
-------

The **apps** command has the following options:

.. list-table::
   :header-rows: 1

   * - Option
     - Description

   * - **list**
     - List all active applications

   * - **restart <APP_NAME>**
     - Restart the specified application

To list active applications, run:

.. code-block:: console

   $ unitctl apps list
   {
     "wasm": {
        "type": "wasm-wasi-component",
        "component": "/www/wasmapp-proxy-component.wasm"
     }
   }

To restart an application, run:

.. code-block:: console

   $ unitctl apps restart wasm
   {
      "success": "Ok"
   }

.. note::

   This command supports operating on multiple instances of Unit at once. To do
   this, use the **-s** option multiple times with different values:

   .. code-block:: console

      $ unitctl -s '127.0.0.1:8001' -s /run/nginx-unit.control.sock app list

++++++++++++++++++++++
Fetch active listeners
++++++++++++++++++++++

Unitctl can query a given control API to fetch all configured listeners.

To list all active listeners, run:

.. code-block:: console

   $ unitctl listeners
   No socket path provided - attempting to detect from running instance
   {
      "127.0.0.1:8080": {
         "pass": "routes"
      }
   }

.. note::

   This command supports operating on multiple instances of Unit at once. To do
   this, use the **-s** option multiple times with different values:

   .. code-block:: console

      $ unitctl -s '127.0.0.1:8001' -s /run/nginx-unit.control.sock listeners

++++++++++++++++++++++++
Check the status of Unit
++++++++++++++++++++++++

Unitctl can query the control API to provide the **status** of the running Unit
daemon.

To get the current status of the Unit, run:

.. code-block:: console

   $ unitctl status -t yaml
   No socket path provided - attempting to detect from running instance
   connections:
      accepted: 0
      active: 0
      idle: 0
      closed: 0
   requests:
      total: 0
   applications: {}

.. note::

   This command supports operating on multiple instances of Unit at once. To do
   this, use the **-s** option multiple times with different values:

   .. code-block:: console

      $ unitctl -s '127.0.0.1:8001' -s /run/nginx-unit.control.sock status

+++++++++++++++++++++++++++++++++++
Send configuration payloads to Unit
+++++++++++++++++++++++++++++++++++

With the **execute** command, Unitctl can accept custom request payloads and
query specified API endpoints with them. Use the **-f** flag to pass the request
payload as a filename or **-** to denote stdin, as shown in the example below.

.. code-block:: console

   $ echo '{
      "listeners": {
         "127.0.0.1:8080": {
               "pass": "routes"
         }
      },

      "routes": [
         {
               "action": {
                  "share": "/www/data$uri"
               }
         }
      ]
   }' | unitctl execute --http-method PUT --path /config -f -
   {
   "success": "Reconfiguration done."
   }

.. note::

   This command supports operating on multiple instances of Unit at once. To do
   this, use the **-s** option multiple times with different values:

   .. code-block:: console

      $ unitctl -s '127.0.0.1:8001' -s /run/nginx-unit.control.sock execute ...

++++++++++++++++++++++++++
Edit current configuration
++++++++++++++++++++++++++

Unitctl can fetch the configuration from a running instance of Unit and load it
in a preconfigured editor on your command line using the **edit** command.

Unitctl tries to use the editor configured with the **EDITOR** environment
variable, but defaults to vim, emacs, nano, vi, or pico if **EDITOR** is not set.

To edit the current configuration, run:

.. code-block:: console

   $ unitctl edit

The configuration loads into the editor, allowing you to make any necessary
changes. Once you save and close the editor, you see the following output:

.. code-block:: console

   {
   "success": "Reconfiguration done."
   }

.. note::

   This command does not support operating on multiple instances of Unit at once.

+++++++++++++++++++++++++++++++++++++++++
Importing the configuration from a folder
+++++++++++++++++++++++++++++++++++++++++

The **import** command lets Unitctl read configuration files, certificates, and
NJS modules from a directory. Unitctl then converts these files into a payload
to reconfigure a Unit daemon.

To export the configuration, run:

.. code-block:: console

   $ unitctl import /opt/unit/config
   Imported /opt/unit/config/certificates/snake.pem -> /certificates/snake.pem
   Imported /opt/unit/config/hello.js -> /js_modules/hello.js
   Imported /opt/unit/config/put.json -> /config
   Imported 3 files

+++++++++++++++++++++++++++++++++++++
Exporting the configuration from Unit
+++++++++++++++++++++++++++++++++++++

The **export** command queries a control API to fetch the running configuration
and NJS modules from a Unit process. The output does not include the currently
stored certificate bundles due to a technical limitation. The output is saved
as a tarball with the filename specified by the **-f** argument. You can also
use standard output with **-f -**, as shown in the examples below:

.. code-block:: console

   $ unitctl export -f config.tar

.. code-block:: console

   $ unitctl export -f -

.. code-block:: console

   $ unitctl export -f - | tar xf - config.json

.. code-block:: console

   $ unitctl export -f - > config.tar

.. warning::

   The exported configuration omits certificates.

.. note::

   This command does not support operating on multiple instances of Unit at once.

+++++++++++++++++++++++++++++++++
Wait for a socket to be available
+++++++++++++++++++++++++++++++++

All commands support waiting for Unix sockets to become available:

.. code-block:: console

   $ unitctl --wait-timeout-seconds=3 --wait-max-tries=4 import /opt/unit/config`
   Waiting for 3s control socket to be available try 2/4...
   Waiting for 3s control socket to be available try 3/4...
   Waiting for 3s control socket to be available try 4/4...
   Timeout waiting for unit to start has been exceeded
