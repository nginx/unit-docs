.. |app| replace:: WordPress
.. |mod| replace:: PHP 7.3+
.. |app-preq| replace:: prerequisites
.. _app-preq: https://wordpress.org/support/article/before-you-install/
.. |app-link| replace:: core files
.. _app-link: https://wordpress.org/download/

#########
WordPress
#########

.. note::

   For a more specific walkthrough that includes SSL setup and NGINX as a
   proxy, see our `blog post
   <https://www.nginx.com/blog/automating-installation-wordpress-with-nginx-unit-on-ubuntu/>`__.

To run the `WordPress <https://wordpress.org>`__ content management system
using Unit:

#. .. include:: ../include/howto_install_unit.rst

#. .. include:: ../include/howto_install_prereq.rst

#. .. include:: ../include/howto_install_app.rst

#. Update the :file:`wp-config.php` `file
   <https://wordpress.org/support/article/editing-wp-config-php/>`_ with your
   database settings and other customizations.

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
                      ":nxt_hint:`share <Serves matching static files>`": ":nxt_ph:`/path/to/app <Path to the application directory; use a real path in your configuration>`$uri",
                      "fallback": {
                          "pass": "applications/wordpress/index"
                      }
                  }
              }
          ],

          "applications": {
              "wordpress": {
                  "type": "php",
                  "targets": {
                      "direct": {
                          "root": ":nxt_ph:`/path/to/app/ <Path to the application directory; use a real path in your configuration>`"
                      },

                      "index": {
                          "root": ":nxt_ph:`/path/to/app/ <Path to the application directory; use a real path in your configuration>`",
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

#. .. include:: ../include/howto_upload_config.rst

   After a successful update, browse to http://localhost and `set up
   <https://wordpress.org/support/article/how-to-install-wordpress/#step-5-run-the-install-script>`_
   your |app| installation:

   .. image:: ../images/wordpress.png
      :width: 100%
      :alt: WordPress on Unit - Setup Screen

   .. note::

      The resulting URI scheme will affect your WordPress configuration; updates
      may require `extra steps
      <https://wordpress.org/support/article/changing-the-site-url/>`_.
