.. meta::
   :og:description: Download official packages, use third-party repositories,
                    or configure a custom build from source.

.. include:: include/replace.rst

############
Installation
############

You can install NGINX Unit in four alternative ways:

- Choose from our official :ref:`binary packages <installation-precomp-pkgs>`
  for a few popular systems.  They're as easy to use as any other packaged
  software and suit most purposes straight out of the box.

- If your preferred OS or language version is missing from the official package
  list, try :ref:`third-party repositories <installation-community-repos>`.  Be
  warned, though: we don't maintain them.

- Run our official :ref:`Docker images <installation-docker>`, prepackaged with
  varied language combinations.

- To fine-tune Unit to your goals, download the :ref:`sources
  <source>`, install the :ref:`toolchain
  <source-prereq-build>`, and :ref:`build <source-config-src>` a
  custom binary from scratch; just make sure you know what you're doing.


.. _source-prereqs:

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

Optional dependencies:

- OpenSSL 1.0.1 or later for :ref:`TLS <configuration-ssl>` support

- PCRE (8.0 or later) or PCRE2 (10.23 or later) for
  :ref:`regular expression matching <configuration-routes-matching-patterns>`


.. _installation-precomp-pkgs:

*****************
Official Packages
*****************

Installing an official precompiled Unit binary package is best on most
occasions; they're available for:

- Amazon |_| Linux :ref:`AMI <installation-amazon-ami>`, Amazon |_| Linux |_|
  :ref:`2 <installation-amazon-20lts>`

- CentOS |_| :ref:`6 <installation-centos-6x>`, :ref:`7
  <installation-centos-8x7x>`, :ref:`8 <installation-centos-8x7x>`

- Debian |_| :ref:`9 <installation-debian-9>`, :ref:`10
  <installation-debian-10>`

- Fedora |_| :ref:`29 <installation-fedora-29>`, :ref:`30
  <installation-fedora-3130>`, :ref:`31 <installation-fedora-3130>`, :ref:`32
  <installation-fedora-32>`, :ref:`33 <installation-fedora-3433>`, :ref:`34
  <installation-fedora-3433>`, :ref:`35 <installation-fedora-35>`


- RHEL |_| :ref:`6 <installation-rhel-6x>`, :ref:`7 <installation-rhel-8x7x>`,
  :ref:`8 <installation-rhel-8x7x>`

- Ubuntu |_| :ref:`16.04 <installation-ubuntu-1604>`, :ref:`18.04
  <installation-ubuntu-1804>`, :ref:`19.10 <installation-ubuntu-1910>`,
  :ref:`20.04 <installation-ubuntu-2004>`, :ref:`20.10
  <installation-ubuntu-2010>`, :ref:`21.04 <installation-ubuntu-2104>`,
  :ref:`21.10 <installation-ubuntu-2110>`

The packages include core executables, developer files, and support for
individual languages.  We also maintain a Homebrew `tap <#homebrew>`__ for
macOS users and a :ref:`module <installation-nodejs-package>` for Node.js at
the `npm <https://www.npmjs.com/package/unit-http>`_ registry.

.. note::

   For details of packaging custom modules that install alongside the official
   Unit, see :ref:`here <modules-pkg>`.


.. _installation-precomp-amazon:

============
Amazon Linux
============

.. tabs::
   :prefix: amazon

   .. tab:: 2.0 LTS

      Supported architecture: x86-64.

      #. To configure Unit's repository, create the following file named
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
            # yum install :nxt_hint:`unit-devel <Required to install the Node.js module and build Go apps>` unit-go unit-jsc8 unit-perl  \
                  unit-php unit-python27 unit-python37
            # systemctl restart unit  # Necessary for Unit to pick up any changes in language module setup

      Runtime details:

      .. list-table::

         * - Control :ref:`socket <security-socket-state>`
           - :file:`/var/run/unit/control.sock`

         * - Log :ref:`file <troubleshooting-log>`
           - :file:`/var/log/unit/unit.log`

         * - Non-privileged :ref:`user and group <security-apps>`
           - :samp:`unit`


   .. tab:: AMI

      .. warning::

         Unit's 1.22+ packages aren't built for Amazon Linux AMI.  This
         distribution is obsolete; please update.

      Supported architecture: x86-64.

      #. To configure Unit's repository, create the following file named
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
            # yum install :nxt_hint:`unit-devel <Required to install the Node.js module and build Go apps>` unit-go unit-jsc8 unit-perl unit-php  \
                  unit-python27 unit-python34 unit-python35 unit-python36
            # systemctl restart unit  # Necessary for Unit to pick up any changes in language module setup

      Runtime details:

      .. list-table::

         * - Control :ref:`socket <security-socket-state>`
           - :file:`/var/run/unit/control.sock`

         * - Log :ref:`file <troubleshooting-log>`
           - :file:`/var/log/unit/unit.log`

         * - Non-privileged :ref:`user and group <security-apps>`
           - :samp:`unit`


.. _installation-precomp-centos:

======
CentOS
======

.. tabs::
   :prefix: centos

   .. tab:: 8.x, 7.x

      Supported architecture: x86-64.

      #. To configure Unit's repository, create the following file named
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
            # yum install :nxt_hint:`unit-devel <Required to install the Node.js module and build Go apps>` unit-go unit-jsc8 unit-jsc11  \
                  unit-perl unit-php unit-python27 unit-python36
            # systemctl restart unit  # Necessary for Unit to pick up any changes in language module setup


      Runtime details:

      .. list-table::

         * - Control :ref:`socket <security-socket-state>`
           - :file:`/var/run/unit/control.sock`

         * - Log :ref:`file <troubleshooting-log>`
           - :file:`/var/log/unit/unit.log`

         * - Non-privileged :ref:`user and group <security-apps>`
           - :samp:`unit`


   .. tab:: 6.x

      .. warning::

         Unit's 1.20+ packages aren't built for CentOS 6.  This distribution is
         obsolete; please update.

      Supported architectures: i386, x86-64.

      #. To configure Unit's repository, create the following file named
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
            # yum install :nxt_hint:`unit-devel <Required to install the Node.js module and build Go apps>` unit-go unit-jsc8 unit-php unit-python
            # systemctl restart unit  # Necessary for Unit to pick up any changes in language module setup

      Runtime details:

      .. list-table::

         * - Control :ref:`socket <security-socket-state>`
           - :file:`/var/run/unit/control.sock`

         * - Log :ref:`file <troubleshooting-log>`
           - :file:`/var/log/unit/unit.log`

         * - Non-privileged :ref:`user and group <security-apps>`
           - :samp:`unit`


