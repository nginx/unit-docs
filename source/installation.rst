.. meta::
   :og:description: Download official packages, use third-party repositories, or configure a custom build from source.

.. include:: include/replace.rst

############
Installation
############

.. _installation-prereqs:

*************
Prerequisites
*************

NGINX Unit compiles and runs on various Unix-like operating systems, including:

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
- PHP |_| 5, 7
- Perl |_| 5.12 or later
- Python |_| 2.6, 2.7, 3
- Ruby |_| 2.0 or later

.. _installation-docker:

*************
Docker Images
*************

To install and run Unit from NGINX's Docker `image repository <https://hub.
docker.com/r/nginx/unit/>`_:

.. code-block:: console

   $ docker pull nginx/unit
   $ docker run -d nginx/unit

Default image tag is :samp:`:latest`; it resolves into a :samp:`-full`
configuration of the latest Unit version.  Other tags:

.. list-table::
    :header-rows: 1

    * - Tag
      - Description

    * - :samp:`|version|-full`
      - Modules for all supported languages.

    * - :samp:`|version|-minimal`
      - No language modules.

    * - :samp:`|version|-<language>`
      - A specific language module, for example :samp:`|version|-ruby2.3` or
        :samp:`|version|-python2.7`.

We also publish these images as tarballs on our `website
<https://packages.nginx.org/unit/docker/>`_:

.. subs-code-block:: console

   $ curl -O https://packages.nginx.org/unit/docker/|version|/nginx-unit-|version|-full.tar.gz
   $ curl -O https://packages.nginx.org/unit/docker/|version|/nginx-unit-|version|-full.tar.gz.sha512
   $ sha512sum -c nginx-unit-|version|-full.tar.gz.sha512
         nginx-unit-|version|-full.tar.gz: OK
   $ docker load < nginx-unit-|version|-full.tar.gz

.. include:: include/socket-log-deb.rst

For further details, see the `repository page <https://hub.docker.com/r/
nginx/unit/>`_ and the official :doc:`Howto <howto/docker>`.

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

.. code-block:: console

   $ docker run -d --mount \
            type=bind,src=/path/to/config/files/,dst=/docker-entrypoint.d/ \
            nginx/unit:latest)


.. _installation-precomp-pkgs:

*****************
Official Packages
*****************

Installing a precompiled Unit binary package is best for most occasions;
`official <https://packages.nginx.org/unit/>`_ binaries are available for:

- Amazon |_| Linux, Amazon |_| Linux |_| 2
- CentOS |_| 6, 7, 8
- Debian |_| 8, 9, 10
- Fedora |_| 28, 29, 30, 31, 32
- RHEL |_| 6, 7, 8
- Ubuntu |_| 16.04, 18.04, 18.10, 19.04, 19.10, 20.04

These include core Unit executables, developer files, and support packages for
individual languages.

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

      #. Install Unit base package and other packages you would like to
         use:

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

      #. Install Unit base package and other packages you would like to use:

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

      #. Install Unit base package and other packages you would like to use:

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
            baseurl=https://packages.nginx.org/unit/centos/$releasever/$basearch/
            gpgcheck=0
            enabled=1

      #. Install Unit base package and other packages you would like to use:

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

      #. Install Unit base package and other packages you would like to use:

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

      #. Install Unit base package and other packages you would like to use:

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

      #. Install Unit base package and other packages you would like to use:

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

   .. tab:: 32

      #. To configure Unit repository, create the following file named
         :file:`/etc/yum.repos.d/unit.repo`:

         .. code-block:: ini

            [unit]
            name=unit repo
            baseurl=https://packages.nginx.org/unit/fedora/$releasever/$basearch/
            gpgcheck=0
            enabled=1

      #. Install Unit base package and other packages you would like to use:

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

      #. Install Unit base package and other packages you would like to use:

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

      #. Install Unit base package and other packages you would like to use:

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

      #. Install Unit base package and other packages you would like to use:

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

      #. Install Unit base package and other packages you would like to use:

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

      #. Install Unit base package and additional packages you would like to
         use:

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

      #. Install Unit base package and other packages you would like to use:

         .. code-block:: console

            # apt update
            # apt install unit
            # apt install :nxt_term:`unit-dev <Required to install the Node.js module and build Go apps>` unit-go unit-jsc11 unit-perl \
                  unit-php unit-python2.7 unit-python3.8 unit-ruby

   .. tab:: 19.10

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

      #. Install Unit base package and other packages you would like to use:

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

      #. Install Unit base package and other packages you would like to use:

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

      #. Install Unit base package and other packages you would like to use:

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

      #. Install Unit base package and other packages you would like to use:

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

      #. Install Unit base package and other packages you would like to use:

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

   | The control socket's pathname is
     :file:`/usr/local/var/run/unit/control.sock`.

   | The :ref:`log <troubleshooting-log>` is
     :file:`/usr/local/var/log/unit/unit.log`.


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

