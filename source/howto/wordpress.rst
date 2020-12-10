#########
WordPress
#########

To `install WordPress
<https://wordpress.org/support/article/how-to-install-wordpress/>`_ if you
haven't already done so:

#. `Check <https://wordpress.org/support/article/before-you-install/>`_
   prerequisites and `configure
   <https://wordpress.org/support/article/creating-database-for-wordpress/>`_
   the WordPress database.

#. Download and extract WordPress `files <https://wordpress.org/download/>`_:

   .. code-block:: console

      $ cd /path/to/
      $ curl -O https://wordpress.org/latest.tar.gz
      $ tar xzf latest.tar.gz

   In this example, the files will be stored in :file:`/path/to/wordpress/`.

#. `Update <https://wordpress.org/support/article/editing-wp-config-php/>`_ the
   :file:`wp-config.php` file with your database settings and other
   customizations.

#. Set up proper `file permissions
   <https://wordpress.org/support/article/changing-file-permissions/>`_ for
   WordPress:

   .. code-block:: console

      # chown -R wp_user:wp_user /path/to/wordpress/
      # find /path/to/wordpress/ -type d -exec chmod g+s {} \;
      # chmod g+w /path/to/wordpress/wp-content
      # chmod -R g+w /path/to/wordpress/wp-content/themes
      # chmod -R g+w /path/to/wordpress/wp-content/plugins

**********
Unit Setup
**********

To run WordPress in Unit:

#. Install :ref:`Unit <installation-precomp-pkgs>` with a PHP language module.

#. .. include:: ../include/get-config.rst

#. Edit the file, adding a listener, two apps, and a route.  First, the route
   serves the :samp:`wp-admin` section of the WordPress site and other URIs
   that explicitly name the :file:`.php` file; next, it filters out static
   assets, relaying them to a :samp:`share`, and passes other requests to
   WordPress's :samp:`/index.php` via the :samp:`wp_index` app:

   .. code-block:: json

      {
          "listeners": {
              "*:8080": {
                  "pass": "routes/wordpress"
              }

          },

          "routes": {
              "wordpress": [
                  {
                      "match": {
                          "uri": [
                              "*.php",
                              "*.php/*",
                              "/wp-admin/"
                          ]
                      },

                      "action": {
                          "pass": "applications/wordpress/direct"
                      }
                  },
                  {
                      "action": {
                          "share": "/path/to/wordpress/",
                          "fallback": {
                              "pass": "applications/wordpress/index"
                          }
                      }
                  }
              ]
          },

          "applications": {
              "wordpress": {
                  "type": "php",
                  "user": "wp_user",
                  "group": "wp_user",
                  "targets": {
                      "direct": {
                          "root": "/path/to/wordpress/"
                      },

                      "index": {
                          "root": "/path/to/wordpress/",
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
      - The :samp:`index` target specifies the :samp:`script` that Unit runs
        for *any* URIs the target receives.

#. Upload the updated configuration:

   .. code-block:: console

      # curl -X PUT --data-binary @config.json --unix-socket \
             /path/to/control.unit.sock http://localhost/config

   After a successful update, browse to http://localhost and `set up
   <https://wordpress.org/support/article/how-to-install-wordpress/#step-5-run-the-install-script>`_
   your WordPress installation.

.. note::

   The resulting URI scheme will affect your WordPress configuration; updates
   may require `extra steps
   <https://wordpress.org/support/article/changing-the-site-url/>`_.
