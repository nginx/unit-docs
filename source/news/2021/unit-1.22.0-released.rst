:orphan:

####################
Unit 1.22.0 Released
####################

Hi,

I'm glad to announce a new release of NGINX Unit.

This is our first release of 2021, and it focuses on improving stability.
There's an extensive list of bugfixes, although many occur in rare conditions
that have so far been observed only in our test environments.  These bugs
were caught due to improvements in our continuous functional testing; our QA,
Andrei Zeliankou, is always looking to increase the testing coverage and use
new techniques to spot various race conditions and leaks, thus improving
the quality of each release.  This very important work never ends.


*********************************************
IMPORTANT: Changes to Official Linux Packages
*********************************************

Starting with this release, the user and group accounts that run non-privileged
Unit processes are changed in our Linux packages:

- in previous packages: :samp:`nobody:nobody`
- in 1.22.0 and later:  :samp:`unit:unit`

These settings are used to serve static files and run applications if
:samp:`user` or :samp:`group` options are not explicitly specified in the app
configuration.

Please take a note of the change and update your configuration appropriately
before upgrading an existing Unit installation with our official packages:
https://unit.nginx.org/installation/#official-packages

The rationale for this change in our packages was that using :samp:`nobody` by
default was very inconvenient while serving static files.  You can always
override these settings with the :option:`!--user` and :option:`!--group`
daemon options in your startup scripts.  See here for more details:
https://unit.nginx.org/howto/source/#startup-and-shutdown


**********************************************
IMPORTANT 2: Changes to official Docker images
**********************************************

Another notable change is also related to our official distributions; in
this case, it affects our Docker images.  Many asked us to provide the most
up-to-date versions of language modules in our Docker images, but there was
no maintainable way of doing this while still relying on the Debian base
image we used before.

Starting with 1.22.0, we stop maintaining images with language modules that use
the old Debian base; instead, now we rely on official Docker images for latest
language versions: https://unit.nginx.org/installation/#docker-images

Our images are available at both Docker Hub and Amazon ECR Public Gallery;
you can also download them at our website.

.. code-block:: none

   Changes with Unit 1.22.0                                         04 Feb 2021

       *) Feature: the ServerRequest and ServerResponse objects of Node.js
          module are now compliant with Stream API.

       *) Feature: support for specifying multiple directories in the "path"
          option of Python apps.

       *) Bugfix: a memory leak occurred in the router process when serving
          files larger than 128K; the bug had appeared in 1.13.0.

       *) Bugfix: apps could stop processing new requests under high load; the
          bug had appeared in 1.19.0.

       *) Bugfix: app processes could terminate unexpectedly under high load;
          the bug had appeared in 1.19.0.

       *) Bugfix: invalid HTTP responses were generated for some unusual status
          codes.

       *) Bugfix: the PHP_AUTH_USER, PHP_AUTH_PW, and PHP_AUTH_DIGEST server
          variables were missing in the PHP module.

       *) Bugfix: the router process could crash with multithreaded apps under
          high load.

       *) Bugfix: Ruby apps with multithreading configured could crash on start
          under load.

       *) Bugfix: mount points weren't unmounted when the "mount" namespace
          isolation was used; the bug had appeared in 1.21.0.

       *) Bugfix: the router process could crash while removing or
          reconfiguring an app that used WebSocket.

       *) Bugfix: a memory leak occurring in the router process when removing
          or reconfiguring an application; the bug had appeared in 1.19.0.


Meanwhile, we continue working on metrics and application restart APIs, SNI
support in TLS, and improvements to process isolation.

As always, we encourage you to follow our roadmap on GitHub, where your ideas
and requests are more than welcome: https://github.com/orgs/nginx/projects/1

Stay tuned!

wbr, Valentin V. Bartenev