.. _installation-precomp-deb:

======
Debian
======

.. tabs::
   :prefix: debian

   .. tab:: 11

      Supported architectures: i386, x86-64.

      #. Download and save NGINX's signing key:

         .. code-block:: console

            # curl --output /usr/share/keyrings/nginx-keyring.gpg  \
                  https://unit.nginx.org/keys/nginx-keyring.gpg

         This eliminates the ``packages cannot be authenticated`` warnings
         during installation.

      #. To configure Unit's repository, create the following file named
         :file:`/etc/apt/sources.list.d/unit.list`:

         .. code-block:: none

            deb [signed-by=/usr/share/keyrings/nginx-keyring.gpg] https://packages.nginx.org/unit/debian/ bullseye unit
            deb-src [signed-by=/usr/share/keyrings/nginx-keyring.gpg] https://packages.nginx.org/unit/debian/ bullseye unit

      #. Install the core package and other packages you need:

         .. code-block:: console

            # apt update
            # apt install unit
            # apt install :nxt_hint:`unit-dev <Required to install the Node.js module and build Go apps>` unit-go unit-jsc11 unit-perl  \
                  unit-php unit-python2.7 unit-python3.9 unit-ruby
            # systemctl restart unit  # Necessary for Unit to pick up any changes in language module setup


      Runtime details:

      .. list-table::

         * - Control :ref:`socket <security-socket-state>`
           - :file:`/var/run/control.unit.sock`

         * - Log :ref:`file <troubleshooting-log>`
           - :file:`/var/log/unit.log`

         * - Non-privileged :ref:`user and group <security-apps>`
           - :samp:`unit`


   .. tab:: 10

      Supported architectures: i386, x86-64.

      #. Download and save NGINX's signing key:

         .. code-block:: console

            # curl --output /usr/share/keyrings/nginx-keyring.gpg  \
                  https://unit.nginx.org/keys/nginx-keyring.gpg

         This eliminates the ``packages cannot be authenticated`` warnings
         during installation.

      #. To configure Unit's repository, create the following file named
         :file:`/etc/apt/sources.list.d/unit.list`:

         .. code-block:: none

            deb [signed-by=/usr/share/keyrings/nginx-keyring.gpg] https://packages.nginx.org/unit/debian/ buster unit
            deb-src [signed-by=/usr/share/keyrings/nginx-keyring.gpg] https://packages.nginx.org/unit/debian/ buster unit

      #. Install the core package and other packages you need:

         .. code-block:: console

            # apt update
            # apt install unit
            # apt install :nxt_hint:`unit-dev <Required to install the Node.js module and build Go apps>` unit-go unit-jsc11 unit-perl  \
                  unit-php unit-python2.7 unit-python3.7 unit-ruby
            # systemctl restart unit  # Necessary for Unit to pick up any changes in language module setup

      Runtime details:

      .. list-table::

         * - Control :ref:`socket <security-socket-state>`
           - :file:`/var/run/control.unit.sock`

         * - Log :ref:`file <troubleshooting-log>`
           - :file:`/var/log/unit.log`

         * - Non-privileged :ref:`user and group <security-apps>`
           - :samp:`unit`


   .. tab:: 9

      .. warning::

         Unit's 1.22+ packages aren't built for Debian 9.

      Supported architectures: i386, x86-64.

      #. Download and save NGINX's signing key:

         .. code-block:: console

            # curl --output /usr/share/keyrings/nginx-keyring.gpg  \
                  https://unit.nginx.org/keys/nginx-keyring.gpg

         This eliminates the ``packages cannot be authenticated`` warnings
         during installation.

      #. To configure Unit's repository, create the following file named
         :file:`/etc/apt/sources.list.d/unit.list`:

         .. code-block:: none

            deb [signed-by=/usr/share/keyrings/nginx-keyring.gpg] https://packages.nginx.org/unit/debian/ stretch unit
            deb-src [signed-by=/usr/share/keyrings/nginx-keyring.gpg] https://packages.nginx.org/unit/debian/ stretch unit

      #. Install the core package and other packages you need:

         .. code-block:: console

            # apt update
            # apt install unit
            # apt install :nxt_hint:`unit-dev <Required to install the Node.js module and build Go apps>` unit-go unit-jsc8 unit-perl  \
                  unit-php unit-python2.7 unit-python3.5 unit-ruby
            # systemctl restart unit  # Necessary for Unit to pick up any changes in language module setup

      Runtime details:

      .. list-table::

         * - Control :ref:`socket <security-socket-state>`
           - :file:`/var/run/control.unit.sock`

         * - Log :ref:`file <troubleshooting-log>`
           - :file:`/var/log/unit.log`

         * - Non-privileged :ref:`user and group <security-apps>`
           - :samp:`unit`


.. _installation-precomp-fedora:

======
Fedora
======

