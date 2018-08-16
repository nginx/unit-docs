
.. highlight:: nginx

######################
Integration with NGINX
######################

Installing Unit Behind NGINX
****************************

Configure NGINX as a static web server and reverse proxy in front of Unit.

NGINX serves static files directly from the filesystem, and the requests
to the applications are forwarded to Unit.

Create an upstream block in ``http`` context of NGINX configuration and add
Unit server IP and port to the upstream block, for example::

    upstream unit_backend {
        server 127.0.0.1:8300;
    }

Create or modify ``server`` and ``location`` blocks in ``http`` context
of NGINX configuration.  Specify static files directory and the name of
Unit upstream.

Example 1
=========

For PHP applications, all requests with URLs ending in ``.php`` will be proxied
to Unit.  All other files will be served directly by NGINX::

    server {

        location / {
            root /var/www/static-data;
        }

        location ~ \.php$ {
            proxy_pass http://unit_backend;
            proxy_set_header Host $host;
        }
    }

Example 2
=========

For the following application, all static files need to be placed in
``/var/www/files`` directory, and referenced by URLs starting with ``/static``.
All other requests will be proxied to Unit::

    server {

        location /static {
            root /var/www/files;
        }

        location / {
            proxy_pass http://unit_backend;
            proxy_set_header Host $host;
        }
    }

Refer to NGINX documentation at https://nginx.org
for more information.
Commercial support and advanced features are available at
https://www.nginx.com.

Securing and Proxying Unit API
******************************

By default, Unit API is available through a Unix domain socket.  In order for
the API to be available remotely, configure a reverse proxy with NGINX.

NGINX can provide security, authentication, and access control to the API.  It
is not recommended to expose unsecure Unit API.

Use the following configuration example for NGINX::

    server {

        # Configure SSL encryption
        server 443 ssl;
        ssl_certificate /path/to/ssl/cert.pem;
        ssl_certificate_key /path/to/ssl/cert.key;

        # Configure SSL client certificate validation
        ssl_client_certificate /path/to/ca.pem;
        ssl_verify_client on;

        # Configure network ACLs
        #allow 1.2.3.4; # Uncomment and change to the IP addresses and networks
                        # of the administrative systems.
        deny all;

        # Configure HTTP Basic authentication
        auth_basic on;
        auth_basic_user_file /path/to/htpasswd.txt;

        location / {
            proxy_pass http://unix:/path/to/control.unit.sock;
        }
    }
