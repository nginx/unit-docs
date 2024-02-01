.. |app| replace:: phpMyAdmin
.. |mod| replace:: PHP
.. |app-preq| replace:: prerequisites
.. _app-preq: https://docs.phpmyadmin.net/en/latest/require.html
.. |app-link| replace:: core files
.. _app-link: https://docs.phpmyadmin.net/en/latest/setup.html#quick-install-1

##########
phpMyAdmin
##########

To run the `phpMyAdmin <https://www.phpmyadmin.net>`_ web tool using Unit:

#. .. include:: ../include/howto_install_unit.rst

#. .. include:: ../include/howto_install_prereq.rst

#. .. include:: ../include/howto_install_app.rst

   .. note::

      Make sure to create the **config.inc.php** file `manually
      <https://docs.phpmyadmin.net/en/latest/setup.html#manually-creating-the-file>`__
      or using the `setup script
      <https://docs.phpmyadmin.net/en/latest/setup.html#using-the-setup-script>`__.

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
                      "uri": ":nxt_hint:`~\\.(css|gif|html?|ico|jpg|js(on)?|png|svg|ttf|woff2?)$ <Enables access to static content only>`"
                  },

                  "action": {
                      ":nxt_hint:`share <Serves matching static files>`": ":nxt_ph:`/path/to/app <Path to the application directory; use a real path in your configuration>`$uri"
                  }
              },
              {
                  "action": {
                      "pass": "applications/phpmyadmin"
                  }
              }
          ],

          "applications": {
              "phpmyadmin": {
                  "type": "php",
                  "root": ":nxt_ph:`/path/to/app/ <Path to the application directory; use a real path in your configuration>`"
              }
          }
      }

#. .. include:: ../include/howto_upload_config.rst

   After a successful update, |app| should be available on the listener’s IP
   address and port:

   .. image:: ../images/phpmyadmin.png
      :width: 100%
      :alt: phpMyAdmin on Unit
