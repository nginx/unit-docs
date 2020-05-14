#######
CakePHP
#######

To run apps based on the `CakePHP <https://cakephp.org>`_ framework using Unit:

#. Install :ref:`Unit <installation-precomp-pkgs>` with a PHP 7.2+ language
   module.

#. `Install
   <https://book.cakephp.org/4/en/installation.html>`_ CakePHP and
   create or deploy your app.  Here, we use CakePHP's `basic template
   <https://book.cakephp.org/4/en/installation.html#create-a-cakephp-project>`_
   and Composer:

   .. code-block:: console

      $ cd /path/to/
      $ composer create-project --prefer-dist cakephp/app:4.* cakephp

   This creates the app's directory tree at :file:`/path/to/cakephp/`.  Its
   :file:`webroot/` subdirectory contains both the root :file:`index.php` and
   the static files; if your app requires additional :file:`.php` scripts, also
   store them here.

#. Finally, prepare and upload the app :ref:`configuration <configuration-php>`
   to Unit (note the use of :samp:`uri`, :samp:`share`, and :samp:`fallback`):

   .. code-block:: json

      {
          "listeners": {
              "*:80": {
                  "pass": "routes/cakephp"
              }
          },

          "routes": {
              "cakephp": [
                  {
                      "match": {
                          ":nxt_term:`uri <Handles all direct script-based requests>`": [
                              "*.php",
                              "*.php/*"
                          ]
                      },

                      "action": {
                          "pass": "applications/cakephp_direct"
                      }
                  },
                  {
                      "action": {
                          ":nxt_term:`share <Serves all kinds of static files>`": "/path/to/cakephp/webroot/",
                          ":nxt_term:`fallback <Uses the index.php at the root as the last resort>`": {
                              "pass": "applications/cakephp_index"
                          }
                      }
                  }
              ]
          },

          "applications": {
              "cakephp_direct": {
                  "type": "php",
                  "root": "/path/to/cakephp/webroot/",
                  "user": ":nxt_term:`www-data <Username that Unit runs the app as, with access to /path/to/cakephp/>`"
              },

              "cakephp_index": {
                  "type": "php",
                  "root": ":nxt_term:`/path/to/cakephp/webroot/ <Path to the index.php script>`",
                  "user": ":nxt_term:`www-data <Username that Unit runs the app as, with access to /path/to/cakephp/>`",
                  "script": ":nxt_term:`index.php <All requests are handled by a single file>`"
              }
          }
      }

   For a detailed discussion, see `Fire It Up
   <https://book.cakephp.org/4/en/installation.html#fire-it-up>`_ in CakePHP
   docs.

   Assuming the config above is saved as :file:`cakephp.json`:

   .. code-block:: console

      # curl -X PUT --data-binary @cakephp.json --unix-socket \
             :nxt_term:`/path/to/control.unit.sock <Path to Unit control socket in your installation>` http://localhost/config

   .. image:: ../images/cakephp.png
      :width: 100%
      :alt: CakePHP Basic Template App on Unit
