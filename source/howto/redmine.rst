.. |app| replace:: Redmine
.. |mod| replace:: Ruby
.. |app-preq| replace:: prerequisites
.. _app-preq: https://www.redmine.org/projects/redmine/wiki/RedmineInstall#Installation-procedure
.. |app-link| replace:: core files
.. _app-link: https://www.redmine.org/projects/redmine/wiki/RedmineInstall#Step-1-Redmine-application

#######
Redmine
#######

To run the `Redmine <https://www.redmine.org>`__ project management system using
Unit:

#. .. include:: ../include/howto_install_unit.rst

#. .. include:: ../include/howto_install_prereq.rst

#. .. include:: ../include/howto_install_app.rst

#. .. include:: ../include/howto_change_ownership.rst

#. Next, :ref:`prepare <configuration-ruby>` the |app| configuration for Unit
   (use a real value for **working_directory**):

   .. code-block:: json

      {
          "listeners": {
              "*:80": {
                  "pass": "applications/redmine"
              }
          },

          "applications": {
              "redmine": {
                  "type": "ruby",
                  "working_directory": ":nxt_ph:`/path/to/app/ <Path to the application directory; use a real path in your configuration>`",
                  "script": ":nxt_hint:`config.ru <Entry point script name, including the file name extension>`",
                  "environment": {
                      "RAILS_ENV": ":nxt_hint:`production <Environment name in the Redmine configuration file>`"
                  }
              }
          }
      }

#. .. include:: ../include/howto_upload_config.rst

   After a successful update, |app| should be available on the listener's IP
   and port:

   .. image:: ../images/redmine.png
      :width: 100%
      :alt: Redmine on Unit - Sample Screen
