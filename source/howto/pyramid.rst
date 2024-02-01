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

      Here, **$VENV** isn't set because Unit picks up the virtual
      environment from **home** in Step |_| 5.

#. Let's see how the apps from the Pyramid `tutorial
   <https://docs.pylonsproject.org/projects/pyramid/en/latest/quick_tutorial>`__
   run on Unit.

   .. tabs::
      :prefix: pyramid

      .. tab:: Single-File

         We modify the `tutorial app
         <https://docs.pylonsproject.org/projects/pyramid/en/latest/quick_tutorial/hello_world.html#steps>`_,
         saving it as **/path/to/app/wsgi.py**:

         .. code-block:: python

            from pyramid.config import Configurator
            from pyramid.response import Response

            def hello_world(request):
                return Response('<body><h1>Hello, World!</h1></body>')

            with Configurator() as config:
                config.add_route('hello', '/')
                config.add_view(hello_world, route_name='hello')
                :nxt_hint:`app <Callable's name is used in Unit configuration>` = config.make_wsgi_app()
            # serve(app, host='0.0.0.0', port=6543)

         Note that we've dropped the server code; also, mind that Unit imports
         the module, so the **if __name__ == '__main__'** idiom would be
         irrelevant.


      .. tab:: INI-Based

         To load the `configuration
         <https://docs.pylonsproject.org/projects/pyramid/en/latest/quick_tutorial/ini.html>`__,
         we place a **wsgi.py** file next to **development.ini** in
         **/path/to/app/**:

         .. code-block:: python

            from pyramid.paster import get_app, setup_logging

            :nxt_hint:`app <Callable's name is used in Unit configuration>` = get_app('development.ini')
            setup_logging('development.ini')

         This `sets up
         <https://docs.pylonsproject.org/projects/pyramid/en/latest/api/paster.html>`__
         the WSGI application for Unit; if the **.ini**'s pathname is
         relative, provide the appropriate **working_directory** in Unit
         configuration.

#. .. include:: ../include/howto_change_ownership.rst

#. Next, :ref:`prepare <configuration-python>` the |app| configuration
   for Unit (use real values for **type**, **home**, and
   **path**):

   .. code-block:: json

      {
          "listeners": {
              "*:80": {
                  "pass": "applications/pyramid"
              }
          },

          "applications": {
              "pyramid": {
                  "type": "python 3.:nxt_ph:`Y <Must match language module version and virtual environment version>`",
                  "working_directory": ":nxt_ph:`/path/to/app/ <Path to the application directory; use a real path in your configuration>`",
                  "path": ":nxt_ph:`/path/to/app/ <Path to the application directory; use a real path in your configuration>`",
                  "home": ":nxt_ph:`/path/to/app/venv/ <Path to the virtual environment, if any>`",
                  "module": ":nxt_hint:`wsgi <WSGI module filename with extension omitted>`",
                  "callable": ":nxt_hint:`app <Name of the callable in the module to run>`"
              }
          }
      }

#. .. include:: ../include/howto_upload_config.rst

   After a successful update, your app should be available on the listener’s IP
   address and port:

   .. code-block:: console

      $ curl http://localhost

            <body><h1>Hello, World!</h1></body>