.. tabs::
   :prefix: fedora

   .. tab:: 35

      Supported architecture: x86-64.

      #. To configure Unit's repository, create the following file named
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
            # yum install :nxt_hint:`unit-devel <Required to install the Node.js module and build Go apps>` unit-go unit-jsc11 unit-jsc8 unit-perl  \
                  unit-php unit-python39 unit-python310 unit-ruby
            # systemctl restart unit  # Necessary for Unit to pick up any changes in language module setup


      Runtime details:

      .. list-table::

         * - Control :ref:`socket <security-socket-state>`
           - :file:`/var/run/unit/control.sock`

         * - Log :ref:`file <troubleshooting-log>`
           - :file:`/var/log/unit/unit.log`

         * - Non-privileged :ref:`user and group <security-apps>`
           - :samp:`unit`


   .. tab:: 34, 33

      Supported architecture: x86-64.

      #. To configure Unit's repository, create the following file named
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
            # yum install :nxt_hint:`unit-devel <Required to install the Node.js module and build Go apps>` unit-go unit-jsc11 unit-jsc8 unit-perl  \
                  unit-php unit-python39 unit-ruby
            # systemctl restart unit  # Necessary for Unit to pick up any changes in language module setup


      Runtime details:

      .. list-table::

         * - Control :ref:`socket <security-socket-state>`
           - :file:`/var/run/unit/control.sock`

         * - Log :ref:`file <troubleshooting-log>`
           - :file:`/var/log/unit/unit.log`

         * - Non-privileged :ref:`user and group <security-apps>`
           - :samp:`unit`


   .. tab:: 32

      Supported architecture: x86-64.

      #. To configure Unit's repository, create the following file named
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
            # yum install :nxt_hint:`unit-devel <Required to install the Node.js module and build Go apps>` unit-go unit-jsc11 unit-jsc8 unit-perl  \
                  unit-php unit-python38 unit-ruby
            # systemctl restart unit  # Necessary for Unit to pick up any changes in language module setup


      Runtime details:

      .. list-table::

         * - Control :ref:`socket <security-socket-state>`
           - :file:`/var/run/unit/control.sock`

         * - Log :ref:`file <troubleshooting-log>`
           - :file:`/var/log/unit/unit.log`

         * - Non-privileged :ref:`user and group <security-apps>`
           - :samp:`unit`


   .. tab:: 31, 30

      .. warning::

         Unit's 1.20+ packages aren't built for Fedora 30; 1.22+ packages
         aren't built for Fedora 31.  These distributions are obsolete; please
         update.

      Supported architecture: x86-64.

      #. To configure Unit's repository, create the following file named
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
            # yum install :nxt_hint:`unit-devel <Required to install the Node.js module and build Go apps>` unit-go unit-jsc11 unit-jsc8 unit-perl  \
                  unit-php unit-python27 unit-python37 unit-ruby
            # systemctl restart unit  # Necessary for Unit to pick up any changes in language module setup


      Runtime details:

      .. list-table::

         * - Control :ref:`socket <security-socket-state>`
           - :file:`/var/run/unit/control.sock`

         * - Log :ref:`file <troubleshooting-log>`
           - :file:`/var/log/unit/unit.log`

         * - Non-privileged :ref:`user and group <security-apps>`
           - :samp:`unit`


   .. tab:: 29

      .. warning::

         Unit's 1.20+ packages aren't built for Fedora 29.  This distribution
         is obsolete; please update.

      Supported architecture: x86-64.

      #. To configure Unit's repository, create the following file named
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
            # yum install :nxt_hint:`unit-devel <Required to install the Node.js module and build Go apps>` unit-go unit-jsc8 unit-perl  \
                  unit-php unit-python27 unit-python37 unit-ruby
            # systemctl restart unit  # Necessary for Unit to pick up any changes in language module setup

      Runtime details:

      .. list-table::

         * - Control :ref:`socket <security-socket-state>`
           - :file:`/var/run/unit/control.sock`

         * - Log :ref:`file <troubleshooting-log>`
           - :file:`/var/log/unit/unit.log`

         * - Non-privileged :ref:`user and group <security-apps>`
           - :samp:`unit`


.. _installation-precomp-rhel:

====
RHEL
====

.. tabs::
   :prefix: rhel

   .. tab:: 8.x, 7.x

      Supported architecture: x86-64.

      #. To configure Unit's repository, create the following file named
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
            # yum install :nxt_hint:`unit-devel <Required to install the Node.js module and build Go apps>` unit-go unit-jsc8 unit-jsc11  \
                  unit-perl unit-php unit-python27 unit-python36
            # systemctl restart unit  # Necessary for Unit to pick up any changes in language module setup

      Runtime details:

      .. list-table::

         * - Control :ref:`socket <security-socket-state>`
           - :file:`/var/run/unit/control.sock`

         * - Log :ref:`file <troubleshooting-log>`
           - :file:`/var/log/unit/unit.log`

         * - Non-privileged :ref:`user and group <security-apps>`
           - :samp:`unit`


   .. tab:: 6.x

      .. warning::

         Unit's 1.20+ packages aren't built for RHEL 6.  This distribution is
         obsolete; please update.

      Supported architectures: i386, x86-64.

      #. To configure Unit's repository, create the following file named
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
            # yum install :nxt_hint:`unit-devel <Required to install the Node.js module and build Go apps>` unit-go unit-jsc8 unit-perl  \
                  unit-php unit-python
            # systemctl restart unit  # Necessary for Unit to pick up any changes in language module setup

      Runtime details:

      .. list-table::

         * - Control :ref:`socket <security-socket-state>`
           - :file:`/var/run/unit/control.sock`

         * - Log :ref:`file <troubleshooting-log>`
           - :file:`/var/log/unit/unit.log`

         * - Non-privileged :ref:`user and group <security-apps>`
           - :samp:`unit`

.. note::

   Use the same steps for binary-compatible distributions such as AlmaLinux,
   Oracle Linux, or Rocky Linux.


.. _installation-precomp-ubuntu:

======
Ubuntu
======

