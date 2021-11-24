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
<configuration-go>` to your apps.  You can :ref:`install
<installation-go-package>` the package from the official Unit repository;
otherwise, :ref:`build <howto/source-modules-go>` it for your version of Go
using Unit's sources.

In Node.js, Unit is supported by an :program:`npm`-hosted `package
<https://www.npmjs.com/package/unit-http>`__ that you :ref:`require
<configuration-nodejs>` in your app code.  You can :ref:`install
<installation-nodejs-package>` the package from the :program:`npm` repository;
otherwise, :ref:`build <howto/source-modules-nodejs>` it for your version of
Node.js using Unit's sources.


.. _modules-emb:

*************************
Embedded Language Modules
*************************

Embedded modules are shared libraries that Unit loads at startup.  Query Unit
to find them in your system:

.. subs-code-block:: console

   $ unitd -h

          ...
         --log FILE           set log filename
                              default: ":nxt_ph:`/default/path/to/unit.log <This is the default log path which can be overridden at runtime>`"

         --modules DIRECTORY  set modules directory name
                              default: ":nxt_ph:`/default/modules/path/ <This is the default modules path which can be overridden at runtime>`"

   $ :nxt_hint:`ps ax | grep unitd <Check whether the defaults were overridden at launch>`
         ...
         unit: main v|version| [unitd --log :nxt_ph:`/runtime/path/to/unit.log <If this option is set, its value is used at runtime>` --modules :nxt_ph:`/runtime/modules/path/ <If this option is set, its value is used at runtime>` ... ]

   $ ls :nxt_ph:`/path/to/modules <Use runtime value if the default was overridden>`

         java.unit.so  perl.unit.so  php.unit.so  python.unit.so  ruby.unit.so

To clarify the module versions, check the :ref:`Unit log <troubleshooting-log>`
to see which modules were loaded at startup:

.. subs-code-block:: console

   # less :nxt_ph:`/path/to/unit.log <Path to log can be determined in the same manner as above>`
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
<howto/source-modules-php>` to be installed next to the official Unit package;
adjust the command samples as needed to fit your scenario.

.. note::

   For details of building Unit language modules, see the source code
   :ref:`howto <source-modules>`; it also describes building
   :doc:`Unit <source>` itself.  For more packaging examples, see our package
   `sources <https://hg.nginx.org/unit/file/tip/pkg/>`_.

..
   Legacy anchors to preserve existing external links.
.. _modules-deb:
.. _modules-rpm:

