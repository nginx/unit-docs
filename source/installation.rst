.. meta::
   :og:description: Download official packages, use third-party repositories, or configure a custom build from source.

.. include:: include/replace.rst

############
Installation
############

You can install NGINX Unit in four alternative ways:

- Choose from our official :ref:`binary packages <installation-precomp-pkgs>`
  for a few popular systems.  They are as easy to use as any other packaged
  software and suit most purposes straight out of the box.

- If your preferred OS or language version is missing from the official package
  list, try :ref:`third-party repositories <installation-community-repos>`.  Be
  warned, though: we don't maintain them.

- Run our official :ref:`Docker images <installation-docker>`, prepackaged with
  varied language combinations.

- To fine-tune Unit to your goals, download the :ref:`sources
  <installation-src>`, install the :ref:`toolchain
  <installation-prereq-build>`, and :ref:`build <installation-config-src>` a
  custom binary from scratch; just make sure you know what you're doing.


.. _installation-prereqs:

*************
Prerequisites
*************

Unit compiles and runs on various Unix-like operating systems, including:

- FreeBSD |_| 10 or later
- Linux |_| 2.6 or later
- macOS |_| 10.6 or later
- Solaris |_| 11

It also supports most modern instruction set architectures, such as:

- ARM
- IA-32
- PowerPC
- MIPS
- S390X
- x86-64

App languages and platforms that Unit can run (including several versions of
the same language):

- Go |_| 1.6 or later
- Java |_| 8 or later
- Node.js |_| 8.11 or later
- PHP |_| 5, 7, 8
- Perl |_| 5.12 or later
- Python |_| 2.6, 2.7, 3
- Ruby |_| 2.0 or later


.. _installation-precomp-pkgs:

*****************
Official Packages
*****************

Installing a precompiled Unit binary package is best for most occasions;
`official <https://packages.nginx.org/unit/>`_ binaries are available for:

- Amazon |_| Linux, Amazon |_| Linux |_| 2
- CentOS |_| 6, 7, 8
- Debian |_| 8, 9, 10
- Fedora |_| 28, 29, 30, 31, 32, 33
- RHEL |_| 6, 7, 8
- Ubuntu |_| 16.04, 18.04, 18.10, 19.04, 19.10, 20.04, 20.10

The packages we provide include core executables, developer files, and support
for individual languages.

We also maintain an official Homebrew `tap
<https://github.com/nginx/homebrew-unit>`_ for macOS users.

.. note::

   Unit's language :ref:`module <installation-nodejs-package>` for Node.js is
   available at the `npm <https://www.npmjs.com/package/unit-http>`_ registry.

.. note::

   For details of packaging custom modules that install alongside the official
   Unit, see :ref:`here <modules-pkg>`.


.. _installation-precomp-amazon:

============
Amazon Linux
============

Supported architectures: :samp:`x86-64`.

.. tabs::
   :prefix: amazon

   .. tab:: 2.0 LTS

      #. To configure Unit repository, create the following file named
         :file:`/etc/yum.repos.d/unit.repo`:

         .. code-block:: ini

            [unit]
            name=unit repo
            baseurl=https://packages.nginx.org/unit/amzn2/$releasever/$basearch/
            gpgcheck=0
            enabled=1

      #. Install the core package and other packages you need:

         .. code-block:: console

            # yum install unit
            # yum install :nxt_term:`unit-devel <Required to install the Node.js module and build Go apps>` unit-go unit-jsc8 unit-perl \
                  unit-php unit-python27 unit-python37

   .. tab:: AMI

      #. To configure Unit repository, create the following file named
         :file:`/etc/yum.repos.d/unit.repo`:

         .. code-block:: ini

            [unit]
            name=unit repo
            baseurl=https://packages.nginx.org/unit/amzn/$releasever/$basearch/
            gpgcheck=0
            enabled=1

      #. Install the core package and other packages you need:

         .. code-block:: console

            # yum install unit
            # yum install :nxt_term:`unit-devel <Required to install the Node.js module and build Go apps>` unit-go unit-jsc8 unit-perl unit-php \
                  unit-python27 unit-python34 unit-python35 unit-python36

.. include:: include/socket-log-rpm.rst


.. _installation-precomp-centos:

======
CentOS
======

.. tabs::
   :prefix: centos

   .. tab:: 8.x, 7.x

      Supported architectures: :samp:`x86-64`.

      #. To configure Unit repository, create the following file named
         :file:`/etc/yum.repos.d/unit.repo`:

         .. code-block:: ini

            [unit]
            name=unit repo
            baseurl=https://packages.nginx.org/unit/centos/$releasever/$basearch/
            gpgcheck=0
            enabled=1

      #. Install the core package and other packages you need:

         .. code-block:: console

            # yum install unit
            # yum install :nxt_term:`unit-devel <Required to install the Node.js module and build Go apps>` unit-go unit-jsc8 unit-jsc11 \
                  unit-perl unit-php unit-python27 unit-python36

   .. tab:: 6.x

      .. warning::

         Unit 1.20+ packages aren't available for CentOS 6.  This distribution
         is obsolete; please update.

      Supported architectures: :samp:`i386`, :samp:`x86-64`.

      #. To configure Unit repository, create the following file named
         :file:`/etc/yum.repos.d/unit.repo`:

         .. code-block:: ini

            [unit]
            name=unit repo
            baseurl=https://packages.nginx.org/unit/centos/$releasever/$basearch/
            gpgcheck=0
            enabled=1

      #. Install the core package and other packages you need:

         .. code-block:: console

            # yum install unit
            # yum install :nxt_term:`unit-devel <Required to install the Node.js module and build Go apps>` unit-go unit-jsc8 unit-php unit-python

.. include:: include/socket-log-rpm.rst


.. _installation-precomp-deb:

======
Debian
======

Supported architectures: :samp:`i386`, :samp:`x86-64`.

.. tabs::
   :prefix: debian

   .. tab:: 10

      #. Download NGINX's `signing key
         <https://nginx.org/keys/nginx_signing.key>`_ and add it to
         :program:`apt`'s keyring:

         .. code-block:: console

            # curl -sL https://nginx.org/keys/nginx_signing.key | apt-key add -

         This eliminates the 'packages cannot be authenticated' warnings during
         installation.

      #. To configure Unit repository, create the following file named
         :file:`/etc/apt/sources.list.d/unit.list`:

         .. code-block:: none

            deb https://packages.nginx.org/unit/debian/ buster unit
            deb-src https://packages.nginx.org/unit/debian/ buster unit

      #. Install the core package and other packages you need:

         .. code-block:: console

            # apt update
            # apt install unit
            # apt install :nxt_term:`unit-dev <Required to install the Node.js module and build Go apps>` unit-go unit-jsc11 unit-perl \
                  unit-php unit-python2.7 unit-python3.7 unit-ruby

   .. tab:: 9

      #. Download NGINX's `signing key
         <https://nginx.org/keys/nginx_signing.key>`_ and add it to
         :program:`apt`'s keyring:

         .. code-block:: console

            # curl -sL https://nginx.org/keys/nginx_signing.key | apt-key add -

         This eliminates the 'packages cannot be authenticated' warnings during
         installation.

      #. To configure Unit repository, create the following file named
         :file:`/etc/apt/sources.list.d/unit.list`:

         .. code-block:: none

            deb https://packages.nginx.org/unit/debian/ stretch unit
            deb-src https://packages.nginx.org/unit/debian/ stretch unit

      #. Install the core package and other packages you need:

         .. code-block:: console

            # apt update
            # apt install unit
            # apt install :nxt_term:`unit-dev <Required to install the Node.js module and build Go apps>` unit-go unit-jsc8 unit-perl \
                  unit-php unit-python2.7 unit-python3.5 unit-ruby

   .. tab:: 8

      .. warning::

         Unit 1.12+ packages aren't available for Debian 8.  This distribution
         is obsolete; please update.

      #. Download NGINX's `signing key
         <https://nginx.org/keys/nginx_signing.key>`_ and add it to
         :program:`apt`'s keyring:

         .. code-block:: console

            # curl -sL https://nginx.org/keys/nginx_signing.key | apt-key add -

         This eliminates the 'packages cannot be authenticated' warnings during
         installation.

      #. To configure Unit repository, create the following file named
         :file:`/etc/apt/sources.list.d/unit.list`:

         .. code-block:: none

            deb https://packages.nginx.org/unit/debian/ jessie unit
            deb-src https://packages.nginx.org/unit/debian/ jessie unit

      #. Install the core package and other packages you need:

         .. code-block:: console

            # apt update
            # apt install unit
            # apt install :nxt_term:`unit-dev <Required to install the Node.js module and build Go apps>` unit-perl unit-php unit-python2.7 \
                  unit-python3.4 unit-ruby

