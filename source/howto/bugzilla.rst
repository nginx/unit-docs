:orphan:

########
Bugzilla
########

To run Bugzilla in Unit:

.. _bugzilla_nginx:

#. Install `NGINX <https://nginx.org/en/download.html>`_.  Currently, it is
   required to serve static files.  Note the :samp:`user` settings in
   :file:`nginx.conf`:

   .. code-block:: nginx

      user <user> <group>;

#. Install :ref:`Unit <installation-precomp-pkgs>` with the appropriate Perl
   language module version.

#. Install `Bugzilla
   <https://bugzilla.readthedocs.io/en/latest/installing/index.html>`_
   prerequisites and source files.

   .. note::

      Unit uses `PSGI <https://metacpan.org/pod/PSGI>`_ to run Perl
      applications; Bugzilla natively supports PSGI since version 5.1.

#. While running :program:`checksetup.pl`, configure :samp:`$webservergroup`
   with the :samp:`<group>` value noted :ref:`earlier <bugzilla_nginx>`.

#. .. include:: ../include/get-config.rst

   This creates a JSON file with Unit's current settings.  Edit the JSON file,
   adding a :ref:`listener <configuration-listeners>` in :samp:`listeners` and
   pointing it to Bugzilla's :file:`app.psgi` file in :samp:`applications`.
   Bugzilla will run on the listener's IP and port.

   .. code-block:: json

      {
          "listeners": {
              "127.0.0.1:8081": {
                  "pass": "applications/bugzilla"
              }
          },

          "applications": {
              "bugzilla": {
                  "type": "perl",
                  "working_directory": "/path/to/bugzilla/",
                  "script": "/path/to/bugzilla/app.psgi",
                  "user": "<user>",
                  "group": "<group>"
              }
          }
      }

#. Upload the updated configuration:

   .. code-block:: console

      # curl -X PUT --data-binary @config.json --unix-socket \
             /path/to/control.unit.sock http://localhost/config

#. Configure NGINX to serve :file:`.js` and :file:`.css` files, proxying other
   requests to Unit:

   .. code-block:: nginx

      server {
          listen 8080;

          location /data/assets/ {
              root /path/to/bugzilla/;
          }

          location / {
              proxy_pass http://127.0.0.1:8081;
              proxy_set_header Host $host;
          }
      }

   For details, refer to `NGINX Admin Guide
   <https://docs.nginx.com/nginx/admin-guide/>`_.

#. Finally, browse to your Bugzilla site and complete the installation:

   .. image:: ../images/bugzilla.png
      :width: 100%
      :alt: Bugzilla in Unit - Setup Screen
