.. |app| replace:: Datasette
.. |mod| replace:: Python 3.6+
.. |app-pip-package| replace:: datasette
.. |app-pip-link| replace:: PIP package
.. _app-pip-link: https://docs.datasette.io/en/stable/installation.html#using-pip

#########
Datasette
#########

To run the `Datasette
<https://docs.datasette.io/en/stable/>`_ data exploration tool using Unit:

#. .. include:: ../include/howto_install_unit.rst

#. .. include:: ../include/howto_install_venv.rst

#. Running |app| on Unit requires a wrapper to expose the `application object
   <https://github.com/simonw/datasette/blob/4f7c0ebd85ccd8c1853d7aa0147628f7c1b749cc/datasette/app.py#L169>`_
   as the ASGI callable. Let's use the following basic version, saving it as
   **/path/to/app/asgi.py**:

   .. code-block:: python

      import glob
      from datasette.app import Datasette

      application = Datasette(glob.glob('*.db')).app()

#. .. include:: ../include/howto_change_ownership.rst

#. Next, :ref:`prepare <configuration-python>` the |app| configuration for
   Unit (use real values for **type**, **home**, and **path**):

   .. code-block:: json

      {
          "listeners": {
              "*:80": {
                  "pass": "applications/datasette"
              }
          },

          "applications": {
              "datasette": {
                  "type": "python 3.:nxt_ph:`Y <Must match language module version and virtual environment version>`",
                  "path": ":nxt_ph:`/path/to/app/ <Path to the ASGI module>`",
                  "home": ":nxt_ph:`/path/to/app/venv/ <Path to the virtual environment, if any>`",
                  "module": ":nxt_hint:`asgi <ASGI module filename with extension omitted>`",
                  "callable": ":nxt_hint:`app <Name of the callable in the module to run>`"
              }
          }
      }

#. .. include:: ../include/howto_upload_config.rst

   After a successful update, |app| should be available on the listener’s IP
   address and port:

   .. image:: ../images/datasette.png
      :width: 100%
      :alt: Datasette on Unit - Query Screen
