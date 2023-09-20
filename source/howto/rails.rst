.. |app| replace:: Ruby on Rails
.. |mod| replace:: Ruby

#############
Ruby on Rails
#############

To run apps based on the `Ruby on Rails <https://rubyonrails.org>`_ framework
using Unit:

#. .. include:: ../include/howto_install_unit.rst

#. `Install
   <https://guides.rubyonrails.org/getting_started.html#creating-a-new-rails-project-installing-rails>`_
   |app| and create or deploy your app.  Here, we use |app|'s `basic template
   <https://guides.rubyonrails.org/getting_started.html#creating-the-blog-application>`_:

   .. code-block:: console

      $ cd :nxt_ph:`/path/to/ <Path where the application directory will be created; use a real path in your configuration>`
      $ rails new :nxt_ph:`app <Arbitrary app name; becomes the application directory name>`

   This creates the app's directory tree at :file:`/path/to/app/`; its
   :file:`public/` subdirectory contains the static files, while the entry
   point is :file:`/path/to/app/config.ru`.

#. .. include:: ../include/howto_change_ownership.rst

#. Next, :ref:`prepare <configuration-ruby>` the |app| configuration (use real
   values for :samp:`share` and :samp:`working_directory`):

   .. code-block:: json

      {
          "listeners": {
              "*:80": {
                  "pass": "routes"
              }
          },

          "routes": [
              {
                  "action": {
                      ":nxt_hint:`share <Serves static files>`": ":nxt_ph:`/path/to/app/ <Path to the application directory; use a real path in your configuration>`public$uri",
                      "fallback": {
                          "pass": "applications/rails"
                      }
                  }
              }
          ],

          "applications": {
              "rails": {
                  "type": "ruby",
                  "script": ":nxt_hint:`config.ru <All requests are handled by a single script, relative to working_directory>`",
                  "working_directory": ":nxt_ph:`/path/to/app/ <Path to the application directory, needed here for 'require_relative' directives; use a real path in your configuration>`"
              }
          }
      }

#. .. include:: ../include/howto_upload_config.rst

   After a successful update, your app should be available on the listener’s IP
   address and port:

   .. image:: ../images/rails.png
      :width: 100%
      :alt: Ruby on Rails Basic Template App on Unit