.. tabs::
   :prefix: ubuntu

   .. tab:: 21.10

      Supported architectures: arm64, x86-64.

      #. Download and save NGINX's signing key:

         .. code-block:: console

            # curl --output /usr/share/keyrings/nginx-keyring.gpg  \
                  https://unit.nginx.org/keys/nginx-keyring.gpg

         This eliminates the ``packages cannot be authenticated`` warnings
         during installation.

      #. To configure Unit's repository, create the following file named
         :file:`/etc/apt/sources.list.d/unit.list`:

         .. code-block:: none

            deb [signed-by=/usr/share/keyrings/nginx-keyring.gpg] https://packages.nginx.org/unit/ubuntu/ impish unit
            deb-src [signed-by=/usr/share/keyrings/nginx-keyring.gpg] https://packages.nginx.org/unit/ubuntu/ impish unit

      #. Install the core package and other packages you need:

         .. code-block:: console

            # apt update
            # apt install unit
            # apt install :nxt_hint:`unit-dev <Required to install the Node.js module and build Go apps>` unit-go unit-jsc11 unit-jsc16 unit-jsc17 unit-jsc18  \
                          unit-perl unit-php unit-python2.7 unit-python3.9 unit-python3.10 unit-ruby
            # systemctl restart unit  # Necessary for Unit to pick up any changes in language module setup


      Runtime details:

      .. list-table::

         * - Control :ref:`socket <security-socket-state>`
           - :file:`/var/run/control.unit.sock`

         * - Log :ref:`file <troubleshooting-log>`
           - :file:`/var/log/unit.log`

         * - Non-privileged :ref:`user and group <security-apps>`
           - :samp:`unit`


   .. tab:: 21.04

      Supported architectures: arm64, x86-64.

      #. Download and save NGINX's signing key:

         .. code-block:: console

            # curl --output /usr/share/keyrings/nginx-keyring.gpg  \
                  https://unit.nginx.org/keys/nginx-keyring.gpg

         This eliminates the ``packages cannot be authenticated`` warnings
         during installation.

      #. To configure Unit's repository, create the following file named
         :file:`/etc/apt/sources.list.d/unit.list`:

         .. code-block:: none

            deb [signed-by=/usr/share/keyrings/nginx-keyring.gpg] https://packages.nginx.org/unit/ubuntu/ hirsute unit
            deb-src [signed-by=/usr/share/keyrings/nginx-keyring.gpg] https://packages.nginx.org/unit/ubuntu/ hirsute unit

      #. Install the core package and other packages you need:

         .. code-block:: console

            # apt update
            # apt install unit
            # apt install :nxt_hint:`unit-dev <Required to install the Node.js module and build Go apps>` unit-go unit-jsc11 unit-jsc15 unit-jsc16 unit-jsc17  \
                          unit-perl unit-php unit-python2.7 unit-python3.9 unit-ruby
            # systemctl restart unit  # Necessary for Unit to pick up any changes in language module setup


      Runtime details:

      .. list-table::

         * - Control :ref:`socket <security-socket-state>`
           - :file:`/var/run/control.unit.sock`

         * - Log :ref:`file <troubleshooting-log>`
           - :file:`/var/log/unit.log`

         * - Non-privileged :ref:`user and group <security-apps>`
           - :samp:`unit`


   .. tab:: 20.10

      .. warning::

         Unit's 1.25+ packages aren't built for Ubuntu 20.10.  This
         distribution is obsolete; please update.

      Supported architectures: arm64, x86-64.

      #. Download and save NGINX's signing key:

         .. code-block:: console

            # curl --output /usr/share/keyrings/nginx-keyring.gpg  \
                  https://unit.nginx.org/keys/nginx-keyring.gpg

         This eliminates the ``packages cannot be authenticated`` warnings
         during installation.

      #. To configure Unit's repository, create the following file named
         :file:`/etc/apt/sources.list.d/unit.list`:

         .. code-block:: none

            deb [signed-by=/usr/share/keyrings/nginx-keyring.gpg] https://packages.nginx.org/unit/ubuntu/ groovy unit
            deb-src [signed-by=/usr/share/keyrings/nginx-keyring.gpg] https://packages.nginx.org/unit/ubuntu/ groovy unit

      #. Install the core package and other packages you need:

         .. code-block:: console

            # apt update
            # apt install unit
            # apt install :nxt_hint:`unit-dev <Required to install the Node.js module and build Go apps>` unit-go unit-jsc11 unit-jsc13 unit-jsc14 unit-jsc15  \
                          unit-perl unit-php unit-python3.8 unit-ruby
            # systemctl restart unit  # Necessary for Unit to pick up any changes in language module setup


      Runtime details:

      .. list-table::

         * - Control :ref:`socket <security-socket-state>`
           - :file:`/var/run/control.unit.sock`

         * - Log :ref:`file <troubleshooting-log>`
           - :file:`/var/log/unit.log`

         * - Non-privileged :ref:`user and group <security-apps>`
           - :samp:`unit`


   .. tab:: 20.04

      Supported architectures: arm64, x86-64.

      #. Download and save NGINX's signing key:

         .. code-block:: console

            # curl --output /usr/share/keyrings/nginx-keyring.gpg  \
                  https://unit.nginx.org/keys/nginx-keyring.gpg

         This eliminates the ``packages cannot be authenticated`` warnings
         during installation.

      #. To configure Unit's repository, create the following file named
         :file:`/etc/apt/sources.list.d/unit.list`:

         .. code-block:: none

            deb [signed-by=/usr/share/keyrings/nginx-keyring.gpg] https://packages.nginx.org/unit/ubuntu/ focal unit
            deb-src [signed-by=/usr/share/keyrings/nginx-keyring.gpg] https://packages.nginx.org/unit/ubuntu/ focal unit

      #. Install the core package and other packages you need:

         .. code-block:: console

            # apt update
            # apt install unit
            # apt install :nxt_hint:`unit-dev <Required to install the Node.js module and build Go apps>` unit-go unit-jsc11 unit-perl  \
                  unit-php unit-python2.7 unit-python3.8 unit-ruby
            # systemctl restart unit  # Necessary for Unit to pick up any changes in language module setup


      Runtime details:

      .. list-table::

         * - Control :ref:`socket <security-socket-state>`
           - :file:`/var/run/control.unit.sock`

         * - Log :ref:`file <troubleshooting-log>`
           - :file:`/var/log/unit.log`

         * - Non-privileged :ref:`user and group <security-apps>`
           - :samp:`unit`


   .. tab:: 19.10

      .. warning::

         Unit's 1.20+ packages aren't built for Ubuntu 19.10.  This
         distribution is obsolete; please update.

      Supported architecture: x86-64.

      #. Download and save NGINX's signing key:

         .. code-block:: console

            # curl --output /usr/share/keyrings/nginx-keyring.gpg  \
                  https://unit.nginx.org/keys/nginx-keyring.gpg

         This eliminates the ``packages cannot be authenticated`` warnings
         during installation.

      #. To configure Unit's repository, create the following file named
         :file:`/etc/apt/sources.list.d/unit.list`:

         .. code-block:: none

            deb [signed-by=/usr/share/keyrings/nginx-keyring.gpg] https://packages.nginx.org/unit/ubuntu/ eoan unit
            deb-src [signed-by=/usr/share/keyrings/nginx-keyring.gpg] https://packages.nginx.org/unit/ubuntu/ eoan unit

      #. Install the core package and other packages you need:

         .. code-block:: console

            # apt update
            # apt install unit
            # apt install :nxt_hint:`unit-dev <Required to install the Node.js module and build Go apps>` unit-go unit-jsc11 unit-perl  \
                  unit-php unit-python2.7 unit-python3.7 unit-python3.8 unit-ruby
            # systemctl restart unit  # Necessary for Unit to pick up any changes in language module setup


      Runtime details:

      .. list-table::

         * - Control :ref:`socket <security-socket-state>`
           - :file:`/var/run/control.unit.sock`

         * - Log :ref:`file <troubleshooting-log>`
           - :file:`/var/log/unit.log`

         * - Non-privileged :ref:`user and group <security-apps>`
           - :samp:`unit`


   .. tab:: 18.04

      Supported architectures: arm64, x86-64.

      #. Download and save NGINX's signing key:

         .. code-block:: console

            # curl --output /usr/share/keyrings/nginx-keyring.gpg  \
                  https://unit.nginx.org/keys/nginx-keyring.gpg

         This eliminates the ``packages cannot be authenticated`` warnings
         during installation.

      #. To configure Unit's repository, create the following file named
         :file:`/etc/apt/sources.list.d/unit.list`:

         .. code-block:: none

            deb [signed-by=/usr/share/keyrings/nginx-keyring.gpg] https://packages.nginx.org/unit/ubuntu/ bionic unit
            deb-src [signed-by=/usr/share/keyrings/nginx-keyring.gpg] https://packages.nginx.org/unit/ubuntu/ bionic unit

      #. Install the core package and other packages you need:

         .. code-block:: console

            # apt update
            # apt install unit
            # apt install :nxt_hint:`unit-dev <Required to install the Node.js module and build Go apps>` unit-go unit-jsc8 unit-jsc11 unit-perl  \
                  unit-php unit-python2.7 unit-python3.6 unit-python3.7 unit-ruby
            # systemctl restart unit  # Necessary for Unit to pick up any changes in language module setup


      Runtime details:

      .. list-table::

         * - Control :ref:`socket <security-socket-state>`
           - :file:`/var/run/control.unit.sock`

         * - Log :ref:`file <troubleshooting-log>`
           - :file:`/var/log/unit.log`

         * - Non-privileged :ref:`user and group <security-apps>`
           - :samp:`unit`


   .. tab:: 16.04

      .. warning::

         Unit's 1.24+ packages aren't built for Ubuntu 16.04.  This
         distribution is obsolete; please update.

      Supported architectures: arm64, i386, x86-64.

      #. Download and save NGINX's signing key:

         .. code-block:: console

            # curl --output /usr/share/keyrings/nginx-keyring.gpg  \
                  https://unit.nginx.org/keys/nginx-keyring.gpg

         This eliminates the ``packages cannot be authenticated`` warnings
         during installation.

      #. To configure Unit's repository, create the following file named
         :file:`/etc/apt/sources.list.d/unit.list`:

         .. code-block:: none

            deb [signed-by=/usr/share/keyrings/nginx-keyring.gpg] https://packages.nginx.org/unit/ubuntu/ xenial unit
            deb-src [signed-by=/usr/share/keyrings/nginx-keyring.gpg] https://packages.nginx.org/unit/ubuntu/ xenial unit

      #. Install the core package and other packages you need:

         .. code-block:: console

            # apt update
            # apt install unit
            # apt install :nxt_hint:`unit-dev <Required to install the Node.js module and build Go apps>` unit-go unit-jsc8 unit-perl unit-php  \
                  unit-python2.7 unit-python3.5 unit-ruby
            # systemctl restart unit  # Necessary for Unit to pick up any changes in language module setup

      Runtime details:

      .. list-table::

         * - Control :ref:`socket <security-socket-state>`
           - :file:`/var/run/control.unit.sock`

         * - Log :ref:`file <troubleshooting-log>`
           - :file:`/var/log/unit.log`

         * - Non-privileged :ref:`user and group <security-apps>`
           - :samp:`unit`


