:orphan:

###################
Unit 1.7.1 Released
###################

Hi,

This is a bugfix release of NGINX Unit that eliminates a security flaw.
All versions of Unit from 0.3 to 1.7 are affected.

Everybody is strongly advised to update to a new version.

.. code-block:: none

   Changes with Unit 1.7.1                                          07 Feb 2019

       *) Security: a heap memory buffer overflow might have been caused in the
          router process by a specially crafted request, potentially resulting
          in a segmentation fault or other unspecified behavior
          (CVE-2019-7401).

       *) Bugfix: install of Go module failed without prior building of Unit
          daemon; the bug had appeared in 1.7.

Release of Unit 1.8 with support for internal request routing and an
experimental Java module is planned for end of February.

wbr, Valentin V. Bartenev
