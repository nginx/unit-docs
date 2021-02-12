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

#. Next, :ref:`prepare <configuration-php>` the |app| configuration for
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
                          "uri": ":nxt_hint:`!/index.php <Avoids serving index.php as static content>`"
                      },
                      "action": {
                          "share": ":nxt_ph:`/path/to/app/blog/public/ <Serves all kinds of static files>`",
                          "fallback": {
                              "pass": ":nxt_hint:`applications/laravel <Uses the index.php at the root as the last resort>`"
                          }
                      }
                  }
              ]
          },

          "applications": {
              "laravel": {
                  "type": "php",
                  "root": ":nxt_ph:`/path/to/app/blog/public/ <Path to the script>`",
                  "script": ":nxt_hint:`index.php <All requests are handled by a single file>`"
              }
          }
      }

#. .. include:: ../include/howto_upload_config.rst

   After a successful update, browse to http://localhost and `set up
   <https://laravel.com/docs/7.x/configuration>`_ your |app| application:

  .. image:: ../images/laravel.png
     :width: 100%
     :alt: Laravel on Unit - Sample Screen