.. _installation-homebrew:

========
Homebrew
========

To install Unit on macOS, use the official Homebrew `tap
<https://github.com/nginx/homebrew-unit>`_:

.. code-block:: console

   $ brew install nginx/unit/unit

This deploys the core Unit binary and the prerequisites for the :ref:`Go
<installation-go-package>` and :ref:`Node.js <installation-nodejs-package>`
language modules.

To install the Java, Perl, Python, and Ruby language modules from Homebrew:

.. code-block:: console

   $ brew install unit-java unit-perl unit-python unit-python3 unit-ruby
   # pkill unitd  # Stop Unit
   # unitd        # Start Unit to pick up any changes in language module setup

Runtime details:

.. list-table::

   * - Control :ref:`socket <security-socket-state>`
     - :file:`/usr/local/var/run/unit/control.sock`

   * - Log :ref:`file <troubleshooting-log>`
     - :file:`/usr/local/var/log/unit/unit.log`

   * - Non-privileged :ref:`user and group <security-apps>`
     - :samp:`nobody`


.. _installation-go-package:

==
Go
==

To build Go apps capable of running on Unit, use the official :samp:`unit-go`
:ref:`package <installation-precomp-pkgs>` or type:

.. subs-code-block:: console

   $ go get unit.nginx.org/go@|version|

Both methods install a Go package that you :ref:`import <configuration-go>` in
your app code.  If you update Unit later, make sure to upgrade the package
using the same method and rebuild your apps.


.. _installation-nodejs-package:

=======
Node.js
=======

Unit's `npm-hosted <https://www.npmjs.com/package/unit-http>`_ Node.js module
is called :program:`unit-http`.  Install it to run Node.js apps on Unit:

