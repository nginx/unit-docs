:orphan:

########
Bugzilla
########

To run Bugzilla in Unit:

#. Install :ref:`Unit <installation-precomp-pkgs>` with the appropriate Perl
   language module version.

#. Install `Bugzilla
   <https://bugzilla.readthedocs.io/en/latest/installing/index.html>`_
   prerequisites and source files.

   .. note::

      Unit uses `PSGI <https://metacpan.org/pod/PSGI>`_ to run Perl
      applications; Bugzilla natively supports PSGI since version 5.1.

#. .. include:: ../include/get-config.rst

   This creates a JSON file with Unit's current settings.  Edit the file,
   adding a :ref:`listener <configuration-listeners>` with a :ref:`route
   <configuration-routes>` that serves requests for static files via a
   conditional :samp:`share` and passes any other requests to Bugzilla's
   :file:`app.psgi`:

   .. code-block:: json

      {
          "listeners": {
              "*:8000": {
                  "pass": "routes/bugzilla"
              }
          },

          "routes": {
              "bugzilla": [
                  {
                      "match": {
                          "uri": [
                              "/data/assets/*",
                              "/docs/*",
                              "/extensions/*",
                              "/images/*",
                              "/js/*",
                              "/skins/*"
                          ]
                      },

                      "action": {
                          "share": "/path/to/bugzilla/"
                      }
                  },

                  {
                      "action": {
                          "pass": "applications/bugzilla"
                      }
                  }
              ]
          },

          "applications": {
              "bugzilla": {
                  "type": "perl",
                  "working_directory": "/path/to/bugzilla/",
                  "script": "/path/to/bugzilla/app.psgi"
              }
          }
      }

#. Upload the updated configuration:

   .. code-block:: console

      # curl -X PUT --data-binary @config.json --unix-socket \
             /path/to/control.unit.sock http://localhost/config

#. Finally, browse to your Bugzilla site and complete the installation:

   .. image:: ../images/bugzilla.png
      :width: 100%
      :alt: Bugzilla in Unit - Setup Screen
