#################
NGINX Integration
#################

Unit is a potent and versatile server in its own right.  However, if you're
used to NGINX's rich feature set, you can deploy it in front of Unit; one
notable use case for NGINX here is securing the Unit control socket.

************************
Fronting Unit with NGINX
************************

Assume you've configured a Unit :ref:`listener <configuration-listeners>` on
:samp:`127.0.0.1:8300`:

   .. code-block:: json

      {
          "127.0.0.1:8300": {
              "pass": "applications/blogs"
          }
      }

In NGINX configuration, create an upstream in the :samp:`http` context,
adding the listener's socket as a :samp:`server`:

.. code-block:: nginx

   http {
       upstream unit_backend {
           server 127.0.0.1:8300;
       }

       server {
           location /unit/ {
               proxy_pass http://unit_backend;
               proxy_set_header Host $host;
           }
       }
   }

A simpler alternative is a direct :samp:`proxy_pass` in your :samp:`location`:

.. code-block:: nginx

   http {
       server {
           location /unit/ {
               proxy_pass http://127.0.0.1:8300;
           }
       }
   }

For details, see the `NGINX documentation <https://nginx.org>`_.  Commercial
support and advanced features are `also available <https://www.nginx.com>`_.

.. _nginx-secure-api:

**********************************
Securely Proxying Unit Control API
**********************************

By default, Unit exposes its :ref:`control API <configuration-mgmt>` via a Unix
domain socket.  These sockets aren't network accessible, so the API is local
only.  To enable secure remote access, you can use NGINX as a reverse proxy.

.. warning::

   Avoid exposing an unprotected control socket to public networks.  Use NGINX
   or a different solution such as SSH for security and authentication.

Use the following configuration template for NGINX:

.. code-block:: nginx

   server {

       # Configure SSL encryption
       listen 443 ssl;

       ssl_certificate :nxt_term:`/path/to/ssl/cert.pem <Path to your PEM file>`;
       ssl_certificate_key :nxt_term:`/path/to/ssl/cert.key <Path to your key file>`;

       # SSL client certificate validation
       ssl_client_certificate :nxt_term:`/path/to/ca.pem <Path to certification authority PEM file>`;
       ssl_verify_client on;

       # Network ACLs
       #:nxt_term:`allow 1.2.3.4 <Uncomment and update with the IP addresses and networks of your administrative systems>`;
       deny all;

       # HTTP Basic authentication
       auth_basic on;
       auth_basic_user_file :nxt_term:`/path/to/htpasswd <Path to your htpasswd file>`;

       location / {
           proxy_pass :nxt_term:`http://unix:/path/to/control.unit.sock <Path to Unit control socket>`;
       }
   }

.. note::

   The same approach can be used for an IP-based control socket:

   .. code-block:: nginx

       location / {
           proxy_pass http://127.0.0.1:8080;
       }