==============
Node.js at npm
==============

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

   You can also :ref:`configure <installation-nodejs>` and :ref:`install
   <installation-bld-src-ext>` the :program:`unit-http` module from sources.


.. _installation-precomp-startup:

====================
Startup and Shutdown
====================

Run :command:`unitd -h` or :command:`unitd --version` to verify Unit is
available or list its settings.  To manage the installation:

.. tabs::
   :prefix: startup-shutdown

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


.. _installation-community-repos:

**********************
Community Repositories
**********************

.. warning::

   These distributions are maintained by respective communities, not NGINX.
   Proceed with caution.

.. _installation-alpine-apk:

============
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

   The control socket's pathname is :file:`/run/control.unit.sock`.


.. _installation-archlinux-aur:

==========
Arch Linux
==========

To install Unit using the `Arch User Repository (AUR)
<https://aur.archlinux.org/pkgbase/nginx-unit/>`_:

.. code-block:: console

   # pacman -S git
   $ git clone https://aur.archlinux.org/nginx-unit.git
   $ cd nginx-unit

.. warning::

   Verify that the :file:`PKGBUILD` and accompanying files aren't malicious or
   untrustworthy.  AUR packages are entirely user produced without
   pre-moderation; use them at your own risk.

.. code-block:: console

   $ makepkg -si

.. note::

   The control socket's pathname is :file:`/run/nginx-unit.control.sock`.


.. _installation-scls:

================
CentOS/RHEL SCLs
================

If you use `SCLo Software Collections
<https://wiki.centos.org/SpecialInterestGroup/SCLo>`_ in your environment, you
can install Unit's PHP modules as packages from the corresponding repo.
Besides other dependencies, the packages require :ref:`core Unit installation
<installation-precomp-pkgs>`.

CentOS:

.. code-block:: console

   # yum install centos-release-scl
   # yum install --enablerepo=centos-sclo-sclo-testing \
         sclo-php70-unit-php sclo-php71-unit-php sclo-php72-unit-php

RHEL:

.. code-block:: console

   # cd /etc/yum.repos.d/
   # curl -O https://copr.fedorainfracloud.org/coprs/rhscl/centos-release-scl/repo/epel-7/rhscl-centos-release-scl-epel-7.repo
   # yum install centos-release-scl
   # yum install --enablerepo=centos-sclo-sclo-testing \
         sclo-php70-unit-php sclo-php71-unit-php sclo-php72-unit-php


.. _installation-freebsd-pkgs-prts:

=======
FreeBSD
=======

.. _installation-freebsd-pkgs:

To install Unit using `FreeBSD packages <https://www.
freebsd.org/doc/en_US.ISO8859-1/books/handbook/pkgng-intro.html>`_, update the
repository and install the `package <https://www.freshports.org/www/unit>`__:

.. code-block:: console

   # pkg install -y unit

.. note::

   The control socket's pathname is :file:`/var/run/unit/control.unit.sock`.

.. _installation-freebsd-prts:

To install Unit using `FreeBSD ports <https://www.
freebsd.org/doc/en_US.ISO8859-1/books/handbook/ports-using.html>`_, update your
port collection.

For :program:`portsnap`:

.. code-block:: console

   # portsnap fetch update

For :program:`svn`:

.. code-block:: console

   # svn update /usr/ports

Next, browse to the port path to build and install the port:

.. code-block:: console

   # cd /usr/ports/www/unit
   # make
   # make install

.. warning::

   These commands compile and install the *port*.  To :program:`make` a Unit
   build with our sources only, see :ref:`below <installation-bld-src>`.

.. note::

   The control socket's pathname is :file:`/var/run/unit/control.unit.sock`.


.. _installation-gnt-prtg:

======
Gentoo
======

To install Unit using `Portage <https://wiki.gentoo.org/wiki/
Handbook:X86/Full/Portage>`_, update the repository and install the `package
<https://packages.gentoo.org/packages/www-servers/nginx-unit>`__:

.. code-block:: console

   # emerge --sync
   # emerge www-servers/nginx-unit

.. note::

   The control socket's pathname is :file:`/run/nginx-unit.sock`.


.. installation-nix:

