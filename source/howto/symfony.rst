.. |app| replace:: Symfony
.. |mod| replace:: PHP 7.2.5+

#######
Symfony
#######

To run apps built with the `Symfony <https://symfony.com>`_ framework using Unit:

#. .. include:: ../include/howto_install_unit.rst

#. Next, `install <https://symfony.com/doc/current/setup.html>`_ Symfony and
   create or deploy your app.  Here, we use Symfony's `reference app
   <https://symfony.com/doc/current/setup.html#the-symfony-demo-application>`_:

   .. code-block:: console

      $ cd /path/to/
      $ symfony new --demo app

   This creates the app's directory tree at :file:`/path/to/app/`.  Its
   :file:`public/` subdirectory contains both the root :file:`index.php` and
   the static files; if your app requires additional :file:`.php` scripts, also
   store them here.

#. .. include:: ../include/howto_change_ownership.rst

#. Next, :ref:`put together <configuration-php>` the |app| configuration for
   Unit (note the use of :samp:`uri`, :samp:`share`, and :samp:`fallback`):

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
                          "pass": "applications/symfony/direct"
                      }
                  },
                  {
                      "action": {
                          ":nxt_term:`share <Serves all kinds of static files>`": "/path/to/app/public/",
                          ":nxt_term:`fallback <Uses the index.php at the root as the last resort>`": {
                              "pass": "applications/symfony/index"
                          }
                      }
                  }
              ]
          },

          "applications": {
              "symfony": {
                  "type": "php",
                  "user": ":nxt_term:`app_user <User and group values must have access to root directories>`",
                  "group": "app_group",
                  "targets": {
                      "direct": {
                          "root": ":nxt_term:`/path/to/app/public/ <Path to the scripts>`"
                      },

                      "index": {
                          "root": ":nxt_term:`/path/to/app/ppublic/ <Path to the script>`",
                          "script": ":nxt_term:`index.php <All requests are handled by a single file>`"
                      }
                  }
              }
          }
      }

   .. note::

      The difference between the :samp:`pass` targets is their usage of the
      :samp:`script` :ref:`setting <configuration-php>`:

      - The :samp:`direct` target runs the :samp:`.php` script from the URI or
        defaults to :samp:`index.php` if the URI omits it.
      - The :samp:`index` target specifies the :samp:`script` that Unit runs
        for *any* URIs the target receives.

   For a detailed discussion, see `Configuring a Web Server
   <https://symfony.com/doc/current/setup/web_server_configuration.html>`_ in
   Symfony docs.

#. .. include:: ../include/howto_upload_config.rst

   After a successful update, your project and apps should be available on the
   listener's IP address and port:

   .. image:: ../images/symfony.png
      :width: 100%
      :alt: Symfony Demo App on Unit - Admin Post Update
