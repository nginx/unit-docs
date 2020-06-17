.. |app| replace:: Joomla
.. |mod| replace:: PHP
.. |app-preq| replace:: prerequisites
.. _app-preq: https://downloads.joomla.org/technical-requirements
.. |app-link| replace:: core files
.. _app-link: https://docs.joomla.org/Special:MyLanguage/J3.x:Installing_Joomla

######
Joomla
######

To run the `Joomla <https://www.joomla.org>`_ content management system using
Unit:

#. .. include:: ../include/howto_install_unit.rst

#. .. include:: ../include/howto_install_prereq.rst

#. .. include:: ../include/howto_install_app.rst

#. .. include:: ../include/howto_change_ownership.rst

#. Next, put together the |app| configuration for Unit:

   .. code-block:: json

      {
          "listeners": {
              "*:80": {
                  "pass": "routes/joomla"
              }
          },

          "routes": {
              "joomla": [
                  {
                      ":nxt_term:`match <Matches direct URLs and the administrative section of the site>`": {
                          "uri": [
                              "*.php",
                              "*.php/*",
                              "/administrator/"
                          ]
                      },

                      "action": {
                          "pass": "applications/joomla/direct"
                      }
                  },
                  {
                      "action": {
                          "share": "/path/to/app/",
                          "fallback": {
                              "pass": ":nxt_term:`applications/joomla/index <Unconditionally matches all remaining URLs, including rewritten ones>`"
                          }
                      }
                  }
              ]
          },

          "applications": {
              "joomla": {
                  "type": "php",
                  "user": ":nxt_term:`unit_user <User and group values must have access to target root directories>`",
                  "group": "unit_group",
                  "targets": {
                      "direct": {
                          "root": "/path/to/app/"
                      },

                      "index": {
                          "root": "/path/to/app/",
                          "script": "index.php"
                      }
                  }
              }
          }
      }

   The first route step handles the admin section and all URLs that specify a
   PHP script; the :samp:`direct` target doesn't set the :samp:`script` option
   to be used by default, so Unit looks for the respective :file:`.php` file.

   The next step serves static files via a :samp:`share`.  Its :samp:`fallback`
   enables rewrite mechanics for `search-friendly URLs
   <https://docs.joomla.org/Enabling_Search_Engine_Friendly_(SEF)_URLs>`_.  All
   requests go to the :samp:`index` target that runs the :file:`index.php`
   script at Joomla's directory root.

#. .. include:: ../include/howto_upload_config.rst

#. After a successful update, browse to http://localhost and `set up
   <https://docs.joomla.org/J3.x:Installing_Joomla#Main_Configuration>`_ your
   |app| installation:

  .. image:: ../images/joomla.png
     :width: 100%
     :alt: Joomla on Unit - Setup Screen

