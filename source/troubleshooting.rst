
.. highlight:: none

###############
Troubleshooting
###############

Unit log for the binary packages is located in ``/var/log/unit.log``.

Log file location can also be found by running ``unitd --help``.

Debug verbosity level of the log is enabled during configuration time::

    # ./configure --debug

Unit and all modules have to be recompiled and reinstalled after reconfiguring.

Please be aware that the debug log size grows very quickly.

Community mailing list is available at unit@nginx.org.
Subscribe to the mailing list by sending email to unit-subscribe@nginx.org
or at `here <https://mailman.nginx.org/mailman/listinfo/unit>`_.
