.. |app| replace:: CakePHP
.. |mod| replace:: PHP 7.2+

#######
CakePHP
#######

To run apps based on the `CakePHP <https://cakephp.org>`_ framework using Unit:

#. .. include:: ../include/howto_install_unit.rst

#. `Install <https://book.cakephp.org/4/en/installation.html>`_ |app| and
   create or deploy your app.  Here, we use |app|'s `basic template
   <https://book.cakephp.org/4/en/installation.html#create-a-cakephp-project>`_
   and Composer:

   .. code-block:: console

      $ cd :nxt_ph:`/path/to/ <Path where the application directory will be created; use a real path in your configuration>`
      $ composer create-project --prefer-dist cakephp/app:4.* :nxt_ph:`app <Arbitrary app name; becomes the application directory name>`

   This creates the app's directory tree at :file:`/path/to/app/`.  Its
   :file:`webroot/` subdirectory contains both the root :file:`index.php` and
   the static files; if your app requires additional :file:`.php` scripts, also
   store them here.

#. .. include:: ../include/howto_change_ownership.rst

#. Next, prepare the app :ref:`configuration <configuration-php>` for Unit (use
   real values for :samp:`share` and :samp:`root`):

   .. code-block:: json

      {
          "listeners": {
              "*:80": {
                  "pass": "routes"
              }
          },

          "routes": [
              {
                  "match": {
                      ":nxt_hint:`uri <Handles all requests that explicitly target PHP scripts>`": [
                          "*.php",
                          "*.php/*"
                      ]
                  },

                  "action": {
                      "pass": "applications/cakephp/direct"
                  }
              },
              {
                  "action": {
                      ":nxt_hint:`share <Unconditionally serves remaining requests that target static files>`": ":nxt_ph:`/path/to/app/webroot <Path to the webroot/ directory; use a real path in your configuration>`$uri",
                      "fallback": {
                          ":nxt_hint:`pass <Serves any requests not served with the 'share' immediately above>`": "applications/cakephp/index"
                      }
                  }
              }
          ],

          "applications": {
              "cakephp": {
                  "type": "php",
                  "targets": {
                      "direct": {
                          "root": ":nxt_ph:`/path/to/app/webroot/ <Path to the webroot/ directory; use a real path in your configuration>`"
                      },

                      "index": {
                          "root": ":nxt_ph:`/path/to/app/webroot/ <Path to the webroot/ directory; use a real path in your configuration>`",
                          "script": ":nxt_hint:`index.php <All requests are handled by a single script>`"
                      }
                  }
              }
          }
      }

   .. note::

      The difference between the :samp:`pass` targets is their usage of the
      :samp:`script` :ref:`setting <configuration-php>`:

      - The :samp:`direct` target runs the :samp:`.php` script from the URI or
        defaults to :samp:`index.php` if the URI omits it.

      - The :samp:`index` target specifies the :samp:`script` that Unit runs
        for *any* URIs the target receives.

   For a detailed discussion, see `Fire It Up
   <https://book.cakephp.org/4/en/installation.html#fire-it-up>`_ in |app|
   docs.

#. .. include:: ../include/howto_upload_config.rst

   After a successful update, your app should be available on the listener’s IP
   address and port:

   .. image:: ../images/cakephp.png
      :width: 100%
      :alt: CakePHP Basic Template App on Unit
