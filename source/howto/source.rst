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

Before configuring and compiling Unit, install the required build tools and the
library files for the :nxt_hint:`required languages <Go, Java, Node.js, PHP,
Perl, Python, and Ruby are supported>` and all other features you want in your
Unit, such as TLS or regular expressions.

The commands below assume you are configuring Unit with all supported languages
and features (**X**, **Y**, and **Z** denote major, minor, and
revision numbers, respectively); omit the packages you won't use.

.. tabs::
   :prefix: prereq
   :toc:

   .. tab:: Debian, Ubuntu

      .. code-block:: console

         # apt install build-essential

      .. code-block:: console

         # apt install golang

      .. code-block:: console

         # apt install curl && \
               curl -sL https://deb.nodesource.com/setup_:nxt_ph:`VERSION <Node.js 8.11 or later is supported>`.x | bash - && \
               apt install nodejs

      .. code-block:: console

         # npm install -g node-gyp

      .. code-block:: console

         # apt install php-dev libphp-embed

      .. code-block:: console

         # apt install libperl-dev

      .. code-block:: console

         # apt install python:nxt_ph:`X <Both Python 2 and Python 3 are supported>`-dev

      .. code-block:: console

         # apt install ruby-dev ruby-rack

      .. code-block:: console

         # apt install openjdk-:nxt_ph:`X <Java 8 or later is supported. Different JDKs may be used>`-jdk

      .. code-block:: console

         # apt install libssl-dev

      .. code-block:: console

         # apt install libpcre2-dev


   .. tab:: Amazon, Fedora, RHEL

      .. code-block:: console

         # yum install gcc make

      .. code-block:: console

         # yum install golang

      .. code-block:: console

         # yum install curl && \
               curl -sL https://rpm.nodesource.com/setup_:nxt_ph:`VERSION <Node.js 8.11 or later is supported>`.x | bash - && \
               yum install nodejs

      .. code-block:: console

         # npm install -g node-gyp

      .. code-block:: console

         # yum install php-devel php-embedded

      .. code-block:: console

         # yum install perl-devel perl-libs

      .. code-block:: console

         # yum install python:nxt_ph:`X <Both Python 2 and Python 3 are supported>`-devel

      .. code-block:: console

         # yum install ruby-devel rubygem-rack

      .. code-block:: console

         # yum install java-:nxt_ph:`X.Y.Z <Java 8 or later is supported. Different JDKs may be used>`-openjdk-devel

      .. code-block:: console

         # yum install openssl-devel

      .. code-block:: console

         # yum install pcre2-devel


   .. tab:: FreeBSD

      Ports:

      .. code-block:: console

         # cd /usr/ports/lang/go/ && make install clean

      .. code-block:: console

         # cd /usr/ports/www/node/ && make install clean

      .. code-block:: console

         # cd /usr/ports/www/npm/ && make install clean && npm i -g node-gyp

      .. code-block:: console

         # cd /usr/ports/lang/php:nxt_ph:`XY <PHP versions 5, 7, and 8 are supported>`/ && make install clean

      .. code-block:: console

         # cd /usr/ports/lang/perl:nxt_ph:`X.Y <Perl 5.12 or later is supported>`/ && make install clean

      .. code-block:: console

         # cd /usr/ports/lang/python/ && make install clean

      .. code-block:: console

         # cd /usr/ports/lang/ruby:nxt_ph:`XY <Ruby 2.0 or later is supported>`/ && make install clean

      .. code-block:: console

         # cd /usr/ports/java/openjdk:nxt_ph:`X <Java 8 or later is supported. Different JDKs may be used>`/ && make install clean

      .. code-block:: console

         # cd /usr/ports/security/openssl/ && make install clean

      .. code-block:: console

         # cd /usr/ports/devel/pcre2/ && make install clean

      Packages:

      .. code-block:: console

         # pkg install go

      .. code-block:: console

         # pkg install node && pkg install npm && npm i -g node-gyp

      .. code-block:: console

         # pkg install php:nxt_ph:`XY <PHP versions 5, 7, and 8 are supported>`

      .. code-block:: console

         # pkg install perl:nxt_ph:`X <Perl 5.12 or later is supported>`

      .. code-block:: console

         # pkg install python

      .. code-block:: console

         # pkg install ruby:nxt_ph:`XY <Ruby 2.0 is supported>`

      .. code-block:: console

         # pkg install openjdk:nxt_ph:`X <Java 8 or later is supported. Different JDKs may be used>`

      .. code-block:: console

         # pkg install openssl

      .. code-block:: console

         # pkg install pcre2


   .. tab:: Solaris

      .. code-block:: console

         # pkg install gcc

      .. code-block:: console

         # pkg install golang

      .. code-block:: console

         # pkg install php-:nxt_ph:`XY <PHP versions 5, 7, and 8 are supported>`

      .. code-block:: console

         # pkg install ruby

      .. code-block:: console

         # pkg install jdk-:nxt_ph:`X <Java 8 or later is supported. Different JDKs may be used>`

      .. code-block:: console

         # pkg install openssl

      .. code-block:: console

         # pkg install pcre

      Also, use :program:`gmake` instead of :program:`make` when :ref:`building
      and installing <source-bld-src>` Unit on Solaris.

