.. |app| replace:: MODX
.. |mod| replace:: PHP
.. |app-preq| replace:: prerequisites
.. _app-preq: https://docs.modx.com/current/en/getting-started/server-requirements
.. |app-link| replace:: core files
.. _app-link: https://modx.com/download

####
MODX
####

To run the `MODX <https://modx.com>`_ content application platform using Unit:

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
                      ":nxt_hint:`uri <Denies access to directories best kept private>`": [
                          "!/.well-known/",
                          "/core/*",
                          "*/.*"
                      ]
                  },

                  "action": {
                      "return": 404
                  }
              },
              {
                  "match": {
                      ":nxt_hint:`uri <Serves direct requests for PHP scripts>`": "*.php"
                  },

                  "action": {
                      "pass": "applications/modx"
                  }
              },
              {
                  "action": {
                      ":nxt_hint:`share <Serves static files>`": ":nxt_ph:`/path/to/app <Path to the application directory; use a real path in your configuration>`$uri",
                      "fallback": {
                          "pass": ":nxt_hint:`applications/modx <A catch-all destination for the remaining requests>`"
                      }
                  }
              }
          ],

          "applications": {
              "modx": {
                  "type": "php",
                  "root": ":nxt_ph:`/path/to/app/ <Path to the application directory; use a real path in your configuration>`"
              }
          }
      }

#. .. include:: ../include/howto_upload_config.rst

   After a successful update, |app| should be available on the listener’s IP
   address and port:

   .. image:: ../images/modx.png
      :width: 100%
      :alt: MODX on Unit - Manager Screen
