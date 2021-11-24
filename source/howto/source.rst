.. include:: ../include/replace.rst

####################
Building From Source
####################

After you've obtained Unit's :ref:`source code <source>`, configure
and compile it to fine-tune and run a custom Unit build.

.. _source-prereq-build:

============================
Installing Required Software
============================

Before configuring and compiling Unit, install the required build tools and
the library files for the supported languages (Go, Java, Node.js, PHP, Perl,
Python, and Ruby), plus other features you want to use with Unit.

The commands below assume you are configuring Unit with all supported languages
and features (:samp:`X`, :samp:`Y`, and :samp:`Z` stand in for major, minor,
and revision numbers, respectively); omit the packages you won't use.

.. tabs::
   :prefix: prereq
   :toc:

   .. tab:: Debian, Ubuntu

      .. code-block:: console

         # apt install build-essential
         # apt install golang
         # curl -sL https://deb.nodesource.com/setup_:nxt_ph:`X.Y <Node.js 8.11 or later is supported>` | bash -
         # apt install nodejs
         # npm install -g node-gyp
         # apt install php-dev libphp-embed
         # apt install libperl-dev
         # apt install python-dev
         # apt install ruby-dev
         # apt install openjdk-:nxt_ph:`X <Java 8 or later is supported. Different JDKs may be used>`-jdk
         # apt install libssl-dev
         # apt install libpcre2-dev


   .. tab:: Amazon, CentOS, Fedora, RHEL

      .. code-block:: console

         # yum install gcc make
         # yum install golang
         # curl -sL https://rpm.nodesource.com/setup_:nxt_ph:`X.Y <Node.js 8.11 or later is supported>` | bash -
         # yum install nodejs
         # npm install -g node-gyp
         # yum install php-devel php-embedded
         # yum install perl-devel perl-libs
         # yum install python-devel
         # yum install ruby-devel
         # yum install java-:nxt_ph:`X.Y.Z <Java 8 or later is supported. Different JDKs may be used>`-openjdk-devel
         # yum install openssl-devel
         # yum install pcre2-devel


   .. tab:: FreeBSD

      Ports:

      .. code-block:: console

         # cd /usr/ports/lang/go/ && make install clean
         # cd /usr/ports/www/node/ && make install clean
         # cd /usr/ports/www/npm/ && make install clean && npm i -g node-gyp
         # cd /usr/ports/lang/php:nxt_ph:`XY <PHP versions 5, 7, and 8 are supported>`/ && make install clean
         # cd /usr/ports/lang/perl:nxt_ph:`X.Y <Perl 5.12 or later is supported>`/ && make install clean
         # cd /usr/ports/lang/python/ && make install clean
         # cd /usr/ports/lang/ruby:nxt_ph:`XY <Ruby 2.0 or later is supported>`/ && make install clean
         # cd /usr/ports/java/openjdk:nxt_ph:`X <Java 8 or later is supported. Different JDKs may be used>`/ && make install clean
         # cd /usr/ports/security/openssl/ && make install clean
         # cd /usr/ports/devel/pcre2/ && make install clean

      Packages:

      .. code-block:: console

         # pkg install go
         # pkg install node && pkg install npm && npm i -g node-gyp
         # pkg install php:nxt_ph:`XY <PHP versions 5, 7, and 8 are supported>`
         # pkg install perl:nxt_ph:`X <Perl 5.12 or later is supported>`
         # pkg install python
         # pkg install ruby:nxt_ph:`XY <Ruby 2.0 is supported>`
         # pkg install openjdk:nxt_ph:`X <Java 8 or later is supported. Different JDKs may be used>`
         # pkg install openssl
         # pkg install pcre2


   .. tab:: Solaris

      .. code-block:: console

         # pkg install gcc
         # pkg install golang
         # pkg install php-:nxt_ph:`XY <PHP versions 5, 7, and 8 are supported>`
         # pkg install ruby
         # pkg install jdk-:nxt_ph:`X <Java 8 or later is supported. Different JDKs may be used>`
         # pkg install openssl
         # pkg install pcre

      Also, use :program:`gmake` instead of :program:`make` when :ref:`building
      and installing <source-bld-src>` Unit on Solaris.


.. _source-config-src:

===================
Configuring Sources
===================

To run system compatibility checks and generate a :file:`Makefile` with core
build instructions for Unit:

.. code-block:: console

   $ ./configure :nxt_ph:`COMPILE-TIME OPTIONS <See the table below>`

To finalize the resulting :file:`Makefile`, configure the :ref:`language
modules <source-modules>` you need.

General options and settings that control compilation, runtime privileges,
or support for certain features:

.. list-table::

   * - :samp:`--help`
     -  Displays a summary of common :program:`./configure` options.

        For language-specific details, run :command:`./configure <language>
        --help` or see :ref:`below <source-modules>`.

   * - :samp:`--cc=pathname`
     - Custom C compiler pathname.

       The default is :samp:`cc`.

   * - :samp:`--cc-opt=options`, :samp:`--ld-opt=options`
     - Extra options for the C compiler and linker.

   * - :samp:`--group=name`, :samp:`--user=name`
     - Group name and username to run Unit's non-privileged :ref:`processes
       <security-apps>`.

       The defaults are :option:`!--user`'s primary group and
       :samp:`nobody`, respectively.

   * - :samp:`--debug`
     - Turns on the :ref:`debug log <troubleshooting-dbg-log>`.

   * - :samp:`--no-ipv6`
     - Turns off IPv6 support.

   * - :samp:`--no-unix-sockets`
     - Turns off Unix domain sockets support.

   * - :samp:`--openssl`
     - Turns on OpenSSL support.  Make sure that OpenSSL (1.0.1 and later)
       header files and libraries are available in your compiler's search path.

       To customize the path, provide the :option:`!--cc-opt` and
       :option:`!--ld-opt` options; you can also set the :envvar:`CFLAGS` and
       :envvar:`LDFLAGS` environment variables before running
       :program:`./configure`.

       For details, see :ref:`configuration-ssl`.

.. _source-config-src-pcre:

By default, Unit relies on the installed version of the `PCRE
<https://www.pcre.org>`_ library to support regular expressions in :ref:`routes
<configuration-routes>`; if both major versions are present, Unit selects
PCRE2.  Two additional flags alter this behavior:

.. list-table::

   * - :samp:`--no-regex`
     - Turns off regex support; any attempts to use a regex in Unit
       configuration will fail.

   * - :samp:`--no-pcre2`
     - Skips the PCRE2 library; the older PCRE 8.x library is used instead.

The next option group customizes Unit's :ref:`runtime directory
structure <source-dir>`:

.. list-table::

   * - :samp:`--prefix=prefix`
     - .. _source-config-src-prefix:

       Destination directory prefix for :ref:`path options
       <source-dir>`: :option:`!--bindir`, :option:`!--sbindir`,
       :option:`!--libdir`, :option:`!--incdir`, :option:`!--mandir`,
       :option:`!--modules`, :option:`!--state`, :option:`!--pid`,
       :option:`!--log`, and :option:`!--control`.

   * - :samp:`--bindir=directory`, :samp:`--sbindir=directory`
     - Directory paths for end-user and sysadmin executables.

       The defaults are :samp:`bin` and :samp:`sbin`, respectively.

   * - :samp:`--control=socket`
     - :ref:`Control API <configuration-mgmt>` socket address in IPv4, IPv6,
       or Unix domain format:

       .. code-block:: console

          $ ./configure --control=127.0.0.1:8080
          $ ./configure --control=[::1]:8080
          $ ./configure --control=:nxt_hint:`unix:/path/to/control.unit.sock <Note the unix: prefix>`

       .. warning::

          Avoid exposing an unprotected control socket to public networks.  Use
          :ref:`NGINX <nginx-secure-api>` or a different solution such as SSH
          for security and authentication.

       The default is :samp:`unix:control.unit.sock`, created as
       :samp:`root` with :samp:`600` permissions.

   * - :samp:`--incdir=directory`, :samp:`--libdir=directory`
     - Directory paths for :program:`libunit` header files and libraries.

       The defaults are :samp:`include` and :samp:`lib`, respectively.

   * - :samp:`--mandir=directory`
     - Directory path where the :samp:`unitd(8)` :program:`man` page is
       installed.

       The default is :samp:`share/man`.

   * - :samp:`--log=pathname`
     - Pathname for Unit's :ref:`log <troubleshooting-log>`.

       The default is :samp:`unit.log`.

   * - :samp:`--modules=directory`
     - Directory path for Unit's language :doc:`modules <modules>`.

       The default is :samp:`modules`.

   * - :samp:`--pid=pathname`
     - Pathname for the PID file of Unit's :program:`main` :ref:`process
       <security-apps>`.

       The default is :samp:`unit.pid`.


   * - :samp:`--state=directory`
     - .. _source-config-src-state:

       Directory path where Unit's state (configuration, certificates, other
       records) is stored between runs.  If you migrate your installation, copy
       the entire directory.

       .. warning::

          Unit's state includes sensitive data and must be owned by
          :samp:`root` with :samp:`700` permissions.  Avoid updating the
          directory by outside means; instead, use Unit's config API to ensure
          data consistency.

       The default is :samp:`state`.

   * - :samp:`--tmp=directory`
     - Defines the temporary file storage location (used to dump large request
       bodies).

       The default value is :samp:`tmp`.


.. _source-dir:

Directory Structure
*******************

To customize Unit's installation and runtime directories, you can both:

- Set the :option:`!--prefix` and path options (their relative settings are
  prefix-based) during :ref:`configuration <source-config-src-prefix>` to
  set up the runtime file structure: Unit uses these settings to locate its
  modules, state, and other files.

- Set the :envvar:`DESTDIR` `variable
  <https://www.gnu.org/prep/standards/html_node/DESTDIR.html>`_ during
  :ref:`installation <source-bld-src>`.  Unit's file structure is
  placed at the specified directory, which can be either the final installation
  target or an intermediate staging location.

