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

      $ cd /path/to/
      $ rails new app

   This creates the app's directory tree at :file:`/path/to/app/`; its
   :file:`public/` subdirectory contains the static files, while the entry
   point is :file:`/path/to/app/config.ru`.

#. .. include:: ../include/howto_change_ownership.rst

#. Prepare the :ref:`configuration <configuration-ruby>` (use real values for
   :samp:`share`, :samp:`script`, :samp:`working_directory`, :samp:`user`, and
   :samp:`group`):

   .. code-block:: json

      {
          "listeners": {
              "*:80": {
                  "pass": "routes/rails"
              }
          },

          "routes": {
              "rails": [
                  {
                      "action": {
                          ":nxt_term:`share <Serves all kinds of static files>`": ":nxt_term:`/path/to/app/public/ <Use a real path in your configuration>`",
                          "fallback": {
                              "pass": "applications/rails"
                          }
                      }
                  }
              ]
          },

          "applications": {
              "rails": {
                  "type": "ruby",
                  "user": ":nxt_term:`app_user <User and group values must have access to the app root directory>`",
                  "group": "app_group",
                  "script": ":nxt_term:`config.ru <All requests are handled by a single script, relative to working_directory>`",
                  "working_directory": ":nxt_term:`/path/to/app/ <Needed for require_relative directives. Use a real path in your configuration>`"
              }
          }
      }

#. .. include:: ../include/howto_upload_config.rst

   After a successful update, your app should be available on the listener’s IP
   address and port:

   .. image:: ../images/rails.png
      :width: 100%
      :alt: Ruby on Rails Basic Template App on Unit
