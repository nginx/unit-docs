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

* Python 2.6, 2.7, 3
* PHP 5, 7
* Go 1.6 or later
* Perl 5.12 or later
* Ruby 2.0 or later

You can run multiple versions of the same language installed on the same
system.

Precompiled Packages
********************

Precompiled binaries for Unit are available for:

 * CentOS 6, 7
 * RHEL 6, 7
 * Amazon Linux
 * Ubuntu 16.04, 17.10
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

    # yum install unit-php unit-python unit-go unit-perl

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

    # yum install unit-php unit-python unit-perl

   For RHEL 7::

    # yum install unit-php unit-python unit-go unit-perl

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

    # yum install unit-php unit-python27 unit-python34 unit-python35 unit-python36 unit-go unit-perl

   For Amazon Linux 2 LTS::

    # yum install unit-php unit-python unit-go unit-perl

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

4. Install Unit base package::

    # apt-get update
    # apt-get install unit

5. Install additional module packages you would like to use.

   For Ubuntu 16.04::

    # apt-get install unit-php unit-python2.7 unit-python3.5 unit-go unit-perl unit-ruby

   For Ubuntu 17.10::

    # apt-get install unit-php unit-python2.7 unit-python3.6 unit-go1.8 unit-go1.9 unit-perl unit-ruby

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

    # apt-get install unit-php unit-python2.7 unit-python3.4 unit-perl unit-ruby

   For Debian 9::

    # apt-get install unit-php unit-python2.7 unit-python3.5 unit-go1.7 unit-go1.8 unit-perl unit-ruby

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
tools plus the library files for each of the available languages (Go, PHP,
and Python) that you want to support.

Ubuntu Prerequisites
--------------------

1. Install the build tools::

    # apt-get install build-essential

2. For Go applications support, install the ``golang`` package::

    # apt-get install golang

3. For PHP applications support, install the ``php-dev`` and ``libphp-embed``
   packages::

    # apt-get install php-dev
    # apt-get install libphp-embed

4. For Python applications support, install the ``python-dev`` package::

    # apt-get install python-dev

5. For Perl applications support, install the ``libperl-dev`` package::

    # apt-get install libperl-dev

6. For Ruby applications support, install the ``ruby-dev`` package::

    # apt-get install ruby-dev

CentOS Prerequisites
--------------------

1. Install the build tools::

    # yum install gcc make

2. For Go applications support, install the ``golang`` package::

    # yum install golang

3. For PHP applications support, install the ``php-devel`` and ``php-embedded``
   packages::

    # yum install php-devel php-embedded

4. For Python applications support, install the ``python-devel`` package::

    # yum install python-devel

5. For Perl applications support, install the ``perl-devel`` and ``perl-libs``
   packages::

    # yum install perl-devel perl-libs

6. For Ruby applications support, install the ``ruby-devel`` package::

    # yum install ruby-devel

Configuring Sources
===================

First you need to run configure script to perform necessary system checks and
generate Makefile required to compile all other stuff::

    # ./configure

With Unit, you can simultaneously run applications that use different versions
of a supported language (Go, PHP, or Python).  You need to configure a separate
Unit module for each one. The following commands create the necessary
instructions in the **Makefile** for each module.

Configuring Go Package
----------------------

NGINX Unit will provide the Go package that is required for running your Go
application inside Unit.

1. Set the ``GOPATH`` environment variable, which sets the output directory
   for the Unit Go package::

    # export GOPATH=/home/user/go_apps

2. Run the following command::

    # ./configure go
    configuring Go package
    checking for Go ... found
     + go version go1.6.2 linux/amd64
     + Go package path: "/home/user/go_apps"

3. Install the Go package in your working GOPATH::

    # make go-install

Building the Go Applications
----------------------------

1. Modify the source file for the Go application, making changes in two
   places:

   a) In the ``import`` section, add ``"nginx/unit"`` on a separate line:

      .. code-block:: go

        import (
            "fmt"
            "net/http"
            "nginx/unit"
        )

   b) In the ``main()`` function, comment out the ``http.ListenandServe``
      function and insert the ``unit.ListenAndServe`` function:

      .. code-block:: go

        func main() {
            http.HandleFunc("/", handler)
            //http.ListenAndServe(":8080", nil)
            unit.ListenAndServe(":8080", nil)
        }

