.. include:: ../include/replace.rst

.. |app| replace:: Plone
.. |mod| replace:: Python 3.6+
.. |app-preq| replace:: prerequisites
.. _app-preq: https://docs.plone.org/manage/installing/requirements.html
.. |app-link| replace:: core files
.. _app-link: https://docs.plone.org/manage/installing/installation.html

#####
Plone
#####

To run the `Plone <https://plone.org>`_ content management system using Unit:

#. .. include:: ../include/howto_install_unit.rst

#. .. include:: ../include/howto_install_prereq.rst

#. Install |app|'s |app-link|_.  Here, we install it at **/path/to/app/**;
   use a real path in your configuration:

   .. code-block:: console

      $ mkdir /tmp/plone && cd /tmp/plone/

   .. code-block:: console

      $ wget https://launchpad.net/plone/:nxt_ph:`A.B <Plone version>`/:nxt_ph:`A.B.C <Plone version>`/+download/Plone-:nxt_ph:`A.B.C <Plone version>`-UnifiedInstaller-1.0.tgz

   .. code-block:: console

      $ tar xzvf Plone-:nxt_ph:`A.B.C <Plone version>`-UnifiedInstaller-1.0.tgz  \
            :nxt_hint:`--strip-components <Avoids creating a redundant subdirectory>`=1

   .. code-block:: console

      $ ./install.sh --target=:nxt_ph:`/path/to/app/ <Path to the application directory; use a real path in your configuration>`  \
                     --with-python=:nxt_ph:`/full/path/to/python <Full pathname of the Python executable used to create Plone's virtual environment>`  \
                     standalone

   .. note::

      |app|'s `Zope <https://plone.org/what-is-plone/zope>`__ instance and
      virtual environment are created in the **zinstance/** subdirectory;
      later, the resulting path is used to configure Unit, so take care to note
      it in your setup.  Also, make sure the Python version specified with
      :option:`!--with-python` matches the module version from Step 1.

#. To run |app| on Unit, add a new configuration file named
   **/path/to/app/zinstance/wsgi.cfg**:

   .. code-block:: cfg

      [buildout]
      extends =
          buildout.cfg

      parts +=
          :nxt_ph:`wsgi.py <The basename is arbitrary; the extension is required to make the resulting Python module discoverable>`

      [wsgi.py]
      recipe = plone.recipe.zope2instance
      user = :nxt_ph:`admin:admin <Instance credentials; omit this line to configure them interactively>`
      eggs =
          ${instance:eggs}
      scripts =
      initialization =
          from Zope2.Startup.run import make_wsgi_app
          wsgiapp = make_wsgi_app({}, '${buildout:parts-directory}:nxt_hint:`/instance/etc/zope.conf <Path to the Zope instance's configuration>`')
          def application(*args, **kwargs):return wsgiapp(*args, **kwargs)

   It creates a new Zope instance.  The part's name must end with **.py**
   for the resulting instance script to be recognized as a Python module; the
   **initialization** `option
   <https://pypi.org/project/plone.recipe.zope2instance/#common-options>`__
   defines a WSGI entry point using **zope.conf** from the **instance**
   part in **buildout.cfg**.

   Rerun Buildout, feeding it the new configuration file:

   .. code-block:: console

      $ cd :nxt_ph:`/path/to/app/ <Path to the application directory; use a real path in your configuration>`zinstance/

   .. code-block:: console

      $ bin/buildout -c wsgi.cfg

            ...
            Installing wsgi.py.
            Generated script '/path/to/app/zinstance/bin/wsgi.py'.

   Thus created, the instance script can be used with Unit.

#. .. include:: ../include/howto_change_ownership.rst

#. Next, :ref:`prepare <configuration-python>` the |app| configuration for Unit
   (use real values for **path** and **home**):

   .. code-block:: json

      {
          "listeners": {
              "*:80": {
                  "pass": "applications/plone"
              }
          },

          "applications": {
              "plone": {
                  "type": "python :nxt_ph:`3.Y <Python executable version used to install Plone>`",
                  "path": ":nxt_ph:`/path/to/app/ <Path to the application directory; use a real path in your configuration>`zinstance/",
                  "home": ":nxt_ph:`/path/to/app/ <Path to the application directory; use a real path in your configuration>`zinstance/",
                  "module": ":nxt_hint:`bin.wsgi <WSGI module's qualified name with extension omitted>`"
              }
          }
      }

#. .. include:: ../include/howto_upload_config.rst

   After a successful update, your |app| instance should be available on the
   listener’s IP address and port:

   .. image:: ../images/plone.png
      :width: 100%
      :alt: Plone on Unit - Setup Screen
