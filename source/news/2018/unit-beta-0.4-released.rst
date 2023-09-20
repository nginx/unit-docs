:orphan:

######################
Unit Beta 0.4 Released
######################

Hello,

I'm glad to announce a new beta of NGINX Unit.  This is mostly bugfix release
in order to eliminate significant regressions in the previous version.

.. code-block:: none

   Changes with Unit 0.4                                            15 Jan 2018

       *) Feature: compatibility with DragonFly BSD.

       *) Feature: "configure php --lib-static" option.

       *) Bugfix: HTTP request body was not passed to application; the bug had
          appeared in 0.3.

       *) Bugfix: HTTP large header buffers allocation and deallocation fixed;
          the bug had appeared in 0.3.

       *) Bugfix: some PHP applications might not work with relative "root"
          path.

You can find links to the source code and precompiled Linux packages here:
https://unit.nginx.org/installation/

Internally, we use Buildbot to build each commit and run tests on a large
number of systems.  We also use various static analysis tools to improve
code quality and check tests coverage.

There is ongoing work on functional tests framework that will allow to avoid
such regressions in the future.  And there are plans to add fuzz testing.

You can learn more about recent Unit changes in this detailed blogpost:
https://www.nginx.com/blog/unit-0-3-beta-release-available-now/

Besides that, please welcome Alexander Borisov who's joined our Unit dev
team today.  His first task is going to be adding Perl/PSGI support.

wbr, Valentin V. Bartenev
