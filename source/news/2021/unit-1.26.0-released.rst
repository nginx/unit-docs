:orphan:

####################
Unit 1.26.0 Released
####################

Hi,

I'm glad to announce a new release of NGINX Unit.

Please read this letter to the end, as it explains some significant changes in
the latest version.  But first, I have great news for the PHP users: now the
interpreter's `OPcache <https://www.php.net/manual/en/book.opcache.php>`__ is
shared between the processes of an app.

In previous versions, due to an architecture limitation (which imposed strong
isolation, much stronger than was sometimes needed), each PHP process had
a separate OPcache memory.  As a result, with some workloads (especially
involving many dynamic processes), performance could degrade because each
new process had to warm up the cache after starting.  Also, it required more
memory because the bytecode of same PHP scripts was duplicated in each process.
Now, all these flaws are finally gone.

Next, we noticed that more and more users use Unit to serve static files,
if only because it's efficient and easy to configure.  Modern apps are all
dynamic, yes, but at the same time, almost all apps and websites have static
resources like images, scripts, styles, fonts, and media files.  It's very
important to supply these resources as fast as possible without any delays
to smoothen the overall user experience.  We take this aspect seriously and
continue improving Unit capabilities as a generic static media web server.

This time, all changes are about configuration flexibility.  You may know that
nginx has a number of different directives that control static file serving:

- :samp:`root`
- :samp:`alias`
- :samp:`try_files`

Some of these are mutually exclusive, some can be combined, some work
differently depending on the location type.  That gives the configuration
a lot of flexibility but may look a bit complicated.  Users kept asking us
to provide the same functionality in Unit, but instead of just repeating
these, we thought about how we can improve this experience to make it easier
to understand without losing flexibility.

Finally, we came up with a solution.  In previous versions, we introduced the
:samp:`share` directive, very similar to the :samp:`root` directive in
:program:`nginx`:

.. code-block:: json

   {
       "share": "/path/to/dir/"
   }

Basically, it specified the so-called document root directory.  To determine a
file to serve, Unit appended the URI from the request to this :samp:`share`
path.  For this request:

.. code-block:: none

   GET /some/file.html

The above configuration served :file:`/path/to/dir/some/file.html`.

In simple times, that's exactly what you want.  Still, there are plenty of
cases when a different file needs to be served and the requested URI doesn't
match a path.  More, you may want to serve a single file for any requests;
the so-called one-page apps often utilize such a scheme.

Such border cases call for a finer degree of control over the full path to
a file.  As a result, we kept receiving suggestions like:

.. code-block:: json

   {
       "share_file": "/path/to/a/file.html"
   }

The idea was to specify the full path to the file instead of the document root
part only.

In parallel, we work variable support so we thought about introducing variable
paths; for instance, you may want to serve different files depending on the
normalized Host header:

.. code-block:: json

   {
       "share_file": "/www/data/$host/app.html"
   }

Sneak peek ahead: we have plans for ways to create custom variables that
extract various parts of the request using regular expressions.

Still, look at the suggested configuration:

.. code-block:: json

  {
      "share_file": "/www/data/$uri"
  }

And compare it to what we had:

.. code-block:: json

  {
      "share": "/www/data/"
  }

These configurations are essentially equal; why bother with another option
at all?  Figuring in the maxim that says that explicit is often better than
implicit, this value:

.. code-block:: none

   "/www/data/$uri"

Is better and more self-descriptive than:

.. code-block:: none

   "/www/data/"

The latter only shows a part of the path, so you need to remind yourself that
the URI is appended to it.  Keeping this in mind and striving to have a cleaner
configuration with fewer options to read about and to choose from, we finally
decided to alter the behaviour of the :samp:`share` option.

Starting with Unit 1.26.0, the :samp:`share` option specifies the *entire* path
to a shared file rather than just the document root.  And yes, the option
supports variables, so you can write:

.. code-block:: json

  {
      "share": "/www/data/$uri"
  }

There won't be a separate :samp:`share_file` option.  I used it only to
illustrate the initial idea and the resulting change; the :samp:`share` option
assumes all relevant functionality instead.

If you run previous versions of Unit and use :samp:`share` in your
configurations, an update to Unit 1.26+ will automatically append :samp:`$uri`
to all your :samp:`share` values to preserve the expected behavior.

