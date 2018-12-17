###############
Troubleshooting
###############

.. _troubleshooting-log:

*******
Logging
*******

Unit maintains a single general-purpose log for diagnostics and troubleshooting
(not to be confused with the :ref:`access log <configuration-access-log>`).
Usually, the log file is found here: :file:`/var/log/unit.log`; to locate it in
your system:

.. code-block:: console

    # unitd --help

        unit options:
        ...
        --log FILE           set log filename
                             default: "/home/user/unit.log"

Use :command:`unitd --log <filename>` to set the location at startup.  To
check the settings of a running :program:`unitd`:

.. code-block:: console

    # ps ax | grep unitd
        ...
        unit: main v1.6 [/usr/sbin/unitd --log /var/log/unit.log --pid /run/unit.pid]

If Unit's not running, see its startup scripts or configuration files in your
system to discover the log location.

.. _troubleshooting-dbg-log:

*********
Debug Log
*********

Unit log has two verbosity modes: common and debug; steps to enable the latter
vary by install method.

.. warning::

    Debug log is meant for developers; it grows rapidly, so enable it only for
    detailed reports and inspection.

==================================
Installation From Our Repositories
==================================

Our :ref:`repositories <installation-precomp-pkgs>` provide a debug version of
:program:`unitd` called :program:`unitd-debug` within the :program:`unit`
package:

.. code-block:: console

    # unitd-debug <command line options>

.. note::

    Also, there are debug symbol packages for core dump analysis; their names
    end in :samp:`-dbg`, like :samp:`unit-dbg`.

========================
Installation From Source
========================

To enable debug-level logging when :ref:`installing from source
<installation-src>`, use the :option:`!--debug` option:

.. code-block:: console

    # ./configure --debug <other options>

Then recompile and reinstall Unit and your specific :ref:`language modules
<installation-src-modules>`.

.. _troubleshooting-support:

***************
Getting Support
***************

Post your questions to our mailing list at unit@nginx.org; to subscribe, email
unit-subscribe@nginx.org or sign up `here
<https://mailman.nginx.org/mailman/listinfo/unit>`_.  You can also visit our
`GitHub repo <https://github.com/nginx/unit>`_ to report an issue, suggest a
feature, or share a problem.

In addition, we offer `commercial support <https://www.nginx.com/support/>`_.