#. First, install the :samp:`unit-dev/unit-devel` :ref:`package
   <installation-precomp-pkgs>`; it's needed to build :program:`unit-http`.

#. Next, build and install :program:`unit-http` globally (this requires
   :program:`npm` and :program:`node-gyp`):

    .. code-block:: console

       # npm install -g --unsafe-perm unit-http

    .. warning::

       The :program:`unit-http` module is platform dependent due to
       optimizations; you can't move it across systems with the rest of
       :file:`node-modules`.  Global installation avoids such scenarios; just
       :ref:`relink <configuration-nodejs>` the migrated app.

#. It's entirely possible to run Node.js apps on Unit :ref:`without
   <configuration-nodejs>` mentioning :samp:`unit-http` in your app sources.
   However, you can explicitly use :samp:`unit-http` in your code instead of
   the built-in :samp:`http`, but mind that such frameworks as Express may
   require extra :doc:`changes <howto/express>`.

If you update Unit later, make sure to update the module as well:

.. code-block:: console

   # npm update -g --unsafe-perm unit-http

.. note::

   You can also :ref:`configure <howto/source-modules-nodejs>` and
   :ref:`install <source-bld-src-ext>` the :program:`unit-http` module
   from sources.


.. _installation-precomp-startup:

====================
Startup and Shutdown
====================

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

      Stop all Unit's processes:

      .. code-block:: console

         # pkill unitd

      For startup options, see :ref:`below <source-startup>`.

.. note::

   Restarting Unit is necessary after installing or uninstalling any language
   modules to pick up the changes.


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

      To install Unit's core executables from the `Alpine Linux packages
      <https://pkgs.alpinelinux.org/packages?name=unit*>`_:

      .. code-block:: console

         # apk update
         # apk upgrade
         # apk add unit

      To install service manager files and specific language modules:

      .. code-block:: console

         # apk add unit-openrc unit-perl unit-php7 unit-python3 unit-ruby
         # service unit restart  # Necessary for Unit to pick up any changes in language module setup

      Runtime details:

      .. list-table::

         * - Control :ref:`socket <source-startup>`
           - :file:`/run/control.unit.sock`

         * - Log :ref:`file <troubleshooting-log>`
           - :file:`/var/log/unit.log`

         * - Non-privileged :ref:`user and group <security-apps>`
           - :samp:`unit`

         * - Startup and shutdown
           - .. code-block:: console

                # :nxt_hint:`service unit enable <Enable Unit to launch automatically at system startup>`
                # :nxt_hint:`service unit restart <Start or restart Unit; one-time action>`
                # :nxt_hint:`service unit stop <Stop a running Unit; one-time action>`
                # :nxt_hint:`service unit disable <Disable Unit's automatic startup>`


   .. tab:: ALT

      To install Unit's core executables and specific language modules from the
      `Sisyphus packages
      <https://packages.altlinux.org/en/sisyphus/srpms/unit>`__:

      .. code-block:: console

         # apt-get update
         # apt-get install unit
         # apt-get install unit-perl unit-php unit-ruby
         # service unit restart  # Necessary for Unit to pick up any changes in language module setup

      Runtime details:

      .. list-table::

         * - Control :ref:`socket <source-startup>`
           - :file:`/run/unit/control.sock`

         * - Log :ref:`file <troubleshooting-log>`
           - :file:`/var/log/unit/unit.log`

         * - Non-privileged :ref:`user and group <security-apps>`
           - :samp:`_unit` (mind the :samp:`_` prefix)

         * - Startup and shutdown
           - .. code-block:: console

                # :nxt_hint:`service unit enable <Enable Unit to launch automatically at system startup>`
                # :nxt_hint:`service unit restart <Start or restart Unit; one-time action>`
                # :nxt_hint:`service unit stop <Stop a running Unit; one-time action>`
                # :nxt_hint:`service unit disable <Disable Unit's automatic startup>`


   .. tab:: Arch

      To install Unit's core executables and all language modules, clone the
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

         * - Control :ref:`socket <source-startup>`
           - :file:`/run/nginx-unit.control.sock`

         * - Log :ref:`file <troubleshooting-log>`
           - :file:`/var/log/nginx-unit.log`

         * - Non-privileged :ref:`user and group <security-apps>`
           - :samp:`nobody`

         * - Startup and shutdown
           - .. code-block:: console

                # :nxt_hint:`systemctl enable unit <Enable Unit to launch automatically at system startup>`
                # :nxt_hint:`systemctl restart unit <Start or restart Unit; one-time action>`
                # :nxt_hint:`systemctl stop unit <Stop a running Unit; one-time action>`
                # :nxt_hint:`systemctl disable unit <Disable Unit's automatic startup>`


   .. tab:: FreeBSD

        To install Unit from `FreeBSD packages
        <https://docs.freebsd.org/en/books/handbook/ports/#pkgng-intro>`_, get
        the core package and other packages you need:

        .. code-block:: console

           # pkg install -y unit
           # pkg install -y :nxt_hint:`libunit <Required to install the Node.js module and build Go apps>`
           # pkg install -y unit-java8  \
                            unit-perl5.32  \
                            unit-php73 unit-php74 unit-php80  \
                            unit-python37  \
                            unit-ruby2.7
           # service unitd restart  # Necessary for Unit to pick up any changes in language module setup

        To install Unit from `FreeBSD ports
        <https://docs.freebsd.org/en/books/handbook/ports/#ports-using>`_,
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
        <https://www.freshports.org/devel/libunit/>`_ (required to
        install the :ref:`Node.js <installation-nodejs-package>` module
        and build :ref:`Go <installation-go-package>` apps), `unit-java
        <https://www.freshports.org/www/unit-java/>`__, `unit-perl
        <https://www.freshports.org/www/unit-perl/>`__, `unit-php
        <https://www.freshports.org/www/unit-php/>`__, `unit-python
        <https://www.freshports.org/www/unit-python/>`__, or `unit-ruby
        <https://www.freshports.org/www/unit-ruby/>`__.  Having done
        that, restart Unit:

        .. code-block:: console

           # service unitd restart  # Necessary for Unit to pick up any changes in language module setup

        Runtime details:

        .. list-table::

           * - Control :ref:`socket <source-startup>`
             - :file:`/var/run/unit/control.unit.sock`

           * - Log :ref:`file <troubleshooting-log>`
             - :file:`/var/log/unit/unit.log`

           * - Non-privileged :ref:`user and group <security-apps>`
             - :samp:`www`

           * - Startup and shutdown
             - .. code-block:: console

                  # :nxt_hint:`service unitd enable <Enable Unit to launch automatically at system startup>`
                  # :nxt_hint:`service unitd restart <Start or restart Unit; one-time action>`
                  # :nxt_hint:`service unitd stop <Stop a running Unit; one-time action>`
                  # :nxt_hint:`service unitd disable <Disable Unit's automatic startup>`


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

         * - Control :ref:`socket <source-startup>`
           - :file:`/run/nginx-unit.sock`

         * - Log :ref:`file <troubleshooting-log>`
           - :file:`/var/log/nginx-unit`

         * - Non-privileged :ref:`user and group <security-apps>`
           - :samp:`nobody`

         * - Startup and shutdown
           - .. code-block:: console

                # :nxt_hint:`rc-update add nginx-unit <Enable Unit to launch automatically at system startup>`
                # :nxt_hint:`rc-service nginx-unit restart <Start or restart Unit; one-time action>`
                # :nxt_hint:`rc-service nginx-unit stop <Stop a running Unit; one-time action>`
                # :nxt_hint:`rc-update del nginx-unit <Disable Unit's automatic startup>`


   .. tab:: NetBSD

      To install Unit's core package and the other packages you need from
      the `NetBSD Package Collection
      <https://cdn.netbsd.org/pub/pkgsrc/current/pkgsrc/www/unit/index.html>`_:

      .. code-block:: console

         # pkg_add unit
         # pkg_add :nxt_hint:`libunit <Required to install the Node.js module and build Go apps>`
         # pkg_add unit-perl  \
                   unit-python2.7  \
                   unit-python3.6 unit-python3.7 unit-python3.8 unit-python3.9
         # service unit restart  # Necessary for Unit to pick up any changes in language module setup

      To build Unit manually, start by updating the package collection:

      .. code-block:: console

         # cd /usr/pkgsrc && cvs update -dP

      Next, browse to the package path to build and install the core Unit
      binaries:

      .. code-block:: console

         # cd /usr/pkgsrc/www/unit/
         # make build install

      Repeat the steps for the other packages you need: `libunit
      <https://cdn.netbsd.org/pub/pkgsrc/current/pkgsrc/devel/libunit/index.html>`__
      (required to install the :ref:`Node.js
      <installation-nodejs-package>` module and build :ref:`Go
      <installation-go-package>` apps), `unit-perl
      <https://cdn.netbsd.org/pub/pkgsrc/current/pkgsrc/www/unit-perl/index.html>`__,
      `unit-php
      <https://cdn.netbsd.org/pub/pkgsrc/current/pkgsrc/www/unit-php/index.html>`__,
      `unit-python
      <https://cdn.netbsd.org/pub/pkgsrc/current/pkgsrc/www/unit-python/index.html>`__,
      or `unit-ruby
      <https://cdn.netbsd.org/pub/pkgsrc/current/pkgsrc/www/unit-ruby/index.html>`__.
      Having done that, restart Unit:

      .. code-block:: console

         # service unitd restart  # Necessary for Unit to pick up any changes in language module setup

      Runtime details:

      .. list-table::

         * - Control :ref:`socket <source-startup>`
           - :file:`/var/run/unit/control.unit.sock`

         * - Log :ref:`file <troubleshooting-log>`
           - :file:`/var/log/unit/unit.log`

         * - Non-privileged :ref:`user and group <security-apps>`
           - :samp:`unit`

         * - Startup and shutdown
           - First, add Unit's startup script to the :file:`/etc/rc.d/`
             directory:

             .. code-block:: console

                # cp /usr/pkg/share/examples/rc.d/unit /etc/rc.d/

             After that, you can start and stop Unit as follows:

             .. code-block:: console

                # :nxt_hint:`service unit restart <Start or restart Unit; one-time action>`
                # :nxt_hint:`service unit stop <Stop a running Unit; one-time action>`

             To enable or disable Unit's automatic startup, edit
             :file:`/etc/rc.conf`:

             .. code-block:: ini

                # Enable service:
                unit=YES

                # Disable service:
                unit=NO


   .. tab:: Nix

      To install Unit's core executables and all language modules using the
      `Nix package manager <https://nixos.org>`_, update the channel, check if
      Unit's available, and install the `package
      <https://github.com/NixOS/nixpkgs/tree/master/pkgs/servers/http/unit>`__:

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

         * - Control :ref:`socket <source-startup>`
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

                # :nxt_hint:`systemctl enable unit <Enable Unit to launch automatically at system startup>`
                # :nxt_hint:`systemctl restart unit <Start or restart Unit; one-time action>`
                # :nxt_hint:`systemctl stop unit <Stop a running Unit; one-time action>`
                # :nxt_hint:`systemctl disable unit <Disable Unit's automatic startup>`


   .. tab:: OpenBSD

        To install Unit from `OpenBSD ports <https://openports.se/www/unit>`_,
        start by updating your port collection, for example:

        .. code-block:: console

           $ cd /usr/
           $ cvs -d anoncvs@anoncvs.spacehopper.org:/cvs checkout -P ports

        Next, browse to the port path to build and install Unit:

        .. code-block:: console

           $ cd /usr/ports/www/unit/
           $ make
           # make install

        This also installs the language modules for Perl, Python, and Ruby;
        other modules can be built and installed from :ref:`source
        <source>`.  Having done that, restart Unit:

        .. code-block:: console

           # rcctl restart unit  # Necessary for Unit to pick up any changes in language module setup

        Runtime details:

        .. list-table::

           * - Control :ref:`socket <source-startup>`
             - :file:`/var/run/unit/control.unit.sock`

           * - Log :ref:`file <troubleshooting-log>`
             - :file:`/var/log/unit/unit.log`

           * - Non-privileged :ref:`user and group <security-apps>`
             - :samp:`_unit`

           * - Startup and shutdown
             - .. code-block:: console

                  # :nxt_hint:`rcctl enable unit <Enable Unit to launch automatically at system startup>`
                  # :nxt_hint:`rcctl restart unit <Start or restart Unit; one-time action>`
                  # :nxt_hint:`rcctl stop unit <Stop a running Unit; one-time action>`
                  # :nxt_hint:`rcctl disable unit <Disable Unit's automatic startup>`


   .. tab:: Remi's RPM

      `Remi's RPM repository
      <https://blog.remirepo.net/post/2019/01/14/PHP-with-the-NGINX-unit-application-server>`_,
      which hosts the latest versions of the PHP stack for CentOS, Fedora, and
      RHEL, also has the core Unit package and the PHP modules.

      To use Remi's versions of Unit's packages, configure `Remi's RPM repo
      <https://blog.remirepo.net/pages/Config-en>`_ first.  Remi's PHP language
      modules are also compatible with the core Unit package from :ref:`our own
      repository <installation-precomp-pkgs>`.

      Next, install Unit and the PHP modules you want:

      .. code-block:: console

         # yum install --enablerepo=remi unit  \
               php54-unit-php php55-unit-php php56-unit-php  \
               php70-unit-php php71-unit-php php72-unit-php php73-unit-php php74-unit-php  \
               php80-unit-php
         # systemctl restart unit  # Necessary for Unit to pick up any changes in language module setup

      Runtime details:

      .. list-table::

         * - Control :ref:`socket <source-startup>`
           - :file:`/run/unit/control.sock`

         * - Log :ref:`file <troubleshooting-log>`
           - :file:`/var/log/unit/unit.log`

         * - Non-privileged :ref:`user and group <security-apps>`
           - :samp:`nobody`

         * - Startup and shutdown
           - .. code-block:: console

                # :nxt_hint:`systemctl enable unit <Enable Unit to launch automatically at system startup>`
                # :nxt_hint:`systemctl restart unit <Start or restart Unit; one-time action>`
                # :nxt_hint:`systemctl stop unit <Stop a running Unit; one-time action>`
                # :nxt_hint:`systemctl disable unit <Disable Unit's automatic startup>`


   .. tab:: SCLo

      If you use `SCLo Software Collections
      <https://wiki.centos.org/SpecialInterestGroup/SCLo>`_, you can install
      Unit's PHP modules as packages from the corresponding repo.  Besides
      other dependencies, the packages require the :ref:`core Unit installation
      <installation-precomp-pkgs>`.

      CentOS:

      .. code-block:: console

         # yum install centos-release-scl
         # yum install --enablerepo=centos-sclo-sclo \
                       sclo-php72-unit-php sclo-php73-unit-php
         # systemctl restart unit  # Necessary for Unit to pick up any changes in language module setup

      RHEL:

      .. code-block:: console

         # cd /etc/yum.repos.d/
         # curl -O https://copr.fedorainfracloud.org/coprs/rhscl/centos-release-scl/repo/epel-7/rhscl-centos-release-scl-epel-7.repo
         # yum install centos-release-scl
         # yum install --enablerepo=centos-sclo-sclo \
                       sclo-php72-unit-php sclo-php73-unit-php
         # systemctl restart unit  # Necessary for Unit to pick up any changes in language module setup

      Runtime details: see :ref:`installation-precomp-centos`,
      :ref:`installation-precomp-rhel`, and
      :ref:`installation-precomp-startup`.


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
     - No language modules; based on the :samp:`debian:buster-slim` `image
       <https://hub.docker.com/_/debian>`__.

   * - :samp:`|version|-go1.17`
     - Single-language image based on the :samp:`golang:1.17`
       `image <https://hub.docker.com/_/golang>`__.

   * - :samp:`|version|-jsc11`
     - Single-language image based on the :samp:`openjdk:11-jdk`
       `image <https://hub.docker.com/_/openjdk>`__.

   * - :samp:`|version|-node16`
     - Single-language image based on the :samp:`node:16`
       `image <https://hub.docker.com/_/node>`__.

   * - :samp:`|version|-perl5.34`
     - Single-language image based on the :samp:`perl:5.34`
       `image <https://hub.docker.com/_/perl>`__.

   * - :samp:`|version|-php8.0`
     - Single-language image based on the :samp:`php:8.0-cli`
       `image <https://hub.docker.com/_/php>`__.

   * - :samp:`|version|-python3.9`
     - Single-language image based on the :samp:`python:3.9`
       `image <https://hub.docker.com/_/python>`__.

   * - :samp:`|version|-ruby3.0`
     - Single-language image based on the :samp:`ruby:3.0`
       `image <https://hub.docker.com/_/ruby>`__.