Coordinate these two options as necessary to customize the directory structure.
One common scenario is installation based on absolute paths:

#. Set absolute runtime paths with :option:`!--prefix` and path options:

   .. code-block:: console

      $ ./configure --state=:nxt_hint:`/var/lib/unit <Sample absolute path>` --log=:nxt_hint:`/var/log/unit.log <Sample absolute pathname>` \
                    --control=:nxt_hint:`unix:/run/control.unit.sock <Sample absolute pathname; note the unix: prefix>` --prefix=:nxt_hint:`/usr/local/ <Sample absolute path>`

   Configured thus, Unit will store its state, log, and control socket at
   custom locations; other files will have default prefix-based paths.  Here,
   :file:`unitd` is put to :file:`/usr/local/sbin/`, modules to
   :file:`/usr/local/modules/`.

#. For further packaging or containerization, specify :option:`!DESTDIR` at
   installation to place the files in a staging location while preserving their
   relative structure.  Otherwise, omit :option:`!DESTDIR` for direct
   installation.

An alternative scenario is a build that you can move around the file system:

#. Set relative runtime paths with :option:`!--prefix` and path options:

   .. code-block:: console

      $ ./configure --state=:nxt_hint:`config <Sample relative path>` --log=:nxt_hint:`log/unit.log <Sample relative pathname>` \
                    --control=:nxt_hint:`unix:control/control.unit.sock <Sample relative pathname>` --prefix=:nxt_hint:`movable <Sample relative path>`

   Configured this way, Unit will store its files by prefix-based paths (both
   default and custom), for example, :file:`<working directory>/movable/sbin/`
   or :file:`<working directory>/movable/config/`.

#. Specify :option:`!DESTDIR` when installing the build.  You can migrate such
   builds if needed; move the entire file structure and launch binaries from
   the *base* directory so that the relative paths stay valid:

   .. code-block:: console

      $ cd :nxt_ph:`DESTDIR <Use a real path instead>`
      # movable/sbin/unitd

You can combine these approaches, but take care to understand how your settings
work together.


.. _source-modules:

===================
Configuring Modules
===================

Next, configure a module for each language you want to use with Unit.  The
:command:`./configure <language>` commands set up individual language modules
and place module-specific instructions in the :file:`Makefile`.

.. note::

   To run apps in several versions of a language, build and install a module
   for each version.  To package custom modules, see the module :ref:`howto
   <modules-pkg>`.

