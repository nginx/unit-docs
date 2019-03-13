.. |_| unicode:: 0xA0
   :trim:

.. highlight:: none

############
Installation
############

System Requirements
*******************

NGINX Unit is tested to compile and run on the following systems:

* Linux 2.6 or later
* FreeBSD 9 or later
* MacOS X
* Solaris 11

Architectures:

* i386
* amd64
* powerpc
* arm

The following application platforms and versions are supported:

* Go 1.6 or later
* Java 8 or later
* Node.js 8.11 or later
* PHP 5, 7
* Perl 5.12 or later
* Python 2.6, 2.7, 3
* Ruby 2.0 or later

You can run multiple versions of the same language installed on the same
system.

.. _installation-docker:

Docker Images
*************

To install and run Unit from our Docker image repository:

.. code-block:: none

   # docker pull nginx/unit
   # docker run -d nginx/unit

By default, the ``:latest`` image tag is used that resolves into a
``-full`` configuration of the latest Unit version.  Other `tags <https://hub.
docker.com/r/nginx/unit/tags/>`_ available:

.. list-table::
    :header-rows: 1

    * - Tag
      - Description

    * - ``<version>-full``
      - Modules for all supported languages.

    * - ``<version>-minimal``
      - No language modules.

    * - ``<version>-<language>``
      - Specific language module only, for example ``1.3-ruby2.3`` or
        ``1.2-python2.7``.

.. include:: include/socket-note.rst

For further details, see the `repository page <https://hub.docker.com/r/
nginx/unit/>`_ and our :doc:`Howto <howto/docker>`.

.. _installation-precomp-pkgs:

Precompiled Packages
********************

Precompiled binaries for Unit are available for:

 * Amazon Linux
 * CentOS 6, 7
 * Debian 8, 9
 * Fedora 28, 29
 * RHEL 6, 7
 * Ubuntu 16.04, 18.04, 18.10

.. _installation-precomp-centos:

CentOS Packages
===============

1. Create the file **/etc/yum.repos.d/unit.repo** with the following
   contents:

   .. code-block:: ini

    [unit]
    name=unit repo
    baseurl=https://packages.nginx.org/unit/centos/$releasever/$basearch/
    gpgcheck=0
    enabled=1

2. Install Unit base package:

   .. code-block:: console

      # yum install unit

3. Install additional module packages you would like to use, e.g.:

   .. code-block:: console

      # yum install unit-php unit-python unit-go unit-perl unit-devel \
            unit-jsc-common unit-jsc8

.. include:: include/socket-note.rst

.. _installation-precomp-rhel:

RHEL Packages
=============

1. Create the file **/etc/yum.repos.d/unit.repo** with the following
   contents:

   .. code-block:: ini

      [unit]
      name=unit repo
      baseurl=https://packages.nginx.org/unit/rhel/$releasever/$basearch/
      gpgcheck=0
      enabled=1

2. Install Unit base package:

   .. code-block:: console

      # yum install unit

3. Install additional module packages you would like to use.

   For RHEL 6:

   .. code-block:: console

      # yum install unit-php unit-python unit-perl unit-devel \
            unit-jsc-common unit-jsc8 unit-jsc11

   For RHEL 7:

   .. code-block:: console

      # yum install unit-php unit-python unit-go unit-perl unit-devel \
            unit-jsc-common unit-jsc8 unit-jsc11

.. include:: include/socket-note.rst

Fedora Packages
===============

1. Create the file :file:`/etc/yum.repos.d/unit.repo` with the following
   contents:

   .. code-block:: ini

      [unit]
      name=unit repo
      baseurl=https://packages.nginx.org/unit/fedora/$releasever/$basearch/
      gpgcheck=0
      enabled=1

2. Install Unit base package:

   .. code-block:: console

      # yum install unit

3. Install additional module packages you would like to use.

   For Fedora 28:

   .. code-block:: console

      # yum install unit-php unit-python27 unit-python36 unit-perl unit-devel \
            unit-jsc-common unit-jsc8 unit-jsc11

   For Fedora 29:

   .. code-block:: console

      # yum install unit-php unit-python27 unit-python37 unit-perl unit-devel \
            unit-jsc-common unit-jsc8 unit-jsc11

