.. include:: ../include/replace.rst

#########
NextCloud
#########

.. note::

   This howto uses NextCloud |_| 16, PHP |_| 7.3, MariaDB, and :program:`apt`;
   adjust it to your scenario as needed.

To `install NextCloud
<https://docs.nextcloud.com/server/16/admin_manual/installation/index.html>`_
if you haven't already done so:

#. Download and extract NextCloud `files
   <https://download.nextcloud.com/server/releases/nextcloud-16.0.4.tar.bz2>`_:

   .. code-block:: console

      $ cd /path/to/
      $ curl -O https://download.nextcloud.com/server/releases/nextcloud-16.0.4.tar.bz2
      $ tar xf nextcloud-16.0.4.tar.bz2

   This creates the :file:`/path/to/nextcloud` directory.

#. Change the directory ownership, supplying a username that will be used to
   configure and run Nextcloud:

   .. code-block:: console

      # chown -R nc_user:nc_user /path/to/nextcloud/

#. Install and check NextCloud's `prerequisites
   <https://docs.nextcloud.com/server/16/admin_manual/installation/source_installation.html#prerequisites-for-manual-installation>`_:

   .. code-block:: console

      # apt install mariadb-server
      # apt install php7.3 php7.3-imagick php7.3-curl php7.3-gd php7.3-intl \
            php7.3-mbstring php7.3-mysql php7.3-xml php7.3-zip
      $ mysql --version
      $ php --version

#. Set up the NextCloud database (note the sample credentials):

   .. code-block:: console

      # mysql -u root -p

          > CREATE DATABASE nextcloud;
          > CREATE USER 'nextuser'@'localhost' IDENTIFIED BY 'nextpass';
          > GRANT ALL PRIVILEGES ON nextcloud.* TO 'nextuser'@'localhost';
          > FLUSH PRIVILEGES;

#. Finish the installation (here, the :program:`occ` `utility
   <https://docs.nextcloud.com/server/16/admin_manual/configuration_server/occ_command.html>`_
   is used; note the credentials and the :program:`sudo -u` username):

   .. code-block:: console

      $ cd /path/to/nextcloud/
      $ sudo -u nc_user php occ maintenance:install --database "mysql" \
             --database-name "nextcloud" --database-user "nextuser"     \
             --database-pass "nextpass" --admin-user "admin" --admin-pass "adminpass"

            Nextcloud was successfully installed

   .. note::

      Verify the resulting settings in
      :file:`/path/to/nextcloud/config/config.php`; in particular, check the
      `trusted domains
      <https://docs.nextcloud.com/server/16/admin_manual/installation/installation_wizard.html#trusted-domains-label>`_
      to ensure your installation will be accessible from within your network:

    .. code-block:: php

       'trusted_domains' =>
       array (
         0 => 'localhost',
         1 => '*.example.com',
       ),

****
Unit
****

To run NextCloud in Unit:

#. Install :ref:`Unit <installation-precomp-pkgs>` with a PHP language module.

#. .. include:: ../include/get-config.rst

#. Edit the configuration, adding a listener, routes, and an app (based on
   NextCloud's own `guide
   <https://docs.nextcloud.com/server/16/admin_manual/installation/nginx.html>`_):

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
                          "uri": [
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
                          "share": "/dev/null/"
                      }
                  },
                  {
                      "match": {
                          "uri": [
                              "/core/ajax/update.php*",
                              "/cron.php*",
                              "/index.php*",
                              "/ocs/v1.php*",
                              "/ocs/v2.php*",
                              "/public.php*",
                              "/remote.php*",
                              "/status.php*"
                          ]
                      },

                      "action": {
                          "pass": "applications/nextcloud/direct"
                      }
                  },
                  {
                      "match": {
                          "uri": [
                              "/ocm-provider*",
                              "/ocs-provider*",
                              "/updater*"
                          ]
                      },

                      "action": {
                          "pass": "routes/nextcloud_fallthrough"
                      }
                  },
                  {
                      "action": {
                          "share": "/path/to/nextcloud/",
                          "fallback": {
                              "pass": "applications/nextcloud/index"
                          }
                      }
                  }
              ],

              "nextcloud_fallthrough": [
                  {
                      "match": {
                          "uri": "*.php*"
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
                      "action": {
                          "pass": "applications/nextcloud/updater"
                      }
                  }
              ]
          },

          "applications": {
              "nextcloud": {
                  "type": "php",
                  "user": "nc_user",
                  "group": "nc_user",
                  "targets": {
                      "direct": {
                          "root": "/path/to/nextcloud/"
                      },

                      "index": {
                          "root": "/path/to/nextcloud/",
                          "script": "index.php"
                      },

                      "ocm": {
                          "root": "/path/to/nextcloud/ocm-provider/",
                          "script": "index.php"
                      },


                      "ocs": {
                          "root": "/path/to/nextcloud/ocs-provider/",
                          "script": "index.php"
                      },

                      "updater": {
                          "root": "/path/to/nextcloud/updater/",
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
      - Other targers specify the :samp:`script` that Unit runs for *any* URIs
        the target receives.

#. Upload the updated configuration:

   .. code-block:: console

      # curl -X PUT --data-binary @config.json --unix-socket \
             /path/to/control.unit.sock http://localhost/config

#. Adjust Unit's :samp:`max_body_size` :ref:`option <configuration-stngs>` to
   avoid potential issues with large file uploads, for example:

   .. code-block:: console

      # curl -X PUT -d '{"http":{"max_body_size": 2147483648}}' --unix-socket \
             /path/to/control.unit.sock http://localhost/config/settings

Finally, browse to your NextCloud site and complete the installation:

   .. image:: ../images/nextcloud.png
      :width: 100%
      :alt: NextCloud in Unit - Home Screen
