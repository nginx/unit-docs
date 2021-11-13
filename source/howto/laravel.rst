.. |app| replace:: Laravel
.. |mod| replace:: PHP
.. |app-preq| replace:: prerequisites
.. _app-preq: https://laravel.com/docs/7.x/installation#server-requirements

#######
Laravel
#######

To run apps based on the `Laravel <https://laravel.com>`_ framework using Unit:

#. .. include:: ../include/howto_install_unit.rst

#. .. include:: ../include/howto_install_prereq.rst

#. Install |app|'s `core files
   <https://laravel.com/docs/7.x/installation#installing-laravel>`__.

#. Create a |app| project.  For our purposes, the path is
   :file:`/path/to/app/`:

   .. code-block:: console

      $ cd :nxt_ph:`/path/to/ <Path where the application directory will be created; use a real path in your configuration>`
      $ laravel new :nxt_ph:`app <Arbitrary app name; becomes the application directory name>`

#. .. include:: ../include/howto_change_ownership.rst

   .. note::

      See the |app| docs for further details on `server configuration
      <https://laravel.com/docs/7.x/installation#web-server-configuration>`_
      and `directory structure <https://laravel.com/docs/7.x/structure>`_.

#. Next, :ref:`prepare <configuration-php>` the |app| configuration for
   Unit (use real values for :samp:`share` and :samp:`root`):

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
                      ":nxt_hint:`share <Serves static files>`": ":nxt_ph:`/path/to/app/ <Path to the application directory; use a real path in your configuration>`public/",
                      "fallback": {
                          "pass": ":nxt_hint:`applications/laravel <Uses the index.php at the root as the last resort>`"
                      }
                  }
              }
          ],

          "applications": {
              "laravel": {
                  "type": "php",
                  "root": ":nxt_ph:`/path/to/app/ <Path to the application directory; use a real path in your configuration>`public/",
                  "script": ":nxt_hint:`index.php <All requests are handled by a single script>`"
              }
          }
      }

#. .. include:: ../include/howto_upload_config.rst

   After a successful update, browse to http://localhost and `set up
   <https://laravel.com/docs/7.x/configuration>`_ your |app| application:

  .. image:: ../images/laravel.png
     :width: 100%
     :alt: Laravel on Unit - Sample Screen