.. include:: include/socket-log-deb.rst


.. _installation-precomp-fedora:

======
Fedora
======

Supported architectures: :samp:`x86-64`.

.. tabs::
   :prefix: fedora

   .. tab:: 33

      #. To configure Unit repository, create the following file named
         :file:`/etc/yum.repos.d/unit.repo`:

         .. code-block:: ini

            [unit]
            name=unit repo
            baseurl=https://packages.nginx.org/unit/fedora/$releasever/$basearch/
            gpgcheck=0
            enabled=1

      #. Install the core package and other packages you need:

         .. code-block:: console

            # yum install unit
            # yum install :nxt_term:`unit-devel <Required to install the Node.js module and build Go apps>` unit-go unit-jsc11 unit-jsc8 unit-perl \
                  unit-php unit-python39 unit-ruby

   .. tab:: 32

      #. To configure Unit repository, create the following file named
         :file:`/etc/yum.repos.d/unit.repo`:

         .. code-block:: ini

            [unit]
            name=unit repo
            baseurl=https://packages.nginx.org/unit/fedora/$releasever/$basearch/
            gpgcheck=0
            enabled=1

      #. Install the core package and other packages you need:

         .. code-block:: console

            # yum install unit
            # yum install :nxt_term:`unit-devel <Required to install the Node.js module and build Go apps>` unit-go unit-jsc11 unit-jsc8 unit-perl \
                  unit-php unit-python38 unit-ruby

   .. tab:: 31, 30

      #. To configure Unit repository, create the following file named
         :file:`/etc/yum.repos.d/unit.repo`:

         .. code-block:: ini

            [unit]
            name=unit repo
            baseurl=https://packages.nginx.org/unit/fedora/$releasever/$basearch/
            gpgcheck=0
            enabled=1

      #. Install the core package and other packages you need:

         .. code-block:: console

            # yum install unit
            # yum install :nxt_term:`unit-devel <Required to install the Node.js module and build Go apps>` unit-go unit-jsc11 unit-jsc8 unit-perl \
                  unit-php unit-python27 unit-python37 unit-ruby

   .. tab:: 29

      #. To configure Unit repository, create the following file named
         :file:`/etc/yum.repos.d/unit.repo`:

         .. code-block:: ini

            [unit]
            name=unit repo
            baseurl=https://packages.nginx.org/unit/fedora/$releasever/$basearch/
            gpgcheck=0
            enabled=1

      #. Install the core package and other packages you need:

         .. code-block:: console

            # yum install unit
            # yum install :nxt_term:`unit-devel <Required to install the Node.js module and build Go apps>` unit-go unit-jsc8 unit-perl \
                  unit-php unit-python27 unit-python37 unit-ruby

   .. tab:: 28

      .. warning::

         Unit 1.12+ packages aren't available for Fedora 28.  This distribution
         is obsolete; please update.

      #. To configure Unit repository, create the following file named
         :file:`/etc/yum.repos.d/unit.repo`:

         .. code-block:: ini

            [unit]
            name=unit repo
            baseurl=https://packages.nginx.org/unit/fedora/$releasever/$basearch/
            gpgcheck=0
            enabled=1

      #. Install the core package and other packages you need:

         .. code-block:: console

            # yum install unit
            # yum install :nxt_term:`unit-devel <Required to install the Node.js module and build Go apps>` unit-go unit-jsc8 unit-perl \
                  unit-php unit-python27 unit-python36 unit-ruby

.. include:: include/socket-log-rpm.rst


.. _installation-precomp-rhel:

====
RHEL
====

.. tabs::
   :prefix: rhel

   .. tab:: 8.x, 7.x

      Supported architectures: :samp:`x86-64`.

      #. To configure Unit repository, create the following file named
         :file:`/etc/yum.repos.d/unit.repo`:

         .. code-block:: ini

            [unit]
            name=unit repo
            baseurl=https://packages.nginx.org/unit/rhel/$releasever/$basearch/
            gpgcheck=0
            enabled=1

      #. Install the core package and other packages you need:

         .. code-block:: console

            # yum install unit
            # yum install :nxt_term:`unit-devel <Required to install the Node.js module and build Go apps>` unit-go unit-jsc8 unit-jsc11 \
                  unit-perl unit-php unit-python27 unit-python36

   .. tab:: 6.x

      Supported architectures: :samp:`i386`, :samp:`x86-64`.

      #. To configure Unit repository, create the following file named
         :file:`/etc/yum.repos.d/unit.repo`:

         .. code-block:: ini

            [unit]
            name=unit repo
            baseurl=https://packages.nginx.org/unit/rhel/$releasever/$basearch/
            gpgcheck=0
            enabled=1

      #. Install the core package and additional packages you need:

         .. code-block:: console

            # yum install unit
            # yum install :nxt_term:`unit-devel <Required to install the Node.js module and build Go apps>` unit-go unit-jsc8 unit-perl \
                  unit-php unit-python

.. include:: include/socket-log-rpm.rst


.. _installation-precomp-ubuntu:

======
Ubuntu
======

