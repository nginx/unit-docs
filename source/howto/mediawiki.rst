.. |app| replace:: MediaWiki
.. |mod| replace:: PHP
.. |app-link| replace:: core files
.. _app-link: https://www.mediawiki.org/wiki/Download

#########
MediaWiki
#########

To run the `MediaWiki <https://www.mediawiki.org>`_ collaboration and
documentation platform using Unit:

#. .. include:: ../include/howto_install_unit.rst

#. .. include:: ../include/howto_install_app.rst

#. .. include:: ../include/howto_change_ownership.rst

#. Next, :ref:`prepare <configuration-php>` the |app| configuration for Unit
   (use real values for :samp:`share` and :samp:`root`):

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
                      ":nxt_hint:`uri <Controls access to directories best kept private>`": [
                          "!/tests/qunit/*",
                          "/cache/*",
                          "/includes/*",
                          "/languages/*",
                          "/maintenance/*",
                          "/tests/*",
                          "/vendor/*"
                      ]
                  },

                  "action": {
                      "return": 404
                  }
              },
              {
                  "match": {
                      ":nxt_hint:`uri <Enables access to application entry points>`": [
                          "/api.php*",
                          "/img_auth.php*",
                          "/index.php*",
                          "/load.php*",
                          "/mw-config/*.php",
                          "/opensearch_desc.php*",
                          "/profileinfo.php*",
                          "/rest.php*",
                          "/tests/qunit/*.php",
                          "/thumb.php*",
                          "/thumb_handler.php*"
                      ]
                  },

                  "action": {
                      "pass": "applications/mw/direct"
                  }
              },
              {
                  "match": {
                      ":nxt_hint:`uri <Enables static access to specific content locations>`": [
                          "!*.php",
                          "!*.json",
                          ":nxt_hint:`!*.htaccess <The negations deny access to the file types listed here>`",
                          "/extensions/*",
                          "/images/*",
                          "/resources/assets/*",
                          "/resources/lib/*",
                          "/resources/src/*",
                          "/skins/*"
                      ]
                  },

                  "action": {
                      ":nxt_hint:`share <Serves matching static files>`": ":nxt_ph:`/path/to/app <Path to the application directory; use a real path in your configuration>`$uri"
                  }
              },
              {
                  "action": {
                      "pass": "applications/mw/index"
                  }
              }
          ],

          "applications": {
              "mw": {
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

   .. note::

      The difference between the :samp:`pass` targets is their usage of the
      :samp:`script` :ref:`setting <configuration-php>`:

      - The :samp:`direct` target runs the :samp:`.php` script from the URI or
        defaults to :samp:`index.php` if the w omits it.

      - The :samp:`index` target specifies the :samp:`script` that Unit runs
        for *any* URIs the target receives.

#. .. include:: ../include/howto_upload_config.rst

#. Browse to http://localhost/mw-config/index.php and set |app| up using
   the settings noted earlier:

   .. image:: ../images/mw_install.png
      :width: 100%
      :alt: MediaWiki on Unit

   Download the newly generated :file:`LocalSettings.php` file and place it
   `appropriately <https://www.mediawiki.org/wiki/Manual:Config_script>`_:

   .. code-block:: console

      $ chmod 600 LocalSettings.php
      # chown :nxt_ph:`unit:unit <Values from Step 3>` LocalSettings.php
      # mv LocalSettings.php :nxt_ph:`/path/to/app/ <Path to the application directory; use a real path in your configuration>`

#. After installation, add a match condition to the first step to disable
   access to the :file:`mw-config/` directory:

   .. code-block:: console

      # curl -X POST -d '"/mw-config/*"'  \
             --unix-socket :nxt_ph:`/path/to/control.unit.sock <Path to Unit's control socket in your installation>`  \
             http://localhost:nxt_hint:`/config/routes/mediawiki/0/match/uri/ <Path to the route's first step condition and the 'uri' value in it>`

            {
                "success": "Reconfiguration done."
            }

   After a successful update, |app| should be available on the listener’s IP
   address and port:

   .. image:: ../images/mw_ready.png
      :width: 100%
      :alt: MediaWiki on Unit
