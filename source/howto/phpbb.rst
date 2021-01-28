.. |app| replace:: phpBB
.. |mod| replace:: PHP
.. |app-preq| replace:: prerequisites
.. _app-preq: https://www.phpbb.com/support/docs/en/3.3/ug/quickstart/requirements/
.. |app-link| replace:: core files
.. _app-link: https://www.phpbb.com/downloads/

#####
phpBB
#####

To run the `phpBB <https://www.phpbb.com>`_ bulletin board using Unit:

#. .. include:: ../include/howto_install_unit.rst

#. .. include:: ../include/howto_install_prereq.rst

#. .. include:: ../include/howto_install_app.rst

#. .. include:: ../include/howto_change_ownership.rst

#. Next, prepare the app :ref:`configuration <configuration-php>` for Unit (use
   real values for :samp:`share`, :samp:`root`, :samp:`user`, and
   :samp:`group`):

   .. code-block:: json

      {
          "listeners": {
              "*:80": {
                  "pass": "routes/phpbb"
              }

          },

          "routes": {
              "phpbb": [
                  {
                      "match": {
                          ":nxt_term:`uri <Denies access to files and directories best kept private>`": [
                              "/cache/*",
                              "/common.php*",
                              "/config.php*",
                              "/config/*",
                              "/db/migration/data/*",
                              "/files/*",
                              "/images/avatars/upload/*",
                              "/includes/*",
                              "/store/*"
                          ]
                      },

                      "action": {
                          "return": 403
                      }
                  },
                  {
                      "match": {
                          "uri": [
                              "*.php",
                              "*.php/*"
                          ]
                      },

                      "action": {
                          "pass": "applications/phpbb/direct"
                      }
                  },
                  {
                      "action": {
                          "share": ":nxt_term:`/path/to/app/ <Serves static content>`",
                          "fallback": {
                              "pass": ":nxt_term:`applications/phpbb/index <Catch-all for requests not yet served by other rules>`"
                          }
                      }
                  }
              ]
          },

          "applications": {
              "phpbb": {
                  "type": "php",
                  "user": ":nxt_term:`app_user <User and group values must have access to the app root directory>`",
                  "group": "app_group",
                  "targets": {
                      "direct": {
                          "root": ":nxt_term:`/path/to/app/ <Use a real path in your configuration>`"
                      },

                      "index": {
                          "root": ":nxt_term:`/path/to/app/ <Use a real path in your configuration>`",
                          "script": "app.php"
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
      - The :samp:`index` target specifies the :samp:`script` that Unit runs
        for *any* URIs the target receives.

#. .. include:: ../include/howto_upload_config.rst

   After a successful update, your app should be available on the listener’s IP
   address and port:

   .. image:: ../images/phpbb.png
      :width: 100%
      :alt: phpBB on Unit

#. Browse to :samp:`/install/app.php` to complete your installation.  Having
   done that, delete the :file:`install/` subdirectory to mitigate security
   risks:

   .. code-block:: console

      $ rm -rf /path/to/app/install/
