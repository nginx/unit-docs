
.. highlight:: none

###############
Troubleshooting
###############

Logging
=======

For diagnostics and troubleshooting, Unit provides a single general-purpose
log.  Usually, the log file is found here: ``/var/log/unit.log``.  To locate
it in your system, run ``unitd --help``::

    # unitd --help

        unit options:
        ...
        --log FILE           set log filename
                             default: "/home/user/unit.log"

As the output above suggests, log location can be customized at startup:
``unitd --log FILE``.  To look at Unit's command line arguments, run the
following command::

    # ps ax | grep unitd

If Unit's not running, refer to Unit-related startup scripts or configuration
files in your system to discover the log file location.

Debug Log
---------

Unit log supports two verbosity modes: common and debug.  The steps
to enable debug-level logging depend on how you install Unit.

Warning: Debug log grows very quickly.  It is intended for developers and
should be enabled for detailed reporting and investigation.

Installation From Our Repositories
**********************************

When you install Unit using the binary packages from :ref:`our repositories
<installation-precomp-pkgs>`, a debug version of ``unitd`` is installed from
the ``unit`` package, called ``unitd-debug``.  To start Unit in debug mode,
run the following command::

    # unitd-debug <command line options>

Also, our repositories include packages with debug symbols for core dump
analysis.  They have ``-dbg`` suffixes, for example ``unit-dbg``.

Installation From Source
************************

To configure debug-level logging when installing from source, use the
``--debug`` option::

    # ./configure --debug

Then recompile and reinstall Unit modules.

Getting Support
===============

Mailing List
------------

For any unresolved questions, a community mailing list is available:
unit@nginx.org.  To subscribe, send an email to unit-subscribe@nginx.org or
sign up `here <https://mailman.nginx.org/mailman/listinfo/unit>`_.

Development
-----------

You can also visit our GitHub repositories to report an issue, suggest a
feature, or ask questions:

* https://github.com/nginx/unit
* https://github.com/nginx/unit-docs
