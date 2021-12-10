.. |app| replace:: Roundcube
.. |mod| replace:: PHP
.. |app-preq| replace:: prerequisites
.. _app-preq: https://github.com/roundcube/roundcubemail/wiki/Installation#install-dependencies
.. |app-link| replace:: core files
.. _app-link: https://roundcube.net/download/

#########
Roundcube
#########

To run the `Roundcube <https://roundcube.net>`_ webmail platform using Unit:

#. .. include:: ../include/howto_install_unit.rst

#. .. include:: ../include/howto_install_prereq.rst

#. .. include:: ../include/howto_install_app.rst

#. .. include:: ../include/howto_change_ownership.rst

#. Next, :ref:`prepare <configuration-php>` the |app| configuration for Unit
   (use real values for :samp:`share` and :samp:`root`):

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
                      ":nxt_hint:`uri <Serves direct requests for PHP scripts and directory-like URIs>`": [
                          "*.php",
                          "*/"
                      ]
                  },

                  "action": {
                      "pass": "applications/roundcube"
                  }
              },
              {
                  "action": {
                      ":nxt_hint:`share <Serves static files>`": ":nxt_ph:`/path/to/app <Path to the application directory; use a real path in your configuration>`$uri"
                  }
              }
          ],

          "applications": {
              "roundcube": {
                  "type": "php",
                  "root": ":nxt_ph:`/path/to/app/ <Path to the application directory; use a real path in your configuration>`"
              }
          }

#. .. include:: ../include/howto_upload_config.rst

   After a successful update, browse to http://localhost/installer/ and `set up
   <https://github.com/roundcube/roundcubemail/wiki/Installation#configuring-roundcube>`_
   your |app| installation:

   .. image:: ../images/roundcube-setup.png
      :width: 100%
      :alt: Roundcube on Unit - Setup Screen

   After installation, switch :samp:`share` and :samp:`root` to the
   :file:`public_html/` subdirectory to `protect
   <https://github.com/roundcube/roundcubemail/wiki/Installation#protect-your-installation>`__
   sensitive data:

   .. code-block:: console

      # curl -X PUT -d ':nxt_ph:`"/path/to/app/ <Path to the application directory; use a real path in your configuration>`public_html$uri"' --unix-socket \
            :nxt_ph:`/path/to/control.unit.sock <Path to Unit's control socket in your installation>` :nxt_hint:`http://localhost/config/routes/1/action/share <Path to the app's document root in our configuration; mind that route steps are zero-indexed>`
      # curl -X PUT -d '":nxt_ph:`/path/to/app/ <Path to the application directory; use a real path in your configuration>`public_html/"' --unix-socket \
            :nxt_ph:`/path/to/control.unit.sock <Path to Unit's control socket in your installation>` :nxt_hint:`http://localhost/config/applications/roundcube/root <Path to the app's root option in Unit's control API>`

   Thus, |app| should be available on the listener’s IP address and port:

   .. image:: ../images/roundcube.png
      :width: 100%
      :alt: Roundcube on Unit - Login Screen