Configurations like this:

.. code-block:: json

  {
      "share": "/www/data/"
  }

Are automatically rewritten as follows:

.. code-block:: json

  {
      "share": "/www/data/$uri"
  }

This occurs only once, after the version update.  If you manage your
configurations using some scripts and store them somewhere else,
make sure to adjust the "share" values there accordingly.

Note that Unit won't fix your :samp:`share` values that you upload in
reconfiguration requests over the control socket API.

To read more about the new share behavior, check the documentation:
https://unit.nginx.org/configuration/#static-files

I hope this transition will be easy and as hassle-free as possible for our
existing users.  For new users, there is nothing to care about, just mind that
blog posts or other sources about previous Unit versions can use configurations
that rely on the discontinued :samp:`share` behavior, so make the necessary
adjustments before copying them.  All docs and howtos at the official Unit
website were already updated: https://unit.nginx.org/howto/

Are you with me? That's not the end of news about :samp:`share`.  Here's one
more, and it's pretty exciting.  Earlier, to implement a :samp:`try_files`-like
behavior, you had to use something like this:

.. code-block:: json

  {
      "share": "path1"

      "fallback": {
          "share": "path2"

          "fallback": {
              "pass": "application/blog"
          }
      }
  }

This snippet tries to serve a file using :file:`path1`; if it doesn't exist or
is inaccessible, it falls back to :file:`path2`, and then passes the request
further, to the blog app.

Now it's much easier to configure:

.. code-block:: json

  {
      "share": [ "path1", "path2" ]

      "fallback": {
          "pass": "application/blog"
      }
  }

The :samp:`share` directive now can accept an array of paths, trying them one
by one until a file is found.  If there is no file to serve, the
:samp:`fallback` action occurs; if no fallback is defined, the result of the
last try is returned.  And yes, all these paths can contain variables:

.. code-block:: json

  {
      "share": [
          "/www/$host$uri",
          "/www/static$uri",
          "/www/app.html"
      ]
  }

For more examples and detailed explanations:
https://unit.nginx.org/configuration/#static-files

In future releases, we'll introduce more variables and the ability to extract
various parts of requests and save them into your custom variables, which will
provide essentially endless flexibility to manipulate file paths.

There are some more notable features in this release as well:

1. Variables support in the :samp:`chroot` option to accompany variable-based
   paths in "share" during static media serving.

   Learn more about Unit's ability to chroot while serving static assets:
   https://unit.nginx.org/configuration/#path-restrictions

2. The :samp:`query` matching option to filter and route requests by arbitrary
   query string values.

   We already had the :samp:`arguments` option that enabled filtering and
   routing requests by particular key-value pairs of query string arguments,
   but the query string doesn't always fit this format.  So, now you can also
   use regexps and wildcard matching to work on the full query string value.

   Learn more about our very flexible and elaborate request filtering and
   routing: https://unit.nginx.org/configuration/#routes

The complete change log for this release is below:

.. code-block:: none

   Changes with Unit 1.26.0                                         18 Nov 2021

       *) Change: the "share" option now specifies the entire path to the files
          it serves, rather than a document root directory to be prepended to
          the request URI.

       *) Feature: automatic adjustment of existing configurations to the new
          "share" behavior when updating from previous versions.

       *) Feature: variables support in the "share" option.

       *) Feature: multiple paths in the "share" option.

       *) Feature: variables support in the "chroot" option.

       *) Feature: PHP opcache is shared between application processes.

       *) Feature: request routing by the query string.

       *) Bugfix: the router and app processes could crash when the requests
          limit was reached by asynchronous or multithreaded apps.

       *) Bugfix: established WebSocket connections could stop reading frames
          from the client after the corresponding listener had been
          reconfigured.

       *) Bugfix: fixed building with glibc 2.34, notably Fedora 35.


Other major features that we are preparing for the next release include:

- basic statistics API for monitoring Unit instances
- various variables for different aspects of request and connection data
- customization of access log format with variables
- custom variables out of regexp captures on various request parameters
- simple request rewrite using variables
- command-line tool to simplify the use of Unit's control socket API

There probably will be even more.

To participate, share your ideas, or discuss new features, you're welcome
to visit Unit's issue tracker on GitHub: https://github.com/nginx/unit/issues

Stay tuned!

wbr, Valentin V. Bartenev
