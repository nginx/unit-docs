:orphan:

.. include:: ../include/replace.rst

###########
Walkthrough
###########

OK, so you've decided to give Unit a try with your web app of choice.  You may
be looking for ways to run it faster with less config overhead, streamline your
technology stack, or simply be tech-curious.  In any case:

.. list-table::
   :header-rows: 1
   :widths: 50 50

   * - Step
     - Things to do

   * - **Check the prerequisites**
     - #. Verify that Unit :ref:`supports <installation-prereqs>` your
          platform and app language version.

       #. If possible, check how your app runs beside Unit to avoid confusion.

   * - **Get Unit in your system**

     - #. Install Unit with the language modules you need.  Your options:

          - Official :samp:`.deb/.rpm` :ref:`packages
            <installation-precomp-pkgs>`
          - Docker :ref:`images <installation-docker>`
          - Third-party :ref:`packages <installation-community-repos>`
          - Source :ref:`build <installation-src>`

       #. Configure and launch Unit in your system:

          - Our own and third-party packages :ref:`rely on
            <installation-precomp-startup>` :program:`systemctl` or
            :program:`service`.
          - Containerized Unit can be :doc:`run <docker>` with common
            :program:`docker` commands.
          - If none of the above applies, customize Unit :ref:`startup
            <installation-startup>` manually.

   * - **Prepare** |_| **the** |_| **app** |_| **for** |_| **Unit**

     - #. *(Only applies to Go/Node.js)* :ref:`Patch <configuration-external>`
          your app to run in Unit.

       #. Choose :ref:`common <configuration-applications>` options such as
          app type, working directory, user/group.

       #. Add :ref:`language-specific <configuration-external>`
          settings such as index, entry module, or executable.

   * - **Plug the app into Unit**

     - #. *(Optional)* Add Unit-wide :ref:`settings <configuration-stngs>` to
          your app's config to run it smoothly.

       #. :ref:`Upload <configuration-mgmt>` your config into Unit to spin up
          the app.

       #. *(Optional)* Set up a :ref:`route <configuration-routes>` to your app
          to benefit from internal routing.

       #. *(Optional)* Upload a :ref:`certificate bundle <configuration-ssl>`
          if you want to support SSL/TLS.

       #. Finally, set up a :ref:`listener <configuration-listeners>` to make
          your app publicly available.

For details of each step, see specific documentation sections.
