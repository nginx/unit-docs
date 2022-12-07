:orphan:

#################
Unit 1.6 Released
#################

Hello,

I'm glad to announce a new release of NGINX Unit.

This release primarily focuses on improvements in Node.js module compatibility;
thanks to our vibrant community, we made great progress here.

Please don't hesitate to report any problems to:

- Github: https://github.com/nginx/unit/issues
- Mailing list: https://mailman.nginx.org/mailman/listinfo/unit

If you have installed the :program:`unit-http` module from `npm
<https://www.npmjs.com>`__, then don't forget to update it besides Unit itself.

Detailed instructions for Node.js installation can be found here:
http://unit.nginx.org/installation/#node-js

.. code-block:: none

   Changes with Unit 1.6                                            15 Nov 2018

       *) Change: "make install" now installs Node.js module as well if it was
          configured.

       *) Feature: "--local" ./configure option to install Node.js module
          locally.

       *) Bugfix: Node.js module might have crashed due to broken reference
          counting.

       *) Bugfix: asynchronous operations in Node.js might not have worked.

       *) Bugfix: various compatibility issues with Node.js applications.

       *) Bugfix: "freed pointer is out of pool" alerts might have appeared in
          log.

       *) Bugfix: module discovery didn't work on 64-bit big-endian systems
          like IBM/S390x.


wbr, Valentin V. Bartenev
