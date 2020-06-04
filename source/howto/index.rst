e. meta::
   :og:description: Run a variety of frameworks and applications, use Unit with Docker, build custom modules, and resolve other issues.

#####
Howto
#####


This section describes various real-life situations and issues that you may
experience with Unit.

**************
App Frameworks
**************

With Unit, you can configure a diverse range of applications based on the
following frameworks:

.. toctree::
   :maxdepth: 1

   cakephp
   catalyst
   django
   express
   flask
   symfony
   yii

************
Applications
************

You can also make use of detailed setup instructions for popular web apps such
as:

.. toctree::
   :maxdepth: 1

   bugzilla
   grafana
   jira
   joomla
   mediawiki
   mercurial
   moin
   nextcloud
   phpbb
   redmine
   trac
   wordpress

*************
Miscellaneous
*************

.. toctree::
   :hidden:
   :maxdepth: 1

   docker
   integration
   Language Modules <modules>
   samples
   walkthrough

- :doc:`docker`: Configure standalone Unit or a Unit-run app in a Docker
  container.

- :doc:`integration`: Run Unit with load balancing, proxying, and
  enhanced security.

- :doc:`modules`: Building new modules and preparing custom packages for
  Unit.

- :doc:`samples`: Sample app configuration instructions for all languages
  supported by Unit.

- :doc:`walkthrough`: A step-by-step guide to application configuration
  in Unit.

If you are interested in a specific use case not yet listed here, please `post
a feature request <https://github.com/nginx/unit-docs/issues>`_ on GitHub.
