.. |app| replace:: OpenGrok
.. |mod| replace:: Java 11+

########
OpenGrok
########

To run the `OpenGrok
<https://github.com/oracle/opengrok>`_ code search engine using Unit:

#. .. include:: ../include/howto_install_unit.rst

#. Follow the official |app| `installation guide
   <https://github.com/oracle/opengrok/wiki/How-to-setup-OpenGrok>`_.  Here,
   we'll place the files at :file:`/path/to/app/`:

   .. code-block:: console

      $ mkdir -p /path/to/app/{src,data,dist,etc,log}
      $ tar -C /path/to/app/dist --strip-components=1 -xzf opengrok-X.Y.Z.tar.gz

   Our servlet container is Unit so we can repackage the :file:`source.war`
   file to an arbitrary directory at `Step 2
   <https://github.com/oracle/opengrok/wiki/How-to-setup-OpenGrok#step2---deploy-the-web-application>`_:

   .. code-block:: console

      $ opengrok-deploy -c /path/to/app/etc/configuration.xml \
            /path/to/app/dist/lib/source.war /path/to/app/

   The resulting pathname is :file:`/path/to/app/source.war`.

#. .. include:: ../include/howto_change_ownership.rst

#. Next, :ref:`prepare <configuration-java>` the |app| configuration for
   Unit:

   .. code-block:: json

      {
          "listeners": {
              "*:80": {
                  "pass": "applications/opengrok"
              }
          },

          "applications": {
              "opengrok": {
                  "type": "java",
                  "webapp": ":nxt_ph:`/path/to/app/source.war <Repackaged in Step 2>`",
                  "options": [
                      "-Djava.awt.headless=true"
                  ]
              }
          }
      }

#. .. include:: ../include/howto_upload_config.rst

   After a successful update, |app| should be available on the listener’s IP
   address and port:

   .. image:: ../images/opengrok.png
      :width: 100%
      :alt: |app| in Unit - Search Screen
