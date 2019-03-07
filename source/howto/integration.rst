:orphan:

#################
NGINX Integration
#################

*****************
Configuring NGINX
*****************

Essentially, NGINX works as a static web server and reverse proxy in front of
Unit, serving static files directly from the filesystem and proxying
application-related requests to Unit.

For a simple NGINX setup, create an upstream in the :samp:`http` configuration
context, adding Unit IP and port:

.. code-block:: nginx

   upstream unit_backend {
       server 127.0.0.1:8300;
   }

Next, specify the static files directory and the upstream in :samp:`server` and
:samp:`location` within :samp:`http`. Examples:

#. NGINX proxies requests with URLs ending in :samp:`.php` to Unit and serves
   other files by itself:

   .. code-block:: nginx

       server {

           location / {
               root /var/www/static-data;
           }

           location ~ \.php$ {
               proxy_pass http://unit_backend;
               proxy_set_header Host $host;
           }
       }

#. URLs starting with :samp:`/static` indicate files from
   :file:`/var/www/files`; other requests are proxied to Unit:

   .. code-block:: nginx

       server {

           location /static {
               root /var/www/files;
           }

           location / {
               proxy_pass http://unit_backend;
               proxy_set_header Host $host;
           }
       }

For details, see the `NGINX documentation <https://nginx.org>`_.  Commercial
support and advanced features are `also available <https://www.nginx.com>`_.

**************************
Securely Proxying Unit API
**************************

By default, Unit exposes its API via a Unix domain socket.  For remote access,
use NGINX as a reverse proxy.

.. warning::

    Use NGINX for robust security, authentication, and access control in
    production scenarios.  We strongly recommend against exposing an unsecured
    Unit API.

Use the following configuration template for NGINX:

.. code-block:: nginx

    server {

        # Configure SSL encryption
        server 443 ssl;
        ssl_certificate /path/to/ssl/cert.pem;
        ssl_certificate_key /path/to/ssl/cert.key;

        # Configure SSL client certificate validation
        ssl_client_certificate /path/to/ca.pem;
        ssl_verify_client on;

        # Configure network ACLs
        #allow 1.2.3.4; # Uncomment and update with the IP addresses
                        # and networks of your administrative systems.
        deny all;

        # Configure HTTP Basic authentication
        auth_basic on;
        auth_basic_user_file /path/to/htpasswd;

        location / {
            proxy_pass http://unix:/path/to/control.unit.sock;
        }
    }
