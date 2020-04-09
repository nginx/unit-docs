
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

   Also, there are debug symbol packages for core dump analysis; their names
   end in :samp:`-dbg`, like :samp:`unit-dbg`.

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
