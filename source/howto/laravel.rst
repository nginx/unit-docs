.. |app| replace:: Laravel
.. |mod| replace:: PHP
.. _app-preq: https://laravel.com/docs/7.x/installation#server-requirements
.. |app-link| replace:: core files
.. _app-link: https://laravel.com/docs/7.x/installation#installing-laravel

#######
Laravel
#######

To run apps based on the `Laravel <https://symfony.com>`_ framework using Unit:

#. .. include:: ../include/howto_install_unit.rst

#. Install and configure |app|'s `prerequisites
   <https://laravel.com/docs/7.x/installation#server-requirements>`__.

#. Install |app|'s `core files
   <https://laravel.com/docs/7.x/installation#installing-laravel>`__.

#. Create a |app| project.  For our purposes, the path is
   :file:`/path/to/app/`:

   .. code-block:: console

      $ cd /path/to/app/
      $ laravel new blog

#. .. include:: ../include/howto_change_ownership.rst

   .. note::

      See the |app| docs for further details on `server configuration
      <https://laravel.com/docs/7.x/installation#web-server-configuration>`_
      and `directory structure <https://laravel.com/docs/7.x/structure>`_.

#. Next, :ref:`put together <configuration-php>` the |app| configuration for
   Unit:

   .. code-block:: json

      {
          "listeners": {
              "*:80": {
                  "pass": "routes/laravel"
              }
          },

          "routes": {
              "laravel": [
                  {
                      "match": {
                          ":nxt_term:`uri <Avoids serving index.php as static content>`": "!/index.php"
                      },
                      "action": {
                          ":nxt_term:`share <Serves all kinds of static files>`": "/path/to/app/blog/public/",
                          ":nxt_term:`fallback <Uses the index.php at the root as the last resort>`": {
                              "pass": "applications/laravel"
                          }
                      }
                  }
              ]
          },

          "applications": {
              "laravel": {
                  "type": "php",
                  "user": ":nxt_term:`unit_user <User and group values must have access to target root directories>`",
                  "group": "unit_group",
                  "root": ":nxt_term:`/path/to/app/blog/public/ <Path to the script>`",
                  "script": ":nxt_term:`index.php <All requests are handled by a single file>`"
              }
          }
      }

#. .. include:: ../include/howto_upload_config.rst

#. After a successful update, browse to http://localhost and `set up
   <https://laravel.com/docs/7.x/configuration>`_ your |app| application:

  .. image:: ../images/laravel.png
     :width: 100%
     :alt: Laravel on Unit - Sample Screen
