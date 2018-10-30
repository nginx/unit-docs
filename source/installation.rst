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

For applications running in NGINX Unit you need the respective programming
languages:

* Go 1.6 or later
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

To install and run Unit from our Docker image repository::

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

For further details, see the `repository page <https://hub.docker.com/r/
nginx/unit/>`_.

.. _installation-precomp-pkgs:

Precompiled Packages
********************

Precompiled binaries for Unit are available for:

 * CentOS 6, 7
 * RHEL 6, 7
 * Amazon Linux
 * Ubuntu 16.04, 17.10, 18.04
 * Debian 8, 9

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

2. Install Unit base package::

    # yum install unit

3. Install additional module packages you would like to use, e.g.::

    # yum install unit-php unit-python unit-go unit-perl unit-devel

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

2. Install Unit base package::

    # yum install unit

3. Install additional module packages you would like to use.

   For RHEL 6::

    # yum install unit-php unit-python unit-perl unit-devel

   For RHEL 7::

    # yum install unit-php unit-python unit-go unit-perl unit-devel

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

2. Install Unit base package::

    # yum install unit

3. Install additional module packages you would like to use, e.g.::

    # yum install unit-php unit-python27 unit-python34 unit-python35 \
          unit-python36 unit-go unit-perl unit-devel

   For Amazon Linux 2 LTS::

    # yum install unit-php unit-python unit-go unit-perl unit-devel

Ubuntu Packages
===============

1. Download the `key <https://nginx.org/keys/nginx_signing.key>`_ used to sign
   the NGINX, |_| Inc. repository and packages.

2. Add the key to the ``apt`` program's keyring::

    # apt-key add nginx_signing.key

   The program can then authenticate the NGINX repository signature,
   which eliminates warnings about a missing PGP key during installation
   of the Unit package.

3. Create the **/etc/apt/sources.list.d/unit.list** file with the
   following contents.

   For Ubuntu 16.04::

    deb https://packages.nginx.org/unit/ubuntu/ xenial unit
    deb-src https://packages.nginx.org/unit/ubuntu/ xenial unit

   For Ubuntu 17.10::

    deb https://packages.nginx.org/unit/ubuntu/ artful unit
    deb-src https://packages.nginx.org/unit/ubuntu/ artful unit

   For Ubuntu 18.04::

    deb https://packages.nginx.org/unit/ubuntu/ bionic unit
    deb-src https://packages.nginx.org/unit/ubuntu/ bionic unit

4. Install Unit base package::

    # apt-get update
    # apt-get install unit

5. Install additional module packages you would like to use.

   For Ubuntu 16.04::

    # apt-get install unit-php unit-python2.7 unit-python3.5 unit-go \
          unit-perl unit-ruby unit-dev

   For Ubuntu 17.10::

    # apt-get install unit-php unit-python2.7 unit-python3.6 unit-go1.8 \
          unit-go1.9 unit-perl unit-ruby unit-dev

   For Ubuntu 18.04::

    # apt-get install unit-php unit-python2.7 unit-python3.6 unit-go1.9 \
          unit-go1.10 unit-perl unit-ruby unit-dev

Debian Packages
===============

1. Download the `key <https://nginx.org/keys/nginx_signing.key>`_ used to sign
   the NGINX, |_| Inc. repository and packages.

2. Add the key to the ``apt`` program's keyring::

    # apt-key add nginx_signing.key

   The program can then authenticate the NGINX repository signature,
   which eliminates warnings about a missing PGP key during installation
   of the Unit package.

3. Create the **/etc/apt/sources.list.d/unit.list** file with the
   following contents.

   For Debian 8::

    deb https://packages.nginx.org/unit/debian/ jessie unit
    deb-src https://packages.nginx.org/unit/debian/ jessie unit

   For Debian 9::

    deb https://packages.nginx.org/unit/debian/ stretch unit
    deb-src https://packages.nginx.org/unit/debian/ stretch unit

4. Install Unit base package::

    # apt-get update
    # apt-get install unit