.. note::

   Control socket is located here: :file:`/var/run/unit/control.sock`.

Amazon Linux Packages
=====================

1. Create the file **/etc/yum.repos.d/unit.repo** with the following
   contents:

   .. code-block:: ini

      [unit]
      name=unit repo
      baseurl=https://packages.nginx.org/unit/amzn/$releasever/$basearch/
      gpgcheck=0
      enabled=1

   For Amazon Linux 2 LTS:

   .. code-block:: ini

      [unit]
      name=unit repo
      baseurl=https://packages.nginx.org/unit/amzn2/$releasever/$basearch/
      gpgcheck=0
      enabled=1

2. Install Unit base package:

   .. code-block:: console

      # yum install unit

3. Install additional module packages you would like to use, e.g.:

   .. code-block:: console

      # yum install unit-php unit-python27 unit-python34 unit-python35 \
            unit-python36 unit-go unit-perl unit-devel unit-jsc-common \
            unit-jsc8 unit-jsc11

   For Amazon Linux 2 LTS:

   .. code-block:: console

      # yum install unit-php unit-python unit-go unit-perl unit-devel \
            unit-jsc-common unit-jsc8 unit-jsc11

.. include:: include/socket-note.rst

Ubuntu Packages
===============

1. Download the `key <https://nginx.org/keys/nginx_signing.key>`_ used to sign
   the NGINX, |_| Inc. repository and packages.

2. Add the key to the ``apt`` program's keyring:

   .. code-block:: console

      # apt-key add nginx_signing.key

   The program can then authenticate the NGINX repository signature,
   which eliminates warnings about a missing PGP key during installation
   of the Unit package.

3. Create the **/etc/apt/sources.list.d/unit.list** file with the
   following contents.

   For Ubuntu 16.04:

   .. code-block:: none

      deb https://packages.nginx.org/unit/ubuntu/ xenial unit
      deb-src https://packages.nginx.org/unit/ubuntu/ xenial unit

   For Ubuntu 18.04:

   .. code-block:: none

      deb https://packages.nginx.org/unit/ubuntu/ bionic unit
      deb-src https://packages.nginx.org/unit/ubuntu/ bionic unit

   For Ubuntu 18.10:

   .. code-block:: none

      deb https://packages.nginx.org/unit/ubuntu/ cosmic unit
      deb-src https://packages.nginx.org/unit/ubuntu/ cosmic unit

4. Install Unit base package:

   .. code-block:: console

      # apt-get update
      # apt-get install unit

5. Install additional module packages you would like to use.

   For Ubuntu 16.04:

   .. code-block:: console

      # apt-get install unit-php unit-python2.7 unit-python3.5 unit-go \
                unit-perl unit-ruby unit-dev unit-jsc-common unit-jsc8

   For Ubuntu 18.04:

   .. code-block:: console

      # apt-get install unit-php unit-python2.7 unit-python3.6 unit-go1.9 \
                unit-go1.10 unit-perl unit-ruby unit-dev unit-jsc-common \
                unit-jsc8 unit-jsc10

   For Ubuntu 18.10:

   .. code-block:: console

      # apt-get install unit-php unit-python2.7 unit-python3.6 unit-python3.7 \
            unit-go1.9 unit-go1.10 unit-perl unit-ruby unit-dev \
            unit-jsc-common unit-jsc8 unit-jsc11

.. include:: include/socket-note.rst

Debian Packages
===============

1. Download the `key <https://nginx.org/keys/nginx_signing.key>`_ used to sign
   the NGINX, |_| Inc. repository and packages.

2. Add the key to the ``apt`` program's keyring:

   .. code-block:: console

      # apt-key add nginx_signing.key

   The program can then authenticate the NGINX repository signature,
   which eliminates warnings about a missing PGP key during installation
   of the Unit package.

