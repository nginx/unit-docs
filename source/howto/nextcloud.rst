:orphan:

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

      # chown -R www-data:www-data /path/to/nextcloud/

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
      $ sudo -u www-data php occ maintenance:install --database "mysql" \
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

**************
NGINX and Unit
**************

To run NextCloud in Unit:

#. Install `NGINX <https://nginx.org/en/download.html>`_.  Currently, NGINX is
   required to serve static files.

#. Install :ref:`Unit <installation-precomp-pkgs>` with a PHP language module.

#. .. include:: ../include/get-config.rst

#. Edit the file, adding an app and a listener to make NextCloud available:

   .. code-block:: json

      {
          "listeners": {
              "127.0.0.1:9000": {
                  "pass": "applications/nextcloud"
              }
          },

          "applications": {
              "nextcloud": {
                  "type": "php",
                  "user": "www-data",
                  "group": "www-data",
                  "root": "/path/to/nextcloud/"
              }
          }
      }

#. Upload the updated configuration:

   .. code-block:: console

      # curl -X PUT --data-binary @config.json --unix-socket \
             /path/to/control.unit.sock http://localhost/config

#. Set up NGINX to serve static files and route PHP requests to Unit (adopted
   from NextCloud's `guide
   <https://docs.nextcloud.com/server/16/admin_manual/installation/nginx.html>`_):

   .. code-block:: nginx

      upstream unit_nextcloud {
          server 127.0.0.1:9000;
      }

      server {
          listen 80;
          server_name nextcloud.example.com;
          root /path/to/nextcloud;

          location = /.well-known/carddav {
              return 301 $scheme://$host:$server_port/remote.php/dav;
          }

          location = /.well-known/caldav {
              return 301 $scheme://$host:$server_port/remote.php/dav;
          }

          location ~ \.(?:css|js|woff2?|svg|gif|map)$ {
              try_files $uri /index.php$request_uri;
          }

          location / {
              rewrite ^ /index.php$request_uri;
          }

          location ~ ^\/(?:build|tests|config|lib|3rdparty|templates|data)\/ {
              deny all;
          }

          location ~ ^\/(?:\.|autotest|occ|issue|indie|db_|console) {
              deny all;
          }

          location ~ ^\/(?:index|remote|public|cron|core\/ajax\/update|status|ocs\/v[12]|updater\/.+|oc[ms]-provider\/.+)\.php(?:$|\/) {
              proxy_pass http://unit_nextcloud;
              proxy_set_header Host $host;
          }

          location ~ ^\/(?:updater|oc[ms]-provider)(?:$|\/) {
              try_files $uri/ =404;
              index index.php;
          }

          location ~ \.(?:css|js|woff2?|svg|gif|map)$ {
              try_files $uri /index.php$request_uri;
          }

          location ~ \.(?:png|html|ttf|ico|jpg|jpeg|bcmap)$ {
              try_files $uri /index.php$request_uri;
          }
      }

   .. note::

      If you use the above config for your purposes, make sure to replace
      placeholders, such as :samp:`/path/to/nextcloud/` in :samp:`root`.
      For details, refer to `NGINX Admin Guide
      <https://docs.nginx.com/nginx/admin-guide/>`_.

Finally, browse to your NextCloud site and complete the installation:

   .. image:: ../images/nextcloud.png
      :width: 100%
      :alt: NextCloud in Unit - Home Screen
