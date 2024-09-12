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
   we'll place the files at **/path/to/app/**:

   .. code-block:: console

      $ mkdir -p :nxt_ph:`/path/to/app/ <Path to the application directory; use a real path in your configuration>`{src,data,dist,etc,log}

   .. code-block:: console

      $ tar -C :nxt_ph:`/path/to/app/ <Path to the application directory; use a real path in your configuration>`dist --strip-components=1 -xzf opengrok-:nxt_ph:`X.Y.Z <Specific OpenGrok version>`.tar.gz

   Our servlet container is Unit so we can repackage the **source.war**
   file to an arbitrary directory at `Step 2
   <https://github.com/oracle/opengrok/wiki/How-to-setup-OpenGrok#step2---deploy-the-web-application>`_:

   .. code-block:: console

      $ opengrok-deploy -c :nxt_ph:`/path/to/app/ <Path to the application directory; use a real path in your configuration>`etc/configuration.xml  \
            :nxt_ph:`/path/to/app/ <Path to the application directory; use a real path in your configuration>`dist/lib/source.war :nxt_ph:`/path/to/app/ <Path to the application directory; use a real path in your configuration>`

   The resulting pathname is **/path/to/app/source.war**.

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
                  "webapp": ":nxt_ph:`/path/to/app/ <Path to the application directory; use a real path in your configuration>`:nxt_hint:`source.war <Repackaged in Step 2>`",
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
      :alt: OpenGrok on Unit - Search Screen