3. Create the **/etc/apt/sources.list.d/unit.list** file with the
   following contents.

   For Debian 8:

   .. code-block:: none

      deb https://packages.nginx.org/unit/debian/ jessie unit
      deb-src https://packages.nginx.org/unit/debian/ jessie unit

   For Debian 9:

   .. code-block:: console

      deb https://packages.nginx.org/unit/debian/ stretch unit
      deb-src https://packages.nginx.org/unit/debian/ stretch unit

4. Install Unit base package:

   .. code-block:: console

      # apt-get update
      # apt-get install unit

5. Install additional module packages you would like to use.

   For Debian 8:

   .. code-block:: console

      # apt-get install unit-php unit-python2.7 unit-python3.4 unit-perl \
                unit-ruby unit-dev

   For Debian 9:

   .. code-block:: console

      # apt-get install unit-php unit-python2.7 unit-python3.5 unit-go1.7 \
                unit-go1.8 unit-perl unit-ruby unit-dev

.. include:: include/socket-note.rst

.. _installation-precomp-pkgs-startup:

Startup and Shutdown
====================

To enable automatic startup for Unit after you install it from precompiled
packages:

    .. code-block:: console

       # systemctl enable unit.service

To start or restart Unit immediately:

    .. code-block:: console

       # systemctl restart unit.service

To stop Unit immediately:

    .. code-block:: console

       # systemctl stop unit.service

To disable automatic startup for Unit:

    .. code-block:: console

       # systemctl disable unit.service

.. _installation-community-repos:

Community Repositories
**********************

.. warning::

    Distributions listed in this section are maintained by their respective
    communities.  NGINX has no control or responsibility over these resources.
    Proceed at your own consideration.

.. _installation-alpine-apk:

Alpine Linux
============

To install core Unit executables using `Alpine Linux packages
<https://pkgs.alpinelinux.org/packages?name=unit*>`_:

.. code-block:: console

   # apk update
   # apk upgrade
   # apk add unit

To install service manager files and specific language modules:

.. code-block:: console

   # apk add unit-openrc unit-perl unit-php7 unit-python3 unit-ruby

.. note::

   Control socket is located here: :file:`/run/control.unit.sock`.

.. _installation-archlinux-aur:

Arch Linux
==========

To install Unit using the `Arch User Repository (AUR)
<https://aur.archlinux.org/pkgbase/nginx-unit/>`_:

.. code-block:: console

   $ sudo pacman -S git
   $ git clone https://aur.archlinux.org/nginx-unit.git
   $ cd nginx-unit

.. warning::

    Verify that the :file:`PKGBUILD` and accompanying files are not malicious
    or untrustworthy.  AUR packages are entirely user produced without
    pre-moderation; you use them at your own risk.

.. code-block:: console

   $ makepkg -si

.. note::

   Control socket is located here: :file:`/run/nginx-unit.control.sock`.

.. _installation-freebsd-pkgs-prts:

FreeBSD
=======

.. _installation-freebsd-pkgs:

To install Unit using `FreeBSD packages <https://www.
freebsd.org/doc/en_US.ISO8859-1/books/handbook/pkgng-intro.html>`_, update the
repository and install the package:

.. code-block:: console

   # pkg install -y unit

.. note::

   Control socket is located here: :file:`/var/run/unit/control.unit.sock`.

.. _installation-freebsd-prts:

To install Unit using `FreeBSD ports <https://www.
freebsd.org/doc/en_US.ISO8859-1/books/handbook/ports-using.html>`_, update your
port collection.

For ``portsnap``:

.. code-block:: console

   # portsnap fetch update

For ``svn``:

.. code-block:: console

   # svn update /usr/ports

Next, browse to the port path to build and install the port:

.. code-block:: console

   # cd /usr/ports/www/unit
   # make
   # make install

Warning: ``make`` here is used in port configuration.  For ``make`` commands
to build Unit from the code in our repositories, see
:ref:`installation-bld-src`.

.. note::

   Control socket is located here: :file:`/var/run/unit/control.unit.sock`.

.. _installation-gnt-prtg:

Gentoo
======

To install Unit using `Portage <https://wiki.gentoo.org/wiki/
Handbook:X86/Full/Portage>`_, update the repository and install the `package
<https://packages.gentoo.org/packages/www-servers/nginx-unit>`_:

.. code-block:: console

   # emerge --sync
   # emerge www-servers/nginx-unit

.. note::

   Control socket is located here: :file:`/run/nginx-unit.sock`.

.. _installation-remirepo:

Remi's RPM Repo
===============

`Remi's RPM repository
<https://blog.remirepo.net/post/2019/01/14/PHP-with-the-NGINX-unit-application-server>`_,
which hosts the latest versions of the PHP stack for CentOS, Fedora, and RHEL,
also has the base Unit package and the PHP modules.

To use Remi's versions of Unit packages, configure `Remi's RPM repo
<https://blog.remirepo.net/pages/Config-en>`_ first.  Remi's PHP language
modules also work with the base Unit package from :ref:`our own repository
<installation-precomp-pkgs>`.

Next, install Unit and the PHP modules you want:

.. code-block:: console

   # yum install --enablerepo=remi unit php54-unit-php php55-unit-php \
         php56-unit-php php70-unit-php php71-unit-php php72-unit-php php73-unit-php

.. note::

   Control socket is located here: :file:`/var/run/unit/control.sock`.

.. _installation-nodejs-package:

Node.js Package
***************

Unit's Node.js package is called :program:`unit-http`.  It uses Unit's
:program:`libunit` library; your Node.js applications :samp:`require` the
package to run in Unit.  You can install it from the NPM `repository
<https://www.npmjs.com/package/unit-http>`_.

Install :program:`libunit` from :program:`unit-dev/unit-devel` :ref:`packages
<installation-precomp-pkgs>` or build it from :ref:`sources
<installation-config-src>`.  Next, install :program:`unit-http` globally:

.. code-block:: console

   # npm install -g --unsafe-perm unit-http

.. warning::

    The :program:`unit-http` package is platform and architecture dependent due
    to performance optimizations.  It can't be moved across different systems
    with the rest of the :file:`node-modules` directory (for example, during
    application migration).  Global installation avoids such scenarios; just
    :ref:`relink the migrated application <configuration-external-nodejs>`.

This should suit most of your needs.  Use the package in your :ref:`Unit-hosted
application <configuration-external-nodejs>` as you would use the built-in
:program:`http` package in common Node.js web applications.

If you update Unit later, make sure to update the NPM package as well:

.. code-block:: console

   # npm update -g --unsafe-perm unit-http

.. note::

    You can also build and install :program:`unit-http` :ref:`manually
    <installation-nodejs>`.

.. _installation-src:

Source Code
***********

This section explains how to compile and install Unit from the source code.

Getting Sources
===============

There are three ways to obtain the Unit source code: from the NGINX, |_| Inc.
Mercurial repository, from GitHub, or in a tarball.

In each case, the sources are placed in the **unit** subdirectory of the
current working directory.

Mercurial Repository
--------------------

1. If you don't already have the Mercurial software, download and install it.
   For example, on Ubuntu systems, run this command:

   .. code-block:: console

      # apt-get install mercurial

2. Download the Unit sources:

   .. code-block:: console

      # hg clone https://hg.nginx.org/unit

GitHub Repository
-----------------

1. If you don't already have the Git software, download it.
   See the `GitHub documentation <https://help.github.com/>`_.

2. Download the Unit sources:

   .. code-block:: console

      # git clone https://github.com/nginx/unit

Tarball
-------

Unit source code tarballs are available at https://unit.nginx.org/download/.

Installing Required Software
============================

Before configuring and compiling Unit, install the required build tools plus
the library files for available languages (Go, Node.js, PHP, Perl, Python, and
Ruby) and the other features you want Unit to support.

The commands below assume you are configuring Unit with all supported
languages and features; otherwise, skip the packages you aren’t going to use.

.. _installation-prereq-build:

Debian, Ubuntu
--------------

.. code-block:: console

   # apt-get install build-essential
   # apt-get install golang
   # curl -sL https://deb.nodesource.com/setup_<Node.js version>.x | bash -; apt-get install nodejs
   # apt-get install php-dev libphp-embed
   # apt-get install libperl-dev
   # apt-get install python-dev
   # apt-get install ruby-dev
   # apt-get install openjdk-8-jdk
   # apt-get install libssl-dev

