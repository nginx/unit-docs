:orphan:

####################
Unit 1.14.0 Released
####################

Hi,

I'm glad to announce a new release of NGINX Unit.

Besides improving the request routing abilities, this release simplifies
operations concerning the Go module.  Now it can also be installed with the
:program:`go get` command:

.. code-block:: console

   $ go get unit.nginx.org/go

Mind, however, that it requires the :program:`unit-dev/unit-devel` `package
<https://unit.nginx.org/installation/#official-packages>`__.

Great effort went into improving the efficiency and avoiding memory bloat in
cases where an application generates gigabytes of response body.  Now Unit can
deal with that without much hassle.  We will continue improving the performance
and increasing efficiency, as this is one of our primary priorities.

.. code-block:: none

   Changes with Unit 1.14.0                                         26 Dec 2019

       *) Change: the Go package import name changed to "unit.nginx.org/go".

       *) Change: Go package now links to libunit instead of including library
          sources.

       *) Feature: ability to change user and group for isolated applications
          when Unit daemon runs as an unprivileged user.

       *) Feature: request routing by source and destination addresses and
          ports.

       *) Bugfix: memory bloat on large responses.


We also updated our Docker images and switched them from Debian 9 to 10 as the
base, so the language module versions have been updated respectively:
https://unit.nginx.org/installation/#docker-images

Python 3.6 module packages were added to CentOS and RHEL 7 repositories,
and Python 3.7 package was added to Amazon Linux 2 LTS.  Please note that
the name of Python 2.7 package in these repositories was changed from
:program:`unit-python` to :program:`unit-python27`.

The Go package now has the same name :program:`unit-go` across all our
repositories and depends on :program:`unit-dev`.

This is the last release of 2019, so I'll use this opportunity to wish
a Happy New Year to our strong community.  Thank you for your requests,
bug reports, ideas, and suggestions.  Everything that we do, we primarily
do for you, our users.

This year, we made 8 releases, with 427 commits to the repository, where 65242
lines were added and 8219 removed.  The biggest features of the year are:

- Support for Java Servlet Containers, which means that now Unit supports
  7 languages

- Advanced internal request routing that allows to filter requests by various
  parameters, including: URI, header fields, arguments, cookies, addresses,
  and ports

- Built-in WebSocket server offloading for Node.js and Java

- Isolation of application processes

- Serving of static files

- Reverse proxying

These features establish a firm basis for further development of Unit as a
general-purpose web server that is able to perform absolutely any task related
to handling and processing web protocols in the most efficient way.  This is
our ultimate goal, and we are eager to achieve it over the coming years.

I'd like to thank everyone who worked hard with me on Unit through the year:

- Andrei Belov - system engineer, who maintained repositories and prepared
  packages

- Andrei Zeliankou - QA engineer, who wrote functional tests and ran fuzzing

- Artem Konev - technical writer, who wrote documentation and blog posts,
  improved the website, and sometimes helped us to arrange
  words in sentences the right way

- Axel Duch - junior developer, who improved request routing

- Igor Sysoev - senior developer and architect, who worked on request routing,
  proxying, and many internal aspects

- Konstantin Pavlov - system engineer, who prepared Docker images and packages

- Maxim Romanov - senior developer, who worked on Java, WebSockets,
  and internal IPC

- Tiago Natel de Moura - senior developer, who worked on isolation features

Thank you guys, I'm happy to work with you.

wbr, Valentin V. Bartenev
