.. |app| replace:: Symfony
.. |mod| replace:: PHP 8.2+

#######
Symfony
#######

To run apps built with the `Symfony <https://symfony.com>`_ framework using Unit:

#. .. include:: ../include/howto_install_unit.rst

#. Next, `install <https://symfony.com/doc/current/setup.html>`_ Symfony and
   create or deploy your app.  Here, we use Symfony's `reference app
   <https://symfony.com/doc/current/setup.html#the-symfony-demo-application>`_:

   .. code-block:: console

      $ cd :nxt_ph:`/path/to/ <Path where the application directory will be created; use a real path in your configuration>`

   .. code-block:: console

      $ symfony new --demo :nxt_ph:`app <Arbitrary app name>`

   This creates the app's directory tree at **/path/to/app/**.  Its
   **public/** subdirectory contains both the root **index.php** and
   the static files; if your app requires additional **.php** scripts, also
   store them here.

#. .. include:: ../include/howto_change_ownership.rst

#. Next, :ref:`prepare <configuration-php>` the |app| configuration for Unit
   (use real values for **share** and **root**):

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
                      ":nxt_hint:`uri <Handles all direct script-based requests>`": [
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
                      ":nxt_hint:`share <Serves static files>`": ":nxt_ph:`/path/to/app/ <Path to the application directory; use a real path in your configuration>`public$uri",
                      "fallback": {
                          "pass": ":nxt_hint:`applications/symfony/index <Uses the index.php at the root as the last resort>`"
                      }
                  }
              }
          ],

          "applications": {
              "symfony": {
                  "type": "php",
                  "targets": {
                      "direct": {
                          "root": ":nxt_ph:`/path/to/app/ <Path to the application directory; use a real path in your configuration>`public/"
                      },

                      "index": {
                          "root": ":nxt_ph:`/path/to/app/ <Path to the application directory; use a real path in your configuration>`public/",
                          "script": ":nxt_hint:`index.php <All requests are handled by a single script>`"
                      }
                  }
              }
          }
      }

   .. note::

      The difference between the **pass** targets is their usage of the
      **script** :ref:`setting <configuration-php>`:

      - The **direct** target runs the **.php** script from the URI or
        defaults to **index.php** if the URI omits it.

      - The **index** target specifies the **script** that Unit runs
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