.. tabs::
   :prefix: ubuntu

   .. tab:: 20.10

      Supported architectures: :samp:`arm64`, :samp:`x86-64`.

      #. Download NGINX's `signing key
         <https://nginx.org/keys/nginx_signing.key>`_ and add it to
         :program:`apt`'s keyring:

         .. code-block:: console

            # curl -sL https://nginx.org/keys/nginx_signing.key | apt-key add -

         This eliminates the 'packages cannot be authenticated' warnings during
         installation.

      #. To configure Unit repository, create the following file named
         :file:`/etc/apt/sources.list.d/unit.list`:

         .. code-block:: none

            deb https://packages.nginx.org/unit/ubuntu/ groovy unit
            deb-src https://packages.nginx.org/unit/ubuntu/ groovy unit

      #. Install the core package and other packages you need:

         .. code-block:: console

            # apt update
            # apt install unit
            # apt install :nxt_term:`unit-dev <Required to install the Node.js module and build Go apps>` unit-go unit-jsc11 unit-jsc13 unit-jsc14 unit-jsc15 \
                          unit-perl unit-php unit-python3.8 unit-ruby

   .. tab:: 20.04

      Supported architectures: :samp:`arm64`, :samp:`x86-64`.

      #. Download NGINX's `signing key
         <https://nginx.org/keys/nginx_signing.key>`_ and add it to
         :program:`apt`'s keyring:

         .. code-block:: console

            # curl -sL https://nginx.org/keys/nginx_signing.key | apt-key add -

         This eliminates the 'packages cannot be authenticated' warnings during
         installation.

      #. To configure Unit repository, create the following file named
         :file:`/etc/apt/sources.list.d/unit.list`:

         .. code-block:: none

            deb https://packages.nginx.org/unit/ubuntu/ focal unit
            deb-src https://packages.nginx.org/unit/ubuntu/ focal unit

      #. Install the core package and other packages you need:

         .. code-block:: console

            # apt update
            # apt install unit
            # apt install :nxt_term:`unit-dev <Required to install the Node.js module and build Go apps>` unit-go unit-jsc11 unit-perl \
                  unit-php unit-python2.7 unit-python3.8 unit-ruby

   .. tab:: 19.10

      .. warning::

         Unit 1.20+ packages aren't available for Ubuntu 19.10.  This
         distribution is obsolete; please update.

      Supported architectures: :samp:`x86-64`.

      #. Download NGINX's `signing key
         <https://nginx.org/keys/nginx_signing.key>`_ and add it to
         :program:`apt`'s keyring:

         .. code-block:: console

            # curl -sL https://nginx.org/keys/nginx_signing.key | apt-key add -

         This eliminates the 'packages cannot be authenticated' warnings during
         installation.

      #. To configure Unit repository, create the following file named
         :file:`/etc/apt/sources.list.d/unit.list`:

         .. code-block:: none

            deb https://packages.nginx.org/unit/ubuntu/ eoan unit
            deb-src https://packages.nginx.org/unit/ubuntu/ eoan unit

      #. Install the core package and other packages you need:

         .. code-block:: console

            # apt update
            # apt install unit
            # apt install :nxt_term:`unit-dev <Required to install the Node.js module and build Go apps>` unit-go unit-jsc11 unit-perl \
                  unit-php unit-python2.7 unit-python3.7 unit-python3.8 unit-ruby

   .. tab:: 19.04

      Supported architectures: :samp:`x86-64`.

      .. warning::

         Unit 1.16+ packages aren't available for Ubuntu 19.04.  This
         distribution is obsolete; please update.

      #. Download NGINX's `signing key
         <https://nginx.org/keys/nginx_signing.key>`_ and add it to
         :program:`apt`'s keyring:

         .. code-block:: console

            # curl -sL https://nginx.org/keys/nginx_signing.key | apt-key add -

         This eliminates the 'packages cannot be authenticated' warnings during
         installation.

      #. To configure Unit repository, create the following file named
         :file:`/etc/apt/sources.list.d/unit.list`:

         .. code-block:: none

            deb https://packages.nginx.org/unit/ubuntu/ disco unit
            deb-src https://packages.nginx.org/unit/ubuntu/ disco unit

      #. Install the core package and other packages you need:

         .. code-block:: console

            # apt update
            # apt install unit
            # apt install :nxt_term:`unit-dev <Required to install the Node.js module and build Go apps>` unit-go unit-jsc11 unit-perl \
                  unit-php unit-python2.7 unit-python3.7 unit-ruby

   .. tab:: 18.10

      Supported architectures: :samp:`x86-64`.

      .. warning::

         Unit 1.12+ packages aren't available for Ubuntu 18.10.  This
         distribution is obsolete; please update.

      #. Download NGINX's `signing key
         <https://nginx.org/keys/nginx_signing.key>`_ and add it to
         :program:`apt`'s keyring:

         .. code-block:: console

            # curl -sL https://nginx.org/keys/nginx_signing.key | apt-key add -

         This eliminates the 'packages cannot be authenticated' warnings during
         installation.

      #. To configure Unit repository, create the following file named
         :file:`/etc/apt/sources.list.d/unit.list`:

         .. code-block:: none

            deb https://packages.nginx.org/unit/ubuntu/ cosmic unit
            deb-src https://packages.nginx.org/unit/ubuntu/ cosmic unit

      #. Install the core package and other packages you need:

         .. code-block:: console

            # apt update
            # apt install unit
            # apt install :nxt_term:`unit-dev <Required to install the Node.js module and build Go apps>` unit-go1.10 unit-jsc8 unit-jsc11 unit-perl \
                  unit-php unit-python2.7 unit-python3.6 unit-python3.7 unit-ruby

   .. tab:: 18.04

      Supported architectures: :samp:`arm64`, :samp:`x86-64`.

      #. Download NGINX's `signing key
         <https://nginx.org/keys/nginx_signing.key>`_ and add it to
         :program:`apt`'s keyring:

         .. code-block:: console

            # curl -sL https://nginx.org/keys/nginx_signing.key | apt-key add -

         This eliminates the 'packages cannot be authenticated' warnings during
         installation.

      #. To configure Unit repository, create the following file named
         :file:`/etc/apt/sources.list.d/unit.list`:

         .. code-block:: none

            deb https://packages.nginx.org/unit/ubuntu/ bionic unit
            deb-src https://packages.nginx.org/unit/ubuntu/ bionic unit

      #. Install the core package and other packages you need:

         .. code-block:: console

            # apt update
            # apt install unit
            # apt install :nxt_term:`unit-dev <Required to install the Node.js module and build Go apps>` unit-go unit-jsc8 unit-jsc11 unit-perl \
                  unit-php unit-python2.7 unit-python3.6 unit-python3.7 unit-ruby

   .. tab:: 16.04

      Supported architectures: :samp:`arm64`, :samp:`i386`, :samp:`x86-64`.

      #. Download NGINX's `signing key
         <https://nginx.org/keys/nginx_signing.key>`_ and add it to
         :program:`apt`'s keyring:

         .. code-block:: console

            # curl -sL https://nginx.org/keys/nginx_signing.key | apt-key add -

         This eliminates the 'packages cannot be authenticated' warnings during
         installation.

      #. To configure Unit repository, create the following file named
         :file:`/etc/apt/sources.list.d/unit.list`:

         .. code-block:: none

            deb https://packages.nginx.org/unit/ubuntu/ xenial unit
            deb-src https://packages.nginx.org/unit/ubuntu/ xenial unit

      #. Install the core package and other packages you need:

         .. code-block:: console

            # apt update
            # apt install unit
            # apt install :nxt_term:`unit-dev <Required to install the Node.js module and build Go apps>` unit-go unit-jsc8 unit-perl unit-php \
                  unit-python2.7 unit-python3.5 unit-ruby

.. include:: include/socket-log-deb.rst


.. _installation-homebrew:

========
Homebrew
========

To install Unit on macOS from our official Homebrew `tap
<https://github.com/nginx/homebrew-unit>`_:

.. code-block:: console

   $ brew install nginx/unit/unit

This deploys the core Unit binary and the prerequisites for :ref:`Go
<installation-go-package>` and :ref:`Node.js <installation-nodejs-package>`
language module installation.

To install Java, Perl, Python, and Ruby language modules from Homebrew:

.. code-block:: console

   $ brew install unit-java unit-perl unit-python unit-python3 unit-ruby

.. note::

   Control :ref:`socket <security-socket-state>`'s pathname:
   :file:`/usr/local/var/run/unit/control.sock`; log :ref:`file
   <troubleshooting-log>`'s pathname: :file:`/usr/local/var/log/unit/unit.log`.


.. _installation-go-package:

==
Go
==

To install the Go language module:

.. code-block:: console

   $ go get unit.nginx.org/go

That's it; now, you can :ref:`use it <configuration-external-go>` to run your
Go apps in Unit.


.. _installation-nodejs-package:

=======
Node.js
=======

Unit's `npm-hosted <https://www.npmjs.com/package/unit-http>`_ Node.js module
is :program:`unit-http`.  Your Node.js apps must :samp:`require` it to run in
Unit:

