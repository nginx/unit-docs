.. |app| replace:: Bugzilla
.. |mod| replace:: Perl
.. |app-preq| replace:: prerequisites
.. _app-preq: https://bugzilla.readthedocs.io/en/latest/installing/linux.html#install-packages
.. |app-link| replace:: core files
.. _app-link: https://bugzilla.readthedocs.io/en/latest/installing/linux.html#bugzilla

########
Bugzilla
########

To run the `Bugzilla <https://www.bugzilla.org>`__ bug tracking system using
Unit:

#. .. include:: ../include/howto_install_unit.rst

#. .. include:: ../include/howto_install_prereq.rst

#. .. include:: ../include/howto_install_app.rst

   .. note::

      Unit uses `PSGI <https://metacpan.org/pod/PSGI>`_ to run Perl
      applications; Bugzilla natively supports PSGI since version 5.1.

#. .. include:: ../include/howto_change_ownership.rst

#. Next, put together the |app| configuration for Unit.  The default
   :file:`.htaccess` scheme in a |app| installation roughly translates into the
   following:

   .. code-block:: json

      {
          "listeners": {
              "*:80": {
                  "pass": "routes/bugzilla"
              }
          },

          "routes": {
              "bugzilla": [
                  {
                      ":nxt_term:`match <Restricts access to .dot files to the public webdot server at research.att.com>`": {
                          "source": "192.20.225.0/24",
                          "uri": "/data/webdot/*.dot"
                      },

                      "action": {
                          "share": "/path/to/app/"
                      }
                  },
                  {
                      "match": {
                          ":nxt_term:`uri <Denies access to certain types of files and directories best kept hidden, allows access to well-known locations>`": [
                              "!/data/assets/*.css",
                              "!/data/assets/*.js",
                              "!/data/webdot/*.png",
                              "!/graphs/*.gif",
                              "!/graphs/*.png",
                              "*.pl",
                              "*.pm",
                              "*.psgi",
                              "*.tmpl",
                              "*/cpanfile",
                              "*/localconfig*",
                              "/Bugzilla/*",
                              "/contrib/*",
                              "/data/*",
                              "/lib/*",
                              "/t/*",
                              "/template/*",
                              "/xt/*"
                          ]
                      },

                      "action": {
                          "return": 403
                      }
                  },
                  {
                      "action": {
                          "share": "/path/to/app/",
                          "fallback": {
                              "pass": "applications/bugzilla"
                          }
                      }
                  }
              ]
          },

          "applications": {
              "bugzilla": {
                  "type": "perl",
                  "user": ":nxt_term:`app_user <User and group values must have access to the working directory>`",
                  "group": "app_group",
                  "working_directory": "/path/to/app/",
                  "script": ":nxt_term:`/path/to/app/app.psgi <Full pathname of the PSGI file>`"
              }
          }
      }

#. .. include:: ../include/howto_upload_config.rst

#. After a successful update, browse to http://localhost and `set up
   <https://bugzilla.readthedocs.io/en/latest/installing/essential-post-install-config.html>`__
   your |app| installation:

   .. image:: ../images/bugzilla.png
      :width: 100%
      :alt: Bugzilla on Unit - Setup Screen
