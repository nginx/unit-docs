.. include:: ../include/replace.rst

Create a virtual environment to install |app|'s |app-pip-link|_:

.. subs-code-block:: console

   $ cd /path/to/app/
   $ :nxt_hint:`python3 --version <Make sure your virtual environment version matches the module version>`
         Python 3.x.y
   $ python3 -m venv venv
   $ source venv/bin/activate
   $ pip install |app-pip-package|
   $ deactivate

.. warning::

   Create your virtual environment with a Python version that matches the
   language module from Step |_| 1 up to the minor number (:samp:`3.x` in this
   example).  Also, the app :samp:`type` in Step |_| 5 must :ref:`resolve
   <configuration-apps-common>` to a similarly matching version; Unit doesn't
   infer it from the environment.


