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

#. Next, :ref:`put together <configuration-php>` the |app| configuration for
   Unit:

   .. code-block:: json

      {
          "listeners": {
              "*:80": {
                  "pass": "routes/ci_app"
              }
          },

          "routes": {
              "ci_app": [
                  {
                      "match": {
                          "uri": "!/index.php"
                      },

                      "action": {
                          ":nxt_term:`share <Public directory path>`": "/path/to/app/public/",
                          "fallback": {
                              "pass": "applications/ci_app"
                          }
                      }
                  }
              ]
          },

          "applications": {
              "ci_app": {
                  "type": "php",
                  "user": ":nxt_term:`unit_user <User and group values must have access to application directories such as app or public>`",
                  "group": "unit_group",
                  ":nxt_term:`root <Public directory path>`": "/path/to/app/public/",
                  "script": "index.php"
              }
          }
      }

#. .. include:: ../include/howto_upload_config.rst

#. After a successful update, your app should be available on the listener’s IP
   address and port:

  .. image:: ../images/codeigniter.png
     :width: 100%
     :alt: CodeIgniter Sample App on Unit
