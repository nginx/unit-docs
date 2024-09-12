.. |app| replace:: MoinMoin
.. |mod| replace:: Python 2
.. |app-preq| replace:: prerequisites
.. _app-preq: https://moinmo.in/MoinMoinDependencies
.. |app-link| replace:: core files
.. _app-link: https://moinmo.in/MoinMoinDownload

########
MoinMoin
########


.. warning::

  So far, Unit doesn't support handling the **REMOTE_USER** headers
  directly, so authentication should be implemented via other means.  For a
  full list of available authenticators, see `here
  <https://moinmo.in/HelpOnAuthentication>`_.

To run the `MoinMoin <https://moinmo.in/MoinMoinWiki>`_ wiki engine using Unit:

#. .. include:: ../include/howto_install_unit.rst

   .. note::

      As of now, MoinMoin `doesn't fully support <https://moinmo.in/Python3>`_
      Python 3.  Mind that Python 2 is officially deprecated.

#. .. include:: ../include/howto_install_prereq.rst

#. .. include:: ../include/howto_install_app.rst

   For example:

   .. code-block:: console

      $ tar xzf moin-:nxt_ph:`X.Y.Z <MoinMoin version>`.tar.gz --strip-components 1 -C :nxt_ph:`/path/to/app/ <Path to the application directory; use a real path in your configuration>`

#. Configure your wiki instances:

   .. tabs::
      :prefix: instance

      .. tab:: Single Wiki

         See the 'Single Wiki' section `here <https://master.moinmo.in/InstallDocs/ServerInstall>`__ for an explanation of these commands:

         .. code-block:: console

            $ cd :nxt_ph:`/path/to/app/ <Path to the application directory; use a real path in your configuration>`

         .. code-block:: console

            $ mkdir single/

         .. code-block:: console

            $ cp :nxt_hint:`wiki/config/wikiconfig.py <Wiki instance configuration>` single/

         .. code-block:: console

            $ cp -r wiki/data/ single/data/

         .. code-block:: console

            $ cp -r wiki/underlay/ single/underlay/

         .. code-block:: console

            $ cp :nxt_hint:`wiki/server/moin.wsgi <WSGI module to run, extension should be changed for proper discovery>` single/moin.py

         Next, `edit
         <https://moinmo.in/HelpOnConfiguration#Configuring_a_single_wiki>`__
         the wiki instance configuration in **wikiconfig.py** as
         appropriate.


      .. tab:: Multiple Wikis

         See the 'Multiple Wikis' section `here <https://master.moinmo.in/InstallDocs/ServerInstall>`__ for an explanation of these commands:

         .. code-block:: console

            $ cd :nxt_ph:`/path/to/app/ <Path to the application directory; use a real path in your configuration>`

         .. code-block:: console

            $ mkdir multi/ multi/wiki1/ multi/wiki2/

         .. code-block:: console

            $ cp wiki/config/wikifarm/* multi/

         .. code-block:: console

            $ cp :nxt_hint:`wiki/config/wikiconfig.py <Wiki instance configuration>` multi/wiki1.py

         .. code-block:: console

            $ cp :nxt_hint:`wiki/config/wikiconfig.py <Wiki instance configuration>` multi/wiki2.py

         .. code-block:: console

            $ cp -r wiki/data/ multi/wiki1/data/

         .. code-block:: console

            $ cp -r wiki/data/ multi/wiki2/data/

         .. code-block:: console

            $ cp -r wiki/underlay/ multi/wiki1/underlay/

         .. code-block:: console

            $ cp -r wiki/underlay/ multi/wiki2/underlay/

         .. code-block:: console

            $ cp :nxt_hint:`wiki/server/moin.wsgi <WSGI module to run, extension should be changed for proper discovery>` multi/moin.py

         Next, `edit
         <https://moinmo.in/HelpOnConfiguration#Configuration_of_multiple_wikis>`__
         the farm configuration in **farmconfig.py** and the wiki instance
         configurations, shown here as **wiki1.py** and **wiki2.py**,
         as appropriate.

#. .. include:: ../include/howto_change_ownership.rst

#. Next, :ref:`prepare <configuration-python>` the |app| configuration for
   Unit (use real values for **path**):

   .. code-block:: json

      {
          "listeners": {
              "*:80": {
                  "pass": "applications/moin"
              }
          },

          "applications": {
              "moin": {
                  "type": "python 2",
                  "path": [
                      ":nxt_ph:`/path/to/app/wsgi/module/ <Path where the WSGI module was stored at Step 4>`",
                      ":nxt_ph:`/path/to/app/ <Path where the MoinMoin directory was extracted at Step 3>`",
                  ],

                  "module": ":nxt_hint:`moin <WSGI file basename>`"
              }
          }
      }

#. .. include:: ../include/howto_upload_config.rst

   After a successful update, |app| should be available on the listener’s IP
   address and port:

   .. image:: ../images/moin.png
      :width: 100%
      :alt: Moin on Unit - Welcome Screen