.. nxt_details:: Enabling njs
   :hash: source-njs

   To build Unit with `njs <https://nginx.org/en/docs/njs/>`__ support,
   download the :program:`njs` code to the same parent directory
   as the Unit code.

   **0.8.2** is the latest version of :program:`njs` that Unit supports.
   Make sure you are in the correct branch before configuring the binaries.

   .. code-block:: console

      $ git clone https://github.com/nginx/njs.git

   .. code-block:: console

      $ cd njs

   .. code-block:: console

      $ git checkout -b 0.8.2 0.8.2

   Next, configure and build the :program:`njs` binaries. Make sure to use the
   `--no-zlib` and `--no-libxml2` options to avoid
   conflicts with Unit's dependencies:

   .. code-block:: console

      $ ./configure :nxt_hint:`--no-zlib --no-libxml2 <Ensures Unit can link against the resulting library>` && make

   Point to the resulting source and build directories when :ref:`configuring
   <source-config-src-njs>` the Unit code.


.. nxt_details:: Enabling WebAssembly
   :hash: source-wasm

   .. tabs::
      :prefix: source-enable-webassembly

      .. tab:: wasm-wasi-component

          To build Unit with support for the WebAssembly Component Model,
          you need **rust** version 1.76.0+, **cargo** and the developer
          package for **clang** as mentioned in the
          :ref:`Required Software Section <source-prereq-build>`.

          Next please refer to
          :ref:`Configuring Modules - WebAssembly <modules-webassembly>` for
          further instructions.

      .. tab:: unit-wasm

          .. warning::
             The **unit-wasm** module is deprecated.
             We recommend using **wasm-wasi-component** instead,
             available in Unit 1.32.0 and later, which supports
             WebAssembly Components using standard WASI 0.2 interfaces.

          To build Unit with the `WebAssembly <https://webassembly.org>`__
          language module,
          you need the
          `Wasmtime <https://wasmtime.dev>`__
          runtime.
          Download the C API
          `files <https://github.com/bytecodealliance/wasmtime/releases/>`__
          suitable for your OS and architecture
          to the same parent directory
          as the Unit code,
          for example:

          .. code-block:: console

             $ cd ..

          .. code-block:: console

             $ wget -O- https://github.com/bytecodealliance/wasmtime/releases/download/v12.0.0/wasmtime-v12.0.0-x86_64-linux-c-api.tar.xz \
                   | tar Jxf -  # Unpacks to the current directory

          Point to the resulting **include** and **lib** directories when
          :ref:`configuring <howto/source-modules-webassembly>` the Unit code.

          To build WebAssembly apps that run on Unit, you need
          the `wasi-sysroot <https://github.com/WebAssembly/wasi-sdk>`__ SDK:

          .. code-block:: console

             $ wget -O- https://github.com/WebAssembly/wasi-sdk/releases/download/wasi-sdk-20/wasi-sysroot-20.0.tar.gz | tar zxf -

          When building the apps, add the following environment variable:

          .. code-block:: console

             WASI_SYSROOT=:nxt_ph:`/path/to/wasi-sysroot-dir/ <wasi-sysroot directory>`


.. _source-config-src:

===================
Configuring Sources
===================

To run system compatibility checks and generate a **Makefile** with core
build instructions for Unit:

