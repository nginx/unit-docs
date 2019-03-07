:orphan:

####
Jira
####

To run `Atlassian Jira <https://www.atlassian.com/software/jira>`_ on Unit,
follow these steps.

.. note::

   Command samples below assume you're using Jira Core 7.13.0.

#. Install :ref:`Unit with Java support <installation-precomp-pkgs>`.

#. Create an installation directory, adding a :samp:`lib` subdirectory to
   download third-party dependencies:

   .. code-block:: console

      # cd /path/to/jira
      # mkdir -p lib
      # cd lib
      # curl http://central.maven.org/maven2/com/atomikos/atomikos-util/3.9.1/atomikos-util-3.9.1.jar -O -C -
      # curl http://central.maven.org/maven2/org/eclipse/jetty/jetty-jndi/9.4.12.v20180830/jetty-jndi-9.4.12.v20180830.jar -O -C -
      # curl http://central.maven.org/maven2/org/eclipse/jetty/jetty-plus/9.4.12.v20180830/jetty-plus-9.4.12.v20180830.jar -O -C -
      # curl http://central.maven.org/maven2/org/eclipse/jetty/jetty-util/9.4.12.v20180830/jetty-util-9.4.12.v20180830.jar -O -C -
      # curl http://central.maven.org/maven2/javax/transaction/jta/1.1/jta-1.1.jar -O -C -
      # curl http://central.maven.org/maven2/com/atomikos/transactions/3.9.1/transactions-3.9.1.jar -O -C -
      # curl http://central.maven.org/maven2/com/atomikos/transactions-api/3.9.1/transactions-api-3.9.1.jar -O -C -
      # curl http://central.maven.org/maven2/com/atomikos/transactions-jdbc/3.9.1/transactions-jdbc-3.9.1.jar -O -C -
      # curl http://central.maven.org/maven2/com/atomikos/transactions-jta/3.9.1/transactions-jta-3.9.1.jar -O -C -
      # curl https://github.com/mar0x/unit-transaction-init/releases/download/1.0/transaction-init-1.0.jar -O -C - -L

#. `Download <https://www.atlassian.com/software/jira/download>`_ and extract
   Jira files:

   .. code-block:: console

      # cd /path/to/jira
      # tar -xzf atlassian-jira-core-7.13.0.tar.gz

#. Patch your Jira configuration, dropping :samp:`env` from the
   :samp:`comp/env/UserTransaction` object path.  This ensures the
   :samp:`UserTransaction` object will be found by your installation:

   .. code-block:: console

      # sed -i -e 's#comp/env/UserTransaction#comp/UserTransaction#g' \
            atlassian-jira-core-7.13.0-standalone/atlassian-jira/WEB-INF/classes/entityengine.xml

#. .. include:: ../include/get-config.rst

   This creates a JSON file with Unit's current settings.  Add a :ref:`listener
   <configuration-listeners>` in :samp:`listeners` and point it to your
   installation directory in :samp:`applications`.  Also, add the following
   options and dependencies:

   .. code-block:: json

      {
          "listeners": {
              "*:8080": {
                  "pass": "applications/jira"
              }
          },

          "applications": {
              "jira": {
                  "working_directory": "/path/to/jira/",
                  "processes": 1,
                  "type": "java",
                  "webapp": "atlassian-jira-core-7.13.0-standalone/atlassian-jira",
                  "options": [
                      "-Djava.awt.headless=true",
                      "-Djavax.accessibility.assistive_technologies= ",
                      "-Djira.home=/path/to/jira/home",
                      "-Dnginx.unit.context.listener=nginx.unit.TransactionInit",
                      "-Xms1024m",
                      "-Xmx1024m"
                  ],
                  "classpath": [
                      "lib/transaction-init-1.0.jar",
                      "lib/atomikos-util-3.9.1.jar",
                      "lib/jta-1.1.jar",
                      "lib/transactions-3.9.1.jar",
                      "lib/transactions-api-3.9.1.jar",
                      "lib/transactions-jdbc-3.9.1.jar",
                      "lib/transactions-jta-3.9.1.jar",
                      "lib/jetty-jndi-9.4.12.v20180830.jar",
                      "lib/jetty-util-9.4.12.v20180830.jar",
                      "lib/jetty-plus-9.4.12.v20180830.jar",
                      "atlassian-jira-core-7.13.0-standalone/lib/hsqldb-1.8.0.5.jar",
                      "atlassian-jira-core-7.13.0-standalone/lib/slf4j-api-1.7.9.jar",
                      "atlassian-jira-core-7.13.0-standalone/lib/slf4j-log4j12-1.7.9.jar",
                      "atlassian-jira-core-7.13.0-standalone/lib/log4j-1.2.16.jar",
                      "atlassian-jira-core-7.13.0-standalone/lib/jcl-over-slf4j-1.7.9.jar"
                   ]
               }
           }
       }

   See :ref:`Java application options <configuration-java>` for details.

   .. note::

      You can't update Jira configuration in Unit after application startup due
      to Jira's own restrictions.

#. Upload the updated configuration:

   .. code-block:: console

      $ curl -X PUT --data-binary @config.json --unix-socket \
             /path/to/control.unit.sock http://localhost/config

   After a successful update, Jira should be available on the listener's IP
   address and port.  Navigate to Jira's URI path (:samp:`http://{IP
   address}:{port}/jira`) to continue setup in your browser:

   .. image:: ../images/jira.png
      :width: 504pt
      :align: center
      :alt: Jira on Unit - Setup Screen