=========
NixOS/Nix
=========

To install Unit using the `Nix package manager <https://nixos.org/nix/>`_,
update the repository and install the `package
<https://github.com/NixOS/nixpkgs/blob/master/pkgs/servers/http/unit/>`__:

.. code-block:: console

   $ nix-channel --update
   $ nix-env -qa 'unit'    # check availability and version
   $ nix-env -i unit       # install Unit

.. note::

   The control socket's pathname is :file:`/run/unit/control.unit.sock`.


.. _installation-remirepo:

===============
Remi's RPM Repo
===============

`Remi's RPM repository
<https://blog.remirepo.net/post/2019/01/14/PHP-with-the-NGINX-unit-application-server>`_,
which hosts the latest versions of the PHP stack for CentOS, Fedora, and RHEL,
also has the base Unit package and the PHP modules.

To use Remi's versions of Unit packages, configure `Remi's RPM repo
<https://blog.remirepo.net/pages/Config-en>`_ first.  Remi's PHP language
modules are also compatible with the base Unit package from :ref:`our own
repository <installation-precomp-pkgs>`.

Next, install Unit and the PHP modules you want:

.. code-block:: console

   # yum install --enablerepo=remi unit php54-unit-php php55-unit-php \
         php56-unit-php php70-unit-php php71-unit-php php72-unit-php php73-unit-php

.. note::

   The control socket's pathname is :file:`/var/run/unit/control.sock`.


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
Ruby) and the other features you want Unit to support.

The commands below assume you are configuring Unit with all supported
languages and features; otherwise, skip the packages you aren’t going to use.

.. tabs::
   :prefix: prereq

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

   .. tab:: Amazon Linux, CentOS, Fedora, RHEL

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

   .. tab:: Solaris

      .. code-block:: console

         # pkg install gcc
         # pkg install golang
         # pkg install :nxt_term:`php-71 <PHP versions 5 and 7 are supported>`
         # pkg install ruby
         # pkg install :nxt_term:`jdk-8 <Java 8 or later is supported. Different JDKs may be used>`
         # pkg install openssl

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

General :program:`./configure` options:

--help
    Displays a summary of common :program:`./configure` options.

    For language-specific details, run :command:`./configure <language>
    --help` or see :ref:`below <installation-src-modules>`.

These options control the compilation process:

--cc=pathname
    Custom C compiler pathname.

    The default is :samp:`cc`.

--cc-opt=options, --ld-opt=options
    Extra options for the C compiler and linker.

The following option pair controls Unit's runtime privileges:

--group=name, --user=name
    Group name and username to run Unit's non-privileged processes.

    The defaults are :option:`!--user`'s primary group and
    :samp:`nobody`, respectively.

These flags enable or disable support of certain features:

--debug
    Turns on the :ref:`debug log <troubleshooting-dbg-log>`.

--no-ipv6
    Turns off IPv6 support.

--no-unix-sockets
    Turns off Unix domain sockets support.

--openssl
    Turns on OpenSSL support.  Make sure that OpenSSL (1.0.1 and later) header
    files and libraries are available in your compiler's search path.

    To customize the path, provide the :option:`!--cc-opt` and
    :option:`!--ld-opt` options; you can also set the :envvar:`CFLAGS` and
    :envvar:`LDFLAGS` environment variables before running
    :program:`./configure`.

    For details, see :ref:`configuration-ssl`.

