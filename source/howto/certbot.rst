################
TLS with Certbot
################

To set up :ref:`SSL/TLS access in Unit <configuration-ssl>`, you need
certificate bundles.  Although you can use self-signed certificates, it's
generally advisable to obtain certificates for your website from a certificate
authority (CA).  For this purpose, you may employ EFF's `Certbot
<https://certbot.eff.org>`__ that issues free certificates signed by `Let's
Encrypt <https://letsencrypt.org>`_, a non-profit CA.

***********************
Generating Certificates
***********************

#. Install :ref:`Unit <installation-precomp-pkgs>` on your website's server.

#. Install `Certbot <https://certbot.eff.org/instructions>`__ on the same
   server, choosing :guilabel:`None of the above` in the :guilabel:`Software`
   dropdown list and the server's OS in the :guilabel:`System` dropdown list
   at EFF's website.

#. Run :program:`certbot` and follow its instructions to generate the
   certificate bundle.  You will be prompted to enter the domain name of the
   website and `validate domain ownership
   <https://letsencrypt.org/docs/challenge-types/>`_; the latter can be done
   differently.

   To use a temporary server for authentication, stop any process listening on
   port 80 and run:

   .. code-block:: console

      # certbot certonly --standalone

   After the certificate bundle is successfully saved, restart the process that
   was listening on port 80.

   If you can't run the temporary server for some reason, use DNS records to
   validate your domain:

   .. code-block:: console

      # certbot certonly --manual --preferred-challenges dns

   .. note::

      You must be able to edit the server's DNS entries to use the second
      method.  Certbot offers other domain validation methods
      (`authenticators
      <https://certbot.eff.org/docs/using.html#getting-certificates-and-choosing-plugins>`_)
      as well, but they're not discussed here for brevity.

   Both commands above store the resulting :file:`.pem` files as follows:

   .. code-block:: none

      :nxt_term:`/etc/letsencrypt/ <Location can be configured, see Certbot help>`
      └── live/
          └── :nxt_term:`www.example.com <Your website name>`
              ├── :nxt_term:`cert.pem <Leaf website certificate>`
              ├── :nxt_term:`chain.pem <Root CA certificate chain>`
              ├── :nxt_term:`fullchain.pem <Concatenation of the two PEMs above>`
              └── :nxt_term:`privkey.pem <Your private key, must be kept secret>`

#. Create a certificate bundle fit for Unit and upload it to the
   :samp:`certificates` section of Unit's :ref:`control API
   <configuration-mgmt>`:

   .. code-block:: console

      # cat /etc/letsencrypt/live/www.example.com/fullchain.pem  \
            /etc/letsencrypt/live/www.example.com/privkey.pem > bundle1.pem

      # curl -X PUT --data-binary @:nxt_term:`bundle1.pem <Bundle file>` --unix-socket  \
             :nxt_term:`/path/to/control.unit.sock <Path to Unit control socket in your installation>`  \
             http://localhost/certificates/:nxt_term:`certbot1 <Internal bundle name in Unit>`

             {
                 "success": "Certificate chain uploaded."
             }

#. Create or update a :ref:`listener <configuration-listeners>` to use the
   uploaded bundle in Unit:

   .. code-block:: console

      # curl -X PUT --data-binary  \
            '{"pass": "applications/ssl_app", "tls": {"certificate": "certbot1"}}'  \
            --unix-socket :nxt_term:`/path/to/control.unit.sock <Path to Unit control socket in your installation>`  \
            'http://localhost/config/listeners/*:443'

#. Try accessing your website via HTTPS:

   .. code-block:: console

      $ curl https://www.example.com -v

            ...
            * TLSv1.3 (OUT), TLS handshake, Client hello (1):
            * TLSv1.3 (IN), TLS handshake, Server hello (2):
            * TLSv1.3 (IN), TLS Unknown, Certificate Status (22):
            * TLSv1.3 (IN), TLS handshake, Unknown (8):
            * TLSv1.3 (IN), TLS Unknown, Certificate Status (22):
            * TLSv1.3 (IN), TLS handshake, Certificate (11):
            * TLSv1.3 (IN), TLS Unknown, Certificate Status (22):
            * TLSv1.3 (IN), TLS handshake, CERT verify (15):
            * TLSv1.3 (IN), TLS Unknown, Certificate Status (22):
            * TLSv1.3 (IN), TLS handshake, Finished (20):
            * TLSv1.3 (OUT), TLS change cipher, Client hello (1):
            * TLSv1.3 (OUT), TLS Unknown, Certificate Status (22):
            * TLSv1.3 (OUT), TLS handshake, Finished (20):
            * SSL connection using TLSv1.3 / TLS_AES_256_GCM_SHA384
            * ALPN, server did not agree to a protocol
            * Server certificate:
            *  subject: CN=www.example.com
            *  start date: Sep 21 22:10:42 2020 GMT
            *  expire date: Dec 20 22:10:42 2020 GMT
            ...


*********************
Renewing Certificates
*********************

Certbot enables renewing the certificates `manually
<https://certbot.eff.org/docs/using.html#renewing-certificates>`_ or
`automatically <https://certbot.eff.org/docs/using.html#automated-renewals>`_.
For manual renewal and rollover:

#. Repeat the steps above to renew the certificates and upload the new bundle
   under a different name:

   .. code-block:: console

      # certbot certonly --standalone

            What would you like to do?
            - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
            1: Keep the existing certificate for now
            2: Renew & replace the cert (may be subject to CA rate limits)

      # cat /etc/letsencrypt/live/www.example.com/fullchain.pem  \
            /etc/letsencrypt/live/www.example.com/privkey.pem > bundle2.pem

      # curl -X PUT --data-binary @:nxt_term:`bundle2.pem <New bundle file>` --unix-socket  \
             :nxt_term:`/path/to/control.unit.sock <Path to Unit control socket in your installation>`  \
             http://localhost/certificates/:nxt_term:`certbot2 <New internal bundle name in Unit>`

             {
                 "success": "Certificate chain uploaded."
             }

   Now you have two certificate bundles uploaded; Unit knows them as
   :samp:`certbot1` and :samp:`certbot2`.  Optionally query the
   :samp:`certificates` section to review common details such as expiry dates,
   subjects, or issuers:

   .. code-block:: console

      # curl --unix-socket :nxt_term:`/path/to/control.unit.sock <Path to Unit control socket in your installation>`  \
            'http://localhost/certificates'

#. Update the :ref:`listener <configuration-listeners>`, switching it to the
   renewed certificate bundle:

   .. code-block:: console

      # curl -X PUT --data-binary 'certbot2' --unix-socket  \
            :nxt_term:`/path/to/control.unit.sock <Path to Unit control socket in your installation>`  \
            'http://localhost/config/listeners/*:443/tls/certificate'

   .. note::

      There's no need to shut Unit down; your server can stay online during the
      rollover.

#. Delete the expired bundle:

   .. code-block:: console

      # curl -X DELETE --unix-socket :nxt_term:`/path/to/control.unit.sock <Path to Unit control socket in your installation>`  \
            'http://localhost/certificates/certbot1'

            {
                "success": "Certificate deleted."
            }

.. note::

   Currently, Certbot doesn't have `installer plugins
   <https://certbot.eff.org/docs/using.html#getting-certificates-and-choosing-plugins>`_
   that enable automatic certificate rollover in Unit.  However, you can set up
   Certbot's `hooks
   <https://certbot.eff.org/docs/using.html?highlight=hooks#renewing-certificates>`_
   using the commands above to the same effect.
