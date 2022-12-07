:orphan:

#################
Unit 1.2 Released
#################

Hello,

I'm glad to announce a new release of NGINX Unit.

.. code-block:: none

   Changes with Unit 1.2                                            07 Jun 2018

       *) Feature: configuration of environment variables for application
          processes.

       *) Feature: customization of php.ini path.

       *) Feature: setting of individual PHP configuration options.

       *) Feature: configuration of execution arguments for Go applications.

       *) Bugfix: keep-alive connections might hang after reconfiguration.


Here's an example of new configuration parameters of application objects:

.. code-block:: json

   {
       "args-example": {
           "type": "go",
           "executable": "/path/to/compiled/go/binary",
           "arguments": ["arg1", "arg2", "arg3"]
       },

       "opts-example": {
           "type": "php",
           "root": "/www/site",
           "script": "phpinfo.php",

           "options": {
               "file": "/path/to/php.ini",
               "admin": {
                   "memory_limit": "256M",
                   "variables_order": "EGPCS",
                   "short_open_tag": "1"
               },
               "user": {
                   "display_errors": "0"
               }
           }
       },

       "env-example": {
           "type": "python",
           "path": "/www/django",
           "module": "wsgi",

           "environment": {
               "DB_ENGINE": "django.db.backends.postgresql_psycopg2",
               "DB_NAME": "mydb",
               "DB_HOST": "127.0.0.1"
           }
       }
   }

Please note that :samp:`environment` can be configured for any type of
application.

Binary Linux packages and Docker images are available here:

- Packages:  https://unit.nginx.org/installation/#official-packages
- Docker:    https://hub.docker.com/r/nginx/unit/tags/

wbr, Valentin V. Bartenev