.. nxt_details:: Customizing Language Versions in Docker Images

   To create a Unit image with a different language version, clone the sources
   and rebuild them locally on a machine with Docker installed.  The build
   command has the following format:

   .. code-block:: console

      $ make build-<language name><language version> VERSION_<language name>=<language version>

   The :program:`make` utility parses the command line to extract the language
   name and version; these values must reference an existing official language
   image to be used as the base for the build.  If not sure whether an official
   image exists for a specific language version, follow the links in the tag
   table above.

   The language name can be :samp:`go`, :samp:`jsc`, :samp:`node`,
   :samp:`perl`, :samp:`php`, :samp:`python`, or :samp:`ruby`; the version is
   defined as :samp:`<major>.<minor>`, except for :samp:`jsc` and :samp:`node`
   that take only major version numbers (as exemplified by the tag table).
   Thus, to create a local image based on Python 3.6 and tagged as
   :samp:`unit:|version|-python3.6`:

   .. subs-code-block:: console

      $ git clone https://github.com/nginx/unit
      $ cd unit
      $ git checkout |version|  # Optional; use to choose a specific Unit version
      $ cd pkg/docker/
      $ make build-:nxt_ph:`python3.6 <Language name and version>` VERSION_:nxt_ph:`python <Language name>`=:nxt_ph:`3.6 <Language version>`

   For details, see the `Makefile
   <https://github.com/nginx/unit/blob/master/pkg/docker/Makefile>`__.  For
   other customization scenarios, see our :doc:`Howto <howto/docker>`.

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
   :prefix: docker

   .. tab:: Docker Hub

      To install and run Unit from NGINX's `repository
      <https://hub.docker.com/r/nginx/unit/>`__ at Docker Hub:

      .. code-block:: console

         $ docker pull docker.io/nginx/unit::nxt_ph:`TAG <Specific image tag; see above for a complete list>`
         $ docker run -d docker.io/nginx/unit::nxt_ph:`TAG <Specific image tag; see above for a complete list>`


   .. tab:: Amazon ECR Public Gallery

      To install and run Unit from NGINX's `repository
      <https://gallery.ecr.aws/nginx/unit>`__ at Amazon ECR Public Gallery:

      .. code-block:: console

         $ docker pull public.ecr.aws/nginx/unit::nxt_ph:`TAG <Specific image tag; see above for a complete list>`
         $ docker run -d public.ecr.aws/nginx/unit::nxt_ph:`TAG <Specific image tag; see above for a complete list>`


   .. tab:: packages.nginx.org

      To install and run Unit from tarballs stored on our `website
      <https://packages.nginx.org/unit/docker/>`_:

      .. subs-code-block:: console

         $ curl -O https://packages.nginx.org/unit/docker/|version|/nginx-unit-:nxt_ph:`TAG <Specific image tag; see above for a complete list>`.tar.gz
         $ curl -O https://packages.nginx.org/unit/docker/|version|/nginx-unit-:nxt_ph:`TAG <Specific image tag; see above for a complete list>`.tar.gz.sha512
         $ sha512sum -c nginx-unit-:nxt_ph:`TAG <Specific image tag; see above for a complete list>`.tar.gz.sha512
               nginx-unit-:nxt_ph:`TAG <Specific image tag; see above for a complete list>`.tar.gz: OK

         $ docker load < nginx-unit-:nxt_ph:`TAG <Specific image tag; see above for a complete list>`.tar.gz

