Run the following command for each directory containing app code or data so
Unit can access it:

.. code-block:: console

   # chown -R :nxt_term:`unit:unit <User and group that Unit's router runs as by default>` :nxt_term:`/path/to/app/ <Path to the application files such as /data/www/app/; use real path in your commands>`

.. note::

   The :samp:`unit:unit` user-group pair is available only with :ref:`official
   packages <installation-precomp-pkgs>`, Docker :ref:`images
   <installation-docker>`, and some :ref:`third-party repos
   <installation-community-repos>`.  Otherwise, account names may differ; run
   the :program:`ps aux | grep unitd` command to be sure.

For further details, including permissions, see the :ref:`security checklist
<security-apps>`.
