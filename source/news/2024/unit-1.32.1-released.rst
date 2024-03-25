:orphan:

####################
Unit 1.32.1 Released
####################

NGINX Unit 1.32.1 is a maintenance release, fixing bugs in the new WebAssembly Language Module and in our NJS implementation.

===============
Resolved issues
===============

This release fixes the following issues:

**************************************************************
Applications of type `wasm-wasi-component` can't be restarted
**************************************************************

Applications deployed as `wasm-wasi-components` can't be restarted using the `restart` endpoint.

After deploying a new Wasm Component binary to disk the restart will trigger a reload of the component in Unit without restarting the server.

As restarts will work independently of the application type, the behavior shipped with **1.32.0** was not right and fixed with this release.


************************************************************
Unit-variables in NGINX JavaScript are constantly cached
************************************************************

With **1.32.0** we have released the possibility to access all Unit variables form inside NJS.

As reported in GitHub issue `#1169 <https://github.com/nginx/unit/issues/1169>`__ the variables are cached and will hold the wrong value, which is definitely not the way this feature should work. With 1.32.1 we have fixed this issue.


==============
Full Changelog
==============

.. code-block:: none

    Changes with Unit 1.32.1                                         26 Mar 2024

        *) Bugfix: NJS variables in templates may have incorrect values due to
           improper caching.

        *) Bugfix: Wasm application process hangs after receiving restart signal
           from the control.



For a full list of changes and bugfixes,
please see the `changelog <../../../CHANGES.txt>`__.