#. First, install the :samp:`unit-dev/unit-devel` :ref:`package
   <installation-precomp-pkgs>`, necessary to build :program:`unit-http`.

#. Next, build and install :program:`unit-http` globally (this step requires
   :program:`npm` and :program:`node-gyp`):

    .. code-block:: console

       # npm install -g --unsafe-perm unit-http

    .. warning::

       The :program:`unit-http` module is platform dependent due to
       optimizations; you can't move it across systems with the rest of
       :file:`node-modules`.  Global installation avoids such scenarios; just
       :ref:`relink <configuration-external-nodejs>` the migrated app.

#. After that, :ref:`use <configuration-external-nodejs>` the module in your
   Node.js app instead of the built-in :program:`http` to run it in Unit.  Mind
   that such frameworks as Express may require extra
   :doc:`changes in your code <howto/express>`.

If you update Unit later, make sure to update the module as well:

.. code-block:: console

   # npm update -g --unsafe-perm unit-http

.. note::

   You can also :ref:`configure <installation-modules-nodejs>` and
   :ref:`install <installation-bld-src-ext>` the :program:`unit-http` module
   from sources.


.. _installation-precomp-startup:

====================
Startup and Shutdown
====================

Run :command:`unitd -h` or :command:`unitd --version` to verify Unit is
available or list its settings.  To manage the installation:

.. tabs::
   :prefix: startup-shutdown
   :toc:

   .. tab:: Amazon, CentOS, Debian, Fedora, RHEL, Ubuntu

      Enable Unit to launch automatically at system startup:

      .. code-block:: console

         # systemctl enable unit

      Start or restart Unit:

      .. code-block:: console

         # systemctl restart unit

      Stop a running Unit:

      .. code-block:: console

         # systemctl stop unit

      Disable Unit's automatic startup:

      .. code-block:: console

         # systemctl disable unit

   .. tab:: Homebrew

      Start Unit as a daemon:

      .. code-block:: console

         # unitd

      Stop all Unit processes:

      .. code-block:: console

         # pkill unitd

      For startup options, see :ref:`below <installation-src-startup>`.


.. _installation-community-repos:

**********************
Community Repositories
**********************

.. warning::

   These distributions are maintained by respective communities, not NGINX.
   Proceed with caution.

..
   Legacy anchors are left here so that external links remain valid

.. _installation-alpine-apk:
.. _installation-archlinux-aur:
.. _installation-scls:
.. _installation-freebsd-pkgs-prts:
.. _installation-gnt-prtg:
.. _installation-nix:
.. _installation-remirepo:

.. tabs::
   :prefix: community
   :toc:

   .. tab:: Alpine

      To install core Unit executables from the `Alpine Linux packages
      <https://pkgs.alpinelinux.org/packages?name=unit*>`_:

      .. code-block:: console

         # apk update
         # apk upgrade
         # apk add unit

      To install service manager files and specific language modules:

      .. code-block:: console

         # apk add unit-openrc unit-perl unit-php7 unit-python3 unit-ruby

      Runtime details:

      .. list-table::

         * - Control :ref:`socket <installation-src-startup>`
           - :file:`/run/control.unit.sock`

         * - Log :ref:`file <troubleshooting-log>`
           - :file:`/var/log/unit.log`

         * - Non-privileged :ref:`user and group <security-apps>`
           - :samp:`unit`

         * - Startup and shutdown
           - .. code-block:: console

                # service unit start
                # service unit stop


   .. tab:: Arch

      To install core Unit executables and all language modules, clone the
      `Arch User Repository (AUR)
      <https://aur.archlinux.org/pkgbase/nginx-unit/>`_:

      .. code-block:: console

         $ git clone https://aur.archlinux.org/nginx-unit.git
         $ cd nginx-unit

      Before proceeding further, verify that the :file:`PKGBUILD` and the
      accompanying files aren't malicious or untrustworthy.  AUR packages are
      user produced without pre-moderation; use them at your own risk.

      Next, build the package:

      .. code-block:: console

         $ makepkg -si

      Runtime details:

      .. list-table::

         * - Control :ref:`socket <installation-src-startup>`
           - :file:`/run/nginx-unit.control.sock`

         * - Log :ref:`file <troubleshooting-log>`
           - :file:`/var/log/nginx-unit.log`

         * - Non-privileged :ref:`user and group <security-apps>`
           - :samp:`nobody`

         * - Startup and shutdown
           - .. code-block:: console

                # systemctl start unit
                # systemctl stop unit


   .. tab:: CentOS/RHEL SCLs

      If you use `SCLo Software Collections
      <https://wiki.centos.org/SpecialInterestGroup/SCLo>`_ in your
      environment, you can install Unit's PHP modules as packages from the
      corresponding repo.  Besides other dependencies, the packages require
      the :ref:`core Unit installation <installation-precomp-pkgs>`.

      CentOS:

      .. code-block:: console

         # yum install centos-release-scl
         # yum install --enablerepo=centos-sclo-sclo \
                       sclo-php72-unit-php sclo-php73-unit-php

      RHEL:

      .. code-block:: console

         # cd /etc/yum.repos.d/
         # curl -O https://copr.fedorainfracloud.org/coprs/rhscl/centos-release-scl/repo/epel-7/rhscl-centos-release-scl-epel-7.repo
         # yum install centos-release-scl
         # yum install --enablerepo=centos-sclo-sclo \
                       sclo-php72-unit-php sclo-php73-unit-php

   .. tab:: FreeBSD

      To install Unit from `FreeBSD packages <https://www.
      freebsd.org/doc/en_US.ISO8859-1/books/handbook/pkgng-intro.html>`_,
      install the core package and other packages you need:

      .. code-block:: console

         # pkg install -y unit
         # pkg install -y :nxt_term:`libunit <Required to install the Node.js module and build Go apps>`
         # pkg install -y unit-java8  \
                          unit-perl5.32  \
                          unit-php73 unit-php74 unit-php80  \
                          unit-python37  \
                          unit-ruby2.7

      To install Unit from `FreeBSD ports <https://www.
      freebsd.org/doc/en_US.ISO8859-1/books/handbook/ports-using.html>`_,
      start by updating your port collection.

      With :program:`portsnap`:

      .. code-block:: console

         # portsnap fetch update

      With :program:`svn`:

      .. code-block:: console

         # svn update /usr/ports

      Next, browse to the port path to build and install the core Unit port:

      .. code-block:: console

         # cd /usr/ports/www/unit/
         # make
         # make install

      Repeat the steps for the other ports you need: `libunit
      <https://www.freshports.org/devel/libunit/>`_ (required to install the
      :ref:`Node.js <installation-nodejs-package>` module and build :ref:`Go
      <installation-go-package>` apps), `unit-java
      <https://www.freshports.org/www/unit-java/>`_, `unit-perl
      <https://www.freshports.org/www/unit-perl/>`_, `unit-php
      <https://www.freshports.org/www/unit-php/>`_, `unit-python
      <https://www.freshports.org/www/unit-python/>`_, or `unit-ruby
      <https://www.freshports.org/www/unit-ruby/>`_.

      Runtime details:

      .. list-table::

         * - Control :ref:`socket <installation-src-startup>`
           - :file:`/var/run/unit/control.unit.sock`

         * - Log :ref:`file <troubleshooting-log>`
           - :file:`/var/log/unit/unit.log`

         * - Non-privileged :ref:`user and group <security-apps>`
           - :samp:`www`

         * - Startup and shutdown
           - .. code-block:: console

                # service unitd start
                # service unitd stop


   .. tab:: Gentoo

      To install Unit using `Portage <https://wiki.gentoo.org/wiki/
      Handbook:X86/Full/Portage>`_, update the repository and install the
      `package
      <https://packages.gentoo.org/packages/www-servers/nginx-unit>`__:

      .. code-block:: console

         # emerge --sync
         # emerge www-servers/nginx-unit

      To install specific language modules and features, apply the
      corresponding `USE flags
      <https://packages.gentoo.org/packages/www-servers/nginx-unit>`_.

      Runtime details:

      .. list-table::

         * - Control :ref:`socket <installation-src-startup>`
           - :file:`/run/nginx-unit.sock`

         * - Log :ref:`file <troubleshooting-log>`
           - :file:`/var/log/nginx-unit`

         * - Non-privileged :ref:`user and group <security-apps>`
           - :samp:`nobody`

         * - Startup and shutdown
           - .. code-block:: console

                # openrc -s nginx-unit start
                # openrc -s nginx-unit stop


   .. tab:: Nix

      To install core Unit executables and all language modules using the `Nix
      package manager <https://nixos.org/nix/>`_, update the channel, check if
      Unit's available, and install the `package
      <https://github.com/NixOS/nixpkgs/blob/master/pkgs/servers/http/unit/>`__:

      .. code-block:: console

         $ nix-channel --update
         $ nix-env -qa 'unit'
         $ nix-env -i unit

      This installs most embedded language modules and such features as SSL or
      IPv6 support.  For a full list of optionals, see the `package definition
      <https://github.com/NixOS/nixpkgs/blob/master/pkgs/servers/http/unit/default.nix>`_;
      for a :file:`.nix` configuration file defining an app, see `this sample
      <https://github.com/NixOS/nixpkgs/blob/master/nixos/tests/web-servers/unit-php.nix>`_.

      Runtime details:

      .. list-table::

         * - Control :ref:`socket <installation-src-startup>`
           - :file:`/run/unit/control.unit.sock`

         * - Log :ref:`file <troubleshooting-log>`
           - :file:`/var/log/unit/unit.log`

         * - Non-privileged :ref:`user and group <security-apps>`
           - :samp:`unit`

         * - Startup and shutdown
           - Add :samp:`services.unit.enable = true;` to
             :file:`/etc/nixos/configuration.nix` and rebuild the
             system configuration:

             .. code-block:: console

                # nixos-rebuild switch

             After that, use :program:`systemctl`:

             .. code-block:: console

                # systemctl start unit
                # systemctl stop unit


   .. tab:: Remi's RPM Repo

      `Remi's RPM repository
      <https://blog.remirepo.net/post/2019/01/14/PHP-with-the-NGINX-unit-application-server>`_,
      which hosts the latest versions of the PHP stack for CentOS, Fedora, and
      RHEL, also has the core Unit package and the PHP modules.

      To use Remi's versions of Unit packages, configure `Remi's RPM repo
      <https://blog.remirepo.net/pages/Config-en>`_ first.  Remi's PHP language
      modules are also compatible with the core Unit package from :ref:`our own
      repository <installation-precomp-pkgs>`.

      Next, install Unit and the PHP modules you want:

      .. code-block:: console

         # yum install --enablerepo=remi unit  \
               php54-unit-php php55-unit-php php56-unit-php  \
               php70-unit-php php71-unit-php php72-unit-php php73-unit-php php74-unit-php  \
               php80-unit-php

      Runtime details:

      .. list-table::

         * - Control :ref:`socket <installation-src-startup>`
           - :file:`/run/unit/control.sock`

         * - Log :ref:`file <troubleshooting-log>`
           - :file:`/var/log/unit/unit.log`

         * - Non-privileged :ref:`user and group <security-apps>`
           - :samp:`nobody`

         * - Startup and shutdown
           - .. code-block:: console

                # systemctl start unit
                # systemctl stop unit


