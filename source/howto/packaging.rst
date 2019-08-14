:orphan:

.. include:: ../include/replace.rst

########################
Packaging Custom Modules
########################

There's always a chance that you need to run a language version that isn't yet
available among the official Unit :ref:`packages <installation-precomp-pkgs>`
but still want to benefit from the convenience of a packaged installation.  In
this case, you can build your own package to be installed alongside the
official distribution, adding the latter as a prerequisite.

Here, we are packaging a custom PHP 7.3 :ref:`module <installation-php>` to be
installed next to the official Unit package; adjust the command samples to your
scenario as needed.  For Debian, Ubuntu, and other :file:`.deb`-based
distributions, see the steps :ref:`here <packaging-deb>`; for CentOS,
Fedora, RHEL, and other :file:`.rpm`-based distributions, follow the steps
:ref:`here <packaging-rpm>`.

.. note::

   For elaborate Unit packaging examples, refer to our packaging system
   `sources <https://hg.nginx.org/unit/file/tip/pkg/>`_.

.. _packaging-deb:

*************
.deb Packages
*************

Assuming you are packaging for the current system and have the official Unit
package installed:

#. Make sure to install the :ref:`prerequisites <installation-prereq-build>`
   for the package.  In our example, it's PHP 7.3 on Debian 10:

   .. code-block:: console

      # apt update
      # apt install ca-certificates apt-transport-https
      # curl -sL https://packages.sury.org/php/apt.gpg | apt-key add -
      # echo "deb https://packages.sury.org/php/ buster main" \
             > /etc/apt/sources.list.d/php.list
      # apt update
      # apt install php7.3
      # apt install php-dev libphp-embed

#. Create a staging directory for your package:

   .. subs-code-block:: console

      $ export UNITTMP=$(mktemp -d -p /tmp -t unit.XXXXXX)
      $ mkdir -p $UNITTMP/unit-php7.3/DEBIAN
      $ cd $UNITTMP

   This creates a folder structure fit for :program:`dpkg-deb`; the
   :file:`DEBIAN` folder will store the package definition.

#. Run :program:`unitd --version` as root and note the :program:`./configure`
   :ref:`flags <installation-config-src>` for later use:

   .. subs-code-block:: console

      # unitd --version

          unit version: |version|
          configured as ./configure <./configure flags>

#. Download Unit sources, :ref:`configure <installation-src-modules>` and build
   your custom module, then put it where Unit will find it:

   .. subs-code-block:: console

      $ curl -O https://unit.nginx.org/download/unit-|version|.tar.gz
      $ tar xzf unit-|version|.tar.gz                                  # Puts Unit sources in the unit-|version| subdirectory
      $ cd unit-|version|
      $ ./configure <./configure flags>                            # Configures the build; use the ./configure flags from unitd output
      $ ./configure php --module=php7.3 --config=php-config        # Configures the module itself
      $ make php7.3                                                # Builds the module in the build/ subdirectory
      $ mkdir -p $UNITTMP/unit-php7.3/<module path>                # Use the module path from the ./configure flags
      $ mv build/php7.3.unit.so $UNITTMP/unit-php7.3/<module path> # Adds the module to the package

#. Create a :file:`control` `file
   <https://www.debian.org/doc/debian-policy/ch-controlfields.html>`_ in the
   :file:`$UNITTMP/unit-php7.3/DEBIAN/` directory; list :samp:`unit` with other
   dependencies:

   .. subs-code-block:: control

      Package: unit-php7.3
      Version: |version|
      Comment0: Use Unit package version for consistency: 'apt show unit | grep Version'
      Architecture: amd64
      Comment1: To get current architecture, run 'dpkg --print-architecture'
      Comment2: For a list of other options, run 'dpkg-architecture -L'
      Depends: unit (= |version|), php7.3, libphp-embed
      Comment3: Specify Unit package version to avoid issues when Unit updates
      Comment4: Again, run 'apt show unit | grep Version' to get this value
      Maintainer: Jane Doe <j.doe@example.com>
      Description: Custom PHP 7.3 language module for NGINX Unit |version|

   Save and close the file.

