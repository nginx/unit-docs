.. |app| replace:: Matomo
.. |mod| replace:: PHP
.. |app-preq| replace:: prerequisites
.. _app-preq: https://matomo.org/docs/requirements/
.. |app-link| replace:: core files
.. _app-link: https://matomo.org/docs/installation/

######
Matomo
######

To run the `Matomo <https://matomo.org>`_ web analytics platform using Unit:

#. .. include:: ../include/howto_install_unit.rst

#. .. include:: ../include/howto_install_prereq.rst

#. .. include:: ../include/howto_install_app.rst

#. .. include:: ../include/howto_change_ownership.rst

#. Next, :ref:`prepare <configuration-php>` the |app| configuration for Unit
   (use real values for :samp:`share` and :samp:`root`).  The default
   :file:`.htaccess` scheme in a |app| installation roughly translates into the
   following:

   .. code-block:: json

      {
          "listeners": {
              "*:80": {
                  "pass": "routes"
              }
          },

          "routes": [
              {
                  "match": {
                      ":nxt_hint:`uri <Handles all PHP scripts that should be public>`": [
                          "/index.php",
                          "/js/index.php",
                          "/matomo.php",
                          "/misc/cron/archive.php",
                          "/piwik.php",
                          "/plugins/HeatmapSessionRecording/configs.php"
                      ]
                  },

                  "action": {
                      "pass": "applications/matomo/direct"
                  }
              },
              {
                  "match": {
                      ":nxt_hint:`uri <Denies access to files and directories best kept private, including internal PHP scripts>`": [
                          "*.php",
                          "*/.htaccess",
                          "/config/*",
                          "/core/*",
                          "/lang/*",
                          "/tmp/*"
                      ]
                  },

                  "action": {
                      "return": 404
                  }
              },
              {
                  "match": {
                      "uri": ":nxt_hint:`~\\.(css|gif|html?|ico|jpg|js(on)?|png|svg|ttf|woff2?)$ <Enables access to static content only>`"
                  },

                  "action": {
                      ":nxt_hint:`share <Serves matching static files>`": ":nxt_ph:`/path/to/app <Path to the application directory; use a real path in your configuration>`$uri"
                  }
              },
              {
                  "match": {
                      ":nxt_hint:`uri <Disables access to certain directories that may nonetheless contain public-facing static content served by the previous rule; forwards all unhandled requests to index.php in the root directory>`": [
                          "!/libs/*",
                          "!/node_modules/*",
                          "!/plugins/*",
                          "!/vendor/*",
                          "!/misc/cron/*",
                          "!/misc/user/*"
                      ]
                  },

                  "action": {
                      ":nxt_hint:`share <Serves remaining static files>`": ":nxt_ph:`/path/to/app <Path to the application directory; use a real path in your configuration>`$uri",
                      "fallback": {
                          "pass": ":nxt_hint:`applications/matomo/index <A catch-all destination for the remaining requests>`"
                      }
                  }
              }
          ],

          "applications": {
              "matomo": {
                  "type": "php",
                  "targets": {
                      "direct": {
                          "root": ":nxt_ph:`/path/to/app/ <Path to the application directory; use a real path in your configuration>`"
                      },

                      "index": {
                          "root": ":nxt_ph:`/path/to/app/ <Path to the application directory; use a real path in your configuration>`",
                          "script": ":nxt_hint:`index.php <All requests are handled by a single script>`"
                      }
                  }
              }
          }
      }

#. .. include:: ../include/howto_upload_config.rst

   After a successful update, |app| should be available on the listener’s IP
   address and port:

   .. image:: ../images/matomo.png
      :width: 100%
      :alt: Matomo on Unit
