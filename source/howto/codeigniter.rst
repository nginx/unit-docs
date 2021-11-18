.. |app| replace:: CodeIgniter
.. |mod| replace:: PHP

###########
CodeIgniter
###########

To run apps built with the `CodeIgniter <https://codeigniter.com>`_ web
framework using Unit:

#. .. include:: ../include/howto_install_unit.rst

#. Download |app|'s `core files
   <https://codeigniter.com/user_guide/installation/index.html>`_ and `build
   <https://codeigniter.com/user_guide/tutorial/index.html>`_ your application.
   Here, let's use a `basic app template
   <https://forum.codeigniter.com/thread-73103.html>`_, installing it at
   :file:`/path/to/app/`.

#. .. include:: ../include/howto_change_ownership.rst

#. Next, :ref:`prepare <configuration-php>` the |app| configuration for
   Unit:

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
                      "uri": ":nxt_hint:`!/index.php <Denies access to index.php as a static file>`"
                  },

                  "action": {
                      ":nxt_hint:`share <Serves static files>`": ":nxt_ph:`/path/to/app/ <Path to the application directory; use a real path in your configuration>`public$uri",
                      "fallback": {
                          ":nxt_hint:`pass <Serves any requests not served with the 'share' immediately above>`": "applications/codeigniter"
                      }
                  }
              }
          ],

          "applications": {
              "codeigniter": {
                  "type": "php",
                  "root": ":nxt_ph:`/path/to/app/ <Path to the application directory; use a real path in your configuration>`public/",
                  "script": ":nxt_hint:`index.php <All requests are served by a single script>`"
              }
          }
      }

#. .. include:: ../include/howto_upload_config.rst

   After a successful update, your app should be available on the listener’s IP
   address and port:

  .. image:: ../images/codeigniter.png
     :width: 100%
     :alt: CodeIgniter Sample App on Unit
