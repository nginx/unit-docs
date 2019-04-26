Prepare Unit configuration for your update.  To obtain an initial template,
query the control API:

.. code-block:: console

   $ curl --unix-socket /path/to/control.unit.sock \
          http://localhost/config/ > config.json

.. note::

   Control socket path may vary; run :command:`unitd --help` or see
   :ref:`installation-startup` for details.
