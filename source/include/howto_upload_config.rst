Upload the updated configuration.  Assuming the JSON above was added to
:file:`config.json`:

.. code-block:: console

   # curl -X PUT --data-binary @config.json --unix-socket \
          :nxt_ph:`/path/to/control.unit.sock <Path to Unit's control socket in your installation>` :nxt_hint:`http://localhost/config/ <Path to the config section in Unit's control API>`

.. note::

   The control socket path may vary; run :program:`unitd -h` or see
   :ref:`source-startup` for details.
