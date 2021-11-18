.. |app| replace:: DokuWiki
.. |mod| replace:: PHP
.. |app-preq| replace:: prerequisites
.. _app-preq: https://www.dokuwiki.org/requirements
.. |app-link| replace:: core files
.. _app-link: https://www.dokuwiki.org/install

########
DokuWiki
########

To run the `DokuWiki <https://www.dokuwiki.org>`_ content management system
using Unit:

#. .. include:: ../include/howto_install_unit.rst

#. .. include:: ../include/howto_install_prereq.rst

#. .. include:: ../include/howto_install_app.rst

   .. code-block:: console

      $ mkdir -p :nxt_ph:`/path/to/app/ <Path to the application directory; use a real path in your configuration>` && cd :nxt_ph:`/path/to/app/ <Path to the application directory; use a real path in your configuration>`
      $ wget https://download.dokuwiki.org/src/dokuwiki/dokuwiki-stable.tgz
      $ tar xvzf dokuwiki-stable.tgz :nxt_hint:`--strip-components <Avoids creating a redundant subdirectory>`=1
      $ rm dokuwiki-stable.tgz

#. .. include:: ../include/howto_change_ownership.rst

#. Next, prepare the app :ref:`configuration <configuration-php>` for Unit (use
   real values for :samp:`share` and :samp:`root`):

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
                      ":nxt_hint:`uri <Denies access to files and directories best kept private>`": [
                          "/data/*",
                          "/conf/*",
                          "/bin/*",
                          "/inc/*",
                          "/vendor/*"
                      ]
                  },

                  "action": {
                      "return": 404
                  }
              },
              {
                  "match": {
                      "uri": [
                          "/",
                          "*.php"
                      ]
                  },

                  "action": {
                      "pass": "applications/dokuwiki"
                  }
              },
              {
                  "action": {
                      ":nxt_hint:`share <Serves static files>`": ":nxt_ph:`/path/to/app <Path to the application directory; use a real path in your configuration>`$uri",
                  }
              }
          ],

          "applications": {
              "dokuwiki": {
                  "type": "php",
                  "root": ":nxt_ph:`/path/to/app/ <Path to the application directory; use a real path in your configuration>`",
                  "index": ":nxt_hint:`doku.php <The app's main script>`"
              }
          }
      }

#. .. include:: ../include/howto_upload_config.rst

   After a successful update, your app should be available on the listener’s IP
   address and port.

#. Browse to :samp:`/install.php` to complete your `installation
   <https://www.dokuwiki.org/installer>`__:

   .. image:: ../images/dokuwiki.png
      :width: 100%
      :alt: DokuWiki on Unit - Installation Screen