2. Build the Go application::

    # go build

If the Go application is executed directly, the unit module will fall back
to the http module.  If the Go application is launched by Unit, it will
communicate with the Unit router via shared memory.

Configuring Perl Modules
------------------------

To configure a Unit module (called **perl.unit.so**) for the version of
Perl that the ``configure`` script finds bundled with the operating system,
run this command::

    # ./configure perl

To configure Unit modules for other versions of Perl (including versions you
have customized), repeat the following command for each one::

    # ./configure perl OPTIONS

where ``OPTIONS`` can be:

--module=<prefix>

  Sets the filename prefix for the Unit module specific to the Perl
  version (that is, the resulting module is called **<prefix>.unit.so**).

--perl=<perl>

  Specifies the particular Perl interpreter.

--include=<directory>

  Specifies the directory for the Perl headers files to use.

For example, this command generates a module called **perl-5.20.unit.so** for
Perl |_| 5.20.2::

    $ ./configure perl --module=perl-5.20 \
                       --perl=perl5.20.2
    configuring Perl module
    checking for Perl ... found
     + Perl version: 5.20.2
     + Perl module: perl-5.20.unit.so

Configuring PHP Modules
-----------------------

To configure a Unit module (called **php.unit.so**) for the version of
PHP that the ``configure`` script finds bundled with the operating system,
run this command::

    # ./configure php

To configure Unit modules for other versions of PHP (including versions you
have customized), repeat the following command for each one::

    # ./configure php OPTIONS

where ``OPTIONS`` can be:

--module=<prefix>

  Sets the filename prefix for the Unit module specific to the PHP
  version (that is, the resulting module is called **<prefix>.unit.so**).

--config=<script>

  Specifies the **php-config** script for the particular version of PHP.

--lib-path=<directory>

  Specifies the directory for the PHP library file to use.

--lib-static

  Enables linking with static library.

For example, this command generates a module called **php70.unit.so** for
PHP |_| 7.0::

    # ./configure php --module=php70  \
                      --config=/usr/lib64/php7.0/php-config  \
                      --lib-path=/usr/lib64/php7.0/lib64
    configuring PHP module
    checking for PHP ... found
     + PHP version: 7.0.22-0ubuntu0.16.04.1
     + PHP SAPI: [apache2handler embed cgi cli fpm]
    checking for PHP embed SAPI ... found
     + PHP module: php70.unit.so

Configuring Python Modules
--------------------------

To configure a Unit module (called **python.unit.so**) for the version of
Python that the ``configure`` script finds bundled with the operating system,
run this command::

    # ./configure python

To configure Unit modules for other versions of Python (including versions you
have customized), repeat the following command for each one::

    # ./configure python OPTIONS

where ``OPTIONS`` can be:

--module=<prefix>

  Sets the filename prefix for the Unit module specific to the Python
  version (that is, the resulting module is called **<prefix>.unit.so**).

--config=<script>

  Specifies the **python-config** script for the particular version of Python.

--lib-path=<directory>

  Specifies the directory for the Python library file to use.

For example, this command generates a module called **py33.unit.so** for
Python |_| 3.3::

    # ./configure python --module=py33  \
                         --config=python-config-3.3
    configuring Python module
    checking for Python ... found
    checking for Python version ... 3.3
     + Python module: py33.unit.so

Configuring Ruby Modules
--------------------------

To configure a Unit module (called **ruby.unit.so**) for the version of
Ruby that the ``configure`` script finds bundled with the operating system,
run this command::

    # ./configure ruby

To configure Unit modules for other versions of Ruby (including versions you
have customized), repeat the following command for each one::

    # ./configure ruby OPTIONS

where ``OPTIONS`` can be:

--module=<prefix>

  Sets the filename prefix for the Unit module specific to the Ruby
  version (that is, the resulting module is called **<prefix>.unit.so**).

--ruby=<ruby>

  Specifies the particular Ruby interpreter.

For example, this command generates a module called **ru23.unit.so** for
Ruby |_| 2.3::

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
