.. |app| replace:: Catalyst
.. |mod| replace:: Perl
.. |app-link| replace:: core files
.. _app-link: https://metacpan.org/dist/Catalyst-Manual/view/lib/Catalyst/Manual/Intro.pod#Install

########
Catalyst
########

To run apps based on the `Catalyst
<https://metacpan.org/dist/Catalyst-Manual>`_ 5.9+ framework using Unit:

#. .. include:: ../include/howto_install_unit.rst

#. Install |app|'s |app-link|_.

#. `Create
   <https://metacpan.org/dist/Catalyst-Manual/view/lib/Catalyst/Manual/Tutorial/02_CatalystBasics.pod#CREATE-A-CATALYST-PROJECT>`_
   a Catalyst app.  Here, let's store it at **/path/to/app/**:

   .. code-block:: console

      $ cd :nxt_ph:`/path/to/ <Path where the application directory will be created; use a real path in your configuration>`

   .. code-block:: console

      $ catalyst.pl :nxt_ph:`app <Arbitrary app name; becomes the application directory name>`

   .. code-block:: console

      $ cd app

   .. code-block:: console

      $ perl Makefile.PL

   Make sure the app's **.psgi** file includes the **lib/**
   directory:

   .. code-block:: perl

      use lib 'lib';
      use app;

#. .. include:: ../include/howto_change_ownership.rst

#. Next, :ref:`prepare <configuration-perl>` the |app| configuration for Unit
   (use real values for **script** and **working_directory**):

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
                  "working_directory": ":nxt_ph:`/path/to/app/ <Needed to use modules from the local lib directory; use a real path in your configuration>`",
                  "script": ":nxt_ph:`/path/to/app/ <Path to the application directory; use a real path in your configuration>`app.psgi"
              }
          }
      }

#. .. include:: ../include/howto_upload_config.rst

   After a successful update, your app should be available on the listener’s IP
   address and port:

   .. image:: ../images/catalyst.png
      :width: 100%
      :alt: Catalyst Basic Template App on Unit
