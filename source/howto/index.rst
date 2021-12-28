.. meta::
   :og:description: Run a variety of frameworks and applications, use Unit with
                    Docker, build custom modules, and resolve other issues.

#####
Howto
#####

This section describes various real-life situations and issues that you may
experience with Unit.

.. toctree::
   :hidden:
   :maxdepth: 1

   docker
   source
   ansible
   integration
   certbot
   Language Modules <modules>
   samples
   security
   walkthrough

- :doc:`docker`: Configure a standalone Unit or a Unit-run app in a Docker
  container.

- :doc:`source`: Build Unit and its language modules from source code.

- :doc:`ansible`: Use a third-party Ansible collection to automate Unit
  deployment.

- :doc:`integration`: Front or secure Unit with NGINX.

- :doc:`certbot`: Use EFF's Certbot with Unit to simplify certificate
  manipulation.

- :doc:`modules`: Build new modules or prepare custom packages for
  Unit.

- :doc:`samples`: Reuse sample app configurations for all languages
  supported by Unit.

- :doc:`security`: Recommendations and considerations for hardening Unit.

- :doc:`walkthrough`: Follow an end-to-end guide to application configuration
  in Unit.


.. _howto-frameworks:

**********
Frameworks
**********

With Unit, you can configure a diverse range of applications based on the
following frameworks:

.. toctree::
   :maxdepth: 1

   bottle
   cakephp
   catalyst
   codeigniter
   django
   djangochannels
   express
   fastapi
   flask
   guillotina
   koa
   laravel
   lumen
   pyramid
   quart
   responder
   rails
   sanic
   springboot
   starlette
   symfony
   yii
   zope

************
Applications
************

You can also make use of detailed setup instructions for popular web apps such
as:

.. toctree::
   :maxdepth: 1

   bugzilla
   datasette
   dokuwiki
   drupal
   grafana
   jira
   joomla
   mailman
   matomo
   mediawiki
   mercurial
   modx
   moin
   nextcloud
   opengrok
   phpbb
   plone
   redmine
   reviewboard
   roundcube
   trac
   wordpress

If you are interested in a specific use case not yet listed here, please `post
a feature request <https://github.com/nginx/unit-docs/issues>`_ on GitHub.