.. tabs::
   :prefix: modules
   :toc:

   .. tab:: Go

      When you run :command:`./configure go`, Unit sets up the Go package that
      lets your applications :ref:`run on Unit <configuration-go>`.  To use the
      package, :ref:`install <source-bld-src-ext>` it in your Go
      environment.  Available configuration options:

      .. list-table::

         * - :samp:`--go=pathname`
           - Specific Go executable pathname, also used in :ref:`make
             <source-bld-src-ext>` targets.

             The default is :samp:`go`.

         * - :samp:`--go-path=directory`
           - Custom directory path for Go package installation.

             The default is :samp:`$GOPATH`.

      .. note::

         The :program:`./configure` script doesn't alter the :envvar:`GOPATH`
         `environment variable <https://github.com/golang/go/wiki/GOPATH>`_.
         The two paths (configuration-time :option:`!--go-path` and
         compile-time :envvar:`GOPATH`) must be coherent at build time for Go
         to locate the Unit package.


   .. tab:: Java

      When you run :command:`./configure java`, the script configures a module
      to support running `Java Web Applications
      <https://download.oracle.com/otndocs/jcp/servlet-3_1-fr-spec/index.html>`_
      on Unit.  Available command options:

      .. list-table::

         * - :samp:`--home=directory`
           - Directory path for Java utilities and header files (required to
             build the module).

             The default is the :samp:`java.home` setting.

         * - :samp:`--jars=directory`
           - Directory path for Unit's custom :file:`.jar` files.

             The default is the Java module path.

         * - :samp:`--lib-path=directory`
           - Directory path for the :file:`libjvm.so` library.

             The default is based on JDK settings.

         * - :samp:`--local-repo=directory`
           - Directory path for local :file:`.jar` repository.

             The default is :samp:`$HOME/.m2/repository/`.

         * - :samp:`--repo=directory`
           - URL path for remote Maven repository.

             The default is :samp:`http://central.maven.org/maven2/`.

         * - :samp:`--module=basename`
           - Name of the module to be built (:file:`<basename>.unit.so`), also
             used in :ref:`make <source-bld-src-emb>` targets.

             The default is :samp:`java`.

      To configure a module called :file:`java11.unit.so` with OpenJDK |_|
      11.0.1:

      .. code-block:: console

         $ ./configure java --module=java11 \
                            --home=/Library/Java/JavaVirtualMachines/jdk-11.0.1.jdk/Contents/Home


   .. tab:: Node.js

      When you run :command:`./configure nodejs`, Unit sets up the
      :program:`unit-http` module that lets your applications :ref:`run on Unit
      <configuration-nodejs>`.  Available configuration options:

      .. list-table::

         * - :samp:`--local=directory`
           - Local directory path for Node.js module installation.

             By default, the module is installed globally :ref:`(recommended)
             <installation-nodejs-package>`.

         * - :samp:`--node=pathname`
           - Specific Node.js executable pathname, also used in
             :ref:`make <source-bld-src-ext>` targets.

             The default is :samp:`node`.

         * - :samp:`--npm=pathname`
           - Specific NPM executable pathname.

             The default is :samp:`npm`.

         * - :samp:`--node-gyp=pathname`
           - Specific :program:`node-gyp` executable pathname.

             The default is :samp:`node-gyp`.


   .. tab:: Perl

      When you run :command:`./configure perl`, the script configures a module
      to support running Perl scripts as applications on Unit.  Available
      command options:

      .. list-table::

         * - :samp:`--perl=pathname`
           - Specific Perl executable pathname.

             The default is :samp:`perl`.

         * - :samp:`--module=basename`
           - Name of the module to be built (:file:`<basename>.unit.so`), also
             used in :ref:`make <source-bld-src-emb>` targets.

             The default is the filename of the :option:`!--perl` executable.

      To configure a module called :file:`perl-5.20.unit.so` for Perl |_|
      5.20.2:

      .. code-block:: console

         $ ./configure perl --module=perl-5.20 \
                            --perl=perl5.20.2


   .. tab:: PHP

      When you run :command:`./configure php`, the script configures a custom
      SAPI module linked with the :program:`libphp` library to support running
      PHP applications on Unit.  Available command options:

      .. list-table::

         * - :samp:`--config=pathname`
           - Pathname of the :program:`php-config` script invoked to configure
             the PHP module.

             The default is :samp:`php-config`.

         * - :samp:`--lib-path=directory`
           - Directory path of the :program:`libphp` library file
             (:file:`libphp*.so` or :file:`libphp*.a`), usually available with
             an :option:`!--enable-embed` PHP build:

             .. code-block:: console

                $ php-config --php-sapis

                      ... embed ...

         * - :samp:`--lib-static`
           - Links the static :program:`libphp` library (:file:`libphp*.a`)
             instead of the dynamic one (:file:`libphp*.so`); requires
             :option:`!--lib-path`.

         * - :samp:`--module=basename`
           - Name of the module to be built (:file:`<basename>.unit.so`), also
             used in :ref:`make <source-bld-src-emb>` targets.

             The default is :option:`!--config`'s filename minus the `-config`
             suffix; thus, :samp:`/path/php7-config` turns into :samp:`php7`.

      To configure a module called :file:`php70.unit.so` for PHP |_| 7.0:

      .. code-block:: console

         $ ./configure php --module=php70 \
                           --config=/usr/lib64/php7.0/bin/php-config \
                           --lib-path=/usr/lib64/php7.0/lib64


   .. tab:: Python

      When you run :command:`./configure python`, the script configures a
      module to support running Python scripts as applications on Unit.
      Available command options:

      .. list-table::

         * - :samp:`--config=pathname`
           - Pathname of the :program:`python-config` script invoked to
             configure the Python module.

             The default is :samp:`python-config`.

         * - :samp:`--lib-path=directory`
           - Custom directory path of the Python runtime library to use with
             Unit.

         * - :samp:`--module=basename`
           - Name of the module to be built (:samp:`<basename>.unit.so`), also
             used in :ref:`make <source-bld-src-emb>` targets.

             The default is :option:`!--config`'s filename minus the `-config`
             suffix; thus, :samp:`/path/python3-config` turns into
             :samp:`python3`.

      .. note::

         The Python interpreter set by :program:`python-config` must be
         compiled with the :option:`!--enable-shared` `option
         <https://docs.python.org/3/using/configure.html#linker-options>`__.

      To configure a module called :file:`py33.unit.so` for Python |_| 3.3:

      .. code-block:: console

         $ ./configure python --module=py33 \
                              --config=python-config-3.3


   .. tab:: Ruby

      When you run :program:`./configure ruby`, the script configures a module
      to support running Ruby scripts as applications on Unit.  Available
      command options:

      .. list-table::

         * - :samp:`--module=basename`
           - Name of the module to be built (:file:`<basename>.unit.so`), also
             used in :ref:`make <source-bld-src-emb>` targets.

             The default is the filename of the :option:`!--ruby` executable.

         * - :samp:`--ruby=pathname`
           - Specific Ruby executable pathname.

             The default is :samp:`ruby`.

      To configure a module called :file:`ru23.unit.so` for Ruby |_| 2.3:

      .. code-block:: console

         $ ./configure ruby --module=ru23 \
                            --ruby=ruby23