.. _installation-docker:

*************
Docker Images
*************

Unit's Docker images come in several language-specific flavors:

.. list-table::
   :header-rows: 1

   * - Tag
     - Description

   * - :samp:`|version|-minimal`
     - No language modules are included.

   * - :samp:`|version|-go1.15`
     - Single-language image based on the :samp:`golang:1.15` `image <https://hub.docker.com/_/golang>`__.

   * - :samp:`|version|-jsc11`
     - Single-language image based on the :samp:`openjdk:11-jdk` `image <https://hub.docker.com/_/openjdk>`__.

   * - :samp:`|version|-node15`
     - Single-language image based on the :samp:`node:15` `image <https://hub.docker.com/_/node>`__.

   * - :samp:`|version|-perl5.32`
     - Single-language image based on the :samp:`perl:5.32` `image <https://hub.docker.com/_/perl>`__.

   * - :samp:`|version|-php8.0`
     - Single-language image based on the :samp:`php:8.0-cli` `image <https://hub.docker.com/_/php>`__.

   * - :samp:`|version|-python3.9`
     - Single-language image based on the :samp:`python:3.9` `image <https://hub.docker.com/_/python>`__.

   * - :samp:`|version|-ruby2.7`
     - Single-language image based on the :samp:`ruby:2.7` `image <https://hub.docker.com/_/ruby>`__.

.. nxt_details:: Images With Pre-1.22.0 Unit Versions

   Before Unit 1.22.0 was released, the following tagging scheme was used:

    .. list-table::
       :header-rows: 1

       * - Tag
         - Description

       * - :samp:`<version>-full`
         - Contains modules for all languages that Unit currently supports.

       * - :samp:`<version>-minimal`
         - No language modules are included.

       * - :samp:`<version>-<language>`
         - A specific language module such as :samp:`1.21.0-ruby2.3` or
           :samp:`1.21.0-python2.7`.

You can obtain the images from these sources:

.. tabs::

   .. tab:: Docker Hub

      To install and run Unit from NGINX's `repository
      <https://hub.docker.com/r/nginx/unit/>`__ at Docker Hub:

      .. code-block:: console

         $ docker pull docker.io/nginx/unit::nxt_term:`TAG <Specific image tag; see above for a complete list>`
         $ docker run -d docker.io/nginx/unit::nxt_term:`TAG <Specific image tag; see above for a complete list>`

   .. tab:: Amazon ECR Public Gallery

      To install and run Unit from NGINX's `repository
      <https://gallery.ecr.aws/nginx/unit>`__ at Amazon ECR Public Gallery:

      .. code-block:: console

         $ docker pull public.ecr.aws/nginx/unit::nxt_term:`TAG <Specific image tag; see above for a complete list>`
         $ docker run -d public.ecr.aws/nginx/unit::nxt_term:`TAG <Specific image tag; see above for a complete list>`

   .. tab:: packages.nginx.org

      To install and run Unit from tarballs stored on our `website
      <https://packages.nginx.org/unit/docker/>`_:

      .. subs-code-block:: console

         $ curl -O https://packages.nginx.org/unit/docker/|version|/nginx-unit-:nxt_term:`TAG <Specific image tag; see above for a complete list>`.tar.gz
         $ curl -O https://packages.nginx.org/unit/docker/|version|/nginx-unit-:nxt_term:`TAG <Specific image tag; see above for a complete list>`.tar.gz.sha512
         $ sha512sum -c nginx-unit-:nxt_term:`TAG <Specific image tag; see above for a complete list>`.tar.gz.sha512
               nginx-unit-:nxt_term:`TAG <Specific image tag; see above for a complete list>`.tar.gz: OK

         $ docker load < nginx-unit-:nxt_term:`TAG <Specific image tag; see above for a complete list>`.tar.gz

.. note::

   Control :ref:`socket <security-socket-state>`'s pathname:
   :file:`/var/run/control.unit.sock`; log :ref:`file <troubleshooting-log>`'s
   pathname: forwarded to the `Docker log collector
   <https://docs.docker.com/config/containers/logging/>`_; non-privileged
   process :ref:`accounts <security-apps>`: :samp:`unit:unit`.

