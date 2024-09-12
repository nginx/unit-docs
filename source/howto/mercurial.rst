.. |app| replace:: Mercurial
.. |mod| replace:: Python
.. |app-link| replace:: core files
.. _app-link: https://www.mercurial-scm.org/wiki/UnixInstall

#########
Mercurial
#########

To install and run the `Mercurial <https://www.mercurial-scm.org>`_ source
control system using Unit:

#. .. include:: ../include/howto_install_unit.rst

#. .. include:: ../include/howto_install_app.rst

#. Optionally, configure a `repository
   <https://www.mercurial-scm.org/wiki/TutorialInit>`_ or choose an existing
   one, noting its directory path.

#. Unit :ref:`uses WSGI <configuration-python>` to run Python apps, so it
   requires a `wrapper
   <https://www.mercurial-scm.org/repo/hg/file/default/contrib/hgweb.wsgi>`_
   script to publish a |app| repo.  Here, it's **/path/to/app/hgweb.py**
   (note the extension); the **application** callable is the entry
   point:

    .. code-block:: python

       from mercurial.hgweb import hgweb

       # path to a repo or a hgweb config file to serve in UTF-8 (see 'hg help hgweb')
       application = hgweb(":nxt_ph:`/path/to/app/repo/or/config/file <Replace with a real path in your configuration>`".encode("utf-8"))

   This is a very basic script; to elaborate on it, see the
   Mercurial repo publishing `guide
   <https://www.mercurial-scm.org/wiki/PublishingRepositories#hgweb>`_.

#. .. include:: ../include/howto_change_ownership.rst

#. Next, prepare the |app| :ref:`configuration
   <configuration-python>` for Unit (use a real value for **path**):

   .. code-block:: json

      {
          "listeners": {
              "*:80": {
                  "pass": "applications/hg"
              }
          },

          "applications": {
              "hg": {
                  "type": "python",
                  "path": ":nxt_ph:`/path/to/app/ <Path to the WSGI file referenced by the module option; use a real path in your configuration>`",
                  "module": ":nxt_hint:`hgweb <WSGI module basename with extension omitted>`"
              }
          }
      }

#. .. include:: ../include/howto_upload_config.rst

   After a successful update, you can proceed to work with your Mercurial
   repository as usual:

   .. code-block:: console

      $ hg config --edit

   .. code-block:: console

      $ hg clone http://localhost/ project/

   .. code-block:: console

      $ cd project/

   .. code-block:: console

      $ touch hg_rocks.txt

   .. code-block:: console

      $ hg add

   .. code-block:: console

      $ hg commit -m 'Official: Mercurial on Unit rocks!'

   .. code-block:: console

      $ hg push

   .. image:: ../images/hg.png
      :width: 100%
      :alt: Mercurial on Unit - Changeset Screen