5. Install additional module packages you would like to use.

   For Debian 8::

    # apt-get install unit-php unit-python2.7 unit-python3.4 unit-perl \
          unit-ruby unit-dev

   For Debian 9::

    # apt-get install unit-php unit-python2.7 unit-python3.5 unit-go1.7 \
          unit-go1.8 unit-perl unit-ruby unit-dev

.. _installation-community-repos:

Community Repositories
**********************

Warning: Distributions listed in this section are maintained by their
respective communities.  NGINX has no control or responsibility over these
resources.  Proceed at your own consideration.

.. _installation-freebsd-pkgs-prts:

FreeBSD
=======

.. _installation-freebsd-pkgs:

To install Unit using `FreeBSD packages <https://www.
freebsd.org/doc/en_US.ISO8859-1/books/handbook/pkgng-intro.html>`_, update the
repository and install the package::

    # pkg install -y unit

.. _installation-freebsd-prts:

To install Unit using `FreeBSD ports <https://www.
freebsd.org/doc/en_US.ISO8859-1/books/handbook/ports-using.html>`_, update your
port collection.

For ``portsnap``::

    # portsnap fetch update

For ``svn``::

    # svn update /usr/ports

Next, browse to the port path to build and install the port::

    # cd /usr/ports/www/unit
    # make
    # make install

Warning: ``make`` here is used in port configuration.  For ``make`` commands
to build Unit from the code in our repositories, see :ref:`installation-src`.

.. _installation-gnt-prtg:

Gentoo
======

To install Unit using `Portage <https://wiki.gentoo.org/wiki/
Handbook:X86/Full/Portage>`_, update the repository and install the `package
<https://packages.gentoo.org/packages/www-servers/nginx-unit>`_::

    # emerge --sync
    # emerge www-servers/nginx-unit

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

    # npm install -g unit-http

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

    # npm update -g unit-http

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
   For example, on Ubuntu systems, run this command::

    # apt-get install mercurial

2. Download the Unit sources::

    # hg clone https://hg.nginx.org/unit

GitHub Repository
-----------------

1. If you don't already have the Git software, download it.
   See the `GitHub documentation <https://help.github.com/>`_.

2. Download the Unit sources::

    # git clone https://github.com/nginx/unit

Tarball
-------

Unit source code tarballs are available at https://unit.nginx.org/download/.

Installing Required Software
============================

Before configuring and compiling Unit, you must install the required build
tools plus the library files for each of the available languages (Go, Node.js,
PHP, Perl, Python, and Ruby) that you want to support.

Ubuntu Prerequisites
--------------------

1. Install the build tools::

    # apt-get install build-essential

2. For Go applications support, install the ``golang`` package::

    # apt-get install golang

3. For Node.js applications support, install the official :program:`nodejs`
   package:

    .. code-block:: console

       # curl -sL https://deb.nodesource.com/setup_<Node.js version>.x | bash -
       # apt-get install nodejs

4. For PHP applications support, install the ``php-dev`` and ``libphp-embed``
   packages::

    # apt-get install php-dev
    # apt-get install libphp-embed

5. For Python applications support, install the ``python-dev`` package::

    # apt-get install python-dev

6. For Perl applications support, install the ``libperl-dev`` package::

    # apt-get install libperl-dev

7. For Ruby applications support, install the ``ruby-dev`` package::

    # apt-get install ruby-dev

CentOS Prerequisites
--------------------

1. Install the build tools::

    # yum install gcc make

2. For Go applications support, install the ``golang`` package::

    # yum install golang

3. For Node.js applications support, install the official :program:`nodejs`
   package:

   .. code-block:: console

       # curl -sL https://rpm.nodesource.com/setup_<Node.js version>.x | bash -
       # yum install nodejs

4. For PHP applications support, install the ``php-devel`` and ``php-embedded``
   packages::

    # yum install php-devel php-embedded

5. For Python applications support, install the ``python-devel`` package::

    # yum install python-devel

6. For Perl applications support, install the ``perl-devel`` and ``perl-libs``
   packages::

    # yum install perl-devel perl-libs

