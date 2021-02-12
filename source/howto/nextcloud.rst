.. include:: ../include/replace.rst

.. |app| replace:: NextCloud
.. |mod| replace:: PHP
.. |app-preq| replace:: prerequisites
.. _app-preq: https://docs.nextcloud.com/server/latest/admin_manual/installation/source_installation.html#prerequisites-for-manual-installation
.. |app-link| replace:: core files
.. _app-link: https://docs.nextcloud.com/server/latest/admin_manual/installation/command_line_installation.html

#########
NextCloud
#########

To run the `NextCloud <https://www.nextcloud.com>`__ share and collaboration
platform using Unit:

#. .. include:: ../include/howto_install_unit.rst

#. .. include:: ../include/howto_install_prereq.rst

#. .. include:: ../include/howto_install_app.rst

   .. note::

      Verify the resulting settings in :file:`/path/to/app/config/config.php`;
      in particular, check the `trusted domains
      <https://docs.nextcloud.com/server/latest/admin_manual/installation/installation_wizard.html#trusted-domains-label>`_
      to ensure the installation is accessible within your network:

    .. code-block:: php

       'trusted_domains' =>
       array (
         0 => 'localhost',
         1 => '*.example.com',
       ),

#. .. include:: ../include/howto_change_ownership.rst

#. Next, :ref:`put together <configuration-php>` the |app| configuration for
   Unit (use real values for :samp:`share` and :samp:`root`).  The following is
   based on NextCloud's own `guide
   <https://docs.nextcloud.com/server/latest/admin_manual/installation/nginx.html>`_:

   .. code-block:: json

      {
          "listeners": {
              "*:80": {
                  "pass": "routes/nextcloud"
              }
          },

          "routes": {
              "nextcloud": [
                  {
                      "match": {
                          ":nxt_hint:`uri <Denies access to files and directories best kept private>`": [
                              "/build/*",
                              "/tests/*",
                              "/config/*",
                              "/lib/*",
                              "/3rdparty/*",
                              "/templates/*",
                              "/data/*",
                              "/.*",
                              "/autotest*",
                              "/occ*",
                              "/issue*",
                              "/indie*",
                              "/db_*",
                              "/console*"
                          ]
                      },

                      "action": {
                          "return": 404
                      }
                  },
                  {
                      "match": {
                          ":nxt_hint:`uri <Serves direct URIs with dedicated scripts>`": [
                              "/core/ajax/update.php*",
                              "/cron.php*",
                              "/index.php*",
                              "/ocm-provider*.php*",
                              "/ocs-provider*.php*",
                              "/ocs/v1.php*",
                              "/ocs/v2.php*",
                              "/public.php*",
                              "/remote.php*",
                              "/status.php*",
                              "/updater*.php*"
                          ]
                      },

                      "action": {
                          "pass": "applications/nextcloud/direct"
                      }
                  },
                  {
                      "match": {
                          "uri": "/ocm-provider*"
                      },

                      "action": {
                          "pass": "applications/nextcloud/ocm"
                      }
                  },
                  {
                      "match": {
                          "uri": "/ocs-provider*"
                      },

                      "action": {
                          "pass": "applications/nextcloud/ocs"
                      }
                  },
                  {
                      "match": {
                          "uri": "/updater*"
                      },

                      "action": {
                          "pass": "applications/nextcloud/updater"
                      }
                  },
                  {
                      "action": {
                          ":nxt_hint:`share <Serves matching static files>`": ":nxt_ph:`/path/to/app/ <Use a real path in your configuration>`",
                          "fallback": {
                              "pass": "applications/nextcloud/index"
                          }
                      }
                  }
              ]
          },

          "applications": {
              "nextcloud": {
                  "type": "php",
                  "targets": {
                      "direct": {
                          "root": ":nxt_hint:`/path/to/app/ <Use a real path in your configuration>`"
                      },

                      "index": {
                          "root": ":nxt_hint:`/path/to/app/ <Use a real path in your configuration>`",
                          "script": "index.php"
                      },

                      "ocm": {
                          "root": ":nxt_hint:`/path/to/app/ocm-provider/ <Use a real path in your configuration>`",
                          "script": "index.php"
                      },


                      "ocs": {
                          "root": ":nxt_hint:`/path/to/app/ocs-provider/ <Use a real path in your configuration>`",
                          "script": "index.php"
                      },

                      "updater": {
                          "root": ":nxt_hint:`/path/to/app/nextcloud/updater/ <Use a real path in your configuration>`",
                          "script": "index.php"
                      }
                  }
              }
          }
      }

   .. note::

      The difference between the :samp:`pass` targets is their usage of the
      :samp:`script` :ref:`setting <configuration-php>`:

      - The :samp:`direct` target runs the :samp:`.php` script from the URI or
        defaults to :samp:`index.php` if the URI omits it.
      - Other targets specify the :samp:`script` that Unit runs for *any* URIs
        the target receives.

#. .. include:: ../include/howto_upload_config.rst

#. Adjust Unit's :samp:`max_body_size` :ref:`option <configuration-stngs>` to
   avoid potential issues with large file uploads, for example:

   .. code-block:: console

      # curl -X PUT -d '{"http":{"max_body_size": 2147483648}}' --unix-socket \
             /path/to/control.unit.sock http://localhost/config/settings

   After a successful update, browse to http://localhost and `set up
   <https://docs.nextcloud.com/server/latest/admin_manual/installation/installation_wizard.html>`_
   your |app| installation:

   .. image:: ../images/nextcloud.png
      :width: 100%
      :alt: NextCloud in Unit - Home Screen