.. _source-bld-src:

============================
Building and Installing Unit
============================

To build and install Unit's executables and language modules that you have
:program:`./configure`'d earlier:

.. code-block:: console

   $ make
   # make install

You can also build and install language modules individually; the specific
method depends on whether the language module is embedded in Unit or packaged
externally.

.. note::

   For further details about Unit's language modules, see :doc:`modules`.


.. _source-bld-src-emb:

Embedded Language Modules
*************************

To build and install the modules for Java, PHP, Perl, Python, or Ruby after
configuration, run :command:`make <module basename>` and :command:`make
<module basename>-install`, for example:

.. code-block:: console

   $ make :nxt_hint:`perl-5.20 <This is the --module option value from ./configure perl>`
   # make :nxt_hint:`perl-5.20 <This is the --module option value from ./configure perl>`-install


.. _source-bld-src-ext:

External Language Modules
*************************

To build and install the modules for Go and Node.js globally after
configuration, run :command:`make <go>-install` and :command:`make
<node>-install`, for example:

.. code-block:: console

   # make :nxt_hint:`go <This is the --go option value from ./configure go>`-install
   # make :nxt_hint:`node <This is the --node option value from ./configure nodejs>`-install

.. note::

   To install the Node.js module locally, run :command:`make
   <node>-local-install`:

   .. code-block:: console

      # make :nxt_hint:`node <This is the --node option value from ./configure nodejs>`-local-install

   If you haven't specified the :option:`!--local` :ref:`directory
   <howto/source-modules-nodejs>` with :program:`./configure nodejs`
   earlier, provide it here: :command:`DESTDIR=/your/project/directory`.  If
   both options are specified, :option:`!DESTDIR` prefixes the
   :option:`!--local` value.

   However, mind that global installation is the recommended method for the
   Node.js module.

If you customize the executable pathname with :option:`!--go` or
:option:`!--node`, use the following pattern:

.. code-block:: console

   $ ./configure nodejs --node=:nxt_hint:`/usr/local/bin/node8.12 <Executable pathname>`
   # make :nxt_hint:`/usr/local/bin/node8.12 <Executable pathname becomes a part of the target>`-install

   $ ./configure go --go=:nxt_hint:`/usr/local/bin/go1.7 <Executable pathname>`
   # make :nxt_hint:`/usr/local/bin/go1.7 <Executable pathname becomes a part of the target>`-install


.. _source-startup:

====================
Startup and Shutdown
====================

.. warning::

   We advise installing Unit from :ref:`precompiled packages
   <installation-precomp-pkgs>`; in this case, startup is :ref:`configured
   <installation-precomp-startup>` automatically.

   Even if you install Unit otherwise, avoid manual startup.  Instead,
   configure a service manager such as :program:`OpenRC` or :program:`systemd`
   or create an :program:`rc.d` script to launch the Unit daemon using the
   options below.

The startup command depends on your :samp:`./configure` options.  If you have
configured :ref:`absolute paths <source-dir>`:

.. code-block:: console

   # :nxt_hint:`unitd <Your PATH environment variable should list a path to unitd>` :nxt_ph:`RUNTIME OPTIONS <See the table below>`

Otherwise, start :program:`unitd` from the :samp:`sbin` subdirectory relative
to installation directory :ref:`prefix <source-config-src-prefix>`:

.. code-block:: console

   # cd :nxt_ph:`/path/to/unit/ <Destination prefix>`
   # :nxt_hint:`sbin/unitd <This preserves relative paths>` :nxt_ph:`RUNTIME OPTIONS <See the table below>`

Run :command:`unitd -h` or :command:`unitd --version` to list Unit's
compile-time settings.  Usually, the defaults don't require overrides; however,
the following runtime options are available.  For details and security notes,
see :ref:`here <source-config-src>`.

General runtime options and :ref:`compile-time setting
<source-config-src>` overrides:

.. list-table::

   * - :samp:`--help`, :samp:`-h`
     - Displays a summary of Unit's command-line options and their compile-time
       defaults.

   * - :samp:`--version`
     - Displays Unit's version and the :program:`./configure` settings it was
       built with.

   * - :samp:`--no-daemon`
     - Runs Unit in non-daemon mode.

   * - :samp:`--control socket`
     - Control API socket address in IPv4, IPv6, or Unix domain format:

       .. code-block:: console

          # unitd --control 127.0.0.1:8080
          # unitd --control [::1]:8080
          # unitd --control :nxt_hint:`unix:/path/to/control.unit.sock <Note the unix: prefix>`

   * - :samp:`--group name`, :samp:`--user name`
     - Group name and user name used to run Unit's non-privileged
       :ref:`processes <security-apps>`.

   * - :samp:`--log pathname`
     - Pathname for Unit's :ref:`log <troubleshooting-log>`.

   * - :samp:`--modules directory`
     - Directory path for Unit's language :doc:`modules <modules>`
       (:file:`*.unit.so` files).

   * - :samp:`--pid pathname`
     - Pathname for the PID file of Unit's :program:`main` :ref:`process
       <security-apps>`.

   * - :samp:`--state directory`
     - Directory path for Unit's state storage.

   * - :samp:`--tmp directory`
     - Directory path for Unit's temporary file storage.

Finally, to stop a running Unit:

.. code-block:: console

   # pkill unitd

This command signals all Unit's processes to terminate in a graceful manner.
