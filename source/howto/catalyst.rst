:orphan:

.. include:: ../include/replace.rst

########
Catalyst
########

Unit enables running Perl web apps based on Catalyst |_| 5.9 and later almost
seamlessly:

#. :ref:`Install Unit <installation-precomp-pkgs>` with the appropriate Perl
   language module version.

#. If you haven’t already done so, `create
   <https://metacpan.org/pod/distribution/Catalyst-Manual/lib/Catalyst/Manual/Tutorial/02_CatalystBasics.pod#CREATE-A-CATALYST-PROJECT>`_
   a Catalyst app in your usual location:

   .. code-block:: console

      $ cd /path/to/apps/
      $ catalyst.pl myapp
      $ cd myapp && perl Makefile.PL
      # chown -R :nxt_term:`catalyst_user:catalyst_group <Used to run the app in Unit>` .

   .. note::

      Make sure the app's :file:`.psgi` file includes the :file:`lib/`
      directory:

      .. code-block:: perl

         use lib 'lib';
         use myapp;

#. .. include:: ../include/get-config.rst

   This creates a JSON file with Unit's current settings.  Edit the file,
   adding a :ref:`listener <configuration-listeners>` entry to point to a Unit
   :ref:`app <configuration-applications>` with your :file:`.psgi` file; the
   app will run on the listener's IP and port:

   .. code-block:: json

      {
          "listeners": {
              "127.0.0.1:8080": {
                  "pass": "applications/catalyst_app"
              }
          },

          "applications": {
              "catalyst_app": {
                  "type": "perl",
                  "script": "/path/to/apps/myapp/myapp.psgi",
                  "user": "catalyst_user",
                  "group": "catalyst_group"
              }
          }
      }

#. Upload the updated configuration:

   .. code-block:: console

      # curl -X PUT --data-binary @config.json --unix-socket \
             /path/to/control.unit.sock http://localhost/config

   After a successful update, your app should be available
   on the listener's IP address and port:

   .. code-block:: console

      $ curl 127.0.0.1:8080