.. tabs::
   :prefix: packages
   :toc:

   .. tab:: .deb

      Assuming you are packaging for the current system and have the official
      Unit package installed:

      #. Make sure to install the :ref:`prerequisites
         <source-prereq-build>` for the package.  In our example,
         it's PHP |_| 7.3 on Debian |_| 10:

         .. code-block:: console

            # apt update
            # apt install :nxt_hint:`ca-certificates apt-transport-https debian-archive-keyring <Needed to install the php7.3 package from the PHP repo>`
            # curl --output /usr/share/keyrings/php-keyring.gpg  \
                  :nxt_hint:`https://packages.sury.org/php/apt.gpg <Adding the repo key to make it usable>`
            # echo "deb [signed-by=/usr/share/keyrings/php-keyring.gpg]  \
                  https://packages.sury.org/php/ buster main" > /etc/apt/sources.list.d/php.list
            # apt update
            # apt install php7.3
            # apt install :nxt_hint:`php-dev libphp-embed <Needed to build the module and the package>`

      #. Create a staging directory for your package:

         .. subs-code-block:: console

            $ export UNITTMP=$(mktemp -d -p /tmp -t unit.XXXXXX)
            $ mkdir -p $UNITTMP/unit-php7.3/DEBIAN
            $ cd $UNITTMP

         This creates a folder structure fit for :program:`dpkg-deb`; the
         :file:`DEBIAN` folder will store the package definition.

      #. Run :program:`unitd --version` and note the :program:`./configure`
         :ref:`flags <source-config-src>` for later use, omitting
         :option:`!--ld-opt`:

         .. subs-code-block:: console

            $ unitd --version

                unit version: |version|
                configured as ./configure :nxt_ph:`FLAGS <Note the flags, omitting --ld-opt>`

      #. Download Unit's sources, :ref:`configure <source-modules>`
         and build your custom module, then put it where Unit will find it:

         .. subs-code-block:: console

            $ curl -O https://unit.nginx.org/download/unit-|version|.tar.gz
            $ tar xzf unit-|version|.tar.gz                                 # Puts Unit's sources in the unit-|version| subdirectory
            $ cd unit-|version|
            $ ./configure :nxt_ph:`FLAGS W/O --LD-OPT <The ./configure flags, except for --ld-opt>`                             # Use the ./configure flags noted in the previous step
            $ ./configure php --module=php7.3 --config=php-config        # Configures the module itself
            $ make php7.3                                                # Builds the module in the build/ subdirectory
            $ mkdir -p $UNITTMP/unit-php7.3/:nxt_ph:`MODULESPATH <Path to Unit's language modules>`                  # Use the module path set by ./configure or by default
            $ mv build/php7.3.unit.so $UNITTMP/unit-php7.3/:nxt_ph:`MODULESPATH <Path to Unit's language modules>`   # Adds the module to the package

      #. Create a :file:`$UNITTMP/unit-php7.3/DEBIAN/control` `file
         <https://www.debian.org/doc/debian-policy/ch-controlfields.html>`__,
         listing :samp:`unit` with other dependencies:

         .. subs-code-block:: control

            Package: unit-php7.3
            Version: |version|
            Comment0: Use Unit's package version for consistency: 'apt show unit | grep Version'
            Architecture: amd64
            Comment1: To get current architecture, run 'dpkg --print-architecture'
            Comment2: For a list of other options, run 'dpkg-architecture -L'
            Depends: unit (= |version|-1~buster), php7.3, libphp-embed
            Comment3: Specify Unit's package version to avoid issues when Unit updates
            Comment4: Again, run 'apt show unit | grep Version' to get this value
            Maintainer: Jane Doe <j.doe@example.com>
            Description: Custom PHP 7.3 language module for NGINX Unit |version|

         Save and close the file.

      #. Build and install the package:

         .. subs-code-block:: console

            $ dpkg-deb -b $UNITTMP/unit-php7.3
            # dpkg -i $UNITTMP/unit-php7.3.deb


   .. tab:: .rpm

      Assuming you are packaging for the current system and have the official
      Unit package installed:

      #. Make sure to install the :ref:`prerequisites
         <source-prereq-build>` for the package.  In our example,
         it's PHP |_| 7.3 on Fedora |_| 30:

         .. code-block:: console

            # yum install -y php-7.3.8
            # yum install php-devel php-embedded

      #. Install RPM development tools and prepare the directory structure:

         .. code-block:: console

            # yum install -y rpmdevtools
            $ rpmdev-setuptree

      #. Create a :file:`.spec` `file
         <https://rpm-packaging-guide.github.io/#what-is-a-spec-file>`__
         to store build commands for your custom package:

         .. code-block:: console

            $ cd ~/rpmbuild/SPECS
            $ rpmdev-newspec unit-php7.3

      #. Run :program:`unitd --version` and note the :program:`./configure`
         :ref:`flags <source-config-src>` for later use, omitting
         :option:`!--ld-opt`:

         .. subs-code-block:: console

            $ unitd --version

                unit version: |version|
                configured as ./configure :nxt_ph:`FLAGS <Note the flags, omitting --ld-opt>`

      #. Edit the :file:`unit-php7.3.spec` file, adding the commands that
         download Unit's sources, :ref:`configure
         <source-modules>` and build your custom module, then
         put it where Unit will find it:

         .. subs-code-block:: spec

            Name:           unit-php7.3
            Version:        |version|
            # Use Unit's package version for consistency: 'yum info unit | grep Version'
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
            # Specify Unit's package version to avoid issues when Unit updates
            # Again, run 'yum info unit | grep Version' to get this value
            Requires:       php >= 7.3
            Requires:       php-embedded

            %description
            Custom language module for NGINX Unit |version| (https://unit.nginx.org).

            Maintainer: Jane Doe <j.doe@example.com>

            %prep
            curl -O https://unit.nginx.org/download/unit-|version|.tar.gz
            # Downloads Unit's sources
            tar --strip-components=1 -xzf unit-|version|.tar.gz
            # Extracts them locally for compilation steps in the %build section

            %build
            ./configure :nxt_ph:`FLAGS W/O --LD-OPT <The ./configure flags, except for --ld-opt>`
            # Configures the build; use the ./configure flags noted in the previous step
            ./configure php --module=php7.3 --config=php-config
            # Configures the module itself
            make php7.3
            # Builds the module

            %install
            DESTDIR=%{buildroot} make php7.3-install
            # Adds the module to the package

            %files
            %attr(0755, root, root) ":nxt_ph:`MODULESPATH <Path to Unit's language modules>`/php7.3.unit.so"
            # Lists the module as package contents to include it in the package build
            # Use the module path set by ./configure or by default

         Save and close the file.

      #. Build and install the package:

         .. code-block:: console

            $ rpmbuild -bb unit-php7.3.spec

                ...
                Wrote: /home/user/rpmbuild/RPMS/<arch>/unit-php7.3-<moduleversion>.<arch>.rpm
                ...

            # yum install -y /home/user/rpmbuild/RPMS/<arch>/unit-php7.3-<moduleversion>.<arch>.rpm
