:orphan:

####################
Unit 1.34.2 Released
####################

We are pleased to announce the release of NGINX Unit 1.34.2. This is a
maintenance release that fixes a couple of issues in the Java WebSocket
code within the Java language module.

- Security: When the NGINX Unit Java Language module is in use, undisclosed
  requests can lead to an infinite loop and cause an increase in CPU resource
  utilization (CVE-2025-1695).

  `F5 SIRT <https://my.f5.com/manage/s/article/K000149959>`__.

- It addresses an issue whereby decoded payload lengths would be limited
  to 32 bits.

Both these issues affect Unit versions from 1.11.0 to 1.34.1. If you use
the Java language module with WebSockets it is strongly suggested to
upgrade.

**************
Full Changelog
**************

.. code-block:: none

Changes with Unit 1.34.2                                         26 Feb 2025

    *) Security: fix missing websocket payload length validation in the Java
       language module which could lead to Java language module processes
       consuming excess CPU. (CVE-2025-1695).

    *) Bugfix: fix incorrect websocket payload length calculation in the
       Java language module.
