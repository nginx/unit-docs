.. include:: ../include/replace.rst

.. |app| replace:: Falcon
.. |mod| replace:: Python 3.5+
.. |app-pip-package| replace:: falcon
.. |app-pip-link| replace:: PIP package
.. _app-pip-link: https://falcon.readthedocs.io/en/stable/user/install.html

######
Falcon
######

To run apps built with the `Falcon <https://falcon.readthedocs.io/en/stable/>`_
web framework using Unit:

#. .. include:: ../include/howto_install_unit.rst

#. Create a virtual environment to install |app|'s |app-pip-link|_, for
   instance:

   .. subs-code-block:: console

      $ cd :nxt_ph:`/path/to/app/ <Path to the application directory; use a real path in your configuration>`
      $ :nxt_hint:`python --version <Make sure your virtual environment version matches the module version>`
            Python :nxt_hint:`X.Y.Z <Major version, minor version, and revision number>`
      $ python -m venv :nxt_hint:`venv <Arbitrary name of the virtual environment>`
      $ source :nxt_hint:`venv <Name of the virtual environment from the previous command>`/bin/activate
      $ pip install |app-pip-package|
      $ deactivate

   .. warning::

      Create your virtual environment with a Python version that matches the
      language module from Step |_| 1 up to the minor number (:samp:`X.Y` in
      this example).  Also, the app :samp:`type` in Step |_| 5 must
      :ref:`resolve <configuration-apps-common>` to a similarly matching
      version; Unit doesn't infer it from the environment.

#. Let's try an updated version of the `quickstart app
   <https://falcon.readthedocs.io/en/stable/user/quickstart.html>`_:

   .. tabs::

      .. tab:: WSGI

         .. code-block:: python

            import falcon


            # Falcon follows the REST architectural style, meaning (among
            # other things) that you think in terms of resources and state
            # transitions, which map to HTTP verbs.
            class HelloUnitResource:
                def on_get(self, req, resp):
                    """Handles GET requests"""
                    resp.status = falcon.HTTP_200  # This is the default status
                    resp.content_type = falcon.MEDIA_TEXT  # Default is JSON, so override
                    resp.text = ('Hello, Unit!')

            # falcon.App instances are callable WSGI apps
            # in larger applications the app is created in a separate file
            app = falcon.App()

            # Resources are represented by long-lived class instances
            hellounit = HelloUnitResource()

            # hellounit will handle all requests to the '/unit' URL path
            app.add_route('/unit', hellounit)

         Note that we’ve dropped the server code; save the file as
         :file:`/path/to/app/wsgi.py`.

      .. tab:: ASGI

         .. code-block:: python

            import falcon
            import falcon.asgi


            # Falcon follows the REST architectural style, meaning (among
            # other things) that you think in terms of resources and state
            # transitions, which map to HTTP verbs.
            class HelloUnitResource:
                async def on_get(self, req, resp):
                    """Handles GET requests"""
                    resp.status = falcon.HTTP_200  # This is the default status
                    resp.content_type = falcon.MEDIA_TEXT  # Default is JSON, so override
                    resp.text = ('Hello, Unit!')

            # falcon.asgi.App instances are callable ASGI apps...
            # in larger applications the app is created in a separate file
            app = falcon.asgi.App()

            # Resources are represented by long-lived class instances
            hellounit = HelloUnitResource()

            # hellounit will handle all requests to the '/unit' URL path
            app.add_route('/unit', hellounit)

         Save the file as :file:`/path/to/app/asgi.py`.

4. .. include:: ../include/howto_change_ownership.rst

#. Next, :ref:`prepare <configuration-python>` the configuration for Unit (use
   real values for :samp:`type`, :samp:`home`, :samp:`module`,
   :samp:`protocol`, and :samp:`path`):

   .. code-block:: json

      {
          "listeners": {
              "*:80": {
                  "pass": "applications/falcon"
              }
          },

          "applications": {
              "falcon": {
                  "type": "python :nxt_ph:`X.Y <Must match language module version and virtual environment version>`",
                  "path": ":nxt_ph:`/path/to/app/ <Path to the WSGI module; use a real path in your configuration>`",
                  "home": ":nxt_ph:`/path/to/app/venv/ <Path to the virtual environment, if any; use a real path in your configuration>`",
                  "module": ":nxt_ph:`module_basename <WSGI/ASGI module basename with extension omitted, such as 'wsgi' or 'asgi' from Step 3>`",
                  "protocol": ":nxt_ph:`wsgi_or_asgi <'wsgi' or 'asgi', as appropriate>`",
                  "callable": ":nxt_hint:`app <Name of the callable in the module to run>`"
              }
          }
      }

#. .. include:: ../include/howto_upload_config.rst

   After a successful update, your app should be available on the listener’s IP
   address and port:

   .. code-block:: console

      $ curl http://localhost/unit

            Hello, Unit!