Runtime details:

.. list-table::

   * - Control :ref:`socket <security-socket-state>`
     - :file:`/var/run/control.unit.sock`

   * - Log :ref:`file <troubleshooting-log>`
     - Forwarded to the `Docker log collector
       <https://docs.docker.com/config/containers/logging/>`_

   * - Non-privileged :ref:`user and group <security-apps>`
     - :samp:`unit`

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
<source-config-src-state>` (:file:`/var/lib/unit/` in official images) of
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
     - :nxt_hint:`Shell scripts <Use shebang in your scripts to specify a
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
            type=bind,src=:nxt_ph:`/path/to/config/files/ <Use a real path instead>`,dst=/docker-entrypoint.d/ \
            nginx/unit:|version|-minimal)


.. _source:

***********
Source Code
***********

You can get Unit's source code from our official Mercurial repository, its
GitHub mirror, or in a tarball.

If you'd like to use `Mercurial <https://www.mercurial-scm.org/downloads>`_:

   .. code-block:: console

      $ hg clone https://hg.nginx.org/unit
      $ cd unit

If you prefer `Git <https://git-scm.com/downloads>`_:

   .. code-block:: console

      $ git clone https://github.com/nginx/unit
      $ cd unit

To download the sources directly from `our site
<https://unit.nginx.org/download/>`_:

   .. subs-code-block:: console

      $ curl -O https://unit.nginx.org/download/unit-|version|.tar.gz
      $ tar xzf unit-|version|.tar.gz
      $ cd unit-|version|

To build Unit and specific language modules from these sources, refer to the
source code :doc:`howto <howto/source>`; to package custom modules, see the
module :ref:`howto <modules-pkg>`.
