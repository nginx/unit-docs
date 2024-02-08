#################
NGINX Integration
#################

Unit is a potent and versatile server in its own right.  However, if you're
used to NGINX's rich feature set, you can deploy it in front of Unit; one
notable use case for NGINX here is securing the Unit control socket.

************************
Fronting Unit with NGINX
************************

Configure a :ref:`listener <configuration-listeners>` in Unit:

   .. code-block:: json

      {
          ":nxt_ph:`127.0.0.1:8080 <Socket address where NGINX proxies requests>`": {
              "pass": ":nxt_ph:`... <Unit's internal request destination>`",
              "forwarded": {
                  "client_ip": ":nxt_hint:`X-Forwarded-For <The header field set by NGINX>`",
                  "source": [
                      ":nxt_ph:`127.0.0.1 <The IP address where NGINX runs>`"
                  ]
              }
          }
      }

Here, **forwarded** is optional; it enables identifying the
:ref:`originating IPs <configuration-listeners-xff>` of requests proxied from
**source**.

In NGINX configuration, create an upstream in the **http** context, adding
the listener's socket as a **server**:

.. code-block:: nginx

   http {
       upstream unit_backend {
           server :nxt_ph:`127.0.0.1:8080 <Unit's listener socket address>`;
       }

       server {
           location :nxt_hint:`/unit/ <Arbitrary location>` {
               proxy_pass http://unit_backend;
               proxy_set_header Host $host;
               proxy_set_header :nxt_hint:`X-Forwarded-For <Unit's listener must list the same name in client_ip/header>` $proxy_add_x_forwarded_for;
           }
       }
   }

A more compact alternative would be a direct **proxy_pass** in your
**location**:

.. code-block:: nginx

   http {
       server {
           location :nxt_hint:`/unit/ <Arbitrary location>` {
               proxy_pass http://:nxt_ph:`127.0.0.1:8080 <Unit's listener socket address>`;
               proxy_set_header Host $host;
               proxy_set_header :nxt_hint:`X-Forwarded-For <Unit's listener must list the same name in client_ip/header>` $proxy_add_x_forwarded_for;
           }
       }
   }

The **proxy_set_header X-Forwarded-For** directives work together with the
listener's **client_ip** option.

For details, see the `NGINX documentation <https://nginx.org>`_.  Commercial
support and advanced features are `also available <https://www.nginx.com>`_.


.. _nginx-secure-api:

************************************
Securely Proxying Unit's Control API
************************************

By default, Unit exposes its :ref:`control API <configuration-mgmt>` via a UNIX
domain socket.  These sockets aren't network accessible, so the API is local
only.  To enable secure remote access, you can use NGINX as a reverse proxy.

.. warning::

   Avoid exposing an unprotected control socket to public networks.  Use NGINX
   or a different solution such as SSH for security and authentication.

Use this configuration template for NGINX (replace placeholders in
**ssl_certificate**, **ssl_certificate_key**,
**ssl_client_certificate**, **allow**, **auth_basic_user_file**,
and **proxy_pass** with real values):

.. code-block:: nginx

   server {

       # Configure SSL encryption
       listen 443 ssl;

       ssl_certificate :nxt_ph:`/path/to/ssl/cert.pem <Path to your PEM file; use a real path in your configuration>`;
       ssl_certificate_key :nxt_ph:`/path/to/ssl/cert.key <Path to your key file; use a real path in your configuration>`;

       # SSL client certificate validation
       ssl_client_certificate :nxt_ph:`/path/to/ca.pem <Path to certification authority PEM file; use a real path in your configuration>`;
       ssl_verify_client on;

       # Network ACLs
       allow :nxt_ph:`1.2.3.4 <Replicate and update as needed with allowed IPs and network CIDRs>`;
       deny all;

       # HTTP Basic authentication
       auth_basic on;
       auth_basic_user_file :nxt_ph:`/path/to/htpasswd <Path to your htpasswd file>`;

       location / {
           proxy_pass http://unix::nxt_ph:`/path/to/control.unit.sock <Path to Unit's control socket>`;
       }
   }

The same approach works for an IP-based control socket:

.. code-block:: nginx

   location / {
       proxy_pass http://:nxt_ph:`127.0.0.1:8080 <Unit's control socket address>`;
   }