Amazon Linux, CentOS, RHEL
--------------------------

.. code-block:: console

   # yum install gcc make
   # yum install golang
   # curl -sL https://rpm.nodesource.com/setup_<Node.js version>.x | bash -; yum install nodejs
   # yum install php-devel php-embedded
   # yum install perl-devel perl-libs
   # yum install python-devel
   # yum install ruby-devel
   # yum install java-1.8.0-openjdk-devel
   # yum install openssl-devel

.. _installation-config-src:

Configuring Sources
===================

First, run system checks and create the :file:`Makefile` that you will update
during language module setup:

.. code-block:: console

   # ./configure <command-line options>

General :program:`./configure` options:

--help
    Displays a brief summary of common :program:`./configure` options.

    For language-specific details, run :command:`./configure <language>
    --help` or see :ref:`below <installation-src-modules>`.

These options control the compilation process:

--cc=pathname
    Specific C compiler pathname.

    The default value is :samp:`cc`.

--cc-opt=options, --ld-opt=options
    Additional C compiler and linker options.

    The default values are empty strings.

The following option pair controls Unit's runtime privileges:

--group=name, --user=name
    Group name and username to run Unit's non-privileged processes.

    The default values are :option:`!user`'s primary group and
    :samp:`nobody`, respectively.

These flags enable or disable support of certain features:

--debug
    Enables the :ref:`debug log <troubleshooting-dbg-log>`.

--no-ipv6
    Disables IPv6 support.

--no-unix-sockets
    Disables Unix domain sockets support.

--openssl
    Enables OpenSSL support.  Make sure that OpenSSL (1.0.1 and later) header
    files and libraries are available in your compiler's search path.

    To customize the path, provide the :option:`!--cc-opt` and
    :option:`!--ld-opt` options;  alternatively, set :envvar:`CFLAGS` and
    :envvar:`LDFLAGS` environment variables before running
    :program:`./configure`.

    For details, see :ref:`configuration-ssl`.

The last option group customizes Unit's :ref:`runtime directory
structure <installation-src-dir>`:

.. _installation-config-src-prefix:

--prefix=prefix

    Destination directory prefix for so-called *path options*:
    :option:`!--bindir`, :option:`!--sbindir`, :option:`!--libdir`,
    :option:`!--incdir`, :option:`!--modules`, :option:`!--state`,
    :option:`!--pid`, :option:`!--log`, and :option:`!--control`.  Their
    relative settings are prefix-based.

    The default value is an empty string.

--bindir=directory, --sbindir=directory
    Directory paths for end-user and sysadmin executables.

    The default values are :samp:`bin` and :samp:`sbin`, respectively.

--control=socket
    Address of the control API socket; Unix sockets (starting with
    :samp:`unix:`), IPv4, and IPv6 sockets are valid here.

    The default value is :samp:`unix:control.unit.sock`, created as
    :samp:`root` with :samp:`600` permissions.

    .. warning::

        For security reasons, avoid opening sockets on public interfaces in
        production.

--incdir=directory, --libdir=directory
    Directory paths for :program:`libunit` header files and libraries.

    The default values are :samp:`include` and :samp:`lib`, respectively.

--log=pathname
    Pathname for Unit's log.

    The default value is :samp:`unit.log`.

--modules=directory
    Directory path for Unit's language modules.

    The default value is :samp:`modules`.

--pid=pathname
    Pathname for the PID file of Unit's daemon process.

    The default value is :samp:`unit.pid`.

--state=directory
    Directory path for Unit's state storage.

    .. warning::

        Unit state includes its runtime configuration, certificates, and other
        private records.  It can be copied as is when you migrate your Unit
        installation; however, mind that it contains sensitive data and must be
        available only to :samp:`root` with :samp:`700` permissions.

    The default value is :samp:`state`.

.. _installation-src-dir:

Directory Structure
-------------------

To customize Unit installation and runtime directories, you can both:

- Set the :option:`!--prefix` and path options during :ref:`configuration
  <installation-config-src-prefix>` to set up the runtime file structure: Unit
  will use these settings to locate its modules, state, and other files.

- Set the :envvar:`DESTDIR` `variable
  <https://www.gnu.org/prep/standards/html_node/DESTDIR.html>`_ during
  :ref:`installation <installation-bld-src>`.  Unit file structure will be
  placed at the specified directory, which can be either the final installation
  target or an intermediate staging location.

