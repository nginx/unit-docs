#########
Mercurial
#########

To install and run the `Mercurial <https://www.mercurial-scm.org/>`_ source
control system using Unit:

#. Install :ref:`Unit <installation-precomp-pkgs>` with a Python language
   module.

#. Next, `install <https://www.mercurial-scm.org/wiki/UnixInstall>`_ Mercurial
   and configure a `repository
   <https://www.mercurial-scm.org/wiki/TutorialInit>`_ or choose an existing
   one.

#. Unit :ref:`uses WSGI <configuration-python>` to run Python apps, so it
   requires a `wrapper
   <https://www.mercurial-scm.org/repo/hg/file/default/contrib/hgweb.wsgi>`_
   script to publish a Mercurial repo.  Here, it's :file:`/path/to/hg/hgweb.py`
   (note the extension); the :samp:`application` callable is the entry point
   for the app:

    .. code-block:: python

       from mercurial.hgweb import hgweb

       # path to a repo or a hgweb config file to serve (see 'hg help hgweb')
       application = hgweb("/path/to/hg/repo/or/config/file")

    .. note::

       This is a very basic script; to elaborate on it, see the
       Mercurial repo publishing `guide
       <https://www.mercurial-scm.org/wiki/PublishingRepositories#hgweb>`_.

#. Set permissions for the application directory to ensure Unit can access it,
   for example:

   .. code-block:: console

      # chown -R hg_user:hg_group /path/to/hg/  # user:group for app config in Unit

#. Finally, prepare and upload the app :ref:`configuration
   <configuration-python>` to Unit (note the use of :samp:`path`):

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
                  "path": ":nxt_term:`/path/to/hg/ <Path to WSGI file referenced by the module option>`",
                  "user": ":nxt_term:`hg_user <Username that Unit runs the app as, with access to /path/to/hg/>`",
                  "module": ":nxt_term:`hgweb <WSGI module name, not a filename>`"
              }
          }
      }

   Assuming the config above is saved as :file:`hg.json`:

   .. code-block:: console

      # curl -X PUT --data-binary @hg.json --unix-socket \
             :nxt_term:`/path/to/control.unit.sock <Path to Unit control socket in your installation>` http://localhost/config

#. After a successful update, you can proceed to work with your Mercurial
   repository as usual:

   .. code-block:: console

      $ hg config --edit
      $ hg clone http://localhost/ project/
      $ cd project/
      $ touch hg_rocks.txt
      $ hg add
      $ hg commit -m 'Official: Mercurial on Unit rocks!'
      $ hg push

   .. image:: ../images/hg.png
      :width: 100%
      :alt: Mercurial on Unit - Changeset Screen
