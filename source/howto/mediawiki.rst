:orphan:

#########
MediaWiki
#########

To install a `MediaWiki <https://www.mediawiki.org/>`_ server using Unit:

#. Install :ref:`Unit <installation-precomp-pkgs>` with a PHP language module.

#. Check and configure MediaWiki's `prerequisites
   <https://www.mediawiki.org/wiki/Manual:Installation_requirements>`_.

#. Download and extract MediaWiki `files
   <https://www.mediawiki.org/wiki/Download>`_:

   .. code-block:: console

      $ mkdir -p /path/to/mediawiki/ /tmp/mediawiki/ && cd :nxt_term:`/tmp/mediawiki/ <Temporary location to download files to>`
      $ curl -O https://releases.wikimedia.org/mediawiki/1.34/mediawiki-1.34.1.tar.gz
      $ tar xzf mediawiki-1.34.1.tar.gz --strip-components 1 -C :nxt_term:`/path/to/mediawiki/ <Target installation location>`
      # chown -R :nxt_term:`mw_user:mw_group <Used to configure the app in Unit>` /path/to/mediawiki/

   In this example, the files will be stored in :file:`/path/to/mediawiki/`.

#. Next, prepare and upload the app configuration to Unit:

   .. code-block:: json

      {
          "listeners": {
              "*:80": {
                  "pass": "routes/mediawiki"
              }

          },

          "routes": {
              "mediawiki": [
                  {
                      "match": {
                          ":nxt_term:`uri <Controls access to directories best kept private>`": [
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
                          "return": 403
                      }
                  },
                  {
                      "match": {
                          ":nxt_term:`uri <Enables access to application entry points>`": [
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
                          "pass": "applications/mw_direct"
                      }
                  },
                  {
                      "match": {
                          ":nxt_term:`uri <Enables static access to specific content locations>`": [
                              "!*.php",
                              "!*.json",
                              "!*.:nxt_term:`htaccess <The negations deny access to file types listed here>`",
                              "/extensions/*",
                              "/images/*",
                              "/resources/assets/*",
                              "/resources/lib/*",
                              "/resources/src/*",
                              "/skins/*"
                          ]
                      },

                      "action": {
                          "share": "/path/to/mediawiki/"
                      }
                  },
                  {
                      "action": {
                          "pass": "applications/mw_index"
                      }
                  }
              ]
          },

          "applications": {
              "mw_direct": {
                  "type": "php",
                  "user": ":nxt_term:`mw_user <Username that Unit runs the app as, with access to /path/to/mediawiki/>`",
                  "root": "/path/to/mediawiki/"
              },

              "mw_index": {
                  "type": "php",
                  "user": ":nxt_term:`mw_user <Username that Unit runs the app as, with access to /path/to/mediawiki/>`",
                  "root": "/path/to/mediawiki/",
                  "script": "index.php"
              }
          }
      }

   .. note::

      The difference between the apps is their usage of the :samp:`script`
      :ref:`setting <configuration-php>`.  Here, :samp:`mw_index` specifies the
      :samp:`script` that Unit runs for *any* URIs the app receives.  In
      contrast, the :samp:`mw_direct` app serves URIs that reference a specific
      :samp:`.php` file by running it; if there's no file specified, it
      defaults to :samp:`index.php`.

#. Assuming the config above is saved as :file:`mediawiki.json`:

   .. code-block:: console

      # curl -X PUT --data-binary @mediawiki.json --unix-socket \
             /path/to/control.unit.sock http://localhost/config

#. Browse to :samp:`/mw-config/index.php` to configure the settings from Step 2
   and complete your installation:

   .. image:: ../images/mw_install.png
      :width: 100%
      :alt: MediaWiki on Unit

   Download the :file:`LocalSettings.php` file created here and place it
   `appropriately <https://www.mediawiki.org/wiki/Manual:Config_script>`_:

   .. code-block:: console

      $ mv LocalSettings.php /path/to/mediawiki/
      $ chmod 600 /path/to/mediawiki/LocalSettings.php
      # chown mw_user /path/to/mediawiki/LocalSettings.php


#. After installation, add a match condition to the first step to disable
   access to the :file:`mw-config/` directory:

   .. code-block:: console

      # curl -X POST -d '"/mw-config/*"' --unix-socket \
             /path/to/control.unit.sock                \
             http://localhost/config/routes/mediawiki/0/match/uri/

            {
                "success": "Reconfiguration done."
            }

   Finally, your wiki is ready!

   .. image:: ../images/mw_ready.png
      :width: 100%
      :alt: MediaWiki on Unit
