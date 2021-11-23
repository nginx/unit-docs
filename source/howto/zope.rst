.. include:: ../include/replace.rst

.. |app| replace:: Zope
.. |mod| replace:: Python 3.6+
.. |app-link| replace:: core files
.. _app-link: https://zope.readthedocs.io/en/latest/INSTALL.html

####
Zope
####

To run apps built with the `Zope <https://zope.org>`_ web framework using Unit:

#. .. include:: ../include/howto_install_unit.rst

#. Install |app|.  Here, we do this at :samp:`/path/to/app/`; use a real path
   in your configuration.

   .. tabs::
      :prefix: installation

      .. tab:: Buildout

         First, install |app|'s `core files
         <https://zope.readthedocs.io/en/latest/INSTALL.html#installing-zope-with-zc-buildout>`__,
         for example:

         .. code-block:: console

            $ pip install -U pip wheel zc.buildout
            $ cd :nxt_ph:`/path/to/app/ <Path to the application directory; use a real path in your configuration>`
            $ wget https://pypi.org/packages/source/Z/Zope/Zope-:nxt_ph:`A.B.C <Zope version>`.tar.gz
            $ tar xfvz Zope-:nxt_ph:`A.B.C <Zope version>`.tar.gz :nxt_hint:`--strip-components <Avoids creating a redundant subdirectory>`=1
            $ buildout

         Next, add a new configuration file named
         :file:`/path/to/app/wsgi.cfg`:

         .. code-block:: cfg

            [buildout]
            extends =
                buildout.cfg

            parts +=
                :nxt_ph:`wsgi.py <The basename is arbitrary; the extension is required to make the resulting Python module discoverable>`

            [wsgi.py]
            recipe = plone.recipe.zope2instance
            user = :nxt_ph:`admin:admin <Instance credentials; omit this line to configure them interactively>`
            zodb-temporary-storage = :nxt_hint:`off <Avoids compatibility issues>`
            eggs =
            scripts =
            initialization =
                from Zope2.Startup.run import make_wsgi_app
                wsgiapp = make_wsgi_app({}, '${buildout:parts-directory}:nxt_hint:`/wsgi.py/etc/zope.conf <Path to the instance's configuration file>`')
                def application(*args, **kwargs):return wsgiapp(*args, **kwargs)

         It creates a new |app| instance.  The part's name must end with
         :samp:`.py` for the resulting instance script to be recognized as a
         Python module; the :samp:`initialization` `option
         <https://pypi.org/project/plone.recipe.zope2instance/#common-options>`__
         defines a WSGI entry point.

         Rerun Buildout, feeding it the new configuration file:

         .. code-block:: console

            $ buildout -c wsgi.cfg

                  ...
                  Installing wsgi.py.
                  Generated script '/path/to/app/bin/wsgi.py'.

         Thus created, the instance script can be used with Unit.

         .. include:: ../include/howto_change_ownership.rst

         Last, :ref:`prepare <configuration-python>` the |app| configuration
         for Unit (use a real value for :samp:`path`):

         .. code-block:: json

            {
                "listeners": {
                    "*:80": {
                        "pass": "applications/zope"
                    }
                },

                "applications": {
                    "zope": {
                        "type": "python 3",
                        "path": ":nxt_ph:`/path/to/app/ <Path to the application directory; use a real path in your configuration>`",
                        "module": ":nxt_hint:`bin.wsgi <WSGI module's qualified name with extension omitted>`"
                    }
                }
            }


      .. tab:: PIP

         Create a virtual environment to install |app|'s `PIP package
         <https://pypi.org/project/Zope/>`__:

         .. code-block:: console

            $ cd :nxt_ph:`/path/to/app/ <Path to the application directory; use a real path in your configuration>`
            $ :nxt_hint:`python3 --version <Make sure your virtual environment version matches the module version>`
                  Python :nxt_hint:`3.Y.Z <Major version, minor version, and revision number>`
            $ python3 -m venv :nxt_hint:`venv <This is the virtual environment directory>`
            $ source venv/bin/activate
            $ pip install 'zope[wsgi]'
            $ deactivate

         .. warning::

            Create your virtual environment with a Python version that matches
            the language module from Step |_| 1 up to the minor number
            (:samp:`3.Y` in this example).  Also, the app :samp:`type` in Unit
            configuration must :ref:`resolve <configuration-apps-common>` to a
            similarly matching version; Unit doesn't infer it from the
            environment.

         After installation, create your |app| `instance
         <https://zope.readthedocs.io/en/latest/operation.html#creating-a-zope-instance>`__:

         .. code-block:: console

            $ :nxt_hint:`venv/bin/mkwsgiinstance <Zope's own script>` -d :nxt_ph:`instance <The Zope instance's home directory>`

         To run the instance on Unit, create a WSGI entry point:

         .. code-block:: python

            from pathlib import Path
            from Zope2.Startup.run import make_wsgi_app

            wsgiapp = make_wsgi_app({}, :nxt_hint:`str(Path(__file__).parent / 'etc/zope.conf' <Path to the instance's configuration file>`))
            def application(*args, **kwargs):return wsgiapp(*args, **kwargs)

         Save the script as :file:`wsgi.py` in the instance home directory
         (here, it's :file:`/path/to/app/instance/`).

         .. include:: ../include/howto_change_ownership.rst

         Last, :ref:`prepare <configuration-python>` the |app| configuration
         for Unit (use real values for :samp:`path` and :samp:`home`):

         .. code-block:: json

            {
                "listeners": {
                    "*:80": {
                        "pass": "applications/zope"
                    }
                },

                "applications": {
                    "zope": {
                        "type": "python :nxt_ph:`3.Y <Must match language module version and virtual environment version>`",
                        "path": ":nxt_ph:`/path/to/app/instance/ <Path to the instance/ subdirectory; use a real path in your configuration>`",
                        "home": ":nxt_ph:`/path/to/app/venv/ <Path to the virtual environment; use a real path in your configuration>`",
                        "module": ":nxt_hint:`wsgi <WSGI module basename with extension omitted>`"
                    }
                }
            }

#. .. include:: ../include/howto_upload_config.rst

   After a successful update, your |app| instance should be available on the
   listener’s IP address and port:

   .. code-block:: console

      $ curl http://localhost

            <!DOCTYPE html>
            <html>
              <head>
            <base href="http://localhost/" />

                <title>Auto-generated default page</title>
                <meta charset="utf-8" />
              </head>
              <body>

                <h2>Zope
                    Auto-generated default page</h2>

                This is Page Template <em>index_html</em>.
              </body>
            </html>
