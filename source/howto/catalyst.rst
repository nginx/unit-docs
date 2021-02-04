.. |app| replace:: Catalyst
.. |mod| replace:: Perl
.. |app-link| replace:: core files
.. _app-link: https://metacpan.org/pod/distribution/Catalyst-Manual/lib/Catalyst/Manual/Intro.pod#Install

########
Catalyst
########

To run apps based on the `Catalyst <https://www.catalystframework.org>`_ 5.9+
framework using Unit:

#. .. include:: ../include/howto_install_unit.rst

#. .. include:: ../include/howto_install_app.rst

#. `Create
   <https://metacpan.org/pod/distribution/Catalyst-Manual/lib/Catalyst/Manual/Tutorial/02_CatalystBasics.pod#CREATE-A-CATALYST-PROJECT>`_
   a Catalyst app.  Here, let's store it at :file:`/path/to/app/`:

   .. code-block:: console

      $ cd /path/to/
      $ catalyst.pl app
      $ cd app
      $ perl Makefile.PL

   Make sure the app's :file:`.psgi` file includes the :file:`lib/`
   directory:

      .. code-block:: perl

         use lib 'lib';
         use app;

#. .. include:: ../include/howto_change_ownership.rst

#. Next, :ref:`prepare <configuration-perl>` the |app| configuration for Unit
   (use real values for :samp:`script` and :samp:`working_directory`):

   .. code-block:: json

      {
          "listeners": {
              "*:80": {
                  "pass": "applications/catalyst"
              }
          },

          "applications": {
              "catalyst": {
                  "type": "perl",
                  "working_directory": ":nxt_term:`/path/to/app/ <Needed to use modules from the local lib directory>`",
                  "script": ":nxt_term:`/path/to/app/app.psgi <Absolute pathname of the PSGI script>`"
              }
          }
      }

#. .. include:: ../include/howto_upload_config.rst

   After a successful update, your app should be available on the listener’s IP
   address and port:

   .. image:: ../images/catalyst.png
      :width: 100%
      :alt: Catalyst Basic Template App on Unit
