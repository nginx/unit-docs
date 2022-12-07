:orphan:

####################
Unit 1.23.0 Released
####################

Hi,

I'm glad to announce a new release of NGINX Unit.

Nowadays, TLS is everywhere, while plain HTTP is almost nonexistent in the
global network.  We are fully aware of this trend and strive to simplify TLS
configuration in Unit as much as possible.  Frankly, there's still much to do,
but the introduction of smart SNI certificate selection marks yet another step
in this direction.

Perhaps, you already know about Unit's certificate storage API that uploads
certificate bundles to a running instance.  Otherwise, if you're not yet fully
informed but still curious, here's a decent overview:
https://unit.nginx.org/certificates/

Basically, you just upload a certificate chain and a key under some name; after
that, you can specify the name (:samp:`mycert` in the example below) with any
listening socket to configure it for HTTPS:

.. code-block:: json

   {
       "listeners": {
           "*:443": {
               "tls": {
                   "certificate": "mycert"
               },

               "pass": "routes"
           }
       }
   }

Unit's API also enables informative introspection of uploaded certificate
bundles so you can monitor their validity and benefit from service discovery.

You can also upload any number of certificate bundles to switch between them on
the fly without restarting the server (yes, Unit's dynamic nature is exactly
like that).  Still, with this release, there are even more options, as you can
supply any number of certificate bundle names with a listener socket:

.. code-block:: json

   {
       "certificate": [ "mycertA", "mycertB", ... ]
   }

For each client, Unit automatically selects a suitable certificate from the
list depending on the domain name the client connects to (and therefore
supplies via the "Server Name Indication" TLS extension).  Thus, you don't even
need to care about matching certificates to server names; Unit handles that for
you.  As a result, there's almost no room for a mistake, which spares more time
for stuff that matters.

As one can reasonably expect, you can always add more certs, delete them, or
edit the cert list on the fly without compromising performance.  That's the
Unit way!

In case you're wondering whom to thank for this shiny new feature: give a warm
welcome to Andrey Suvorov, a new developer on our team.  He will continue
working on TLS improvements in Unit, and his TODO list is already stacked.
Still, if you'd like to suggest a concept or have a particular interest in some
feature, just start a ticket on GitHub; we are open to your ideas:
https://github.com/nginx/unit/issues

Also, plenty of solid bug fixing work was done by the whole team.  See the full
change log below:

.. code-block:: none

   Changes with Unit 1.23.0                                         25 Mar 2021

       *) Feature: support for multiple certificate bundles on a listener via
          the Server Name Indication (SNI) TLS extension.

       *) Feature: "--mandir" ./configure option to specify the directory for
          man page installation.

       *) Bugfix: the router process could crash on premature TLS connection
          close; the bug had appeared in 1.17.0.

       *) Bugfix: a connection leak occurred on premature TLS connection close;
          the bug had appeared in 1.6.

       *) Bugfix: a descriptor and memory leak occurred in the router process
          when processing small WebSocket frames from a client; the bug had
          appeared in 1.19.0.

       *) Bugfix: a descriptor leak occurred in the router process when
          removing or reconfiguring an application; the bug had appeared in
          1.19.0.

       *) Bugfix: persistent storage of certificates might've not worked with
          some filesystems in Linux, and all uploaded certificate bundles were
          forgotten after restart.

       *) Bugfix: the controller process could crash while requesting
          information about a certificate with a non-DNS SAN entry.

       *) Bugfix: the controller process could crash on manipulations with a
          certificate containing a SAN and no standard name attributes in
          subject or issuer.

       *) Bugfix: the Ruby module didn't respect the user locale for defaults
          in the Encoding class.

       *) Bugfix: the PHP 5 module failed to build with thread safety enabled;
          the bug had appeared in 1.22.0.


Other notable features we are working on include:

- statistics API
- process control API
- chrooting on a per-request basis during static file serving
- MIME types filtering for static files
- configuring ciphers and other OpenSSL settings

So much more to come!

Also, if you'd like to know more about Unit and prefer watching fun videos
instead of reading tedious documentation, I'm happy to recommend Timo Stark,
our own PM Engineer.  Recently, he started regularly streaming on Twitch and
YouTube:

- https://www.twitch.tv/h30ne
- https://www.youtube.com/Tippexs91

Tomorrow (March 26), at 10 p.m. CET (or 2 p.m. PDT), he is going on air to
livestream his using Unit's brand-new SNI feature to automate the certbot
setup: https://youtu.be/absaan-8y1Q

Everyone is welcome!

wbr, Valentin V. Bartenev
