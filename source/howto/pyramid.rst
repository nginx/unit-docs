.. |app| replace:: Pyramid
.. |mod| replace:: Python 3

#######
Pyramid
#######

To run apps built with the `Pyramid <https://trypyramid.com>`_ web framework
using Unit:

#. .. include:: ../include/howto_install_unit.rst

#. Create a virtual environment to install |app|'s `PIP package
   <https://docs.pylonsproject.org/projects/pyramid/en/latest/narr/install.html#installing-pyramid-on-a-unix-system>`_
   (note that there's no need to set :samp:`$VENV`):

   .. code-block:: console

      $ cd /path/to/app/
      $ python3 -m venv venv
      $ venv/bin/activate
      $ pip install pyramid
      $ deactivate

#. Let's try a modified version of a `tutorial app
   <https://docs.pylonsproject.org/projects/pyramid/en/latest/quick_tutorial/hello_world.html#steps>`_,
   saving it as :file:`/path/to/app/wsgi.py`:

   .. code-block:: python

      from pyramid.config import Configurator
      from pyramid.response import Response


      def hello_world(request):
          return Response('<body><h1>Hello World!</h1></body>')

      with Configurator() as config:
          config.add_route('hello', '/')
          config.add_view(hello_world, route_name='hello')
          :nxt_term:`application <Callable name expected by Unit>` = config.make_wsgi_app()

   Note that we've dropped the server code and altered the callable name.

#. .. include:: ../include/howto_change_ownership.rst

#. Next, :ref:`put together <configuration-php>` the |app| configuration for
   Unit:

   .. code-block:: json

      {
          "listeners": {
              "*:80": {
                  "pass": "applications/pyramid_app"
              }
          },

          "applications": {
              "pyramid_app": {
                  "type": "python 3",
                  "user": ":nxt_term:`unit_user <User and group values must have access to target root directories>`",
                  "group": "unit_group",
                  "path": "/path/to/app/",
                  "home": "/path/to/app/venv/",
                  "module": "wsgi"
              }
          }
      }

#. .. include:: ../include/howto_upload_config.rst

#. After a successful update, your app should be available on the listener’s IP
   address and port:

   .. code-block:: console

      $ curl http://localhost

            <body><h1>Hello World!</h1></body>
