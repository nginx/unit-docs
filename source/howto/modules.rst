.. include:: ../include/replace.rst

#############################
Working With Language Modules
#############################

Languages supported by Unit fall into these two categories:

- :ref:`External <modules-ext>` (Go, Node.js): Run outside Unit and communicate
  with it via wrapper packages.
- :ref:`Embedded <modules-emb>` (Java, Perl, PHP, Python, Ruby): Execute in
  runtimes that Unit loads at startup.

For any specific language and its version, Unit needs a language module.

.. _modules-ext:

*************************
External Language Modules
*************************

External modules are regular language libraries or packages that you install
like any other.  They provide common web functionality, communicating with Unit
from the app's runspace.

In Go, Unit support is implemented with a package that you :ref:`import
<configuration-external-go>` to your apps.  You can :ref:`install
<installation-go>` the package from the official Unit repository; otherwise,
:ref:`build <installation-go>` it for your version of Go using Unit sources.

In Node.js, Unit is supported by an :program:`npm`-hosted `package
<https://www.npmjs.com/package/unit-http>`__ that you :ref:`require
<configuration-external-nodejs>` in your app code.  You can :ref:`install
<installation-nodejs-package>` the package from the :program:`npm` repository;
otherwise, :ref:`build <installation-nodejs>` it for your version of Node.js
using Unit sources.


.. _modules-emb:

*************************
Embedded Language Modules
*************************

Embedded modules are shared libraries that Unit loads at startup.  Query Unit
to find them in your system:

.. subs-code-block:: console

   # unitd -h             # Run as root to check default log and module paths
          ...

         --log FILE           set log filename
                              default: "/default/path/to/unit.log"

         --modules DIRECTORY  set modules directory name
                              default: "/default/modules/path/"

   $ ps ax | grep unitd   # Check whether the defaults were overridden at launch
         ...
         unit: main v|version| [unitd --log /runtime/path/to/unit.log --modules /runtime/modules/path/ ... ]

   $ ls /path/to/modules

         java.unit.so  perl.unit.so  php.unit.so  python.unit.so  ruby.unit.so

To clarify the module versions, check the :ref:`Unit log <troubleshooting-log>`
to see which modules were loaded at startup:

.. subs-code-block:: console

   # less /path/to/unit.log
         ...
         discovery started
         module: <language> <version> "/path/to/modules/<module name>.unit.so"
         ...

If a language version is not listed, Unit can't run apps that rely on it;
however, you can add new modules:

- If possible, use the official :ref:`language packages
  <installation-precomp-pkgs>` for easy integration and maintenance.

- If you installed Unit via a :ref:`third-party repo
  <installation-community-repos>`, check whether a suitable language package is
  available there.

- If you want a customized yet reusable solution, :ref:`prepare <modules-pkg>`
  your own package to be installed beside Unit.

.. _modules-pkg:

========================
Packaging Custom Modules
========================

There's always a chance that you need to run a language version that isn't yet
available among the official Unit :ref:`packages <installation-precomp-pkgs>`
but still want to benefit from the convenience of a packaged installation.  In
this case, you can build your own package to be installed alongside the
official distribution, adding the latter as a prerequisite.

Here, we are packaging a custom PHP |_| 7.3 :ref:`module
<installation-modules-php>` to be installed next to the official Unit package;
adjust the command samples to your scenario as needed.  For Debian, Ubuntu, and
other :file:`.deb`-based distributions, see the steps :ref:`here
<modules-deb>`; for CentOS, Fedora, RHEL, and other :file:`.rpm`-based
distributions, follow the steps :ref:`here <modules-rpm>`.

.. note::

   For elaborate Unit packaging examples, refer to our packaging system
   `sources <https://hg.nginx.org/unit/file/tip/pkg/>`_.

.. _modules-deb:

.deb Packages
#############

Assuming you are packaging for the current system and have the official Unit
package installed:

#. Make sure to install the :ref:`prerequisites <installation-prereq-build>`
   for the package.  In our example, it's PHP |_| 7.3 on Debian |_| 10:

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
   :ref:`flags <installation-config-src>` for later use, omitting
   :option:`!--ld-opt`:

   .. subs-code-block:: console

      # unitd --version

          unit version: |version|
          configured as ./configure <./configure flags>

#. Download Unit sources, :ref:`configure <installation-src-modules>` and build
   your custom module, then put it where Unit will find it:

   .. subs-code-block:: console

      $ curl -O https://unit.nginx.org/download/unit-|version|.tar.gz
      $ tar xzf unit-|version|.tar.gz                                 # Puts Unit sources in the unit-|version| subdirectory
      $ cd unit-|version|
      $ ./configure <./configure flags w/o --ld-opt>               # Configures the build; use the ./configure flags from unitd output
      $ ./configure php --module=php7.3 --config=php-config        # Configures the module itself
      $ make php7.3                                                # Builds the module in the build/ subdirectory
      $ mkdir -p $UNITTMP/unit-php7.3/<module path>                # Use the module path from the ./configure flags
      $ mv build/php7.3.unit.so $UNITTMP/unit-php7.3/<module path> # Adds the module to the package

#. Create a :file:`control` `file
   <https://www.debian.org/doc/debian-policy/ch-controlfields.html>`__ in the
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

.. _modules-rpm:

.rpm Packages
#############

Assuming you are packaging for the current system and have the official Unit
package installed:

#. Make sure to install the :ref:`prerequisites <installation-prereq-build>`
   for the package.  In our example, it's PHP |_| 7.3 on Fedora |_| 30:

   .. code-block:: console

      # yum install -y php-7.3.8
      # yum install php-devel php-embedded

#. Install RPM development tools and prepare the directory structure:

   .. code-block:: console

      # yum install -y rpmdevtools
      $ rpmdev-setuptree

#. Create a :file:`.spec` `file
   <https://rpm-packaging-guide.github.io/#what-is-a-spec-file>`__ to store
   build commands for your custom package:

   .. code-block:: console

      $ cd ~/rpmbuild/SPECS
      $ rpmdev-newspec unit-php7.3

#. Run :program:`unitd --version` as root and note the :program:`./configure`
   :ref:`flags <installation-config-src>` for later use, omitting
   :option:`!--ld-opt`:

   .. subs-code-block:: console

      # unitd --version

          unit version: |version|
          configured as ./configure <./configure flags>

#. Edit the :file:`unit-php7.3.spec` file, adding the commands that download
   Unit sources, :ref:`configure <installation-src-modules>` and build your
   custom module, then put it where Unit will find it:

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
      ./configure <./configure flags w/o --ld-opt>
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
