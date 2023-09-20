:orphan:

#################
Unit 1.1 Released
#################

Hello,

I'm glad to announce a new release of NGINX Unit.  This is mostly a bugfix
release with stability and compatibility improvements.

.. code-block:: none

   Changes with Unit 1.1                                            26 Apr 2018

       *) Bugfix: Python applications that use the write() callable did not
          work.

       *) Bugfix: virtual environments created with Python 3.3 or above might
          not have worked.

       *) Bugfix: the request.Read() function in Go applications did not
          produce EOF when the whole body was read.

       *) Bugfix: a segmentation fault might have occurred while access log
          reopening.

       *) Bugfix: in parsing of IPv6 control socket addresses.

       *) Bugfix: loading of application modules was broken on OpenBSD.

       *) Bugfix: a segmentation fault might have occurred when there were two
          modules with the same type and version; the bug had appeared in 1.0.

       *) Bugfix: alerts "freed pointer points to non-freeble page" might have
          appeared in log on 32-bit platforms.


A half of these issues were reported on GitHub by our users.  Thank you all
for helping us make Unit better.

If you have encountered a problem with Unit or have any ideas for improvements,
please feel free to share here:

- Mailing list: https://mailman.nginx.org/mailman3/lists/unit.nginx.org/
- GitHub: https://github.com/nginx/unit/issues

wbr, Valentin V. Bartenev
