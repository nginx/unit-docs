:orphan:

####################
Unit 1.18.0 Released
####################

Hi,

I'm glad to announce a new release of NGINX Unit.

This release includes a few internal routing improvements that simplify some
configurations and a new isolation option for chrooting application processes
called :samp:`rootfs`.

.. code-block:: none

   Changes with Unit 1.18.0                                        28 May 2020

       *) Feature: the "rootfs" isolation option for changing root filesystem
          for an application.

       *) Feature: multiple "targets" in PHP applications.

       *) Feature: support for percent encoding in the "uri" and "arguments"
          matching options and in the "pass" option.


Also, our official packages for the recently released Ubuntu 20.04 (Focal Fossa)
are available now: https://unit.nginx.org/installation/#ubuntu

At least two of the features in this release deserve special attention.


****************************
Changing The Root Filesystem
****************************

Security is our top priority, so let's look closer at the :samp:`rootfs`
option first.

The coolest thing about it is that it's not just a simple :program:`chroot()`
system call as some may expect.  It's not a secret that :program:`chroot()` is
not intended for security purposes, and there's plenty of ways for an attacker
to get out of the chrooted directory (just check "man 2 chroot").  That's why
on modern systems Unit can use :program:`pivot_root()` with the :samp:`mount`
namespace isolation enabled, which is way more secure and pretty similar to
putting your application in an individual container.

Also, our goal is to make any security option as easy to use as possible.
In this case, Unit automatically tries to mount all the necessary
language-specific dependencies inside a new root, so you won't need
to care about them.  Currently, this capability works for selected languages
only, but the support will be extended in the next releases.

For more information and examples of :samp:`rootfs` usage, check the
documentation: https://unit.nginx.org/configuration/#process-isolation

Now to the second feature...


**********************************
Multiple PHP Application "Targets"
**********************************

The other major update in this release is called :samp:`targets`, aiming to
simplify configuration for many PHP applications.  Perhaps, it is best
illustrated by an example: WordPress.  This is one of many applications that
use two different addressing schemes:

1. Most user requests are handled by :file:`index.php` regardless of the actual
   request URI.

2. Administration interface and some components rely on direct requests
   to specific :file:`.php` scripts named in the URI.

Earlier, users had to configure two Unit applications to handle this disparity:

.. code-block:: json

   {
       "wp_index": {
           "type": "php",
           "user": "wp_user",
           "group": "wp_user",
           "root": "/path/to/wordpress/",
           "script": "index.php"
       },

       "wp_direct": {
           "type": "php",
           "user": "wp_user",
           "group": "wp_user",
           "root": "/path/to/wordpress/"
       }
   }

The first app directly executes the :file:`.php` scripts named by the URI,
whereas the second one passes all requests to :file:`index.php`.

Now, you can use :samp:`targets` instead:

.. code-block:: json

   {
       "wp": {
           "type": "php",
           "user": "wp_user",
           "group": "wp_user",

           "targets": {
               "index": {
                   "root": "/path/to/wordpress/",
                   "script": "index.php"
               },

               "direct": {
                   "root": "/path/to/wordpress/"
               }
           }
       }
   }

The complete example is available in our WordPress howto:
https://unit.nginx.org/howto/wordpress/

You can configure as many :samp:`targets` in one PHP application as you want,
routing requests between them using various sophisticated request matching
rules.

Check our website to know more about the new option:
https://unit.nginx.org/configuration/#targets

To learn more about request matching rules:
https://unit.nginx.org/configuration/#matching-conditions

Finally, see here for more howtos: https://unit.nginx.org/howto/

We have plenty of them, covering many popular web applications and frameworks,
but if your favorite one is still missing, let us know by opening a ticket here:
https://github.com/nginx/unit-docs/issues

To keep the finger on the pulse, refer to our further plans in the roadmap here:
https://github.com/orgs/nginx/projects/1

Stay tuned!

wbr, Valentin V. Bartenev
