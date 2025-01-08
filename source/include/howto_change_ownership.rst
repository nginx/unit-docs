Run the following command so Unit can access :nxt_hint:`the application
directory <If the application uses several directories, run the command for
each one>`:

.. code-block:: console

   # chown -R :nxt_hint:`unit:unit <User and group that Unit's router runs as by default>` :nxt_ph:`/path/to/app/ <Path to the application files such as /data/www/app/; use a real path in your commands>`

.. note::

   The **unit:unit** user-group pair is available only with :ref:`official
   packages <installation-precomp-pkgs>`, Docker :ref:`images
   <installation-docker>`, and some :ref:`third-party repos
   <installation-community-repos>`.  Otherwise, account names may differ; run
   the :program:`ps aux | grep unitd` command to be sure.

For further details, including permissions, see the :ref:`security checklist
<security-apps>`.