The last option group customizes Unit's :ref:`runtime directory
structure <installation-src-dir>`:

.. _installation-config-src-prefix:

--prefix=prefix

    Destination directory prefix for :ref:`path options
    <installation-src-dir>`: :option:`!--bindir`, :option:`!--sbindir`,
    :option:`!--libdir`, :option:`!--incdir`, :option:`!--modules`,
    :option:`!--state`, :option:`!--pid`, :option:`!--log`, and
    :option:`!--control`.

--bindir=directory, --sbindir=directory
    Directory paths for end-user and sysadmin executables.

    The defaults are :samp:`bin` and :samp:`sbin`, respectively.

--control=socket
    Control API socket address in IPv4, IPv6, or Unix (with :samp:`unix:`
    prefix) domain format:

    .. code-block:: console

       $ ./configure --control=unix:/path/to/control.unit.sock
       $ ./configure --control=127.0.0.1:8080
       $ ./configure --control=[::1]:8080

    .. warning::

       Avoid exposing an unprotected control socket to public networks.  Use
       :ref:`NGINX <nginx-secure-api>` or a different solution such as SSH for
       security and authentication.

    The default is :samp:`unix:control.unit.sock`, created as
    :samp:`root` with :samp:`600` permissions.

--incdir=directory, --libdir=directory
    Directory paths for :program:`libunit` header files and libraries.

    The defaults are :samp:`include` and :samp:`lib`, respectively.

--log=pathname
    Pathname for Unit's log.

    The default is :samp:`unit.log`.

--modules=directory
    Directory path for Unit's language modules.

    The default is :samp:`modules`.

--pid=pathname
    Pathname for the PID file of Unit's daemon process.

    The default is :samp:`unit.pid`.

.. _installation-config-src-state:

--state=directory
    Directory path for Unit's state storage.  It contains runtime
    configuration, certificates, and other records; if you migrate your
    installation, copy the entire directory.

    .. warning::

       Unit state includes sensitive data and must be owned by :samp:`root`
       with :samp:`700` permissions.  Avoid updating the directory by outside
       means; instead, use Unit's config API to ensure data consistency.

    The default is :samp:`state`.


--tmp=directory

    Defines the temporary files location (used to dump large request bodies).

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


.. _installation-go:

Go
**

When you run :command:`./configure go`, Unit sets up the Go package that lets
your applications :ref:`run in Unit <configuration-external-go>`.  To use the
package, :ref:`install <installation-bld-src-ext>` it in your Go environment.
Available configuration options:

--go=pathname
    Specific Go executable pathname, also used for :ref:`make
    <installation-bld-src-ext>` targets.

    The default is :samp:`go`.

--go-path=directory
    Custom directory path for Go package installation.

    The default is :samp:`$GOPATH`.

.. note::

   The :program:`./configure` script doesn't alter the :envvar:`GOPATH`
   `environment variable <https://github.com/golang/go/wiki/GOPATH>`_. The
   two paths (configuration-time :option:`!--go-path` and compile-time
   :envvar:`GOPATH`) must be coherent at build time for Go to locate the Unit
   package.


.. _installation-java:

Java
****

When you run :command:`./configure java`, the script configures a module to
support running `Java Web Applications
<https://download.oracle.com/otndocs/jcp/servlet-3_1-fr-spec/index.html>`_ in
Unit.  Available command options:

--home=directory
    Directory path for Java utilities and header files (required to build the
    module).

    The default is the :samp:`java.home` setting.

--jars=directory
    Directory path for Unit's custom :file:`.jar` files.

    The default is the Java module path.

--lib-path=directory
    Directory path for the :file:`libjvm.so` library.

    The default is based on JDK settings.

--local-repo=directory
    Directory path for local :file:`.jar` repository.

    The default is :samp:`$HOME/.m2/repository/`.

--repo=directory
    URL path for remote Maven repository.

    The default is :samp:`http://central.maven.org/maven2/`.

--module=filename
    Name of the Java module to be built (:file:`<module>.unit.so`), also
    used for :ref:`make <installation-bld-src-emb>` targets.

    The default is :samp:`java`.

To configure a module called :file:`java11.unit.so` with OpenJDK |_| 11.0.1:

.. code-block:: console

   $ ./configure java --module=java11 \
                      --home=/Library/Java/JavaVirtualMachines/jdk-11.0.1.jdk/Contents/Home


.. _installation-nodejs:

Node.js
*******

When you run :command:`./configure nodejs`, Unit sets up the
:program:`unit-http` module that lets your applications :ref:`run in Unit
<configuration-external-nodejs>`.  Available configuration options:

--local=directory
    Local directory path for Node.js module installation.

    By default, the module is installed globally :ref:`(recommended)
    <installation-nodejs-package>`.

--node=pathname
    Specific Node.js executable pathname, also used for
    :ref:`make <installation-bld-src-ext>` targets.

    The default is :samp:`node`.

--npm=pathname
    Specific NPM executable pathname.

    The default is :samp:`npm`.

--node-gyp=pathname
    Specific :program:`node-gyp` executable pathname.

    The default is :samp:`node-gyp`.


.. _installation-perl:

Perl
****

When you run :command:`./configure perl`, the script configures a module to
support running Perl scripts as applications in Unit.  Available command
options:

--perl=pathname
        Specific Perl executable pathname.

        The default is :samp:`perl`.

--module=filename
        Name of the Perl module to be built
        (:file:`<module>.unit.so`), also used for :ref:`make
        <installation-bld-src-emb>` targets.

        The default is the filename of the :option:`!--perl` executable.

To configure a module called :file:`perl-5.20.unit.so` for Perl |_| 5.20.2:

