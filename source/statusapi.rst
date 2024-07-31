 .. meta::
   :og:description: Query global and per-application usage statistics
                    from NGINX Unit.

.. include:: include/replace.rst

.. _configuration-stats:

****************
Status API
****************

Unit collects information about the loaded language models, as well as
instance- and app-wide metrics, and makes them available via the **GET**-only
**/status** section of the :ref:`control API <configuration-api>`:

.. list-table::
    :header-rows: 1

    * - Option
      - Description

    * - **modules**
      - Object;
        lists currently loaded language modules.

    * - **connections**
      - Object;
        lists per-instance connection statistics.

    * - **requests**
      - Object;
        lists per-instance request statistics.

    * - **applications**
      - Object;
        each option item lists per-app process and request statistics.

Example:

.. code-block:: json

   {
       "modules": {
           "python": [
               {
                   "version": "3.12.3",
                   "lib": "/opt/unit/modules/python.unit.so"
               },
               {
                   "version": "3.8",
                   "lib": "/opt/unit/modules/python-3.8.unit.so"
               }
           ],

           "php": {
              "version": "8.3.4",
              "lib": "/opt/unit/modules/php.unit.so"
           }
       },

       "connections": {
           "accepted": 1067,
           "active": 13,
           "idle": 4,
           "closed": 1050
       },

       "requests": {
           "total": 1307
       },

       "applications": {
           "wp": {
               "processes": {
                   "running": 14,
                   "starting": 0,
                   "idle": 4
               },

               "requests": {
                   "active": 10
               }
           }
       }
   }

Each item in the **modules** object lists one of the currently loaded language
modules, the installed version (or versions) of the module, and the path to the
module file:

.. list-table::
    :header-rows: 1

    * - Option
      - Description

    * - **name**
      - String;
        language module name.

    * - **version**
      - String;
        language module version. If multiple versions are loaded,
        the list contains multiple items.

    * - **lib**
      - String;
        path to the language module file.

The **connections** object offers the following Unit instance metrics:

.. list-table::
    :header-rows: 1

    * - Option
      - Description

    * - **accepted**
      - Integer;
        total accepted connections during the instance's lifetime.

    * - **active**
      - Integer;
        current active connections for the instance.

    * - **idle**
      - Integer;
        current idle connections for the instance.

    * - **closed**
      - Integer;
        total closed connections during the instance's lifetime.

Example:

.. code-block:: json

   "connections": {
       "accepted": 1067,
       "active": 13,
       "idle": 4,
       "closed": 1050
   }

.. note::

   For details of instance connection management,
   refer to
   :ref:`configuration-stngs`.

The **requests** object currently exposes a single instance-wide metric:

.. list-table::
    :header-rows: 1

    * - Option
      - Description

    * - **total**
      - Integer;
        total non-API requests during the instance's lifetime.

Example:

.. code-block:: json

   "requests": {
       "total": 1307
   }

Each item in **applications** describes an app
currently listed in the **/config/applications**
:ref:`section <configuration-applications>`:

.. list-table::
    :header-rows: 1

    * - Option
      - Description

    * - **processes**
      - Object;
        lists per-app process statistics.

    * - **requests**
      - Object;
        similar to **/status/requests**,
        but includes only the data for a specific app.

Example:

.. code-block:: json

   "applications": {
       "wp": {
           "processes": {
               "running": 14,
               "starting": 0,
               "idle": 4
           },

           "requests": {
               "active": 10
           }
       }
   }

The **processes** object exposes the following per-app metrics:

.. list-table::
    :header-rows: 1

    * - Option
      - Description

    * - **running**
      - Integer;
        current running app processes.

    * - **starting**
      - Integer;
        current starting app processes.

    * - **idle**
      - Integer;
        current idle app processes.

Example:

.. code-block:: json

   "processes": {
       "running": 14,
       "starting": 0,
       "idle": 4
   }

.. note::

   For details of per-app process management,
   refer to
   :ref:`configuration-proc-mgmt`.
