.. |app| replace:: Sanic
.. |mod| replace:: Python 3.6+

#####
Sanic
#####

To run apps built with the `Sanic
<https://sanic.readthedocs.io/en/latest/>`_ web framework using Unit:

#. .. include:: ../include/howto_install_unit.rst

#. Create a virtual environment to install |app|'s `PIP package
   <https://sanic.readthedocs.io/en/latest/sanic/getting_started.html#install-sanic>`_:

   .. code-block:: console

      $ cd /path/to/app/
      $ python3 -m venv venv
      $ source venv/bin/activate
      $ pip install sanic
      $ deactivate

#. Let's try a version of a `tutorial app
   <https://sanic.readthedocs.io/en/latest/sanic/getting_started.html#create-a-file-called-main-py>`_,
   saving it as :file:`/path/to/app/asgi.py`:

   .. code-block:: python

      from sanic import Sanic
      from sanic.response import json

      app = Sanic()

      @app.route("/")
      async def test(request):
          return json({"hello": "world"})

#. .. include:: ../include/howto_change_ownership.rst

#. Next, :ref:`put together <configuration-python>` the |app| configuration for
   Unit:

   .. code-block:: json

      {
          "listeners": {
              "*:80": {
                  "pass": "applications/sanic_app"
              }
          },

          "applications": {
              "sanic_app": {
                  "type": "python 3",
                  "user": ":nxt_term:`unit_user <User and group values must have access to path and home directories>`",
                  "group": "unit_group",
                  "path": ":nxt_term:`/path/to/app/ <Path to the ASGI module>`",
                  "home": ":nxt_term:`/path/to/app/venv/ <Path to the virtual environment, if any>`",
                  "module": ":nxt_term:`asgi <ASGI module filename with extension omitted>`",
                  "callable": ":nxt_term:`app <Name of the callable in the module to run>`"
              }
          }
      }

#. .. include:: ../include/howto_upload_config.rst

#. After a successful update, your app should be available on the listener’s IP
   address and port:

   .. code-block:: console

      $ curl http://localhost

            {"hello":"world"}