.. code-block:: console

   $ ./configure :nxt_ph:`COMPILE-TIME OPTIONS <See the table below>`

Finalize the resulting **Makefile** by configuring the :ref:`language
modules <source-modules>` you need before proceeding further.

General options and settings that control compilation, runtime privileges,
or support for certain features:

.. list-table::

   * - **--help**
     -  Displays a summary of common :program:`./configure` options.

        For language-specific details, run :command:`./configure <language>
        --help` or see :ref:`below <source-modules>`.

   * - **--cc=pathname**
     - Custom C compiler pathname.

       The default is **cc**.

   * - **--cc-opt=options**, **--ld-opt=options**
     - Extra options for the C compiler and linker.

   * - **--group=name**, **--user=name**
     - Group name and username to run Unit's non-privileged :ref:`processes
       <security-apps>`.

       The defaults are :option:`!--user`'s primary group and
       **nobody**, respectively.

   * - **--debug**
     - Turns on the :ref:`debug log <troubleshooting-dbg-log>`.

   * - **--no-ipv6**
     - Turns off IPv6 support.

   * - **--no-unix-sockets**
     - Turns off UNIX domain sockets support for control and routing.

   * - **--openssl**
     - Turns on OpenSSL support.  Make sure OpenSSL (1.0.1+) header files and
       libraries are in your compiler's path; it can be set with the
       :option:`!--cc-opt` and :option:`!--ld-opt` options or the
       :envvar:`CFLAGS` and :envvar:`LDFLAGS` environment variables when
       running :program:`./configure`.

       For details of TLS configuration in Unit, see :ref:`configuration-ssl`.


.. _source-config-src-pcre:

By default, Unit relies on the locally installed version of the `PCRE
<https://www.pcre.org>`_ library to support regular expressions in :ref:`routes
<configuration-routes>`; if both major versions are present, Unit selects
PCRE2.  Two additional options alter this behavior:

.. list-table::

   * - **--no-regex**
     - Turns off regex support; any attempts to use a regex in Unit
       configuration cause an error.

   * - **--no-pcre2**
     - Ignores PCRE2; the older PCRE 8.x library is used instead.

.. _source-config-src-njs:

Unit also supports the use of `njs <https://nginx.org/en/docs/njs/>`__ scripts
in configuration; to enable this feature, use the respective option:

.. list-table::

   * - **--njs**
     - Turns on :program:`njs` support; requires **--openssl**.

