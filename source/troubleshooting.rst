
###############
Troubleshooting
###############

.. _troubleshooting-log:

*******
Logging
*******

Unit maintains a single general-purpose :nxt_term:`log <A system-wide log for
runtime messaging, usually found at /var/log/unit.log>` for diagnostics and
troubleshooting (not to be confused with the :ref:`access log
<configuration-access-log>`).  To find out its default location in your Unit
installation:

.. code-block:: console

   $ unitd --help

       unit options:
       ...
       --log FILE           set log filename
                            default: "/path/to/unit.log"

The :option:`!--log` option overrides the default value; if Unit is already
running, check whether this option is set:

.. subs-code-block:: console

   $ ps ax | grep unitd
       ...
       unit: main v|version| [/path/to/unitd ... --log /path/to/unit.log ...]

If Unit isn't running, see its system startup scripts or configuration files to
check if :option:`!--log` is set, and how.

.. note::

   Mind that our Docker images forward their log output to the `Docker log
   collector <https://docs.docker.com/config/containers/logging/>`_ instead of
   a file.


.. _troubleshooting-dbg-log:

*********
Debug Log
*********

Unit log has two verbosity modes: common and debug; steps to enable the latter
vary by install method.

.. warning::

   Debug log is meant for developers; it grows rapidly, so enable it only for
   detailed reports and inspection.

=========================
Installing From Our Repos
=========================

Our :ref:`repositories <installation-precomp-pkgs>` provide a debug version of
:program:`unitd` called :program:`unitd-debug` within the :program:`unit`
package:

.. code-block:: console

   # unitd-debug <command line options>

.. note::

   Also, there are debug symbol packages for :ref:`core dump analysis
   <troubleshooting-core-dumps>`; their names end in :samp:`-dbg`, like
   :samp:`unit-dbg`.

==========================
Running From Docker Images
==========================

To enable debug-level logging when using our Docker :ref:`images
<installation-docker>`:

.. subs-code-block:: console

   $ docker run -d nginx/unit:|version|-full unitd-debug --no-daemon \
                --control unix:/var/run/control.unit.sock

Another option is adding a new layer in a Dockerfile:

.. subs-code-block:: docker

   FROM nginx/unit:|version|-full

   CMD ["unitd-debug","--no-daemon","--control","unix:/var/run/control.unit.sock"]

The :samp:`CMD` instruction above replaces the default :program:`unitd`
executable with its debug version.

====================
Building From Source
====================

To enable debug-level logging when :ref:`installing from source
<installation-src>`, use the :option:`!--debug` option:

.. code-block:: console

   $ ./configure --debug <other options>

Then recompile and reinstall Unit and your specific :ref:`language modules
<installation-src-modules>`.


.. _troubleshooting-core-dumps:

**********
Core Dumps
**********

Core dumps help developers to resolve Unit crashes; providing them with your
feedback is recommended.

.. note::

   This section assumes you're running Unit as :samp:`root` (recommended).

.. warning::

   Disable core dumping on live production systems to avoid wasting disk space.

===============
Systemd Service
===============

To enable saving core dumps while running Unit as a :program:`systemd` service
(for example, with :ref:`packaged installations <installation-precomp-pkgs>`),
adjust the `service settings
<https://www.freedesktop.org/software/systemd/man/systemd.exec.html>`_ in
:file:`/lib/systemd/system/unit.service`:

.. code-block:: ini

   [Service]
   ...
   LimitCORE=infinity
   LimitNOFILE=655356

Alternatively, update the `global settings
<https://www.freedesktop.org/software/systemd/man/systemd.directives.html>`_
in :file:`/etc/systemd/system.conf`:

.. code-block:: ini

   [Manager]
   ...
   DefaultLimitCORE=infinity
   DefaultLimitNOFILE=655356

Next, reload the service configuration and restart Unit to reproduce the crash
condition:

.. code-block:: console

   # systemctl daemon-reload
   # systemctl restart unit.service

After a crash, locate the core dump file:

.. code-block:: console

   # coredumpctl -1                     # optional

         TIME                            PID   UID   GID SIG COREFILE  EXE
         Mon 2020-07-27 11:05:40 GMT    1157     0     0  11 present   /usr/sbin/unitd

   # ls -al /var/lib/systemd/coredump/  # default, see also /etc/systemd/coredump.conf and /etc/systemd/coredump.conf.d/*.conf

         ...
         -rw-r----- 1 root root 177662 Jul 27 11:05 core.unitd.0.6135489c850b4fb4a74795ebbc1e382a.1157.1590577472000000.lz4

============
Manual Setup
============

Linux
*****

Check the `core dump settings
<https://www.man7.org/linux/man-pages/man5/limits.conf.5.html>`__ in
:file:`/etc/security/limits.conf`, adjusting them if necessary:

.. code-block:: none

   root           soft    core       0          # disables core dumps by default
   root           hard    core       unlimited  # enables raising the size limit

Next, `raise
<https://www.man7.org/linux/man-pages/man1/bash.1.html>`_ the core dump size
limit and restart Unit to reproduce the crash condition:

.. code-block:: console

   # ulimit -c unlimited
   # cd /path/to/unit/
   # sbin/unitd           # or sbin/unitd-debug

After a crash, locate the core dump file:

.. code-block:: console

   # ls -al /path/to/unit/working/directory/  # default location, see /proc/sys/kernel/core_pattern

         ...
         -rw-r----- 1 root root 177662 Jul 27 11:05 core.1157

FreeBSD
*******

Check the `core dump settings
<https://www.freebsd.org/cgi/man.cgi?query=sysctl>`__ in
:file:`/etc/sysctl.conf`, adjusting them if necessary:

.. code-block:: ini

   kern.coredump=1
   # must be set to 1
   kern.corefile=/path/to/core/files/%N.core
   # must provide a valid pathname

Alternatively, update the settings in runtime:

.. code-block:: console

   # sysctl kern.coredump=1
   # sysctl kern.corefile=/path/to/core/files/%N.core

Next, restart Unit to reproduce the crash condition.  If installed as a
service:

.. code-block:: console

   # service unitd restart

If installed manually:

.. code-block:: console

   # cd /path/to/unit/
   # sbin/unitd

After a crash, locate the core dump file:

.. code-block:: console

   # ls -al /path/to/core/files/

         ...
         -rw-------  1 root     root  9912320 Jul 27 11:05 unitd.core

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