.. code-block:: console

   $ ./configure perl --module=perl-5.20 \
                      --perl=perl5.20.2


.. _installation-php:

PHP
***

When you run :command:`./configure php`, the script configures a module to
support running PHP applications in Unit via PHP's :program:`embed` SAPI.
Available command options:

--config=pathname
    Pathname of the :program:`php-config` script invoked to configure the PHP
    module.

    The default is :samp:`php-config`.

--lib-path=directory
    Directory path of PHP's :program:`embed` SAPI library file
    (:file:`libphp<version>.so` or :file:`.a`).

--lib-static
    Links the static :program:`embed` SAPI library (:file:`libphp<version>.a`)
    instead of the dynamic one (:file:`libphp<version>.so`); requires
    :option:`!--lib-path`.

--module=filename
    Name of the PHP module to be built (:file:`<module>.unit.so`), also used
    for :ref:`make <installation-bld-src-emb>` targets.

    The default is :option:`!--config`'s filename minus the
    `-config` suffix (:samp:`/path/php7-config` to :samp:`php7`).

To configure a module called :file:`php70.unit.so` for PHP |_| 7.0:

.. code-block:: console

   $ ./configure php --module=php70 \
                     --config=/usr/lib64/php7.0/bin/php-config \
                     --lib-path=/usr/lib64/php7.0/lib64


.. _installation-python:

Python
******

When you run :command:`./configure python`, the script configures a module to
support running Python scripts as applications in Unit.  Available command
options:

--config=pathname
    Pathname of the :program:`python-config` script invoked to configure
    the Python module.

    The default is :samp:`python-config`.

--lib-path=directory
    Custom directory path of the Python runtime library to use with Unit.

--module=filename
    Name of the Python module to be built (:samp:`<module>.unit.so`), also used
    for :ref:`make <installation-bld-src-emb>` targets.

    The default is :option:`!--config`'s filename minus the `-config` suffix
    (:samp:`/path/python3-config` to :samp:`python3`).

To configure a module called :file:`py33.unit.so` for Python |_| 3.3:

.. code-block:: console

   $ ./configure python --module=py33 \
                        --config=python-config-3.3


.. _installation-ruby:

Ruby
****

When you run :program:`./configure ruby`, the script configures a module to
support running Ruby scripts as applications in Unit.  Available command
options:

--module=filename
    Name of the Ruby module to be built (:file:`<module>.unit.so`), also used
    for :ref:`make <installation-bld-src-emb>` targets.

    The default is the filename of the :option:`!--ruby` executable.

--ruby=pathname
    Specific Ruby executable pathname.

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
   <installation-nodejs>` with :program:`./configure nodejs` earlier, provide
   it here: :command:`DESTDIR=/your/project/directory`.  If both options are
   specified, :option:`!DESTDIR` prefixes the :option:`!--local` value.

   However, mind that global installation is the recommended method for the
   Node.js module.

If you customize the executable pathname with :option:`!--go` or
:option:`!--node`, use the following pattern:

.. code-block:: console

   $ ./configure nodejs --node=/usr/local/bin/node8.12
   # make /usr/local/bin/node8.12-install

   $ ./configure go --go=/usr/local/bin/go1.7
   # make /usr/local/bin/go1.7-install


.. _installation-startup:

=======
Startup
=======
We advise installing Unit from :ref:`precompiled packages
<installation-precomp-pkgs>`; in this case, startup is :ref:`configured
<installation-precomp-startup>` automatically.

Even if you install Unit otherwise, manual startup isn't recommended.  Instead,
configure a service manager such as :program:`OpenRC` or :program:`systemd` or
create an :program:`rc.d` script to launch the Unit daemon using the options
below.

Run :program:`unitd` as :samp:`root` from the :samp:`sbin` installation
subdirectory.  Usually, the default compile-time settings don't require
overrides; use the :option:`!--help` option to review their values.  For
details and security notes, see :ref:`here <installation-config-src>`.

General options:

--help, -h
    Displays a summary of Unit's command-line options and their
    default values set at compile time.

--no-daemon
    Runs Unit in non-daemon mode.

--version
    Displays Unit's version and the :program:`./configure` settings it was
    built with.

The following options override :ref:`compile-time settings
<installation-config-src>`:

--control socket
    Control API socket address in IPv4, IPv6, or Unix (with :samp:`unix:`
    prefix) domain format:

    .. code-block:: console

       # unitd --control unix:/path/to/control.unit.sock
       # unitd --control 127.0.0.1:8080
       # unitd --control [::1]:8080

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