When :option:`!--njs` is enabled, the :option:`!--cc-opt` and
:option:`!--ld-opt` option values should point to the **src/**
and **build/** subdirectories of the :program:`njs` source code.
For example, if you cloned the :program:`njs` repo beside the Unit repo:

.. subs-code-block:: console

   $ ./configure --njs --openssl \
                 --cc-opt="-I../njs/src/ -I../njs/build/"  \
                 --ld-opt="-L../njs/build/"  \
                 ...

The next option group customizes Unit's runtime :ref:`directory
structure <source-dir>`:

.. list-table::

   * - **--prefix=PREFIX**
     - .. _source-config-src-prefix:

       Destination directory prefix for :ref:`path options
       <source-dir>`:
       :option:`!--bindir`,
       :option:`!--sbindir`,
       :option:`!--includedir`,
       :option:`!--libdir`,
       :option:`!--modulesdir`,
       :option:`!--datarootdir`,
       :option:`!--mandir`,
       :option:`!--localstatedir`,
       :option:`!--libstatedir`,
       :option:`!--runstatedir`,
       :option:`!--logdir`,
       :option:`!--tmpdir`,
       :option:`!--control`,
       :option:`!--pid`,
       :option:`!--log`.

       The default is **/usr/local**.

   * - **--exec-prefix=EXEC_PREFIX**
     - Destination directory prefix for the executable directories only.

       The default is the **PREFIX** value.

   * - **--bindir=BINDIR**, **--sbindir=SBINDIR**
     - Directory paths for client and server executables.

       The defaults are **EXEC_PREFIX/bin** and **EXEC_PREFIX/sbin**.

   * - **--includedir=INCLUDEDIR**, **--libdir=LIBDIR**
     - Directory paths for :program:`libunit` header files and libraries.

       The defaults are **PREFIX/include** and **EXEC_PREFIX/lib**.

   * - **--modulesdir=MODULESDIR**
     - Directory path for Unit's language :doc:`modules <modules>`.

       The default is **LIBDIR/unit/modules**.

   * - **--datarootdir=DATAROOTDIR**, **--mandir=MANDIR**
     - Directory path for **unitd(8)** data storage and its subdirectory
       where the :program:`man` page is installed.

       The defaults are **PREFIX/share** and **DATAROOTDIR/man**.

   * - **--localstatedir=LOCALSTATEDIR**
     - Directory path where Unit stores its runtime state, PID file,
       control socket, and logs.

       The default is **PREFIX/var**.

   * - **--libstatedir=LIBSTATEDIR**
     - .. _source-config-src-state:

       Directory path where Unit's runtime state (configuration, certificates,
       other resources) is stored between runs.  If you migrate your
       installation, copy the entire directory.

       .. warning::

          The directory is sensitive and must be owned by **root** with
          **700** permissions.  Don't change its contents externally; use
          the config API to ensure integrity.

       The default is **LOCALSTATEDIR/run/unit**.

   * - **--logdir=LOGDIR**, **--log=LOGFILE**
     - Directory path and filename for Unit's :ref:`log <troubleshooting-log>`.

       The defaults are **LOCALSTATEDIR/log/unit** and
       **LOGDIR/unit.log**.

   * - **--runstatedir=RUNSTATEDIR**
     - Directory path where Unit stores its PID file and control socket.

       The default is **LOCALSTATEDIR/run/unit**.

   * - **--pid=pathname**
     - Pathname for the PID file of Unit's :program:`main` :ref:`process
       <security-apps>`.

       The default is **RUNSTATEDIR/unit.pid**.

   * - **--control=SOCKET**
     - :ref:`Control API <configuration-mgmt>` socket address in IPv4, IPv6,
       or UNIX domain format:

       .. code-block:: console

          $ ./configure --control=127.0.0.1:8080

       .. code-block:: console

          $ ./configure --control=[::1]:8080

       .. code-block:: console

          $ ./configure --control=unix:/path/to/control.unit.sock  # Note the unix: prefix

       .. warning::

          Avoid exposing an unprotected control socket in public networks.  Use
          :ref:`NGINX <nginx-secure-api>` or a different solution such as SSH
          for security and authentication.

       The default is **unix:RUNSTATEDIR/control.unit.sock**, created as
       **root** with **600** permissions.

   * - **--tmpdir=TMPDIR**
     - Defines the temporary file storage location (used to dump large request
       bodies).

       The default value is **/tmp**.


.. _source-dir:

Directory Structure
*******************

By default, :command:`make install` installs Unit at the following pathnames:

.. list-table::
   :header-rows: 1

   * - Directory
     - Default Path

   * - **bin** directory
     - **/usr/local/bin/**

   * - **sbin** directory
     - **/usr/local/sbin/**

   * - **lib** directory
     - **/usr/local/lib/**

   * - **include** directory
     - **/usr/local/include/**

   * - **tmp** directory
     - **/tmp/**

   * - Man pages
     - **/usr/local/share/man/**

   * - Language modules
     - **/usr/local/lib/unit/modules/**

   * - Runtime state
     - **/usr/local/var/lib/unit/**

   * - PID file
     - **/usr/local/var/run/unit/unit.pid**

   * - Log file
     - **/usr/local/var/log/unit/unit.log**

   * - Control API socket
     - **unix:/usr/local/var/run/unit/control.unit.sock**

The defaults are designed to work for most cases; to customize this layout,
set the :option:`!--prefix` and its related options during :ref:`configuration
<source-config-src-prefix>`, defining the resulting file structure.


.. _source-modules:

===================
Configuring Modules
===================

Next, configure a module for each language you want to use with Unit.  The
:command:`./configure <language>` commands set up individual language modules
and place module-specific instructions in the **Makefile**.

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
      package, :ref:`install <source-bld-src-ext>` it in your Go environment.
      Available configuration options:

      .. list-table::

         * - **--go=pathname**
           - Specific Go executable pathname, also used in :ref:`make
             <source-bld-src-ext>` targets.

             The default is **go**.

         * - **--go-path=directory**
           - Custom directory path for Go package installation.

             The default is **$GOPATH**.

      .. note::

         Running :program:`./configure go` doesn't alter the :envvar:`GOPATH`
         `environment variable <https://github.com/golang/go/wiki/GOPATH>`_, so
         configure-time :option:`!--go-path` and compile-time :envvar:`$GOPATH`
         must be coherent for Go to find the resulting package.

         .. code-block:: console

            $ GOPATH=<Go package installation path> GO111MODULE=auto go build -o :nxt_ph:`app <Executable name>` :nxt_ph:`app.go <Application source code>`


   .. tab:: Java

      When you run :command:`./configure java`, the script configures a module
      to support running `Java Web Applications
      <https://download.oracle.com/otndocs/jcp/servlet-3_1-fr-spec/index.html>`_
      on Unit.  Available command options:

      .. list-table::

         * - **--home=directory**
           - Directory path for Java utilities and header files to build the
             module.

             The default is the **java.home** setting.

         * - **--jars=directory**
           - Directory path for Unit's custom **.jar** files.

             The default is the Java module path.

         * - **--lib-path=directory**
           - Directory path for the **libjvm.so** library.

             The default is based on JDK settings.

         * - **--local-repo=directory**
           - Directory path for the local **.jar** repository.

             The default is **$HOME/.m2/repository/**.

         * - **--repo=directory**
           - URL path for the remote Maven repository.

             The default is **http://central.maven.org/maven2/**.

         * - **--module=basename**
           - Resulting module's name (**<basename>.unit.so**), also used
             in :ref:`make <source-bld-src-emb>` targets.

             The default is **java**.

      To configure a module called **java11.unit.so** with OpenJDK |_|
      11.0.1:

      .. code-block:: console

         $ ./configure java --module=java11  \
                            --home=/Library/Java/JavaVirtualMachines/jdk-11.0.1.jdk/Contents/Home


   .. tab:: Node.js

      When you run :command:`./configure nodejs`, Unit sets up the
      :program:`unit-http` module that lets your applications :ref:`run on Unit
      <configuration-nodejs>`.  Available configuration options:

      .. list-table::

         * - **--local=directory**
           - Local directory path where the resulting module is installed.

             By default, the module is installed globally :ref:`(recommended)
             <installation-nodejs-package>`.

         * - **--node=pathname**
           - Specific Node.js executable pathname, also used in
             :ref:`make <source-bld-src-ext>` targets.

             The default is **node**.

         * - **--npm=pathname**
           - Specific :program:`npm` executable pathname.

             The default is **npm**.

         * - **--node-gyp=pathname**
           - Specific :program:`node-gyp` executable pathname.

             The default is **node-gyp**.


   .. tab:: Perl

      When you run :command:`./configure perl`, the script configures a module
      to support running Perl scripts as applications on Unit.  Available
      command options:

      .. list-table::

         * - **--perl=pathname**
           - Specific Perl executable pathname.

             The default is **perl**.

         * - **--module=basename**
           - Resulting module's name (**<basename>.unit.so**), also
             used in :ref:`make <source-bld-src-emb>` targets.

             The default is the filename of the :option:`!--perl` executable.

      To configure a module called **perl-5.20.unit.so** for Perl |_|
      5.20.2:

      .. code-block:: console

         $ ./configure perl --module=perl-5.20  \
                            --perl=perl5.20.2


   .. tab:: PHP

      When you run :command:`./configure php`, the script configures a custom
      SAPI module linked with the :program:`libphp` library to support running
      PHP applications on Unit.  Available command options:

      .. list-table::

         * - **--config=pathname**
           - Pathname of the :program:`php-config` script used to set up
             the resulting module.

             The default is **php-config**.

         * - **--lib-path=directory**
           - Directory path of the :program:`libphp` library file
             (**libphp*.so** or **libphp*.a**), usually available with
             an :option:`!--enable-embed` PHP build:

             .. code-block:: console

                $ php-config --php-sapis

                      ... embed ...

         * - **--lib-static**
           - Links the static :program:`libphp` library (**libphp*.a**)
             instead of the dynamic one (**libphp*.so**); requires
             :option:`!--lib-path`.

         * - **--module=basename**
           - Resulting module's name (**<basename>.unit.so**), also
             used in :ref:`make <source-bld-src-emb>` targets.

             The default is :option:`!--config`'s filename minus the `-config`
             suffix; thus, **--config=/path/php7-config** yields
             **php7.unit.so**.

      To configure a module called **php70.unit.so** for PHP |_| 7.0:

      .. code-block:: console

         $ ./configure php --module=php70  \
                           --config=/usr/lib64/php7.0/bin/php-config  \
                           --lib-path=/usr/lib64/php7.0/lib64


   .. tab:: Python

      When you run :command:`./configure python`, the script configures a
      module to support running Python scripts as applications on Unit.
      Available command options:

      .. list-table::

         * - **--config=pathname**
           - Pathname of the :program:`python-config` script used to
             set up the resulting module.

             The default is **python-config**.

         * - **--lib-path=directory**
           - Custom directory path of the Python runtime library to use with
             Unit.

         * - **--module=basename**
           - Resulting module's name (**<basename>.unit.so**), also
             used in :ref:`make <source-bld-src-emb>` targets.

             The default is :option:`!--config`'s filename minus the `-config`
             suffix; thus, **/path/python3-config** turns into
             **python3**.

      .. note::

         The Python interpreter set by :program:`python-config` must be
         compiled with the :option:`!--enable-shared` `option
         <https://docs.python.org/3/using/configure.html#linker-options>`__.

      To configure a module called **py33.unit.so** for Python |_| 3.3:

      .. code-block:: console

         $ ./configure python --module=py33  \
                              --config=python-config-3.3


   .. tab:: Ruby

      When you run :program:`./configure ruby`, the script configures a module
      to support running Ruby scripts as applications on Unit.  Available
      command options:

      .. list-table::

         * - **--module=basename**
           - Resulting module's name (**<basename>.unit.so**), also
             used in :ref:`make <source-bld-src-emb>` targets.

             The default is the filename of the :option:`!--ruby` executable.

         * - **--ruby=pathname**
           - Specific Ruby executable pathname.

             The default is **ruby**.

      To configure a module called **ru23.unit.so** for Ruby |_| 2.3:

      .. code-block:: console

         $ ./configure ruby --module=ru23  \
                            --ruby=ruby23

   .. tab:: WebAssembly

      .. _modules-webassembly:

      When you run :program:`./configure wasm-wasi-component`,
      the script configures a module to support running WebAssembly
      components on Unit.

      The module doesn't accept any extra configuration parameters.
      The module's basename is wasm-wasi-component.

   .. tab:: Unit-Wasm

      .. warning::
         Unit 1.32.0 and later support the WebAssembly Component Model and WASI
         0.2 APIs.
         We recommend using the new implementation.

      When you run :program:`./configure wasm`, the script configures a module
      to support running WebAssembly applications on Unit.
      Available command options:

      .. list-table::

         * - **--module=basename**
           - Resulting module's name (**<basename>.unit.so**), also
             used in :ref:`make <source-bld-src-emb>` targets.

         * - **--runtime=basename**
           - The WebAssembly runtime to use.

             The default is **wasmtime**.

         * - **--include-path=path**
           - The directory path to the runtime's header files.

         * - **--lib-path=path**
           - The directory path to the runtime's library files.

         * - **--rpath=<path>**
           - The directory path that designates the run-time library search
             path.

             If specified without a value,
             assumes the **--lib-path** value.

      To configure a module called **wasm.unit.so**:

      .. code-block:: console

         $ ./configure wasm --include-path=:nxt_ph:`/path/to/wasmtime <Runtime's header directory>`/include  \
                            --lib-path=:nxt_ph:`/path/to/wasmtime <Runtime's library directory>`/lib \
                            --rpath