For more details, see the repository pages (`Docker Hub
<https://hub.docker.com/r/nginx/unit/>`_, `Amazon ECR Public Gallery
<https://gallery.ecr.aws/nginx/unit>`_) and our :doc:`Howto <howto/docker>`.


.. _installation-docker-init:

=====================
Initial Configuration
=====================

Official images support initial container configuration, implemented with an
:samp:`ENTRYPOINT` `script
<https://docs.docker.com/engine/reference/builder/#entrypoint>`_.

First, the script checks the Unit :ref:`state directory
<installation-config-src-state>` (:file:`/var/lib/unit/` in official images) of
the container.  If it's empty, the script processes certain file types in the
container's :file:`/docker-entrypoint.d/` directory:

.. list-table::
   :header-rows: 1

   * - File Type
     - Purpose/Action

   * - :file:`.pem`
     - :ref:`Certificate bundles <configuration-ssl>` are uploaded under
       respective names: :samp:`cert.pem` to :samp:`certificates/cert`.

   * - :file:`.json`
     - :ref:`Configuration snippets <configuration-mgmt>` are uploaded as
       to the :samp:`config` section of Unit's configuration.

   * - :file:`.sh`
     - :nxt_term:`Shell scripts <Use shebang in your scripts to specify a
       custom shell>` that run in the container after the :file:`.pem` and
       :file:`.json` files are uploaded.

.. note::

   The script issues warnings about any other file types in the
   :file:`/docker-entrypoint.d/` directory.  Also, your shell
   scripts must have execute permissions set.

This mechanism allows you to customize your containers at startup, reuse
configurations, and automate your workflows, reducing manual effort.  To use
the feature, add :samp:`COPY` directives for certificate bundles, configuration
fragments, and shell scripts to your :file:`Dockerfile` derived from an
official image:

