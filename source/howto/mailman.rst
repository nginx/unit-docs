.. |app| replace:: Mailman
.. |mod| replace:: Python 3.7+

###########
Mailman Web
###########

To install and run the web UI for the `Mailman 3
<https://docs.list.org/en/latest/index.html>`_  suite using Unit:

#. .. include:: ../include/howto_install_unit.rst

#. Follow |app|'s `guide
   <https://docs.list.org/en/latest/install/virtualenv.html#virtualenv-install>`__
   to install its prerequisites and core files, but stop at `setting up a WSGI
   server
   <https://docs.list.org/en/latest/install/virtualenv.html#setting-up-a-wsgi-server>`__;
   we'll use Unit instead.  Also, note the following settings (values from the
   guide are given after the colon):

   - Virtual environment path: :file:`/opt/mailman/venv/`
   - Installation path: :file:`/etc/mailman3/`
   - Static file path: :file:`/opt/mailman/web/static/`
   - User and group: :samp:`mailman:mailman`

   These are needed to configure Unit.

#. Run the following command so Unit can access |app|'s static files:

   .. code-block:: console

      # chown -R :nxt_hint:`unit:unit <User and group that Unit's router runs as by default>` :nxt_hint:`/opt/mailman/web/static/ <Mailman's static file path>`
   .. note::

      The :samp:`unit:unit` user-group pair is available only with
      :ref:`official packages <installation-precomp-pkgs>`, Docker :ref:`images
      <installation-docker>`, and some :ref:`third-party repos
      <installation-community-repos>`.  Otherwise, account names may differ;
      run the :program:`ps aux | grep unitd` command to be sure.

   Alternatively, add Unit's unprivileged user account to |app|'s group so Unit
   can access the static files:

   .. code-block:: console

      # usermod -a -G :nxt_hint:`mailman <Mailman's user group noted in Step 2>` :nxt_hint:`unit <User that Unit's router runs as by default>`

#. Next, prepare the |app| :ref:`configuration <configuration-python>` for Unit
   (use values from Step 2 for :samp:`share`, :samp:`path`, and :samp:`home`):

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
                      "uri": ":nxt_hint:`/static/* <Matches requests for web UI's static content>`"
                  },

                  "action": {
                      ":nxt_hint:`share <Serves static files>`": ":nxt_hint:`/opt/mailman/web/ <Mailman's static file path without the 'static/' part; URIs starting with /static/ are thus served from /opt/mailman/web/static/>`$uri"
                  }
              },
              {
                  "action": {
                      "pass": "applications/mailman_web"
                  }
              }
          ],

          "applications": {
              "mailman_web": {
                  "type": "python :nxt_ph:`3.X <Must match language module version and virtual environment version>`",
                  "path": ":nxt_hint:`/etc/mailman3/ <Mailman's installation path you noted in Step 2>`",
                  "home": ":nxt_hint:`/opt/mailman/venv/ <Mailman's virtual environment path you noted in Step 2>`",
                  "module": ":nxt_hint:`mailman_web.wsgi <Qualified name of the WSGI module, relative to installation path>`",
                  "user": ":nxt_hint:`mailman <Mailman's user group noted in Step 2>`",
                  ":nxt_hint:`environment <App-specific environment variables>`": {
                      "DJANGO_SETTINGS_MODULE": ":nxt_hint:`settings <Web configuration module name, relative to installation path>`"
                  }
              }
          }
      }

#. .. include:: ../include/howto_upload_config.rst

   After a successful update, |app|'s web UI should be available on the
   listener’s IP address and port:

   .. image:: ../images/mailman.png
      :width: 100%
      :alt: Mailman on Unit - Lists Screen
