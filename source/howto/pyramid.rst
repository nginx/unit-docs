.. |app| replace:: Pyramid
.. |mod| replace:: Python 3
.. |app-pip-package| replace:: pyramid
.. |app-pip-link| replace:: PIP package
.. _app-pip-link: https://docs.pylonsproject.org/projects/pyramid/en/latest/narr/install.html#installing-pyramid-on-a-unix-system

#######
Pyramid
#######

To run apps built with the `Pyramid <https://trypyramid.com>`_ web framework
using Unit:

#. .. include:: ../include/howto_install_unit.rst

#. .. include:: ../include/howto_install_venv.rst

   .. note::

      Here, :samp:`$VENV` isn't set because Unit picks up the virtual
      environment from :samp:`home` in Step |_| 5.

#. Let's try a modified version of a `tutorial app
   <https://docs.pylonsproject.org/projects/pyramid/en/latest/quick_tutorial/hello_world.html#steps>`_,
   saving it as :file:`/path/to/app/wsgi.py`:

   .. code-block:: python

      from pyramid.config import Configurator
      from pyramid.response import Response


      def hello_world(request):
          return Response('<body><h1>Hello, World!</h1></body>')

      with Configurator() as config:
          config.add_route('hello', '/')
          config.add_view(hello_world, route_name='hello')
          app = config.make_wsgi_app()
      # serve(app, host='0.0.0.0', port=6543)

   Note that we've dropped the server code.

#. .. include:: ../include/howto_change_ownership.rst

#. Next, :ref:`put together <configuration-python>` the |app| configuration for
   Unit:

   .. code-block:: json

      {
          "listeners": {
              "*:80": {
                  "pass": "applications/pyramid"
              }
          },

          "applications": {
              "pyramid": {
                  "type": ":nxt_term:`python 3.x <Must match language module version and virtual environment version>`",
                  "user": ":nxt_term:`app_user <User and group values must have access to path and home directories>`",
                  "group": "app_group",
                  "path": "/path/to/app/",
                  "home": "/path/to/app/venv/",
                  "module": "wsgi",
                  "callable": ":nxt_term:`app <Name of the callable in the module to run>`"
              }
          }
      }

#. .. include:: ../include/howto_upload_config.rst

#. After a successful update, your app should be available on the listener’s IP
   address and port:

   .. code-block:: console

      $ curl http://localhost

            <body><h1>Hello, World!</h1></body>
