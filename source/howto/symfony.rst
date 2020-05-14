#######
Symfony
#######

To run apps based on the `Symfony <https://symfony.com>`_ framework using Unit:

#. Install :ref:`Unit <installation-precomp-pkgs>` with a PHP language module.

#. Next, `install <https://symfony.com/doc/current/setup.html>`_ Symfony and
   create or deploy your app.  Here, we use Symfony's `reference app
   <https://symfony.com/doc/current/setup.html#the-symfony-demo-application>`_:

   .. code-block:: console

      $ cd /path/to/
      $ symfony new --demo my_project

   This creates the app's directory tree at :file:`/path/to/my_project`.  Its
   :file:`public/` subdirectory contains both the root :file:`index.php` and
   the static files; if your app requires additional :file:`.php` scripts, also
   store them here.

#. Finally, prepare and upload the app :ref:`configuration <configuration-php>`
   to Unit (note the use of :samp:`uri`, :samp:`share`, and :samp:`fallback`):

   .. code-block:: json

      {
          "listeners": {
              "*:80": {
                  "pass": "routes/symfony"
              }
          },

          "routes": {
              "symfony": [
                  {
                      "match": {
                          ":nxt_term:`uri <Handles all direct script-based requests>`": [
                              "*.php",
                              "*.php/*"
                          ]
                      },

                      "action": {
                          "pass": "applications/symfony_direct"
                      }
                  },
                  {
                      "action": {
                          ":nxt_term:`share <Serves all kinds of static files>`": "/path/to/my_project/public/",
                          ":nxt_term:`fallback <Uses the index.php at the root as the last resort>`": {
                              "pass": "applications/symfony_index"
                          }
                      }
                  }
              ]
          },

          "applications": {
              "symfony_direct": {
                  "type": "php",
                  "root": ":/path/to/my_project/public/",
                  "user": ":nxt_term:`www-data <Username that Unit runs the app as, with access to /path/to/my_project/>`"
              },

              "symfony_index": {
                  "type": "php",
                  "root": ":nxt_term:`/path/to/my_project/public/ <Path to the script>`",
                  "user": ":nxt_term:`www-data <Username that Unit runs the app as, with access to /path/to/my_project/>`",
                  "script": ":nxt_term:`index.php <All requests are handled by a single file>`"
              }
          }
      }

   For a detailed discussion, see `Configuring a Web Server
   <https://symfony.com/doc/current/setup/web_server_configuration.html>`_ in
   Symfony docs.

   Assuming the config above is saved as :file:`symfony.json`:

   .. code-block:: console

      # curl -X PUT --data-binary @symfony.json --unix-socket \
             :nxt_term:`/path/to/control.unit.sock <Path to Unit control socket in your installation>` http://localhost/config

   .. image:: ../images/symfony.png
      :width: 100%
      :alt: Symfony Demo App on Unit - Admin Post Update
