.. include:: ../include/replace.rst
.. |app| replace:: Jira
.. |mod| replace:: Java
.. |app-link| replace:: core files
.. _app-link: https://www.atlassian.com/software/jira/update

####
Jira
####

.. note::

   This howto uses the 8.19.1 version; other versions may have different
   dependencies and options.

To run `Atlassian Jira <https://www.atlassian.com/software/jira>`_ using Unit:

#. .. include:: ../include/howto_install_unit.rst

#. .. include:: ../include/howto_install_app.rst

   For example:

   .. code-block:: console

      $ cd :nxt_ph:`/path/to/app/ <Path to the application directory; use a real path in your configuration>`

   .. code-block:: console

      $ curl https://www.atlassian.com/software/jira/downloads/binary/atlassian-jira-software-8.19.1.tar.gz -O -C -

   .. code-block:: console

      $ tar xzf atlassian-jira-core-8.19.1.tar.gz --strip-components 1

#. Download |app|'s third-party dependencies to the **lib** subdirectory:

   .. code-block:: console

      $ cd lib/

   .. code-block:: console

      $ curl https://github.com/mar0x/unit-transaction-init/releases/download/2.0/transaction-init-2.0.jar -O -C -

   .. code-block:: console

      $ curl https://repo1.maven.org/maven2/com/atomikos/atomikos-util/5.0.8/atomikos-util-5.0.8.jar -O -C -

   .. code-block:: console

      $ curl https://repo1.maven.org/maven2/com/atomikos/transactions-api/5.0.8/transactions-api-5.0.8.jar -O -C -

   .. code-block:: console

      $ curl https://repo1.maven.org/maven2/com/atomikos/transactions-jdbc/5.0.8/transactions-jdbc-5.0.8.jar -O -C -

   .. code-block:: console

      $ curl https://repo1.maven.org/maven2/com/atomikos/transactions-jta/5.0.8/transactions-jta-5.0.8.jar -O -C -

   .. code-block:: console

      $ curl https://repo1.maven.org/maven2/com/atomikos/transactions/5.0.8/transactions-5.0.8.jar -O -C -

   .. code-block:: console

      $ curl https://repo1.maven.org/maven2/javax/transaction/jta/1.1/jta-1.1.jar -O -C -

   .. code-block:: console

      $ curl https://repo1.maven.org/maven2/org/eclipse/jetty/jetty-jndi/11.0.6/jetty-jndi-10.0.6.jar -O -C -

   .. code-block:: console

      $ curl https://repo1.maven.org/maven2/org/eclipse/jetty/jetty-plus/11.0.6/jetty-plus-10.0.6.jar -O -C -

   .. code-block:: console

      $ curl https://repo1.maven.org/maven2/org/eclipse/jetty/jetty-util/11.0.6/jetty-util-10.0.6.jar -O -C -

   Later, these **.jar** files will be listed in the **classpath**
   option of the Unit configuration.

#. Patch your |app| configuration, dropping **env** from the
   **comp/env/UserTransaction** object path.  This ensures the
   **UserTransaction** object will be found by your installation:

   .. code-block:: console

      $ cd :nxt_ph:`/path/to/app/ <Path to the application directory; use a real path in your configuration>`

   .. code-block:: console

      $ sed -i 's#comp/env/UserTransaction#comp/UserTransaction#g'  \
            atlassian-jira/WEB-INF/classes/entityengine.xml

#. .. include:: ../include/howto_change_ownership.rst

#. Next, :ref:`put together <configuration-java>` the |app| configuration (use
   real values for **working_directory** and **jira.home**):

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
                  "webapp": "atlassian-jira",
                  ":nxt_hint:`options <Jira-specific startup options>`": [
                      "-Djava.awt.headless=true",
                      "-Djavax.accessibility.assistive_technologies= ",
                      "-Djira.home=:nxt_ph:`/path/to/jira/home/ <Path to your Jira home directory; use a real path in your configuration>`",
                      "-Dnginx.unit.context.listener=nginx.unit.TransactionInit",
                      "-Xms1024m",
                      "-Xmx1024m"
                  ],
                  ":nxt_hint:`classpath <Required third-party dependencies from Step 3>`": [
                      "lib/atomikos-util-5.0.8.jar",
                      "lib/hsqldb-1.8.0.10.jar",
                      "lib/jcl-over-slf4j-1.7.30.jar",
                      "lib/jetty-jndi-10.0.6.jar",
                      "lib/jetty-plus-10.0.6.jar",
                      "lib/jetty-util-10.0.6.jar",
                      "lib/jta-1.1.jar",
                      "lib/log4j-1.2.17-atlassian-3.jar",
                      "lib/slf4j-api-1.7.30.jar",
                      "lib/slf4j-log4j12-1.7.30.jar",
                      "lib/transaction-init-2.0.jar",
                      "lib/transactions-5.0.8.jar",
                      "lib/transactions-api-5.0.8.jar",
                      "lib/transactions-jdbc-5.0.8.jar",
                      "lib/transactions-jta-5.0.8.jar"
                  ]
              }
          }
      }

   See :ref:`Java application options <configuration-java>` for details.

   .. note::

      You can't update the configuration in Unit after startup due to |app|'s
      own restrictions.

#. .. include:: ../include/howto_upload_config.rst

   After a successful update, |app| should be available on the listener's IP
   address and port.  Browse to http://localhost/jira to continue the setup in
   your browser:

   .. image:: ../images/jira.png
      :width: 100%
      :alt: Jira on Unit - Setup Screen