Coordinate these two options as necessary to customize the directory structure.
One common scenario is installation based on absolute paths.

1. Set absolute runtime paths with :option:`!--prefix` and path options:

   .. code-block:: console

      # ./configure --state=/var/lib/unit --log=/var/log/unit.log \
                    --control=unix:/run/control.unit.sock --prefix=/usr/local/

   This configuration will access its state, log, and control socket at custom
   locations; other files will be accessed by default prefix-based paths:
   :file:`/usr/local/sbin/`, :file:`/usr/local/modules/`, and so on.

2. If you're building Unit on the system where you intend to run it, omit
   :option:`!DESTDIR` during installation; the files will be placed at the
   specified paths.  If you're building Unit for further packaging or
   containerization, specify :option:`!DESTDIR` to place the files in a staging
   location, preserving their relative structure.

An alternative scenario is a build that you can move around the filesystem.

1. Set relative runtime paths with :option:`!--prefix` and path options:

   .. code-block:: console

      # ./configure --state=config --log=log/unit.log \
                    --control=unix:control/control.unit.sock --prefix=movable

   This configuration will access its files by prefix-based paths (both default
   and custom): :file:`<working directory>/movable/sbin/`, :file:`<working
   directory>/movable/config/`, and so on.

2. Specify :option:`!DESTDIR` during installation to place the build where
   needed.  You can move it around your system or across compatible systems;
   however, make sure to relocate the entire file structure and start Unit
   binaries from the base directory so that the relative paths remain valid:

   .. code-block:: console

      # cd <DESTDIR>
      # movable/sbin/unitd <command-line options>

You can also combine these two approaches as you see fit; nevertheless, always
take care to understand how your settings actually work together.

.. _installation-src-modules:

Configuring Modules
===================

Next, configure a module for each language you want to use with Unit.  The
:command:`./configure <language>` commands set up individual language modules
and place module-specific instructions in the :file:`Makefile`.

.. note::

    Unit can run applications in several versions of a supported language side
    by side: you need to configure, build, and install a separate module for
    each version.

.. _installation-go:

Configuring Go
--------------

When you run :command:`./configure go`, Unit sets up the Go package that your
applications will use to run in Unit.  To use the package, install it in your
Go environment.  Available configuration options:

--go=pathname
    Specific Go executable pathname.  Also used for :ref:`build and install
    <installation-bld-src-ext>` commands.

    The default value is :samp:`go`.

--go-path=directory
    Custom directory path for Go package installation.

    The default value is :samp:`$GOPATH`.

.. note::

    The :program:`./configure` script doesn't alter the :envvar:`GOPATH`
    `environment variable <https://github.com/golang/go/wiki/GOPATH>`_. Make
    sure these two paths, the configuration-time :option:`!--go-path` and
    compile-time :envvar:`GOPATH`, are coherent so that Go can import and use
    the Unit package.

.. _installation-java:

Configuring Java
----------------

When you run :command:`./configure java`, the script configures a module to
support running `Java Web Applications
<https://download.oracle.com/otndocs/jcp/servlet-3_1-fr-spec/index.html>`_ in
Unit.  Available command options:

--home=directory
    Directory path for Java utilities and header files (required to build the
    module).

    The default value is the :samp:`java.home` setting.

--jars=directory
    Directory path for Unit's custom :file:`.jar` files.

    The default value is the Java module path.

--lib-path=directory
    Directory path for the :file:`libjvm.so` library.

    The default value is derived from JDK settings.

--local-repo=directory
    Directory path for local :file:`.jar` repository.

    The default value is :samp:`$HOME/.m2/repository/`.

--repo=directory
    URL path for remote Maven repository.

    The default value is :samp:`http://central.maven.org/maven2/`.