7. For Ruby applications support, install the ``ruby-devel`` package::

    # yum install ruby-devel

.. _installation-config-src:

Configuring Sources
===================

First, run system checks and create the :file:`Makefile` that you will update
during language module setup:

.. code-block:: console

    # ./configure

The :program:`./configure` script has the following options available:

--help
    Displays a brief summary of general :program:`./configure` options.

    For language-specific details, run :command:`./configure <language>
    --help`.

--cc=pathname
    Specific C compiler pathname.

    The default value is :samp:`cc`.

--cc-opt=options
    Additional C compiler options.

--ld-opt=options
    Additional linker options.

--prefix=directory

    Destination directory prefix for relative pathnames (can
    occur in :option:`!--bindir`, :option:`!--sbindir`, :option:`!--libdir`,
    :option:`!--incdir`, :option:`!--modules`, :option:`!--state`,
    :option:`!--pid`, :option:`!--log`, and :option:`!--control`).

    Specify the prefix to customize Unit's post-installation directory
    structure.

--bindir=directory
    Directory name for end-user executables; relative path here is
    :option:`!--prefix`-based.

    The default value is :samp:`bin`.

--sbindir=directory
    Directory name for sysadmin executables; relative path here is
    :option:`!--prefix`-based.

    The default value is :samp:`sbin`.

--libdir=directory
    Directory name for :program:`libunit` library files; relative path here is
    :option:`!--prefix`-based.

    The default value is :samp:`lib`.

--incdir=directory
    Directory name for :program:`libunit` include files; relative path here is
    :option:`!--prefix`-based.

    The default value is :samp:`include`.

--modules=directory
    Directory name for Unit language modules; relative path here is
    :option:`!--prefix`-based.

    The default value is :samp:`modules`.

--state=directory
    State directory name; relative path here is :option:`!--prefix`-based.

    The default value is :samp:`state`.

--pid=filename
    Filename for the PID file of Unit's daemon process; relative path here is
    :option:`!--prefix`-based.

    The default value is :samp:`unit.pid`.

--log=filename
    Filename for the Unit log; relative path here is :option:`!--prefix`-based.

    The default value is :samp:`unit.log`.

--control=socket
    Address of the control API socket; Unix sockets (starting with
    :samp:`unix:`), IPv4, and IPv6 sockets are valid here.  For Unix sockets,
    relative path here is :option:`!--prefix`-based.

    The default value is :samp:`unix:control.unit.sock`.

--user=name
    Username to run Unit's non-privileged processes.

    The default value is :samp:`nobody`.

--group=name
    Group name to run Unit's non-privileged processes.

    The default value is :option:`!--user`'s primary group.

--openssl
    Enables OpenSSL support.  Make sure that OpenSSL (1.0.1 and later) header
    files and libraries are available in your compiler's search path.

    To customize the path, provide the :option:`!--cc-opt` and
    :option:`!--ld-opt` options;  alternatively, set :envvar:`CFLAGS` and
    :envvar:`LDFLAGS` environment variables before running
    :program:`./configure`.

    For details, see :ref:`configuration-ssl`.

--debug
    Enables the :ref:`debug log <troubleshooting-dbg-log>`.

--no-unix-sockets
    Disables Unix domain sockets support.

--no-ipv6
    Disables IPv6 support.

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
    Specific Go executable pathname.

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

To build and install the Go package for Unit after configuration, run
:command:`make go-install`:

.. code-block:: console

    # ./configure go
    # make go-install

If you customize the Go executable pathname, use the following pattern:

.. code-block:: console

    # ./configure go --go=/usr/local/bin/go1.7
    # make /usr/local/bin/go1.7-install

.. _installation-nodejs:

Configuring Node.js
-------------------

When you run :command:`./configure nodejs`, Unit sets up the
:program:`unit-http` package that your applications will use to :ref:`run in
Unit <configuration-external-nodejs>`.  Available configuration options:

--node=pathname
    Specific Node.js executable pathname.

    The default value is :samp:`node`.

