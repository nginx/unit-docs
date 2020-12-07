Upload the updated configuration.  Assuming the JSON above was added to
:file:`config.json`:

.. code-block:: console

   # curl -X PUT --data-binary @config.json --unix-socket \
          :nxt_term:`/path/to/control.unit.sock <Path to Unit control socket in your installation>` :nxt_term:`http://localhost/config/ <Path to config section in Unit API>`

.. note::

   The control socket path may vary; run :program:`unitd --help` or see
   :ref:`installation-src-startup` for details.
