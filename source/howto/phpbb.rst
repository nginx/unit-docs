#####
phpBB
#####

To install the `phpBB <https://www.phpbb.com>`_ bulletin board using Unit:

#. Install :ref:`Unit <installation-precomp-pkgs>` with a PHP language module.

#. Check and configure phpBB's `prerequisites
   <https://www.phpbb.com/support/docs/en/3.3/ug/quickstart/requirements/>`_.

#. Download and extract phpBB `files <https://www.phpbb.com/downloads/>`_:

   .. code-block:: console

      $ cd /path/to/phpbb/
      $ curl -O https://download.phpbb.com/pub/release/3.3/3.3.0/phpBB-3.3.0.zip
      $ unzip phpBB-3.3.0.zip
      $ mv :nxt_term:`phpBB3/* <optional, directory path normalization>` ./ && rm -rf phpBB3/
      # chown -R :nxt_term:`phpbb_user:phpbb_group <Used to configure the apps in Unit>` .

   In this example, the files will be stored in :file:`/path/to/phpbb/`.

#. Next, prepare and upload the app configuration to Unit:

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
                          "pass": "applications/phpbb_direct"
                      }
                  },
                  {
                      "action": {
                          ":nxt_term:`share <Serves static content>`": "/path/to/phpbb/",
                          ":nxt_term:`fallback <Catch-all for requests not yet served by other rules>`": {
                              "pass": "applications/phpbb_index"
                          }
                      }
                  }
              ]
          },

          "applications": {
              "phpbb_direct": {
                  "type": "php",
                  "user": ":nxt_term:`phpbb_user <Username that Unit runs the app as, with access to /path/to/phpbb/>`",
                  "root": "/path/to/phpbb/"
              },

              
              "phpbb_index": {
                  "type": "php",
                  "user": ":nxt_term:`phpbb_user <Username that Unit runs the app as, with access to /path/to/phpbb/>`",
                  "root": "/path/to/phpbb/",
                  "script": "app.php"
              }
          }
      }

   .. note::

      The difference between the apps is their usage of the :samp:`script`
      :ref:`setting <configuration-php>`.  Here, :samp:`phpbb_index` specifies
      the :samp:`script` that Unit runs for *any* URIs the app receives.  In
      contrast, the :samp:`phpbb_direct` app serves URIs that reference a
      specific :samp:`.php` file by running it; if there's no file specified,
      it defaults to :samp:`index.php`.

#. Assuming the config above is saved as :file:`phpbb.json`:

   .. code-block:: console

      # curl -X PUT --data-binary @phpbb.json --unix-socket \
             /path/to/control.unit.sock http://localhost/config

#. Browse to :samp:`/install/app.php` to configure the settings from Step 2 and
   complete your installation.  Having done that, delete the :file:`install/`
   subdirectory to mitigate security risks:

   .. code-block:: console

      $ rm -rf /path/to/phpbb/install/

   Finally, your board is ready!

   .. image:: ../images/phpbb.png
      :width: 100%
      :alt: phpBB on Unit
