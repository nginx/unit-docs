:orphan:

#######
Redmine
#######

#. Install :ref:`Unit with Ruby support <installation-precomp-pkgs>`.

#. Download and install Redmine with `necessary prerequisites
   <https://www.redmine.org/projects/redmine/wiki/RedmineInstall>`_.  Make sure
   your application works:

   .. code-block:: console

      $ cd path/to/redmine
      $ bundle exec rails server webrick -e :nxt_term:`production <Environment name, used for RAILS_ENV in Unit app config>` # refer to Redmine docs for details
      $ curl localhost:3000

   Next, we'll make this installation run on Unit.

#. .. include:: ../include/get-config.rst

   This creates a JSON file with Unit's current settings.  In
   :samp:`listeners`, add a :ref:`listener <configuration-listeners>` that
   points to your app in :samp:`applications`; the app must reference
   the path to Redmine and the Rails environment to use:

   .. code-block:: json

      {
          "listeners": {
              "*:3000": {
                  "pass": "applications/redmine"
              }
          },

          "applications": {
              "redmine": {
                  "type": "ruby",
                  "user": "redmine",
                  "working_directory": ":nxt_term:`/path/to/redmine/ <Where Redmine is installed>`",
                  "script": "config.ru",
                  "environment": {
                      "RAILS_ENV": ":nxt_term:`production<Environment name in Redmine config>`"
                  }
           }
       }

   See :ref:`Ruby application options <configuration-ruby>` for details.

#. Upload the updated configuration:

   .. code-block:: console

      # curl -X PUT --data-binary @config.json --unix-socket \
             /path/to/control.unit.sock http://localhost/config

   After a successful update, Redmine should be available on the listener's IP
   and port:

   .. image:: ../images/redmine.png
      :width: 100%
      :alt: Redmine in Unit - Sample Screen
