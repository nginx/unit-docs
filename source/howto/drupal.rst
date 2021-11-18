.. |app| replace:: Drupal
.. |mod| replace:: PHP
.. |app-preq| replace:: prerequisites
.. _app-preq: https://www.drupal.org/docs/system-requirements
.. |app-link| replace:: core files
.. _app-link: https://www.drupal.org/docs/develop/using-composer/using-composer-to-install-drupal-and-manage-dependencies#download-core

######
Drupal
######

To run the `Drupal <https://www.drupal.org>`_ content management system using
Unit:

#. .. include:: ../include/howto_install_unit.rst

#. .. include:: ../include/howto_install_prereq.rst

#. .. include:: ../include/howto_install_app.rst

#. .. include:: ../include/howto_change_ownership.rst

#. Next, :ref:`prepare <configuration-php>` the |app| configuration for Unit.
   The default :file:`.htaccess` `scheme <https://github.com/drupal/drupal>`__
   in a |app| installation roughly translates into the following (use real
   values for :samp:`share` and :samp:`root`):

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
                      ":nxt_hint:`uri <Denies access to certain types of files and directories best kept hidden, allows access to well-known locations according to RFC 5785>`": [
                          "!*/.well-known/*",
                          "/vendor/*",
                          "/core/profiles/demo_umami/modules/demo_umami_content/default_content/*",
                          "*.engine",
                          "*.inc",
                          "*.install",
                          "*.make",
                          "*.module",
                          "*.po",
                          "*.profile",
                          "*.sh",
                          "*.theme",
                          "*.tpl",
                          "*.twig",
                          "*.xtmpl",
                          "*.yml",
                          "*/.*",
                          "*/Entries*",
                          "*/Repository",
                          "*/Root",
                          "*/Tag",
                          "*/Template",
                          "*/composer.json",
                          "*/composer.lock",
                          "*/web.config",
                          "*sql",
                          "*.bak",
                          "*.orig",
                          "*.save",
                          "*.swo",
                          "*.swp",
                          "*~"
                      ]
                  },

                  "action": {
                      "return": 404
                  }
              },
              {
                  "match": {
                      ":nxt_hint:`uri <Allows direct access to core PHP scripts>`": [
                          "/core/authorize.php",
                          "/core/core.api.php",
                          "/core/globals.api.php",
                          "/core/install.php",
                          "/core/modules/statistics/statistics.php",
                          "~^/core/modules/system/tests/https?\\.php",
                          "/core/rebuild.php",
                          "/update.php"
                      ]
                  },

                  "action": {
                      "pass": "applications/drupal/direct"
                  }
              },
              {
                  "match": {
                      ":nxt_hint:`uri <Explicitly denies access to any PHP scripts other than index.php>`": [
                          "!/index.php*",
                          "*.php"
                      ]
                  },

                  "action": {
                      "return": 404
                  }
              },
              {
                  "action": {
                      ":nxt_hint:`share <Serves static files>`": ":nxt_ph:`/path/to/app/web <Path to the web/ directory; use a real path in your configuration>`$uri",
                      "fallback": {
                          "pass": ":nxt_hint:`applications/drupal/index <Funnels all requests to index.php>`"
                      }
                  }
              }
          ],

          "applications": {
              "drupal": {
                  "type": "php",
                  "targets": {
                      "direct": {
                          "root": ":nxt_ph:`/path/to/app/web/ <Path to the web/ directory; use a real path in your configuration>`"
                      },

                      "index": {
                          "root": ":nxt_ph:`/path/to/app/web/ <Path to the web/ directory; use a real path in your configuration>`",
                          "script": ":nxt_hint:`index.php <All requests are handled by a single script>`"
                      }
                  }
              }
          }
      }

   .. note::

      The difference between the :samp:`pass` targets is their usage of
      the :samp:`script` :ref:`setting <configuration-php>`:

      - The :samp:`direct` target runs the :samp:`.php` script from the
        URI or :samp:`index.php` if the URI omits it.

      - The :samp:`index` target specifies the :samp:`script` that Unit
        runs for *any* URIs the target receives.

#. .. include:: ../include/howto_upload_config.rst

   After a successful update, browse to http://localhost and `set up
   <https://www.drupal.org/docs/develop/using-composer/using-composer-to-install-drupal-and-manage-dependencies#s-install-drupal-using-the-standard-web-interface>`_
   your |app| installation:

  .. image:: ../images/drupal.png
     :width: 100%
     :alt: Drupal on Unit - Setup Screen
