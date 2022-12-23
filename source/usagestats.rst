 .. meta::
   :og:description: Query global and per-application usage statistics
                    from NGINX Unit.

.. include:: include/replace.rst

.. _configuration-stats:

****************
Usage Statistics
****************

Unit collects instance- and app-wide metrics,
available via the :samp:`GET`-only :samp:`/status` section of the
:ref:`control API <configuration-api>`:

.. list-table::
    :header-rows: 1

    * - Option
      - Description

    * - :samp:`connections`
      - Object;
        lists per-instance connection statistics.

    * - :samp:`requests`
      - Object;
        lists per-instance request statistics.

    * - :samp:`applications`
      - Object;
        each option item lists per-app process and request statistics.

Example:

.. code-block:: json

   {
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

The :samp:`connections` object offers the following Unit instance metrics:

.. list-table::
    :header-rows: 1

    * - Option
      - Description

    * - :samp:`accepted`
      - Integer;
        total accepted connections during the instance's lifetime.

    * - :samp:`active`
      - Integer;
        current active connections for the instance.

    * - :samp:`idle`
      - Integer;
        current idle connections for the instance.

    * - :samp:`closed`
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

The :samp:`requests` object currently exposes a single instance-wide metric:

.. list-table::
    :header-rows: 1

    * - Option
      - Description

    * - :samp:`total`
      - Integer;
        total non-API requests during the instance's lifetime.

Example:

.. code-block:: json

   "requests": {
       "total": 1307
   }

Each item in :samp:`applications` describes an app
currently listed in the :samp:`/config/applications`
:ref:`section <configuration-applications>`:

.. list-table::
    :header-rows: 1

    * - Option
      - Description

    * - :samp:`processes`
      - Object;
        lists per-app process statistics.

    * - :samp:`requests`
      - Object;
        similar to :samp:`/status/requests`,
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

The :samp:`processes` object exposes the following per-app metrics:

.. list-table::
    :header-rows: 1

    * - Option
      - Description

    * - :samp:`running`
      - Integer;
        current running app processes.

    * - :samp:`starting`
      - Integer;
        current starting app processes.

    * - :samp:`idle`
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
