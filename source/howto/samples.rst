:orphan:

###########
App Samples
###########

.. note::

   These steps assume Unit was already :ref:`installed
   <installation-precomp-pkgs>` with the language module and/or package for
   each app.

.. _sample-go:

**
Go
**

Let's configure the following basic app, saved as :file:`/www/app.go`:

.. code-block:: go

   package main

   import (
       "io";
       "net/http";
       "unit.nginx.org/go"
   )

   func main() {
       http.HandleFunc("/",func (w http.ResponseWriter, r *http.Request) {
           io.WriteString(w, "Hello, Unit!")
       })
       unit.ListenAndServe(":8080", nil)
   }

Compile it using the source code from the Go language package you have
:ref:`installed <installation-precomp-pkgs>` or :ref:`built <installation-go>`
earlier:

.. code-block:: console

   $ cp -r <package installation path>/src/* $GOPATH/src/
   $ go build -o /www/app /www/app.go

Upload the :ref:`app config <configuration-external>` to Unit and test it:

.. code-block:: console

   # curl -X PUT --data-binary '{         \
     "listeners": {                       \
         "*:8080": {                      \
             "pass": "applications/go_app"\
         }                                \
     },                                   \
     "applications": {                    \
         "go_app": {                      \
             "type": "external",          \
             "working_directory": "/www/",\
             "executable": "/www/app"     \
         }                                \
     }                                    \
     }' --unix-socket /path/to/control.unit.sock http://localhost/config/

   $ curl localhost:8080

       Hello, Unit!

For a more elaborate example, see the Dockerfile :download:`here
<../downloads/Dockerfile.go.txt>`.

.. _sample-nodejs:

*******
Node.js
*******

Let's configure the following basic app, saved as :file:`/www/app.js`:

.. code-block:: javascript

   #!/usr/bin/env node

   require("unit-http").createServer(function (req, res) {
       res.writeHead(200, {"Content-Type": "text/plain"});
       res.end("Hello, Unit!")
   }).listen()

Make it executable and link the Node.js language package you've :ref:`installed
<installation-nodejs-package>` earlier:

.. code-block:: console

   $ cd /www
   $ chmod +x app.js
   $ npm link unit-http

Upload the :ref:`app config <configuration-external>` to Unit and test it:

.. code-block:: console

   # curl -X PUT --data-binary '{           \
     "listeners": {                         \
         "*:8080": {                        \
             "pass": "applications/node_app"\
         }                                  \
     },                                     \
     "applications": {                      \
         "node_app": {                      \
             "type": "external",            \
             "working_directory": "/www/",  \
             "executable": "app.js"         \
         }                                  \
     }                                      \
     }' --unix-socket /path/to/control.unit.sock http://localhost/config/

   $ curl localhost:8080

       Hello, Unit!

For a more elaborate example, see the Dockerfile :download:`here
<../downloads/Dockerfile.nodejs.txt>`.

.. _sample-java:

****
Java
****

Let's configure the following basic app, saved as :file:`/www/index.jsp`:

.. code-block:: jsp

   <%@ page language="java" contentType="text/plain" %>
   <%= "Hello, Unit!" %>

Upload the :ref:`app config <configuration-java>` to Unit and test it:

.. code-block:: console

   # curl -X PUT --data-binary '{           \
     "listeners": {                         \
         "*:8080": {                        \
             "pass": "applications/java_app"\
         }                                  \
     },                                     \
     "applications": {                      \
         "java_app": {                      \
             "type": "java",                \
             "webapp": "/www/"              \
         }                                  \
     }                                      \
     }' --unix-socket /path/to/control.unit.sock http://localhost/config/

   $ curl localhost:8080

       Hello, Unit!

For a more elaborate example, see the Dockerfile :download:`here
<../downloads/Dockerfile.java.txt>`.

.. _sample-perl:

****
Perl
****

Let's configure the following basic app, saved as :file:`/www/app.psgi`:

.. code-block:: perl

   my $app = sub {
       return [
           "200",
           [ "Content-Type" => "text/plain" ],
           [ "Hello, Unit!" ],
       ];
   };

Upload the :ref:`app config <configuration-perl>` to Unit and test it:

.. code-block:: console

   # curl -X PUT --data-binary '{           \
     "listeners": {                         \
         "*:8080": {                        \
             "pass": "applications/perl_app"\
         }                                  \
     },                                     \
     "applications": {                      \
         "perl_app": {                      \
             "type": "perl",                \
             "working_directory": "/www/",  \
             "script": "/www/app.psgi"      \
         }                                  \
     }                                      \
     }' --unix-socket /path/to/control.unit.sock http://localhost/config/

   $ curl localhost:8080

       Hello, Unit!

For a more elaborate example, see the Dockerfile :download:`here
<../downloads/Dockerfile.perl.txt>`.

.. _sample-php:

***
PHP
***

Let's configure the following basic app, saved as :file:`/www/index.php`:

.. code-block:: php

   <?php echo "Hello, Unit!"; ?>

Upload the :ref:`app config <configuration-php>` to Unit and test it:

.. code-block:: console

   # curl -X PUT --data-binary '{          \
     "listeners": {                        \
         "*:8080": {                       \
             "pass": "applications/php_app"\
         }                                 \
     },                                    \
     "applications": {                     \
         "php_app": {                      \
             "type": "php",                \
             "root": "/www/"               \
         }                                 \
     }                                     \
     }' --unix-socket /path/to/control.unit.sock http://localhost/config/

   $ curl localhost:8080

       Hello, Unit!

For a more elaborate example, see the Dockerfile :download:`here
<../downloads/Dockerfile.php.txt>`.

.. _sample-python:

******
Python
******

Let's configure the following basic app, saved as :file:`/www/wsgi.py`:

.. code-block:: python

   def application(environ, start_response):
       start_response("200 OK", [("Content-Type", "text/plain")])
       return (b"Hello, Unit!")

Upload the :ref:`app config <configuration-python>` to Unit and test it:

.. code-block:: console

   # curl -X PUT --data-binary '{             \
     "listeners": {                           \
         "*:8080": {                          \
             "pass": "applications/python_app"\
         }                                    \
     },                                       \
     "applications": {                        \
         "python_app": {                      \
             "type": "python",                \
             "path": "/www/",                 \
             "module": "wsgi"                 \
         }                                    \
     }                                        \
     }' --unix-socket /path/to/control.unit.sock http://localhost/config/

   $ curl localhost:8080

       Hello, Unit!

For a more elaborate example, see the Dockerfile :download:`here
<../downloads/Dockerfile.python.txt>`.

.. _sample-ruby:

****
Ruby
****

Let's configure the following basic app, saved as :file:`/www/config.ru`:

.. code-block:: ruby

   app = Proc.new do |env|
       ["200", {
           "Content-Type" => "text/plain",
       }, ["Hello, Unit!"]]
   end

   run app

Upload the :ref:`app config <configuration-ruby>` to Unit and test it:

.. code-block:: console

   # curl -X PUT --data-binary '{           \
     "listeners": {                         \
         "*:8080": {                        \
             "pass": "applications/ruby_app"\
         }                                  \
     },                                     \
     "applications": {                      \
         "ruby_app": {                      \
             "type": "ruby",                \
             "working_directory": "/www/",  \
             "script": "config.ru"          \
         }                                  \
     }                                      \
     }' --unix-socket /path/to/control.unit.sock http://localhost/config/

   $ curl localhost:8080

       Hello, Unit!

For a more elaborate example, see the Dockerfile :download:`here
<../downloads/Dockerfile.ruby.txt>`.
