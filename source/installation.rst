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

   You can also :ref:`configure <installation-modules-nodejs>` and
   :ref:`install <installation-bld-src-ext>` the :program:`unit-http` module
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

      For startup options, see :ref:`below <installation-src-startup>`.

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

         * - Control :ref:`socket <installation-src-startup>`
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

         * - Control :ref:`socket <installation-src-startup>`
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

         * - Control :ref:`socket <installation-src-startup>`
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

           * - Control :ref:`socket <installation-src-startup>`
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

         * - Control :ref:`socket <installation-src-startup>`
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

         * - Control :ref:`socket <installation-src-startup>`
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
        <installation-src>`.  Having done that, restart Unit:

        .. code-block:: console

           # rcctl restart unit  # Necessary for Unit to pick up any changes in language module setup

        Runtime details:

        .. list-table::

           * - Control :ref:`socket <installation-src-startup>`
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

         * - Control :ref:`socket <installation-src-startup>`
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


.. _installation-src:

***********
Source Code
***********

=================
Obtaining Sources
=================

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
the library files for the supported languages (Go, Java, Node.js, PHP, Perl,
Python, and Ruby), and other features you want to use with Unit.

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
      and installing <installation-bld-src>` Unit on Solaris.


.. _installation-config-src:

===================
Configuring Sources
===================

To run system compatibility checks and generate a :file:`Makefile` with core
build instructions for Unit:

.. code-block:: console

   $ ./configure :nxt_ph:`COMPILE-TIME OPTIONS <See the table below>`

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
     - Directory path for Unit's language :doc:`modules <howto/modules>`.

       The default is :samp:`modules`.

   * - :samp:`--pid=pathname`
     - Pathname for the PID file of Unit's :program:`main` :ref:`process
       <security-apps>`.

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
     - Defines the temporary file storage location (used to dump large request
       bodies).

       The default value is :samp:`tmp`.


.. _installation-src-dir:

Directory Structure
*******************

To customize Unit's installation and runtime directories, you can both:

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
   :prefix: modules
   :toc:

   .. tab:: Go

      When you run :command:`./configure go`, Unit sets up the Go package that
      lets your applications :ref:`run on Unit <configuration-go>`.  To use the
      package, :ref:`install <installation-bld-src-ext>` it in your Go
      environment.  Available configuration options:

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
             used in :ref:`make <installation-bld-src-emb>` targets.

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
      to support running Perl scripts as applications on Unit.  Available
      command options:

      .. list-table::

         * - :samp:`--perl=pathname`
           - Specific Perl executable pathname.

             The default is :samp:`perl`.

         * - :samp:`--module=basename`
           - Name of the module to be built (:file:`<basename>.unit.so`), also
             used in :ref:`make <installation-bld-src-emb>` targets.

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
             used in :ref:`make <installation-bld-src-emb>` targets.

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
             used in :ref:`make <installation-bld-src-emb>` targets.

             The default is :option:`!--config`'s filename minus the `-config`
             suffix; thus, :samp:`/path/python3-config` turns into
             :samp:`python3`.

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

To build and install Unit's executables and language modules that you have
:program:`./configure`'d earlier:

.. code-block:: console

   $ make
   # make install

You can also build and install language modules individually; the specific
method depends on whether the language module is embedded in Unit or packaged
externally.

.. note::

   For further details about Unit's language modules, see :doc:`howto/modules`.


.. _installation-bld-src-emb:

Embedded Language Modules
*************************

To build and install the modules for Java, PHP, Perl, Python, or Ruby after
configuration, run :command:`make <module basename>` and :command:`make
<module basename>-install`, for example:

.. code-block:: console

   $ make :nxt_hint:`perl-5.20 <This is the --module option value from ./configure perl>`
   # make :nxt_hint:`perl-5.20 <This is the --module option value from ./configure perl>`-install


.. _installation-bld-src-ext:

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
   <installation-modules-nodejs>` with :program:`./configure nodejs`
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

   # :nxt_hint:`unitd <Your PATH environment variable should list a path to unitd>` :nxt_ph:`RUNTIME OPTIONS <See the table below>`

Otherwise, start :program:`unitd` from the :samp:`sbin` subdirectory relative
to installation directory :ref:`prefix <installation-config-src-prefix>`:

.. code-block:: console

   # cd :nxt_ph:`/path/to/unit/ <Destination prefix>`
   # :nxt_hint:`sbin/unitd <This preserves relative paths>` :nxt_ph:`RUNTIME OPTIONS <See the table below>`

Run :command:`unitd -h` or :command:`unitd --version` to list Unit's
compile-time settings.  Usually, the defaults don't require overrides; however,
the following runtime options are available.  For details and security notes,
see :ref:`here <installation-config-src>`.

General runtime options and :ref:`compile-time setting
<installation-config-src>` overrides:

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
     - Directory path for Unit's language :doc:`modules <howto/modules>`
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
