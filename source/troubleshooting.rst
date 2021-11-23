.. meta::
   :og:description: Troubleshoot issues using logs, core dumps, and community
                    support.

.. include:: include/replace.rst

###############
Troubleshooting
###############

.. _troubleshooting-log:

*******
Logging
*******

Unit maintains a single general-purpose :nxt_hint:`log <A system-wide log for
runtime messaging, usually found at /var/log/unit.log>` for diagnostics and
troubleshooting (not to be confused with the :ref:`access log
<configuration-access-log>`).  To find out its default location in your
installation:

.. code-block:: console

   $ unitd -h

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

Unit's log has two verbosity modes, common and debug; the steps to enable debug
vary by install method.

.. warning::

   Debug log is meant for developers; it grows rapidly, so enable it only for
   detailed reports and inspection.

.. tabs::
   :prefix: debug-log
   :toc:

   .. tab:: Installing From Our Repos

      Our :ref:`repositories <installation-precomp-pkgs>` provide a debug
      version of :program:`unitd` called :program:`unitd-debug` within the
      :program:`unit` package:

      .. code-block:: console

         # unitd-debug <command line options>


   .. tab:: Running From Docker Images

      To enable debug-level logging when using our Docker :ref:`images
      <installation-docker>`:

      .. subs-code-block:: console

         $ docker run -d nginx/unit:|version|-full unitd-debug --no-daemon  \
               --control unix:/var/run/control.unit.sock

      Another option is adding a new layer in a Dockerfile:

      .. subs-code-block:: docker

         FROM nginx/unit:|version|-full

         CMD ["unitd-debug","--no-daemon","--control","unix:/var/run/control.unit.sock"]

      The :samp:`CMD` instruction above replaces the default :program:`unitd`
      executable with its debug version.


   .. tab:: Building From Source

      To enable debug-level logging when :ref:`installing from source
      <installation-src>`, use the :option:`!--debug` option:

      .. code-block:: console

         $ ./configure --debug <other options>

      Then recompile and reinstall Unit and your :ref:`language
      modules <installation-src-modules>` of choice.


.. _troubleshooting-core-dumps:

**********
Core Dumps
**********

Core dumps help us investigate crashes; attach them when :ref:`reporting an
issue <troubleshooting-support>`.  For builds from :ref:`our repositories
<installation-precomp-pkgs>`, we maintain debug symbols in special packages;
they have the original packages' names with the :samp:`-dbg` suffix appended,
such as :samp:`unit-dbg`.

.. note::

   This section assumes you're running Unit as :samp:`root` (recommended).

.. tabs::
   :prefix: core-dumps
   :toc:

   .. tab:: Linux: systemd

      To enable saving core dumps while running Unit as a :program:`systemd`
      service (for example, with :ref:`packaged installations
      <installation-precomp-pkgs>`), adjust the `service settings
      <https://www.freedesktop.org/software/systemd/man/systemd.exec.html>`_ in
      :file:`/lib/systemd/system/unit.service`:

      .. code-block:: ini

         [Service]
         ...
         LimitCORE=infinity
         LimitNOFILE=65535

      Alternatively, update the `global settings
      <https://www.freedesktop.org/software/systemd/man/systemd.directives.html>`_
      in :file:`/etc/systemd/system.conf`:

      .. code-block:: ini

         [Manager]
         ...
         DefaultLimitCORE=infinity
         DefaultLimitNOFILE=65535

      Next, reload the service configuration and restart Unit to reproduce the
      crash condition:

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


   .. tab:: Linux: Manual Setup

      Check the `core dump settings
      <https://www.man7.org/linux/man-pages/man5/limits.conf.5.html>`__ in
      :file:`/etc/security/limits.conf`, adjusting them if necessary:

      .. code-block:: none

         root           soft    core       0          # disables core dumps by default
         root           hard    core       unlimited  # enables raising the size limit

      Next, `raise <https://www.man7.org/linux/man-pages/man1/bash.1.html>`_
      the core dump size limit and restart Unit to reproduce the crash
      condition:

      .. code-block:: console

         # ulimit -c unlimited
         # cd /path/to/unit/
         # sbin/unitd           # or sbin/unitd-debug

      After a crash, locate the core dump file:

      .. code-block:: console

         # ls -al /path/to/unit/working/directory/  # default location, see /proc/sys/kernel/core_pattern

               ...
               -rw-r----- 1 root root 177662 Jul 27 11:05 core.1157


   .. tab:: FreeBSD

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

      Next, restart Unit to reproduce the crash condition.  If Unit is
      installed as a service:

      .. code-block:: console

         # service unitd restart

      If it's installed manually:

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

.. list-table::
   :header-rows: 1

   * - Support |_| Channel
     - Details

   * - GitHub
     - Visit our `repo <https://github.com/nginx/unit>`__ to submit issues,
       suggest features, ask questions, or see the roadmap.

   * - Mailing lists
     - To post questions to unit@nginx.org and get notifications, including
       release news, email unit-subscribe@nginx.org or sign up `here
       <https://mailman.nginx.org/mailman/listinfo/unit>`_.  To receive all OSS
       release announcements from NGINX, join the general mailing list `here
       <https://mailman.nginx.org/mailman/listinfo/nginx-announce>`__.

   * - Security alerts
     - Please report security issues to `security-alert@nginx.org
       <security-alert@nginx.org>`__, specifically mentioning NGINX Unit in the
       subject and following the `CVSS v3.1
       <https://www.first.org/cvss/v3.1/specification-document>`_
       specification.

In addition, we offer `commercial support <https://www.nginx.com/support/>`_.