--npm=pathname
    Specific NPM executable pathname.

    The default value is :samp:`npm`.

--node-gyp=pathname
    Specific :program:`node-gyp` executable pathname.

    The default value is :samp:`node-gyp`.

Next, run :command:`make node-install` to build and install the
:samp:`unit-http` package globally:

.. code-block:: console

    # ./configure nodejs
    # make node-install

If you customize the Node.js executable pathname, use the following pattern:

.. code-block:: console

    # ./configure nodejs --node=/usr/local/bin/node8.12
    # make /usr/local/bin/node8.12-install

Optionally, run :command:`make node-local-install` to install the
:program:`unit-http` package locally:

    .. code-block:: console

        # ./configure nodejs
        # make node-local-install DESTDIR=/your/project/directory

.. _installation-perl:

Configuring Perl
----------------

When you run :command:`./configure perl`, the script configures a module to
support running Perl scripts as applications in Unit.  Available command
options:

--include=directory
        Directory path to Perl headers (required to build the module).

        The default is Perl's `$Config{archlib}/CORE <https://perldoc.perl.
        org/Config.html>`_ directory.

--perl=pathname
        Specific Perl executable pathname.

        The default value is :samp:`perl`.

--module=filename
        Target name for the Perl module that Unit will build
        (:file:`<filename>.unit.so`).

        The default value is the filename of the :option:`!--perl` executable.

To configure a module called :file:`perl-5.20.unit.so` for Perl |_| 5.20.2:

.. code-block:: console

    # ./configure perl --module=perl-5.20 \
                       --perl=perl5.20.2

        configuring Perl module
        checking for Perl ... found
         + Perl version: 5.20.2
         + Perl module: perl-5.20.unit.so

To build and install the configured module separately:

.. code-block:: console

    # make perl-5.20
    # make perl-5.20-install

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
    (:file:`<filename>.unit.so`).

    The default value is :option:`!--config`'s filename without the
    `-config` suffix (thus, :samp:`/usr/bin/php7-config` yields
    :samp:`php7`).

For example, this command configures a module called :file:`php70.unit.so` for
PHP |_| 7.0:

.. code-block:: console

    # ./configure php --module=php70  \
                      --config=/usr/lib64/php7.0/bin/php-config  \
                      --lib-path=/usr/lib64/php7.0/lib64

        configuring PHP module
        checking for PHP ... found
         + PHP version: 7.0.22-0ubuntu0.16.04.1
         + PHP SAPI: [apache2handler embed cgi cli fpm]
        checking for PHP embed SAPI ... found
         + PHP module: php70.unit.so

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
    (:samp:`<filename>.unit.so`).

    The default value is :option:`!--config`'s filename without the `-config`
    suffix (thus, :samp:`/usr/bin/python3-config` yields :samp:`python3`).

For example, this command configures a module called :file:`py33.unit.so` for
Python |_| 3.3:

.. code-block:: console

    # ./configure python --module=py33  \
                         --config=python-config-3.3

        configuring Python module
        checking for Python ... found
        checking for Python version ... 3.3
         + Python module: py33.unit.so

.. _installation-ruby:

Configuring Ruby
----------------

When you run :program:`./configure ruby`, the script configures a module to
support running Ruby scripts as applications in Unit.  Available command
options:

--module=filename
        Target name for the Ruby module that Unit will build
        (:file:`<filename>.unit.so`).

        The default value is the filename of the :option:`!--ruby` executable.

--ruby=pathname
        Specific Ruby executable pathname.

        The default value is :samp:`ruby`.

For example, this command configures a module called :file:`ru23.unit.so` for
Ruby |_| 2.3:

.. code-block:: console

    # ./configure ruby --module=ru23  \
                       --ruby=ruby23

        configuring Ruby module
        checking for Ruby ... found
         + Ruby version: 2.3.0
         + Ruby module: ru23.unit.so

Compiling Sources
=================

To compile the Unit executable and all configured modules run this command::

    # make all

Installing from Sources
=======================

To install Unit with all modules and Go packages, run the following command::

    # make install
