:orphan:

#################
Unit 1.7 Released
#################

Hi,

I'm glad to announce a new release of NGINX Unit.

This is a bugfix release with a primary focus on the stabilization of
the Node.js module.  We have made great progress with it, and now Node.js
support is in much better shape than before.

.. code-block:: none

   Changes with Unit 1.7                                            20 Dec 2018

       *) Change: now rpath is set in Ruby module only if the library was not
          found in default search paths; this allows to meet packaging
          restrictions on some systems.

       *) Bugfix: "disable_functions" and "disable_classes" PHP options set via
          Control API did not work.

       *) Bugfix: Promises on request data in Node.js were not triggered.

       *) Bugfix: various compatibility issues with Node.js applications.

       *) Bugfix: a segmentation fault occurred in Node.js module if
          application tried to read request body after request.end() was
          called.

       *) Bugfix: a segmentation fault occurred in Node.js module if
          application attempted to send header twice.

       *) Bugfix: names of response header fields in Node.js module were
          erroneously treated as case-sensitive.

       *) Bugfix: uncatched exceptions in Node.js were not logged.

       *) Bugfix: global install of Node.js module from sources was broken on
          some systems; the bug had appeared in 1.6.

       *) Bugfix: traceback for exceptions during initialization of Python
          applications might not be logged.

       *) Bugfix: PHP module build failed if PHP interpreter was built with
          thread safety enabled.

Highly likely, this is the last release of Unit in 2018, so I would like to
wish you a Happy New Year on the behalf of the entire Unit team.

2018 was an exciting year in Unit development.  Many important features have
been introduced, including:

- Advanced Process Management, which allows scaling application processes
  dynamically depending on the amount of load.  Thanks go to Maxim Romanov
  who primarily worked on this feature.

  Documentation: https://unit.nginx.org/configuration/#process-management

- Perl, Ruby, and Node.js application support.  Thanks to Alexander Borisov
  who implemented these language modules.

- TLS support and Certificates Storage API that allows to dynamically
  configure TLS certificates.  Thanks to Igor Sysoev who collaborated with
  me on this feature.

  Documentation: https://unit.nginx.org/certificates/

- C API language modules were moved into a separate library; this helped a lot
  with Node.js integration and aids the upcoming Java support.  Thanks again
  to Maxim Romanov for this work.

- Essential access logging support.
  Documentation: https://unit.nginx.org/configuration/#access-log

- Advanced settings for applications including environment variables, runtime
  arguments, PHP options, and php.ini path customization.

I can’t imagine releasing any of these features without the effort of our QA
engineer, Andrey Zelenkov, who relentlessly improves test coverage of Unit
codebase, runs various fuzzing tests, and reports any suspicious behaviour
to the developers.

In addition, one of the most important achievements of the year was a tangible
improvement of documentation quality.  The unit.nginx.org website is up-to-date
now and covers all the features introduced in the new and previous Unit
releases.  This duty was successfully carried out by our technical writer,
Artem Konev.

Besides, he continues refactoring the documentation and plans to introduce
HowTos for various use cases and applications.  If you have any particular
suggestions concerning applications you’d like to configure with Unit,
please create a feature request in our documentation issue tracker on GitHub:
https://github.com/nginx/unit-docs/issues

Thanks to our system engineers, Andrei Belov and Konstantin Pavlov, who are
toiling over packages in our own repositories and images in Docker hub.

Thanks to our product manager Nick Shadrin who helps us to envision our
strategy and gives excellent talks on conferences around the world.
You can see him in the latest Unit demo session at NGINX Conf 2018:
https://www.youtube.com/watch?v=JQZKbIG3uro

Of course, everything I’ve just mentioned wouldn’t be possible without our
vibrant community; our users who are eager to move their projects to Unit;
everyone who reports bugs and suggests features, guiding us to the right path.
We urge everybody to participate via our mailing list at unit/at/nginx.org or
on GitHub: https://github.com/nginx/unit

I gladly mention 洪志道 (Hong Zhi Dao) as one of the most active community
members who not only reports bugs but also reads our code, asks pointed
questions, and regularly sends patches with improvements.  Thank you very much
for your contribution.

Special thanks go to the maintainers of Unit packages in various community
repositories: Sergey A. Osokin (FreeBSD), Ralph Seichter (Gentoo), André
Klitzing (Alpine Linux), and Julian Brost (Arch Linux).  Sorry if I didn't
mention anyone else who maintains Unit packages for other distributions; you
can open an issue for your repository to be included in the Installation
section at unit.nginx.org: https://github.com/nginx/unit-docs/issues

Unfortunately, we weren’t able to achieve each and every of our audacious
goals this year.  The development of some features is postponed until
the upcoming year.

Currently, there is ongoing work on WebSocket support, the Java module,
request routing, and static files serving.

We have already made good progress on the Java module.  This work is underway
in a separate GitHub public `repository <https://github.com/mar0x/unit>`__, so
everybody willing to run their Java applications on Unit can participate.

Many other good things and announcements about Unit will surely happen in 2019.
Thank you for staying with us, and all the best.

wbr, Valentin V. Bartenev
