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

#. Next, :ref:`prepare <configuration-php>` the |app| configuration for
   Unit (use real values for :samp:`share` and :samp:`root`):

   .. code-block:: json

      {
          "listeners": {
              "*:80": {
                  "pass": "routes"
              }
          },

          "routes": [
              {
                  "match": {
                      ":nxt_hint:`uri <Matches direct URLs and the administrative section of the site>`": [
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
                      ":nxt_hint:`share <Serves matching static files>`": ":nxt_ph:`/path/to/app <Path to the application directory; use a real path in your configuration>`$uri",
                      "fallback": {
                          "pass": ":nxt_hint:`applications/joomla/index <Unconditionally matches all remaining URLs, including rewritten ones>`"
                      }
                  }
              }
          ],

          "applications": {
              "joomla": {
                  "type": "php",
                  "targets": {
                      "direct": {
                          "root": ":nxt_ph:`/path/to/app/ <Path to the application directory; use a real path in your configuration>`"
                      },

                      "index": {
                          "root": ":nxt_ph:`/path/to/app/ <Path to the application directory; use a real path in your configuration>`",
                          "script": ":nxt_hint:`index.php <All requests are handled by a single script>`"
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

   After a successful update, |app| should be available on the listener’s IP
   and port to finish the `setup
   <https://docs.joomla.org/J3.x:Installing_Joomla#Main_Configuration>`_:

  .. image:: ../images/joomla.png
     :width: 100%
     :alt: Joomla on Unit - Setup Screen

