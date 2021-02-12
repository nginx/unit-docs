.. |app| replace:: MoinMoin
.. |mod| replace:: Python 2
.. |app-preq| replace:: prerequisites
.. _app-preq: https://moinmo.in/MoinMoinDependencies
.. |app-link| replace:: core files
.. _app-link: https://moinmo.in/MoinMoinDownload

########
MoinMoin
########


.. warning::

  So far, Unit doesn't support handling the :samp:`REMOTE_USER` headers
  directly, so authentication should be implemented via other means.  For a
  full list of available authenticators, see `here
  <https://moinmo.in/HelpOnAuthentication>`_.

To run the `MoinMoin <https://moinmo.in/MoinMoinWiki>`_ wiki engine using Unit:

#. .. include:: ../include/howto_install_unit.rst

   .. note::

      As of now, MoinMoin `doesn't fully support <https://moinmo.in/Python3>`_
      Python 3.  Mind that Python 2 is officially deprecated.

#. .. include:: ../include/howto_install_prereq.rst

#. .. include:: ../include/howto_install_app.rst

   For example:

   .. code-block:: console

      $ mkdir -p /path/to/app/ /tmp/app/ && cd :nxt_hint:`/tmp/app/ <Temporary location to download files to>`
      $ curl -O http://static.moinmo.in/files/moin-1.9.11.tar.gz
      $ tar xzf moin-1.9.11.tar.gz --strip-components 1 -C :nxt_ph:`/path/to/app/ <Target installation location>`
      $ cd :nxt_ph:`/path/to/app/wiki/ <WSGI module location in a single-instance installation>`
      $ cp :nxt_hint:`config/wikiconfig.py <Instance config, see https://moinmo.in/HelpOnConfiguration>` ./
      $ cp :nxt_hint:`server/moin.wsgi <WSGI module to run, extension should be changed for proper discovery>` ./moin.py

#. .. include:: ../include/howto_change_ownership.rst

#. Next, :ref:`prepare <configuration-python>` the |app| configuration for
   Unit (use a real value for :samp:`path`):

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
                  "path": ":nxt_hint:`/path/to/app/wiki/ <Path to the WSGI file>`",
                  "module": ":nxt_hint:`moin <WSGI file basename>`"
              }
          }
      }

#. .. include:: ../include/howto_upload_config.rst

   After a successful update, |app| should be available on the listener’s IP
   address and port:

   .. image:: ../images/moin.png
      :width: 100%
      :alt: Moin on Unit - Welcome Screen