.. subs-code-block:: docker

   FROM nginx/unit:|version|-minimal
   COPY ./*.pem  /docker-entrypoint.d/
   COPY ./*.json /docker-entrypoint.d/
   COPY ./*.sh   /docker-entrypoint.d/

.. note::

   Mind that running Unit even once populates its :samp:`state` directory; this
   prevents the script from executing, so this script-based initialization must
   occur before you run Unit within your derived image.

This feature comes in handy if you want to tie Unit to a certain app
configuration for later use.  For ad-hoc initialization, you can mount a
directory with configuration files to a container at startup:

.. subs-code-block:: console

   $ docker run -d --mount \
            type=bind,src=/path/to/config/files/,dst=/docker-entrypoint.d/ \
            nginx/unit:|version|-minimal)


.. _installation-src:

***********
Source Code
***********

=================
Obtaining Sources
=================

You can get Unit source code from our official Mercurial repository, its
GitHub mirror, or in a tarball.

If you'd like to use `Mercurial <https://www.mercurial-scm.org/downloads>`_:

   .. code-block:: console

      $ hg clone https://hg.nginx.org/unit
      $ cd unit

If you prefer `Git <https://git-scm.com/downloads>`_:

   .. code-block:: console

      $ git clone https://github.com/nginx/unit
      $ cd unit

To download sources directly from `our site
<https://unit.nginx.org/download/>`_:

   .. subs-code-block:: console

      $ curl -O https://unit.nginx.org/download/unit-|version|.tar.gz
      $ tar xzf unit-|version|.tar.gz
      $ cd unit-|version|


.. _installation-prereq-build:

============================
Installing Required Software
============================

Before configuring and compiling Unit, install the required build tools plus
the library files for available languages (Go, Node.js, PHP, Perl, Python, and
Ruby) and other features you want Unit to support.

The commands below assume you are configuring Unit with all supported
languages and features; otherwise, skip the packages you aren’t going to use.

.. tabs::
   :prefix: prereq
   :toc:

   .. tab:: Debian, Ubuntu

      .. code-block:: console

         # apt install build-essential
         # apt install golang
         # curl -sL :nxt_term:`https://deb.nodesource.com/setup_version.x <Node.js 8.11 or later is supported>` | bash -
         # apt install nodejs
         # npm install -g node-gyp
         # apt install php-dev libphp-embed
         # apt install libperl-dev
         # apt install python-dev
         # apt install ruby-dev
         # apt install :nxt_term:`openjdk-8-jdk <Java 8 or later is supported. Different JDKs may be used>`
         # apt install libssl-dev
         # apt install libpcre2-dev

   .. tab:: Amazon, CentOS, Fedora, RHEL

      .. code-block:: console

         # yum install gcc make
         # yum install golang
         # curl -sL :nxt_term:`https://rpm.nodesource.com/setup_version.x <Node.js 8.11 or later is supported>` | bash -
         # yum install nodejs
         # npm install -g node-gyp
         # yum install php-devel php-embedded
         # yum install perl-devel perl-libs
         # yum install python-devel
         # yum install ruby-devel
         # yum install :nxt_term:`java-1.8.0-openjdk-devel <Java 8 or later is supported. Different JDKs may be used>`
         # yum install openssl-devel
         # yum install pcre2-devel

   .. tab:: FreeBSD

      Ports:

      .. code-block:: console

         # cd /usr/ports/lang/go/ && make install clean
         # cd /usr/ports/www/node/ && make install clean
         # cd /usr/ports/www/npm/ && make install clean && npm i -g node-gyp
         # cd :nxt_term:`/usr/ports/lang/php73/ <PHP versions 5 and 7 are supported>` && make install clean
         # cd :nxt_term:`/usr/ports/lang/perl5.28/ <Perl 5.12 or later is supported>` && make install clean
         # cd /usr/ports/lang/python/ && make install clean
         # cd :nxt_term:`/usr/ports/lang/ruby25/ <Ruby 2.0 or later is supported>` && make install clean
         # cd :nxt_term:`/usr/ports/java/openjdk8/ <Java 8 or later is supported. Different JDKs may be used>` && make install clean
         # cd /usr/ports/security/openssl/ && make install clean
         # cd /usr/ports/devel/pcre2/ && make install clean

      Packages:

      .. code-block:: console

         # pkg install go
         # pkg install node && pkg install npm && npm i -g node-gyp
         # pkg install :nxt_term:`php73 <PHP versions 5 and 7 are supported>`
         # pkg install :nxt_term:`perl5 <Perl 5.12 or later is supported>`
         # pkg install python
         # pkg install :nxt_term:`ruby25 <Ruby 2.0 is supported>`
         # pkg install :nxt_term:`openjdk8 <Java 8 or later is supported. Different JDKs may be used>`
         # pkg install openssl
         # pkg install pcre2

   .. tab:: Solaris

      .. code-block:: console

         # pkg install gcc
         # pkg install golang
         # pkg install :nxt_term:`php-71 <PHP versions 5 and 7 are supported>`
         # pkg install ruby
         # pkg install :nxt_term:`jdk-8 <Java 8 or later is supported. Different JDKs may be used>`
         # pkg install openssl
         # pkg install pcre

      Also, use :program:`gmake` instead of :program:`make` when :ref:`building
      and installing <installation-bld-src>` Unit on Solaris.


.. _installation-config-src:

===================
Configuring Sources
===================

To run system compatibility checks and generate a :file:`Makefile` with core
build instructions for Unit:

.. code-block:: console

   $ ./configure <command-line options>

To finalize the resulting :file:`Makefile`, configure the :ref:`language
modules <installation-src-modules>` you need.

General options and settings that control compilation, runtime privileges,
or support for certain features:

.. list-table::

   * - :samp:`--help`
     -  Displays a summary of common :program:`./configure` options.

        For language-specific details, run :command:`./configure <language>
        --help` or see :ref:`below <installation-src-modules>`.

   * - :samp:`--cc=pathname`
     - Custom C compiler pathname.

       The default is :samp:`cc`.

   * - :samp:`--cc-opt=options`, :samp:`--ld-opt=options`
     - Extra options for the C compiler and linker.

   * - :samp:`--group=name`, :samp:`--user=name`
     - Group name and username to run Unit's non-privileged processes.

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

.. _installation-config-src-pcre:

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
structure <installation-src-dir>`:

.. list-table::

   * - :samp:`--prefix=prefix`

     - .. _installation-config-src-prefix:

       Destination directory prefix for :ref:`path options
       <installation-src-dir>`: :option:`!--bindir`, :option:`!--sbindir`,
       :option:`!--libdir`, :option:`!--incdir`, :option:`!--modules`,
       :option:`!--state`, :option:`!--pid`, :option:`!--log`, and
       :option:`!--control`.

   * - :samp:`--bindir=directory`, :samp:`--sbindir=directory`
     - Directory paths for end-user and sysadmin executables.

       The defaults are :samp:`bin` and :samp:`sbin`, respectively.

   * - :samp:`--control=socket`
     - :ref:`Control API <configuration-mgmt>` socket address in IPv4, IPv6,
       or Unix domain format:

       .. code-block:: console

          $ ./configure --control=:nxt_term:`unix:/path/to/control.unit.sock <Note the unix: prefix>`
          $ ./configure --control=127.0.0.1:8080
          $ ./configure --control=[::1]:8080

       .. warning::

          Avoid exposing an unprotected control socket to public networks.  Use
          :ref:`NGINX <nginx-secure-api>` or a different solution such as SSH
          for security and authentication.

       The default is :samp:`unix:control.unit.sock`, created as
       :samp:`root` with :samp:`600` permissions.

   * - :samp:`--incdir=directory`, :samp:`--libdir=directory`
     - Directory paths for :program:`libunit` header files and libraries.

       The defaults are :samp:`include` and :samp:`lib`, respectively.

   * - :samp:`--log=pathname`
     - Pathname for Unit's log.

       The default is :samp:`unit.log`.

   * - :samp:`--modules=directory`
     - Directory path for Unit's language modules.

       The default is :samp:`modules`.

   * - :samp:`--pid=pathname`
     - Pathname for the PID file of Unit's daemon process.

       The default is :samp:`unit.pid`.


   * - :samp:`--state=directory`
     - .. _installation-config-src-state:

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
     - Defines the temporary files location (used to dump large request
       bodies).

       The default value is :samp:`tmp`.


.. _installation-src-dir:

Directory Structure
*******************

To customize Unit installation and runtime directories, you can both:

- Set the :option:`!--prefix` and path options (their relative settings are
  prefix-based) during :ref:`configuration <installation-config-src-prefix>` to
  set up the runtime file structure: Unit uses these settings to locate its
  modules, state, and other files.

- Set the :envvar:`DESTDIR` `variable
  <https://www.gnu.org/prep/standards/html_node/DESTDIR.html>`_ during
  :ref:`installation <installation-bld-src>`.  Unit's file structure is
  placed at the specified directory, which can be either the final installation
  target or an intermediate staging location.

Coordinate these two options as necessary to customize the directory structure.
One common scenario is installation based on absolute paths:

#. Set absolute runtime paths with :option:`!--prefix` and path options:

   .. code-block:: console

      $ ./configure --state=/var/lib/unit --log=/var/log/unit.log \
                    --control=unix:/run/control.unit.sock --prefix=/usr/local/

   Configured thus, Unit will store its state, log, and control socket at
   custom locations; other files will have default prefix-based paths.  Here,
   :file:`unitd` is put to :file:`/usr/local/sbin/`, modules to
   :file:`/usr/local/modules/`.

#. For further packaging or containerization, specify :option:`!DESTDIR` at
   installation to place the files in a staging location while preserving their
   relative structure.  Otherwise, omit :option:`!DESTDIR` for direct
   installation.

An alternative scenario is a build that you can move around the filesystem:

#. Set relative runtime paths with :option:`!--prefix` and path options:

   .. code-block:: console

      $ ./configure --state=config --log=log/unit.log \
                    --control=unix:control/control.unit.sock --prefix=movable

   Configured this way, Unit will store its files by prefix-based paths (both
   default and custom), for example, :file:`<working directory>/movable/sbin/`
   or :file:`<working directory>/movable/config/`.

#. Specify :option:`!DESTDIR` when installing the build.  You can migrate such
   builds if needed; move the entire file structure and launch binaries from
   the *base* directory so that the relative paths stay valid:

   .. code-block:: console

      $ cd <DESTDIR>
      # movable/sbin/unitd <command-line options>

You can combine these approaches, but take care to understand how your settings
work together.


.. _installation-src-modules:

===================
Configuring Modules
===================

Next, configure a module for each language you want to use with Unit.  The
:command:`./configure <language>` commands set up individual language modules
and place module-specific instructions in the :file:`Makefile`.

.. note::

   To run apps in several versions of a language, build and install a module
   for each version.

..
   Legacy anchors are left here so that external links remain valid

.. _installation-go:
.. _installation-java:
.. _installation-nodejs:
.. _installation-perl:
.. _installation-php:
.. _installation-python:
.. _installation-ruby:

.. tabs::
   :prefix: installation-modules
   :toc:

   .. tab:: Go

      When you run :command:`./configure go`, Unit sets up the Go package that
      lets your applications :ref:`run in Unit <configuration-external-go>`.
      To use the package, :ref:`install <installation-bld-src-ext>` it in your
      Go environment.  Available configuration options:

      .. list-table::

         * - :samp:`--go=pathname`
           - Specific Go executable pathname, also used in :ref:`make
             <installation-bld-src-ext>` targets.

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
      in Unit.  Available command options:

      .. list-table::

         * - :samp:`--home=directory`
           - Directory path for Java utilities and header files (required to build
             the module).

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

         * - :samp:`--module=filename`
           - Name of the module to be built (:file:`<module>.unit.so`), also
             used in :ref:`make <installation-bld-src-emb>` targets.

             The default is :samp:`java`.

      To configure a module called :file:`java11.unit.so` with OpenJDK |_|
      11.0.1:

      .. code-block:: console

         $ ./configure java --module=java11 \
                            --home=/Library/Java/JavaVirtualMachines/jdk-11.0.1.jdk/Contents/Home

   .. tab:: Node.js

      When you run :command:`./configure nodejs`, Unit sets up the
      :program:`unit-http` module that lets your applications :ref:`run in Unit
      <configuration-external-nodejs>`.  Available configuration options:

      .. list-table::

         * - :samp:`--local=directory`
           - Local directory path for Node.js module installation.

             By default, the module is installed globally :ref:`(recommended)
             <installation-nodejs-package>`.

         * - :samp:`--node=pathname`
           - Specific Node.js executable pathname, also used in
             :ref:`make <installation-bld-src-ext>` targets.

             The default is :samp:`node`.

         * - :samp:`--npm=pathname`
           - Specific NPM executable pathname.

             The default is :samp:`npm`.

         * - :samp:`--node-gyp=pathname`
           - Specific :program:`node-gyp` executable pathname.

             The default is :samp:`node-gyp`.

   .. tab:: Perl

      When you run :command:`./configure perl`, the script configures a module
      to support running Perl scripts as applications in Unit.  Available
      command options:

      .. list-table::

         * - :samp:`--perl=pathname`
           - Specific Perl executable pathname.

             The default is :samp:`perl`.

         * - :samp:`--module=filename`
           - Name of the module to be built
             (:file:`<module>.unit.so`), also used in :ref:`make
             <installation-bld-src-emb>` targets.

             The default is the filename of the :option:`!--perl` executable.

      To configure a module called :file:`perl-5.20.unit.so` for Perl |_|
      5.20.2:

      .. code-block:: console

         $ ./configure perl --module=perl-5.20 \
                            --perl=perl5.20.2

   .. tab:: PHP

      When you run :command:`./configure php`, the script configures a module
      to support running PHP applications in Unit via PHP's :program:`embed`
      SAPI.  Available command options:

      .. list-table::

         * - :samp:`--config=pathname`
           - Pathname of the :program:`php-config` script invoked to configure the
             PHP module.

             The default is :samp:`php-config`.

         * - :samp:`--lib-path=directory`
           - Directory path of PHP's :program:`embed` SAPI library file
             (:file:`libphp<version>.so` or :file:`.a`).

         * - :samp:`--lib-static`
           - Links the static :program:`embed` SAPI library
             (:file:`libphp<version>.a`) instead of the dynamic one
             (:file:`libphp<version>.so`); requires :option:`!--lib-path`.

         * - :samp:`--module=filename`
           - Name of the module to be built (:file:`<module>.unit.so`), also used
             in :ref:`make <installation-bld-src-emb>` targets.

             The default is :option:`!--config`'s filename minus the `-config`
             suffix; thus, :samp:`/path/php7-config` turns into :samp:`php7`.

      To configure a module called :file:`php70.unit.so` for PHP |_| 7.0:

      .. code-block:: console

         $ ./configure php --module=php70 \
                           --config=/usr/lib64/php7.0/bin/php-config \
                           --lib-path=/usr/lib64/php7.0/lib64

   .. tab:: Python

      When you run :command:`./configure python`, the script configures a
      module to support running Python scripts as applications in Unit.
      Available command options:

      .. list-table::

         * - :samp:`--config=pathname`
           - Pathname of the :program:`python-config` script invoked to configure
             the Python module.

             The default is :samp:`python-config`.

         * - :samp:`--lib-path=directory`
           - Custom directory path of the Python runtime library to use with Unit.

         * - :samp:`--module=filename`
           - Name of the module to be built (:samp:`<module>.unit.so`), also
             used in :ref:`make <installation-bld-src-emb>` targets.

             The default is :option:`!--config`'s filename minus the `-config`
             suffix; thus, :samp:`/path/python3-config` turns into :samp:`python3`.

      To configure a module called :file:`py33.unit.so` for Python |_| 3.3:

      .. code-block:: console

         $ ./configure python --module=py33 \
                              --config=python-config-3.3

   .. tab:: Ruby

      When you run :program:`./configure ruby`, the script configures a module
      to support running Ruby scripts as applications in Unit.  Available
      command options:

      .. list-table::

         * - :samp:`--module=filename`
           - Name of the module to be built (:file:`<module>.unit.so`), also
             used in :ref:`make <installation-bld-src-emb>` targets.

             The default is the filename of the :option:`!--ruby` executable.

         * - :samp:`--ruby=pathname`
           - Specific Ruby executable pathname.

             The default is :samp:`ruby`.

      To configure a module called :file:`ru23.unit.so` for Ruby |_| 2.3:

      .. code-block:: console

         $ ./configure ruby --module=ru23 \
                            --ruby=ruby23


.. _installation-bld-src:

============================
Building and Installing Unit
============================

To build and install Unit executables and language modules that you have
:program:`./configure`'d earlier:

.. code-block:: console

   $ make
   # make install

You can also build and install language modules individually; the specific
method depends on whether the language module is embedded in Unit or packaged
externally.

.. note::

   For further details about Unit language modules, see :doc:`howto/modules`.


.. _installation-bld-src-emb:

Embedded Language Modules
*************************

To build and install Unit modules for Java, PHP, Perl, Python, or Ruby after
configuration, run :command:`make <module>` and :command:`make
<module>-install`, for example:

.. code-block:: console

   $ make :nxt_term:`perl-5.20 <This is the --module option value from ./configure perl>`
   # make :nxt_term:`perl-5.20 <This is the --module option value from ./configure perl>`-install


.. _installation-bld-src-ext:

External Language Modules
*************************

To build and install Unit modules for Go and Node.js globally after
configuration, run :command:`make <go>-install` and :command:`make
<node>-install`, for example:

.. code-block:: console

   # make :nxt_term:`go <This is the --go option value from ./configure go>`-install
   # make :nxt_term:`node <This is the --node option value from ./configure nodejs>`-install

.. note::

   To install the Node.js module locally, run :command:`make
   <node>-local-install`:

   .. code-block:: console

      # make :nxt_term:`node <This is the --node option value from ./configure nodejs>`-local-install

   If you haven't specified the :option:`!--local` :ref:`directory
   <installation-modules-nodejs>` with :program:`./configure nodejs`
   earlier, provide it here: :command:`DESTDIR=/your/project/directory`.  If
   both options are specified, :option:`!DESTDIR` prefixes the
   :option:`!--local` value.

   However, mind that global installation is the recommended method for the
   Node.js module.

If you customize the executable pathname with :option:`!--go` or
:option:`!--node`, use the following pattern:

.. code-block:: console

   $ ./configure nodejs --node=/usr/local/bin/node8.12
   # make /usr/local/bin/node8.12-install

   $ ./configure go --go=/usr/local/bin/go1.7
   # make /usr/local/bin/go1.7-install


.. _installation-src-startup:

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
configured :ref:`absolute paths <installation-src-dir>`:

.. code-block:: console

   # :nxt_term:`unitd <Your PATH environment variable should list a path to unitd>`

Otherwise, start :program:`unitd` from the :samp:`sbin` subdirectory relative
to installation directory :ref:`prefix <installation-config-src-prefix>`:

.. code-block:: console

   # cd :nxt_term:`/path/to/unit/ <Destination prefix>`
   # :nxt_term:`sbin/unitd <This preserves relative paths>`

Run :command:`unitd -h` or :command:`unitd --version` to list Unit's
compile-time settings.  Usually, the defaults don't require overrides; however,
the following runtime options are available.  For details and security notes,
see :ref:`here <installation-config-src>`.

General runtime options and :ref:`compile-time setting <installation-config-src>`
overrides:

.. list-table::

   * - :samp:`--help`, :samp:`-h`
     - Displays a summary of Unit's command-line options and their compile-time
       defaults.

   * - :samp:`--no-daemon`
     - Runs Unit in non-daemon mode.

   * - :samp:`--version`
     - Displays Unit's version and the :program:`./configure` settings it was
       built with.

   * - :samp:`--control socket`
     - Control API socket address in IPv4, IPv6, or Unix (with :samp:`unix:`
       prefix) domain format:

       .. code-block:: console

          # unitd --control unix:/path/to/control.unit.sock
          # unitd --control 127.0.0.1:8080
          # unitd --control [::1]:8080

   * - :samp:`--group name`, :samp:`--user name`
     - Group name and user name used to run Unit's non-privileged processes.

   * - :samp:`--log pathname`
     - Pathname for the Unit log.

   * - :samp:`--modules directory`
     - Directory path for Unit language modules
       (:file:`<module>.unit.so` files).

   * - :samp:`--pid pathname`
     - Pathname for the PID file of Unit's :program:`main` process.

   * - :samp:`--state directory`
     - Directory path for Unit state storage.

Finally, to stop a running Unit:

.. code-block:: console

   # pkill unitd

This command signals all Unit processes to terminate in a graceful manner.
