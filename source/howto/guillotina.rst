.. |app| replace:: Guillotina
.. |mod| replace:: Python 3.7+
.. |app-pip-package| replace:: guillotina
.. |app-pip-link| replace:: PIP package
.. _app-pip-link: https://guillotina.readthedocs.io/en/latest/training/installation.html

##########
Guillotina
##########

To run apps built with the `Guillotina
<https://guillotina.readthedocs.io/en/latest/>`_ web framework using Unit:

#. .. include:: ../include/howto_install_unit.rst

#. .. include:: ../include/howto_install_venv.rst

#. Let's try a version of the `tutorial app
   <https://guillotina.readthedocs.io/en/latest/#build-a-guillotina-app>`_,
   saving it as **/path/to/app/asgi.py**:

   .. code-block:: python

      from guillotina import configure
      from guillotina import content
      from guillotina import schema
      from guillotina.factory import make_app
      from zope import interface


      class IMyType(interface.Interface):
          textline = schema.TextLine()


      @configure.contenttype(
          type_name="MyType",
          schema=IMyType,
          behaviors=["guillotina.behaviors.dublincore.IDublinCore"],
      )
      class MyType(content.Resource):
          pass


      @configure.service(
          context=IMyType,
          method="GET",
          permission="guillotina.ViewContent",
          name="@textline",
      )
      async def textline_service(context, request):
          return {"textline": context.textline}


      :nxt_hint:`application <Callable name that Unit looks for>` = make_app(
              settings={
                  "applications": ["__main__"],
                  "root_user": {"password": "root"},
                  "databases": {
                      "db": {"storage": "DUMMY_FILE", "filename": "dummy_file.db",}
                  },
              }
          )

   Note that all server calls and imports are removed.

#. .. include:: ../include/howto_change_ownership.rst

#. Next, :ref:`prepare <configuration-python>` the |app| configuration for
   Unit (use real values for **type**, **home**, and **path**):

   .. code-block:: json

      {
          "listeners": {
              "*:80": {
                  "pass": "applications/guillotina"
              }
          },

          "applications": {
              "guillotina": {
                  "type": "python 3.:nxt_ph:`Y <Must match language module version and virtual environment version>`",
                  "path": ":nxt_ph:`/path/to/app/ <Path to the ASGI module>`",
                  "home": ":nxt_ph:`/path/to/app/venv/ <Path to the virtual environment, if any>`",
                  "module": ":nxt_hint:`asgi <ASGI module filename with extension omitted>`",
                  "protocol": ":nxt_hint:`asgi <Protocol hint for Unit, required to run Guillotina apps>`"
              }
          }
      }

#. .. include:: ../include/howto_upload_config.rst

   After a successful update, your app should be available on the listener’s IP
   address and port:

   .. code-block:: console

      $ curl -XPOST --user root:root http://localhost/db \
             -d '{ "@type": "Container", "id": "container" }'

            {"@type":"Container","id":"container","title":"container"}

   .. code-block:: console

      $ curl --user root:root http://localhost/db/container

            {
                "@id": "http://localhost/db/container",
                "@type": "Container",
                "@name": "container",
                "@uid": "84651300b2f14170b2b2e4a0f004b1a3",
                "@static_behaviors": [
                ],
                "parent": {
                },
                "is_folderish": true,
                "creation_date": "2020-10-16T14:07:35.002780+00:00",
                "modification_date": "2020-10-16T14:07:35.002780+00:00",
                "type_name": "Container",
                "title": "container",
                "uuid": "84651300b2f14170b2b2e4a0f004b1a3",
                "__behaviors__": [
                ],
                "items": [
                ],
                "length": 0
            }
