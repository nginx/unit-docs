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

#. Prepare the app :ref:`configuration <configuration-ruby>` for Unit (use real
   values for :samp:`working_directory`, :samp:`user`, and :samp:`group`):

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
                  "user": ":nxt_term:`app_user <User and group values must have access to the working directory>`",
                  "group": "app_group",
                  "working_directory": ":nxt_term:`/path/to/app/ <Where Redmine is installed>`",
                  "script": "config.ru",
                  "environment": {
                      "RAILS_ENV": ":nxt_term:`production <Environment name in Redmine config>`"
                  }
              }
          }
      }

#. .. include:: ../include/howto_upload_config.rst

   After a successful update, |app| should be available on the listener's IP
   and port:

   .. image:: ../images/redmine.png
      :width: 100%
      :alt: Redmine in Unit - Sample Screen
