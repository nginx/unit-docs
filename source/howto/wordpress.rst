:orphan:

#########
WordPress
#########

To `install WordPress <https://codex.wordpress.org/Installing_WordPress>`_ if
you haven't already done so:

#. `Check <https://wordpress.org/about/requirements/>`_ prerequisites and
   `configure
   <https://codex.wordpress.org/Installing_WordPress#Step_2:_Create_the_Database_and_a_User>`_
   the WordPress database.

#. Download and extract WordPress `files <https://wordpress.org/download/>`_:

   .. code-block:: console

      $ cd /path/to/
      $ wget https://wordpress.org/latest.tar.gz
      $ tar xzvf latest.tar.gz

   In this example, the files will be stored in :file:`/path/to/wordpress/`.

#. `Update <https://codex.wordpress.org/Editing_wp-config.php>`_ the
   :file:`wp-config.php` file with your database settings and other
   customizations.

#. Set up proper `file permissions
   <https://codex.wordpress.org/Changing_File_Permissions>`_ for WordPress:

   .. code-block:: console

      # chown -R wpuser:www-data /path/to/wordpress/
      # find /path/to/wordpress/ -type d -exec chmod g+s {} \;
      # chmod g+w /path/to/wordpress/wp-content
      # chmod -R g+w /path/to/wordpress/wp-content/themes
      # chmod -R g+w /path/to/wordpress/wp-content/plugins

**************
NGINX and Unit
**************

To run WordPress in Unit:

#. Install `NGINX <https://nginx.org/en/download.html>`_.  Currently, NGINX is
   required to serve static files.

#. Install :ref:`Unit <installation-precomp-pkgs>` with a PHP language module.

#. .. include:: ../include/get-config.rst

#. Edit the file, adding two apps and their listeners to serve direct and
   indirect WordPress URLs:

   .. code-block:: json

      {
          "listeners": {
              "127.0.0.1:8090": {
                  "pass": "applications/wp_index"
              },

              "127.0.0.1:8091": {
                  "pass": "applications/wp_direct"
              }
          },

          "applications": {
              "wp_index": {
                  "type": "php",
                  "user": "wpuser",
                  "group": "www-data",
                  "root": "/path/to/wordpress/",
                  "script": "index.php"
              },

              "wp_direct": {
                  "type": "php",
                  "user": "wpuser",
                  "group": "www-data",
                  "root": "/path/to/wordpress/",
                  "index": "index.php"
              }
          }
      }

   .. note::

      The difference between the two apps is their usage of :samp:`script` and
      :samp:`index` :ref:`settings <configuration-php>`.  Here,
      :samp:`wp_index` specifies the :samp:`script` that Unit will run for
      *any* URL it receives (with WordPress, this is typical of the
      :file:`index.php`).  The :samp:`wp_direct` app will serve URLs that
      explicitly specify a PHP file name.  This isolates the :samp:`wp-admin`
      section from the rest of WordPress, allowing to maintain different
      per-app settings.

#. Upload the updated configuration:

   .. code-block:: console

      $ curl -X PUT --data-binary @config.json --unix-socket \
             /path/to/control.unit.sock http://localhost/config

#. Configure NGINX to serve static files and route requests between the apps
   you have set up in Unit:

   .. code-block:: nginx

      upstream unit_wp_index {
          server 127.0.0.1:8090;
      }

      upstream unit_wp_direct {
          server 127.0.0.1:8091;
      }

      server {
          listen      80;
          server_name localhost;
          root        /path/to/wordpress/;

          location / {
              try_files $uri @index_php;
          }

          location @index_php {
              proxy_pass       http://unit_wp_index;
              proxy_set_header Host $host;
          }

          location /wp-admin {
              index index.php;
          }

          location ~* \.php$ {
              try_files        $uri =404;
              proxy_pass       http://unit_wp_direct;
              proxy_set_header Host $host;
          }
      }

   For details, refer to `NGINX Admin Guide
   <https://docs.nginx.com/nginx/admin-guide/>`_.

Finally, browse to your WordPress site and `complete the installation
<https://codex.wordpress.org/Installing_WordPress#Finishing_installation>`_.

.. note::

   Resulting URL scheme will trickle into your WordPress configuration;
   updates may require `extra steps
   <https://codex.wordpress.org/Changing_The_Site_URL>`_.

***************
Further Reading
***************

See a detailed walkthrough in our blog:
https://www.nginx.com/blog/installing-wordpress-with-nginx-unit/
