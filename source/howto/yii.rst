:orphan:

###
Yii
###

To run apps based on the `Yii <https://www.yiiframework.com>`_ framework using
Unit:

#. Install :ref:`Unit <installation-precomp-pkgs>` with a PHP language module.

#. Next, `install
   <https://www.yiiframework.com/doc/guide/2.0/en/start-installation>`_ Yii and
   create or deploy your app.  Here, we use Yii's `basic project template
   <https://www.yiiframework.com/doc/guide/2.0/en/start-installation#installing-from-composer>`_
   and Composer:

   .. code-block:: console

      $ cd /path/to/
      $ composer create-project --prefer-dist yiisoft/yii2-app-basic yii

   This creates the app's directory tree at :file:`/path/to/yii`.  Its
   :file:`web/` subdirectory contains both the root :file:`index.php` and
   the static files; if your app requires additional :file:`.php` scripts, also
   store them here.

#. Finally, prepare and upload the app :ref:`configuration <configuration-php>`
   to Unit (note the use of :samp:`uri`, :samp:`share`, and :samp:`fallback`):

   .. code-block:: json

      {
          "listeners": {
              "*:80": {
                  "pass": "routes/yii"
              }
          },

          "routes": {
              "yii": [
                  {
                      "match": {
                          ":nxt_term:`uri <Handles all direct script-based requests, filters out the assets directory>`": [
                              "!/assets/*",
                              "*.php",
                              "*.php/*"
                          ]
                      },

                      "action": {
                          "pass": "applications/yii_direct"
                      }
                  },
                  {
                      "action": {
                          ":nxt_term:`share <Serves all kinds of static files>`": "/path/to/yii/web/",
                          ":nxt_term:`fallback <Uses the index.php at the root as the last resort>`": {
                              "pass": "applications/yii_index"
                          }
                      }
                  }
              ]
          },

          "applications": {
              "yii_direct": {
                  "type": "php",
                  "root": ":/path/to/yii/web/",
                  "user": ":nxt_term:`www-data <Username that Unit runs the app as, with access to /path/to/yii/>`"
              },

              "yii_index": {
                  "type": "php",
                  "root": ":nxt_term:`/path/to/yii/web/ <Path to the script>`",
                  "user": ":nxt_term:`www-data <Username that Unit runs the app as, with access to /path/to/yii/>`",
                  "script": ":nxt_term:`index.php <All requests are handled by a single file>`"
              }
          }
      }

   For a detailed discussion, see `Configuring Web Servers
   <https://www.yiiframework.com/doc/guide/2.0/en/start-installation#configuring-web-servers>`_
   and `Running Applications
   <https://www.yiiframework.com/doc/guide/2.0/en/start-workflow>`_ in Yii
   docs.

   Assuming the config above is saved as :file:`yii.json`:

   .. code-block:: console

      # curl -X PUT --data-binary @yii.json --unix-socket \
             :nxt_term:`/path/to/control.unit.sock <Path to Unit control socket in your installation>` http://localhost/config

   .. image:: ../images/yii.png
      :width: 100%
      :alt: Yii Basic Template App on Unit