--module=filename
    Target name for the Java module that Unit will build
    (:file:`<module>.unit.so`).  Also used for :ref:`build and install
    <installation-bld-src-emb>` commands.

    The default value is :samp:`java`.

To configure a module called :file:`java11.unit.so` with OpenJDK 11.0.1:

.. code-block:: console

   # ./configure java --module=java11 \
                      --home=/Library/Java/JavaVirtualMachines/jdk-11.0.1.jdk/Contents/Home

.. _installation-nodejs:

Configuring Node.js
-------------------

When you run :command:`./configure nodejs`, Unit sets up the
:program:`unit-http` package that your applications will use to :ref:`run in
Unit <configuration-external-nodejs>`.  Available configuration options:

--local=directory
    Local directory path for Node.js package installation.

    By default, the package is installed globally :ref:`(recommended)
    <installation-nodejs-package>`.

--node=pathname
    Specific Node.js executable pathname.  Also used for
    :ref:`build and install <installation-bld-src-ext>` commands.

    The default value is :samp:`node`.

--npm=pathname
    Specific NPM executable pathname.

    The default value is :samp:`npm`.

--node-gyp=pathname
    Specific :program:`node-gyp` executable pathname.

    The default value is :samp:`node-gyp`.

.. _installation-perl:

Configuring Perl
----------------

When you run :command:`./configure perl`, the script configures a module to
support running Perl scripts as applications in Unit.  Available command
options:

--include=directory
        Directory path to Perl headers (required to build the module).

        The default is Perl's `$Config<archlib>/CORE <https://perldoc.perl.
        org/Config.html>`_ directory.

--perl=pathname
        Specific Perl executable pathname.

        The default value is :samp:`perl`.

--module=filename
        Target name for the Perl module that Unit will build
        (:file:`<module>.unit.so`).  Also used for :ref:`build and install
        <installation-bld-src-emb>` commands.

        The default value is the filename of the :option:`!perl` executable.

To configure a module called :file:`perl-5.20.unit.so` for Perl |_| 5.20.2:

.. code-block:: console

   # ./configure perl --module=perl-5.20 \
                      --perl=perl5.20.2

.. _installation-php:

Configuring PHP
---------------

When you run :command:`./configure php`, the script configures a module to
support running PHP applications in Unit via PHP's :program:`embed` SAPI.
Available command options:

--config=pathname
    Pathname of the :program:`php-config` script invoked to configure the PHP
    module.

    The default value is :samp:`php-config`.

--lib-path=directory
    Directory path of PHP's :program:`embed` SAPI library file
    (:file:`libphp<version>.so` or :file:`libphp<version>.a`).

--lib-static
    Enables linking with the static :program:`embed` SAPI library
    (:file:`libphp<version>.a`).  If this option is specified,
    :option:`!--lib-path` is also required.

--module=filename
    Target name for the PHP module that Unit will build
    (:file:`<module>.unit.so`).  Also used for :ref:`build and install
    <installation-bld-src-emb>` commands.

    The default value is :option:`!config`'s filename without the
    `-config` suffix (thus, :samp:`/usr/bin/php7-config` yields
    :samp:`php7`).

To configure a module called :file:`php70.unit.so` for PHP |_| 7.0:

.. code-block:: console

   # ./configure php --module=php70  \
                     --config=/usr/lib64/php7.0/bin/php-config  \
                     --lib-path=/usr/lib64/php7.0/lib64

.. _installation-python:

Configuring Python
------------------

When you run :command:`./configure python`, the script configures a module to
support running Python scripts as applications in Unit.  Available command
options:

--config=pathname
    Pathname of the :program:`python-config` script invoked to configure
    the Python module.

    The default value is :samp:`python-config`.

--lib-path=directory
    Custom directory path of the Python runtime library to use with Unit.

--module=filename
    Target name for the Python module that Unit will build
    (:samp:`<module>.unit.so`).  Also used for :ref:`build and install
    <installation-bld-src-emb>` commands.

    The default value is :option:`!config`'s filename without the `-config`
    suffix (thus, :samp:`/usr/bin/python3-config` yields :samp:`python3`).

To configure a module called :file:`py33.unit.so` for Python |_| 3.3:

.. code-block:: console

   # ./configure python --module=py33  \
                        --config=python-config-3.3

.. _installation-ruby:

Configuring Ruby
----------------

When you run :program:`./configure ruby`, the script configures a module to
support running Ruby scripts as applications in Unit.  Available command
options:

--module=filename
        Target name for the Ruby module that Unit will build
        (:file:`<module>.unit.so`).  Also used for :ref:`build and install
        <installation-bld-src-emb>` commands.

        The default value is the filename of the :option:`!ruby` executable.

--ruby=pathname
        Specific Ruby executable pathname.

        The default value is :samp:`ruby`.

To configure a module called :file:`ru23.unit.so` for Ruby |_| 2.3:

.. code-block:: console

   # ./configure ruby --module=ru23  \
                      --ruby=ruby23

.. _installation-bld-src:

Building and Installing Unit
============================

To build Unit executables and language modules that you have
:program:`./configure`'d earlier and install them:

.. code-block:: console

   # make
   # make install

You can also build and install language modules individually; the specific
method depends on whether the language module is embedded in Unit or packaged
externally.

.. _installation-bld-src-emb:

Embedded Language Modules
-------------------------

To build and install Unit modules for Java, PHP, Perl, Python, or Ruby after
configuration, run :command:`make <module>` and :command:`make
<module>-install`, for example:

.. code-block:: console

   # make perl-5.20
   # make perl-5.20-install

.. _installation-bld-src-ext:

External Language Packages
--------------------------

To build and install Unit packages for Go and Node.js after configuration, run
:command:`make <go>-install` and :command:`make <node>-install`, for example:

.. code-block:: console

   # make go-install
   # make node-install

.. note::

    To install the Node.js package locally, run :command:`make
    <node>-local-install`:

    .. code-block:: console

       # make node-local-install

    If you haven't specified the :option:`!local` :ref:`directory
    <installation-nodejs>` with :program:`./configure nodejs` earlier, provide
    it here: :command:`DESTDIR=/your/project/directory`.  If both options are
    specified, :option:`!DESTDIR` prefixes the :option:`!local` value.
    However, the recommended method is :ref:`global installation
    <installation-nodejs-package>`.

If you customize the executable pathname with :option:`!go` or
:option:`!node`, use the following pattern:

.. code-block:: console

   # ./configure nodejs --node=/usr/local/bin/node8.12
   # make /usr/local/bin/node8.12-install

   # ./configure go --go=/usr/local/bin/go1.7
   # make /usr/local/bin/go1.7-install

.. _installation-startup:

Startup
=======

We advise installing Unit from :ref:`preconfigured packages
<installation-precomp-pkgs>`; in this case, startup is configured
automatically.

Even if you install Unit otherwise, manual startup is not recommended.
Instead, configure a service manager such as :program:`OpenRC` or
:program:`systemd` or create an :program:`rc.d` script to launch the Unit
daemon using the options below; refer to your system guides for detailed
instructions.

To start the daemon, run :program:`unitd` as :samp:`root` from the :samp:`sbin`
installation subdirectory.  Usually, there's no need to override compile-time
settings; use the :option:`!--help` command-line option to review their
values.  For details and security notes, refer to
:ref:`installation-config-src`.

General options:

--help, -h
    Displays a brief summary of Unit's command-line options and their
    default values that were configured at compile time.

--no-daemon
    Runs Unit in non-daemon mode.

--version
    Displays Unit version and :program:`./configure` settings it was built
    with.

The following options override compile-time settings:

--control socket
    Address of the control API socket.  IPv4, IPv6, and Unix domain sockets
    are supported.

--group name, --user name
    Group name and user name used to run Unit's non-privileged processes.

--log pathname
    Pathname for the Unit log.

--modules directory
    Directory path for Unit language modules
    (:file:`<module>.unit.so` files).

--pid pathname
    Pathname for the PID file of Unit's :program:`main` process.

--state directory
    Directory path for Unit state storage.