.. _source-bld-src:

============================
Building and Installing Unit
============================

To build and install Unit's executables and language modules that you have
:program:`./configure`'d earlier:

.. code-block:: console

   $ make

.. code-block:: console

   # make install

Mind that **make install** requires setting up Unit's :ref:`directory
structure <source-dir>` with :program:`./configure` first.

To run Unit from the build directory tree without installing:

.. code-block:: console

   $ ./configure --prefix=./build

.. code-block:: console

   $ make

.. code-block:: console

   $ ./build/sbin/unitd

You can also build and install language modules individually; the specific
method depends on whether the language module is embedded in Unit (Java, Perl,
PHP, Python, Ruby) or packaged externally (Go, Node.js).

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

.. code-block:: console

   # make :nxt_hint:`perl-5.20 <This is the --module option value from ./configure perl>`-install

.. _source-bld-src-ext:

External Language Modules
*************************

To build and install the modules for Go and Node.js globally after
configuration, run :command:`make <go>-install` and :command:`make
<node>-install`, for example:

.. code-block:: console

   # make :nxt_hint:`go <This is the --go option value from ./configure go>`-install

.. code-block:: console

   # make :nxt_hint:`node <This is the --node option value from ./configure nodejs>`-install

.. note::

   To install the Node.js module locally, run :command:`make
   <node>-local-install`:

   .. code-block:: console

      # make :nxt_hint:`node <This is the --node option value from ./configure nodejs>`-local-install

   If you haven't specified the :option:`!--local` :ref:`directory
   <howto/source-modules-nodejs>` with :program:`./configure nodejs`
   earlier, provide it here:

   .. code-block:: console

      # DESTDIR=/your/project/directory/ make node-local-install

   If both options are specified, :option:`!DESTDIR` prefixes the
   :option:`!--local` value set by :program:`./configure nodejs`.

   Finally, mind that global installation is preferable for the Node.js module.

If you customized the executable pathname with :option:`!--go` or
:option:`!--node`, use the following pattern:

.. code-block:: console

   $ ./configure nodejs --node=:nxt_hint:`/usr/local/bin/node8.12 <Executable pathname>`

.. code-block:: console

   # make :nxt_hint:`/usr/local/bin/node8.12 <Executable pathname becomes a part of the target>`-install

.. code-block:: console

   $ ./configure go --go=:nxt_hint:`/usr/local/bin/go1.7 <Executable pathname>`

.. code-block:: console

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
   configure a service manager (:program:`OpenRC`, :program:`systemd`, and so
   on) or create an :program:`rc.d` script to launch the Unit daemon using the
   options below.

The startup command depends on the directories you set with
:program:`./configure`, but their default values place the :program:`unitd`
binary in a well-known place, so:

.. code-block:: console

   # :nxt_hint:`unitd <Your PATH environment variable should list a path to unitd>` :nxt_ph:`RUNTIME OPTIONS <See the table below>`

Run :command:`unitd -h` or :command:`unitd --version` to list Unit's
compile-time settings.  Usually, the defaults don't require overrides; still,
the following runtime options are available.  For their compile-time
counterparts, see :ref:`here <source-config-src>`.

.. list-table::

   * - **--help**, **-h**
     - Displays a summary of the command-line options and their defaults.

   * - **--version**
     - Displays Unit's version and the :program:`./configure` settings it was
       built with.

   * - **--no-daemon**
     - Runs Unit in non-daemon mode.

   * - **--control socket**
     - Control API socket address in IPv4, IPv6, or UNIX domain format:

       .. code-block:: console

          # unitd --control 127.0.0.1:8080

       .. code-block:: console

          # unitd --control [::1]:8080

       .. code-block:: console

          # unitd --control :nxt_hint:`unix:/path/to/control.unit.sock <Note the unix: prefix>`

   * - **--control-mode**
     - Sets the permission of the UNIX domain control socket. Default: 0600

   * - **--control-user**
     - Sets the owner of the UNIX domain control socket.

   * - **--control-group**
     - Sets the group of the UNIX domain control socket.

   * - **--group name**, **--user name**
     - Group name and user name used to run Unit's non-privileged
       :ref:`processes <security-apps>`.

   * - **--log pathname**
     - Pathname for Unit's :ref:`log <troubleshooting-log>`.

   * - **--modules directory**
     - Directory path for Unit's language :doc:`modules <modules>`
       (***.unit.so** files).

   * - **--pid pathname**
     - Pathname for the PID file of Unit's :program:`main` :ref:`process
       <security-apps>`.

   * - **--state directory**
     - Directory path for Unit's state storage.

   * - **--tmp directory**
     - Directory path for Unit's temporary file storage.

Finally, to stop a running Unit:

.. code-block:: console

   # pkill unitd

This command signals all Unit's processes to terminate in a graceful manner.