#. Build and install the package:

   .. subs-code-block:: console

      $ dpkg-deb -b $UNITTMP/unit-php7.3
      # dpkg -i $UNITTMP/unit-7.3.deb

#. Finally, restart Unit and check out the log to make sure your module was
   loaded:

   .. code-block:: console

      # systemctl restart unit
      # less /path/to/unit.log

          ...
         [info] discovery started
         [notice] module: <module name and version> "<module path>/php7.3.unit.so"

.. _packaging-rpm:

*************
.rpm Packages
*************

Assuming you are packaging for the current system and have the official Unit
package installed:

#. Make sure to install the :ref:`prerequisites <installation-prereq-build>`
   for the package.  In our example, it's PHP 7.3 on Fedora 30:

   .. code-block:: console

      # yum install -y php-7.3.8
      # yum install php-devel php-embedded

#. Install RPM development tools and prepare the directory structure:

   .. code-block:: console

      # yum install -y rpmdevtools
      $ rpmdev-setuptree

#. Create a :file:`.spec` `file
   <https://rpm-packaging-guide.github.io/#what-is-a-spec-file>`_ for your
   custom package:

   .. code-block:: console

      $ cd ~/rpmbuild/SPECS
      $ rpmdev-newspec unit-php7.3

#. Run :program:`unitd --version` as root and note the :program:`./configure`
   :ref:`flags <installation-config-src>` for later use:

   .. subs-code-block:: console

      # unitd --version

          unit version: |version|
          configured as ./configure <./configure flags>

#. Edit the :file:`unit-php7.3.spec` file as follows (see inline comments for
   details):

   .. subs-code-block:: spec

      Name:           unit-php7.3
      Version:        |version|
      # Use Unit package version for consistency: 'yum info unit | grep Version'
      Release:        1%{?dist}
      Summary:        Custom language module for NGINX Unit

      License:        ASL 2.0
      # Unit uses ASL 2.0; your license depends on the language you are packaging
      URL:            https://example.com
      BuildRequires:  gcc
      BuildRequires:  make
      BuildRequires:  php-devel
      BuildRequires:  php-embedded
      Requires:       unit = |version|
      # Specify Unit package version to avoid issues when Unit updates
      # Again, run 'yum info unit | grep Version' to get this value
      Requires:       php >= 7.3
      Requires:       php-embedded

      %description
      Custom language module for NGINX Unit |version| (https://unit.nginx.org).

      Maintainer: Jane Doe <j.doe@example.com>

      %prep
      curl -O https://unit.nginx.org/download/unit-|version|.tar.gz
      # Downloads Unit sources
      tar --strip-components=1 -xzf unit-|version|.tar.gz
      # Extracts them locally for compilation steps in the %build section

      %build
      ./configure <./configure flags>
      # Configures the build; use the ./configure flags from unitd output
      ./configure php --module=php7.3 --config=php-config
      # Configures the module itself
      make php7.3
      # Builds the module

      %install
      DESTDIR=%{buildroot} make php7.3-install
      # Adds the module to the package

      %files
      %attr(0755, root, root) "<module path>/php7.3.unit.so"
      # Lists the module as package contents to include it in the package build
      # Use the module path from the ./configure flags

   Save and close the file.

#. Build and install the package:

   .. code-block:: console

      $ rpmbuild -bb unit-php7.3.spec

          ...
          Wrote: /home/user/rpmbuild/RPMS/<arch>/unit-php7.3-<version>.<arch>.rpm
          ...

      # yum install -y /home/user/rpmbuild/RPMS/<arch>/unit-php7.3-<version>.<arch>.rpm

#. Finally, restart Unit and check out the log to make sure your module was
   loaded:

   .. code-block:: console

      # systemctl restart unit
      # less /path/to/unit.log

          ...
         [info] discovery started
         [notice] module: <module name and version> "<module path>/php7.3.unit.so"
