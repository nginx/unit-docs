########
MoinMoin
########


.. warning::

  So far, Unit doesn't support handling the :samp:`REMOTE_USER` headers
  directly, so authentication should be implemented via other means.  For a
  full list of available authenticators, see `here
  <https://moinmo.in/HelpOnAuthentication>`_.

To install and run the `MoinMoin <https://moinmo.in/MoinMoinWiki>`_ wiki engine
using Unit:

#. Install :ref:`Unit <installation-precomp-pkgs>` with a Python 2 language
   module.

   .. note::

      As of now, MoinMoin `doesn't fully support <https://moinmo.in/Python3>`_
      Python 3.  Mind that Python 2 is officially deprecated.

#. Download MoinMoin `files <https://moinmo.in/MoinMoinDownload>`_, install the
   `prerequisites <https://moinmo.in/MoinMoinDependencies>`_, and configure
   ownership:

   .. code-block:: console

      $ mkdir -p /path/to/moin/ /tmp/moin/ && cd :nxt_term:`/tmp/moin/ <Temporary location to download files to>`
      $ curl -O http://static.moinmo.in/files/moin-1.9.10.tar.gz
      $ tar xzf moin-1.9.10.tar.gz --strip-components 1 -C :nxt_term:`/path/to/moin/ <Target installation location>`
      $ cd :nxt_term:`/path/to/moin/wiki/ <WSGI module location in a single-instance installation>`
      $ cp :nxt_term:`config/wikiconfig.py <Instance config, see https://moinmo.in/HelpOnConfiguration>` ./
      $ cp :nxt_term:`server/moin.wsgi <WSGI module to run, extension should be changed for proper discovery>` ./moin.py
      # chown -R :nxt_term:`moin_user:moin_group <Used to configure the app in Unit>` /path/to/moin/

#. Next, prepare and upload the app :ref:`configuration <configuration-python>`
   to Unit:

   .. code-block:: json

      {
          "listeners": {
              "*:80": {
                  "pass": "applications/moin"
              }
          },

          "applications": {
              "moin": {
                  "type": "python 2",
                  "path": ":nxt_term:`/path/to/moin/wiki/ <Path to the WSGI file>`",
                  "user": ":nxt_term:`moin_user <Username that Unit runs the app as, with access to /path/to/moin/>`",
                  "module": ":nxt_term:`moin <WSGI file basename>`"
              }
          }
      }

   Assuming the config is saved as :file:`moin.json`:

   .. code-block:: console

      # curl -X PUT --data-binary @moin.json --unix-socket \
             /var/run/control.unit.sock http://localhost/config

   .. image:: ../images/moin.png
      :width: 100%
      :alt: Moin on Unit - Welcome Screen
