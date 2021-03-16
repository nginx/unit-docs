.. include:: ../include/replace.rst
.. |app| replace:: Jira
.. |mod| replace:: Java
.. |app-link| replace:: core files
.. _app-link: https://www.atlassian.com/software/jira/download


####
Jira
####

.. note::

   Command samples below assume you're using |app| |_| Core |_| 7.13.0.

To run `Atlassian Jira <https://www.atlassian.com/software/jira>`_ using Unit:

#. .. include:: ../include/howto_install_unit.rst

#. .. include:: ../include/howto_install_app.rst

   For example:

   .. code-block:: console

      $ cd :nxt_ph:`/path/to/app/ <Path to the application directory; use a real path in your configuration>`
      $ tar xzf atlassian-jira-core-7.13.0.tar.gz

#. Add a :samp:`lib` subdirectory to download third-party dependencies:

   .. code-block:: console

      $ mkdir /path/to/app/lib/ && cd /path/to/app/lib/
      $ curl http://central.maven.org/maven2/com/atomikos/atomikos-util/3.9.1/atomikos-util-3.9.1.jar -O -C -
      $ curl http://central.maven.org/maven2/org/eclipse/jetty/jetty-jndi/9.4.12.v20180830/jetty-jndi-9.4.12.v20180830.jar -O -C -
      $ curl http://central.maven.org/maven2/org/eclipse/jetty/jetty-plus/9.4.12.v20180830/jetty-plus-9.4.12.v20180830.jar -O -C -
      $ curl http://central.maven.org/maven2/org/eclipse/jetty/jetty-util/9.4.12.v20180830/jetty-util-9.4.12.v20180830.jar -O -C -
      $ curl http://central.maven.org/maven2/javax/transaction/jta/1.1/jta-1.1.jar -O -C -
      $ curl http://central.maven.org/maven2/com/atomikos/transactions/3.9.1/transactions-3.9.1.jar -O -C -
      $ curl http://central.maven.org/maven2/com/atomikos/transactions-api/3.9.1/transactions-api-3.9.1.jar -O -C -
      $ curl http://central.maven.org/maven2/com/atomikos/transactions-jdbc/3.9.1/transactions-jdbc-3.9.1.jar -O -C -
      $ curl http://central.maven.org/maven2/com/atomikos/transactions-jta/3.9.1/transactions-jta-3.9.1.jar -O -C -
      $ curl https://github.com/mar0x/unit-transaction-init/releases/download/1.0/transaction-init-1.0.jar -O -C - -L

   Later, these :file:`.jar` files will be listed in the :samp:`classpath`
   option of the Unit configuration.

#. Patch your |app| configuration, dropping :samp:`env` from the
   :samp:`comp/env/UserTransaction` object path.  This ensures the
   :samp:`UserTransaction` object will be found by your installation:

   .. code-block:: console

      $ sed -i 's#comp/env/UserTransaction#comp/UserTransaction#g' \
            atlassian-jira-core-7.13.0-standalone/atlassian-jira/WEB-INF/classes/entityengine.xml

#. .. include:: ../include/howto_change_ownership.rst

#. Next, :ref:`put together <configuration-java>` the |app| configuration (use
   a real value for :samp:`working_directory`):

   .. code-block:: json

      {
          "listeners": {
              "*:80": {
                  "pass": "applications/jira"
              }
          },

          "applications": {
              "jira": {
                  "type": "java",
                  "working_directory": ":nxt_ph:`/path/to/app/ <Path to the application directory; use a real path in your configuration>`",
                  "webapp": "atlassian-jira-core-7.13.0-standalone/atlassian-jira",
                  ":nxt_hint:`options <App-specific startup options>`": [
                      "-Djava.awt.headless=true",
                      "-Djavax.accessibility.assistive_technologies= ",
                      "-Djira.home=/path/to/jira/home",
                      "-Dnginx.unit.context.listener=nginx.unit.TransactionInit",
                      "-Xms1024m",
                      "-Xmx1024m"
                  ],
                  ":nxt_hint:`classpath <Required dependencies>`": [
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

      You can't update |app| configuration in Unit after application startup
      due to its own restrictions.

#. .. include:: ../include/howto_upload_config.rst

   After a successful update, |app| should be available on the listener's IP
   address and port.  Browse to http://localhost/jira to continue the setup in
   your browser:

   .. image:: ../images/jira.png
      :width: 100%
      :alt: Jira on Unit - Setup Screen
