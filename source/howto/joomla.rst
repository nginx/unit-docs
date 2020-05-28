######
Joomla
######

To install and run the `Joomla <https://www.joomla.org>`_ content management
system using Unit:

#. Install :ref:`Unit <installation-precomp-pkgs>` with a PHP language module.

#. Next, `install
   <https://docs.joomla.org/Special:MyLanguage/J3.x:Installing_Joomla>`_ Joomla
   and its `prerequisites
   <https://downloads.joomla.org/technical-requirements>`_ if you haven't
   already done so.

#. Set permissions for the application directory to ensure Unit can access it,
   for example:

   .. code-block:: console

      # chown -R joomla_user:joomla_group /path/to/joomla/  # user:group for app config in Unit

#. Finally, prepare and upload the app :ref:`configuration <configuration-php>`
   to Unit (note the use of :samp:`script` in :samp:`joomla_index`):

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
                          "share": "/path/to/joomla/",
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
                  "user": "joomla_user",
                  "targets": {
                      "direct": {
                          "root": "/path/to/joomla/"
                      },

                      "index": {
                          "root": "/path/to/joomla/",
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

   Assuming the config above is saved as :file:`joomla.json`:

   .. code-block:: console

      # curl -X PUT --data-binary @joomla.json --unix-socket \
             :nxt_term:`/path/to/control.unit.sock <Path to Unit control socket in your installation>` http://localhost/config

#. After a successful update, you can proceed to set up your Joomla
   installation in the browser:

   .. image:: ../images/joomla.png
      :width: 100%
      :alt: Joomla on Unit - Setup Screen

