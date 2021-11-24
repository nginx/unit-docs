###########
App Samples
###########

.. note::

   These steps assume Unit was already :ref:`installed
   <installation-precomp-pkgs>` with the language module for each app.

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
           io.WriteString(w, "Hello, Go on Unit!")
       })
       unit.ListenAndServe(":8080", nil)
   }

Compile it using the source code from the Go language package you have
:ref:`installed <installation-precomp-pkgs>` or :ref:`built
<howto/source-modules-go>` earlier:

.. code-block:: console

   $ cp -r <package installation path>/src/* $GOPATH/src/
   $ go build -o /www/app /www/app.go

Upload the :ref:`app config <configuration-go>` to Unit and test it:

.. code-block:: console

   # curl -X PUT --data-binary '{
     "listeners": {
         "*:8080": {
             "pass": "applications/go"
         }
     },
     "applications": {
         "go": {
             "type": "external",
             "working_directory": "/www/",
             "executable": "/www/app"
         }
     }
     }' --unix-socket :nxt_ph:`/path/to/control.unit.sock <Path to Unit's control socket in your installation>` http://localhost/config/

   $ curl http://localhost:8080

       Hello, Go on Unit!

Try this sample out with the Dockerfile :download:`here
<../downloads/Dockerfile.go.txt>` or use a more elaborate app example:

.. subs-code-block:: go

   package main

   import (
       "crypto/sha256";
       "fmt";
       "io";
       "io/ioutil";
       "encoding/json";
       "net/http";
       "strings";
       "unit.nginx.org/go"
   )

   func formatRequest(r *http.Request) string {

       h := make(map[string]string)
       m := make(map[string]string)
       t := make(map[string]interface{})

       m["message"] = "Kirov reporting"
       m["agent"] = "NGINX Unit |version|"

       body, _ := ioutil.ReadAll(r.Body)
       m["body"] = fmt.Sprintf("%s", body)

       m["sha256"] = fmt.Sprintf("%x", sha256.Sum256([]byte(m["body"])))

       data, _ := json.Marshal(m)
       for name, _ := range r.Header {
           h[strings.ToUpper(name)] = r.Header.Get(name)
       }
       _ = json.Unmarshal(data, &t)
       t["headers"] = h

       js, _ := json.MarshalIndent(t, "", "    ")

       return fmt.Sprintf("%s", js)
   }

   func main() {
       http.HandleFunc("/",func (w http.ResponseWriter, r *http.Request) {
           w.Header().Set("Content-Type", "application/json; charset=utf-8")
           io.WriteString(w, formatRequest(r))
       })
       unit.ListenAndServe(":8080", nil)
   }


.. _sample-java:

****
Java
****

Let's configure the following basic app, saved as :file:`/www/index.jsp`:

.. code-block:: jsp

   <%@ page language="java" contentType="text/plain" %>
   <%= "Hello, JSP on Unit!" %>

Upload the :ref:`app config <configuration-java>` to Unit and test it:

.. code-block:: console

   # curl -X PUT --data-binary '{
     "listeners": {
         "*:8080": {
             "pass": "applications/java"
         }
     },
     "applications": {
         "java": {
             "type": "java",
             "webapp": "/www/"
         }
     }
     }' --unix-socket :nxt_ph:`/path/to/control.unit.sock <Path to Unit's control socket in your installation>` http://localhost/config/

   $ curl http://localhost:8080

       Hello, JSP on Unit!

Try this sample out with the Dockerfile :download:`here
<../downloads/Dockerfile.java.txt>` or use a more elaborate app example (you'll
need to `download <https://cliftonlabs.github.io/json-simple/>`__ and :ref:`add
<configuration-java>` the :program:`json-simple` library to your app's
:samp:`classpath` option):

.. subs-code-block:: jsp

   <%@ page language="java" contentType="application/json; charset=utf-8" %>
   <%@ page import="com.github.cliftonlabs.json_simple.JsonObject" %>
   <%@ page import="com.github.cliftonlabs.json_simple.Jsoner" %>
   <%@ page import="java.io.BufferedReader" %>
   <%@ page import="java.math.BigInteger" %>
   <%@ page import="java.nio.charset.StandardCharsets" %>
   <%@ page import="java.security.MessageDigest" %>
   <%@ page import="java.util.Enumeration" %>
   <%
   JsonObject r = new JsonObject();

   r.put("message", "Kirov reporting");
   r.put("agent", "NGINX Unit |version|");

   JsonObject headers = new JsonObject();
   Enumeration h = request.getHeaderNames();
   while (h.hasMoreElements()) {
       String name = (String)h.nextElement();
       headers.put(name, request.getHeader(name));
   }
   r.put("headers", headers);

   BufferedReader  br = request.getReader();
   String          body = "";
   String          line = br.readLine();
   while (line != null) {
       body += line;
       line = br.readLine();
   }
   r.put("body", body);

   MessageDigest   md = MessageDigest.getInstance("SHA-256");
   byte[]          bytes = md.digest(body.getBytes(StandardCharsets.UTF_8));
   BigInteger      number = new BigInteger(1, bytes);
   StringBuilder   hex = new StringBuilder(number.toString(16));
   r.put("sha256", hex.toString());

   out.println(Jsoner.prettyPrint((Jsoner.serialize(r))));
   %>


.. _sample-nodejs:

*******
Node.js
*******

Let's configure the following basic app, saved as :file:`/www/app.js`:

.. code-block:: javascript

   #!/usr/bin/env node

   require(":nxt_hint:`unit-http <It's important to use unit-http instead of the regular http module>`").createServer(function (req, res) {
       res.writeHead(200, {"Content-Type": "text/plain"});
       res.end("Hello, Node.js on Unit!")
   }).listen()

Make it executable and link the Node.js language package you've :ref:`installed
<installation-nodejs-package>` earlier:

.. code-block:: console

   $ cd /www
   $ chmod +x app.js
   $ npm link unit-http

Upload the :ref:`app config <configuration-nodejs>` to Unit and test it:

.. code-block:: console

   # curl -X PUT --data-binary '{
     "listeners": {
         "*:8080": {
             "pass": "applications/node"
         }
     },
     "applications": {
         "node": {
             "type": "external",
             "working_directory": "/www/",
             "executable": "app.js"
         }
     }
     }' --unix-socket :nxt_ph:`/path/to/control.unit.sock <Path to Unit's control socket in your installation>` http://localhost/config/

   $ curl http://localhost:8080

       Hello, Node.js on Unit!

Try this sample out with the Dockerfile :download:`here
<../downloads/Dockerfile.nodejs.txt>` or use a more elaborate app example:

.. subs-code-block:: javascript

   #!/usr/bin/env node

   const cr = require("crypto")
   const bd = require("body")
   require("unit-http").createServer(function (req, res) {
       bd (req, res, function (err, body) {
           res.writeHead(200, {"Content-Type": "application/json; charset=utf-8"})

           var r = {
               "agent":    "NGINX Unit |version|",
               "message":  "Kirov reporting"
           }

           r["headers"] = req.headers
           r["body"] = body
           r["sha256"] = cr.createHash("sha256").update(r["body"]).digest("hex")

           res.end(JSON.stringify(r, null, "    ").toString("utf8"))
       })
   }).listen()

.. note::

   You can run a version of the same app :ref:`without
   <configuration-nodejs-loader>` requiring the :samp:`unit-http` module
   explicitly.


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
           [ "Hello, Perl on Unit!" ],
       ];
   };

Upload the :ref:`app config <configuration-perl>` to Unit and test it:

.. code-block:: console

   # curl -X PUT --data-binary '{
     "listeners": {
         "*:8080": {
             "pass": "applications/perl"
         }
     },
     "applications": {
         "perl": {
             "type": "perl",
             "working_directory": "/www/",
             "script": "/www/app.psgi"
         }
     }
     }' --unix-socket :nxt_ph:`/path/to/control.unit.sock <Path to Unit's control socket in your installation>` http://localhost/config/

   $ curl http://localhost:8080

       Hello, Perl on Unit!

Try this sample out with the Dockerfile :download:`here
<../downloads/Dockerfile.perl.txt>` or use a more elaborate app example:

.. subs-code-block:: perl

   use strict;

   use Digest::SHA qw(sha256_hex);
   use JSON;
   use Plack;
   use Plack::Request;

   my $app = sub {
       my $env = shift;
       my $req = Plack::Request->new($env);
       my $res = $req->new_response(200);
       $res->header("Content-Type" => "application/json; charset=utf-8");

       my $r = {
           "message"   => "Kirov reporting",
           "agent"     => "NGINX Unit |version|",
           "headers"   => $req->headers->psgi_flatten(),
           "body"      => $req->content,
           "sha256"    => sha256_hex($req->content),
       };

       my $json = JSON->new();
       $res->body($json->utf8->pretty->encode($r));

       return $res->finalize();
   };


.. _sample-php:

***
PHP
***

Let's configure the following basic app, saved as :file:`/www/index.php`:

.. code-block:: php

   <?php echo "Hello, PHP on Unit!"; ?>

Upload the :ref:`app config <configuration-php>` to Unit and test it:

.. code-block:: console

   # curl -X PUT --data-binary '{
     "listeners": {
         "*:8080": {
             "pass": "applications/php"
         }
     },
     "applications": {
         "php": {
             "type": "php",
             "root": "/www/"
         }
     }
     }' --unix-socket :nxt_ph:`/path/to/control.unit.sock <Path to Unit's control socket in your installation>` http://localhost/config/

   $ curl http://localhost:8080

       Hello, PHP on Unit!

Try this sample out with the Dockerfile :download:`here
<../downloads/Dockerfile.php.txt>` or use a more elaborate app example:

.. subs-code-block:: php

   <?php

   header("Content-Type: application/json; charset=utf-8");

   $r = array (
      "message" => "Kirov reporting",
      "agent"   => "NGINX Unit |version|"
   );

   foreach ($_SERVER as $header => $value)
      if (strpos($header, "HTTP_") === 0)
         $r["headers"][$header] = $value;

   $r["body"] = file_get_contents("php://input");
   $r["sha256"] = hash("sha256", $r["body"]);

   echo json_encode($r, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES);

   ?>


.. _sample-python:

******
Python
******

Let's configure the following basic app, saved as :file:`/www/wsgi.py`:

.. code-block:: python

   def application(environ, start_response):
       start_response("200 OK", [("Content-Type", "text/plain")])
       return (b"Hello, Python on Unit!")

Upload the :ref:`app config <configuration-python>` to Unit and test it:

.. code-block:: console

   # curl -X PUT --data-binary '{
     "listeners": {
         "*:8080": {
             "pass": "applications/python"
         }
     },
     "applications": {
         "python": {
             "type": "python",
             "path": "/www/",
             "module": "wsgi"
         }
     }
     }' --unix-socket :nxt_ph:`/path/to/control.unit.sock <Path to Unit's control socket in your installation>` http://localhost/config/

   $ curl http://localhost:8080

       Hello, Python on Unit!

Try this sample out with the Dockerfile :download:`here
<../downloads/Dockerfile.python.txt>` or use a more elaborate app example:

.. subs-code-block:: python

   import hashlib, json

   def application(env, start_response):
       start_response("200 OK", [("Content-Type",
                                  "application/json; charset=utf-8")])

       r = {}

       r["message"] = "Kirov reporting"
       r["agent"] = "NGINX Unit |version|"

       r["headers"] = {}
       for header in [_ for _ in env.keys() if _.startswith("HTTP_")]:
           r["headers"][header] = env[header]

       bytes = env["wsgi.input"].read()
       r["body"] = bytes.decode("utf-8")
       r["sha256"] = hashlib.sha256(bytes).hexdigest()

       return json.dumps(r, indent=4).encode("utf-8")

.. _sample-ruby:

****
Ruby
****

Let's configure the following basic app, saved as :file:`/www/config.ru`:

.. code-block:: ruby

   app = Proc.new do |env|
       ["200", {
           "Content-Type" => "text/plain",
       }, ["Hello, Ruby on Unit!"]]
   end

   run app

Upload the :ref:`app config <configuration-ruby>` to Unit and test it:

.. code-block:: console

   # curl -X PUT --data-binary '{
     "listeners": {
         "*:8080": {
             "pass": "applications/ruby"
         }
     },
     "applications": {
         "ruby": {
             "type": "ruby",
             "working_directory": "/www/",
             "script": "config.ru"
         }
     }
     }' --unix-socket :nxt_ph:`/path/to/control.unit.sock <Path to Unit's control socket in your installation>` http://localhost/config/

   $ curl http://localhost:8080

       Hello, Ruby on Unit!

Try this sample out with the Dockerfile :download:`here
<../downloads/Dockerfile.ruby.txt>` or use a more elaborate app example:

.. subs-code-block:: ruby

   require "digest"
   require "json"

   app = Proc.new do |env|
       body = env["rack.input"].read
       r = {
           "message" => "Kirov reporting",
           "agent"   => "NGINX Unit |version|",
           "body"    => body,
           "headers" => env.select { |key, value| key.include?("HTTP_") },
           "sha256"  => Digest::SHA256.hexdigest(body)
       }

       ["200", {
           "Content-Type" => "application/json; charset=utf-8",
       }, [JSON.pretty_generate(r)]]
   end;

   run app

