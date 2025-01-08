################
TLS with Certbot
################

To set up :ref:`SSL/TLS access in Unit <configuration-ssl>`, you need
certificate bundles.  Although you can use self-signed certificates, it's
advisable to obtain certificates for your website from a certificate authority
(CA).  For this purpose, you may employ EFF's `Certbot
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

#. Run the :program:`certbot` utility and follow its instructions to create the
   certificate bundle.  You'll be prompted to enter the domain name of the
   website and `validate domain ownership
   <https://letsencrypt.org/docs/challenge-types/>`_; the latter can be done
   differently.  Perhaps, the easiest approach is to use the `webroot
   <https://eff-certbot.readthedocs.io/en/stable/using.html#webroot>`__ method
   by having Certbot store a certain file locally and then access it by your
   domain name.  First, configure Unit with a temporary route at port 80:

   .. code-block:: json

      {
          "listeners": {
              ":nxt_hint:`*:80 <Certbot attempts to reach the domain name at port 80>`": {
                  "pass": "routes/acme"
              }
          },

          "routes": {
              "acme": [
                  {
                      "match": {
                          "uri": ":nxt_hint:`/.well-known/acme-challenge/* <The URI that Certbot probes to download the file>`"
                      },

                      "action": {
                          "share": ":nxt_ph:`/var/www/www.example.com$uri/ <Arbitrary directory, preferably the one used for storing static files>`"
                      }
                  }
              ]
          }
      }

   Make sure the **share** directory is accessible for Unit's :ref:`router
   process <security-apps>` user account, usually **unit:unit**.

   Next, run :program:`certbot`, supplying the **share** directory as the
   webroot path:

   .. code-block:: console

      # certbot certonly --webroot -w :nxt_ph:`/var/www/www.example.com/ <Path where the file should be stored>` -d :nxt_ph:`www.example.com <Your domain name>`

   If you can't employ the previous method for some reason, try using DNS
   records to validate your domain:

   .. code-block:: console

      # certbot certonly --manual --preferred-challenges dns -d :nxt_ph:`www.example.com <Your domain name>`

   Certbot will provide instructions on updating the DNS entries to prove
   domain ownership.

   Any such :program:`certbot` command stores the resulting **.pem** files
   as follows:

   .. code-block:: none

      :nxt_hint:`/etc/letsencrypt/ <Location can be configured, see Certbot help>`
      └── live/
          └── :nxt_hint:`www.example.com <Your website name>`
              ├── :nxt_hint:`cert.pem <Leaf website certificate>`
              ├── :nxt_hint:`chain.pem <Root CA certificate chain>`
              ├── :nxt_hint:`fullchain.pem <Concatenation of the two PEMs above>`
              └── :nxt_hint:`privkey.pem <Your private key, must be kept secret>`

   .. note::

      Certbot offers other validation methods (`authenticators
      <https://eff-certbot.readthedocs.io/en/stable/using.html#getting-certificates-and-choosing-plugins>`_)
      as well, but they're omitted here for brevity.

#. Create a certificate bundle fit for Unit and upload it to the
   **certificates** section of Unit's :ref:`control API
   <configuration-api>`:

   .. code-block:: console

      # cat /etc/letsencrypt/live/www.example.com/fullchain.pem  \
            /etc/letsencrypt/live/www.example.com/privkey.pem > :nxt_ph:`bundle1.pem <Arbitrary certificate bundle's filename>`

   .. code-block:: console

      # curl -X PUT --data-binary @:nxt_ph:`bundle1.pem <Certificate bundle's filename>`  \
             --unix-socket :nxt_ph:`/path/to/control.unit.sock <Path to Unit's control socket in your installation>`  \
             http://localhost/certificates/:nxt_ph:`certbot1 <Certificate bundle name in Unit's configuration>`

             {
                 "success": "Certificate chain uploaded."
             }

#. Create or update a :ref:`listener <configuration-listeners>` to use the
   uploaded bundle in Unit:

   .. code-block:: console

      # curl -X PUT --data-binary  \
            '{"pass": "applications/ssl_app", "tls": {"certificate": ":nxt_ph:`certbot1 <Certificate bundle name in Unit's configuration>`"}}'  \
            --unix-socket :nxt_ph:`/path/to/control.unit.sock <Path to Unit's control socket in your installation>`  \
            'http://localhost/config/listeners/:nxt_hint:`*:443 <Listener's name in Unit's configuration>`'

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
<https://eff-certbot.readthedocs.io/en/stable/using.html#renewing-certificates>`_
or `automatically
<https://eff-certbot.readthedocs.io/en/stable/using.html#automated-renewals>`_.
For manual renewal and rollover:

#. Repeat the preceding steps to renew the certificates and upload the new
   bundle under a different name:

   .. code-block:: console

      # certbot certonly --standalone

            What would you like to do?
            - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
            1: Keep the existing certificate for now
            2: Renew & replace the cert (may be subject to CA rate limits)

   .. code-block:: console

      # cat /etc/letsencrypt/live/www.example.com/fullchain.pem  \
            /etc/letsencrypt/live/www.example.com/privkey.pem > :nxt_ph:`bundle2.pem <Arbitrary certificate bundle's filename>`

   .. code-block:: console

      # curl -X PUT --data-binary @:nxt_ph:`bundle2.pem <Certificate bundle's filename>`  \
             --unix-socket :nxt_ph:`/path/to/control.unit.sock <Path to Unit's control socket in your installation>`  \
             http://localhost/certificates/:nxt_ph:`certbot2 <Certificate bundle name in Unit's configuration>`

             {
                 "success": "Certificate chain uploaded."
             }

   Now you have two certificate bundles uploaded; Unit knows them as
   **certbot1** and **certbot2**.  Optionally, query the
   **certificates** section to review common details such as expiry dates,
   subjects, or issuers:

   .. code-block:: console

      # curl --unix-socket :nxt_ph:`/path/to/control.unit.sock <Path to Unit's control socket in your installation>`  \
             http://localhost/certificates

#. Update the :ref:`listener <configuration-listeners>`, switching it to the
   renewed certificate bundle:

   .. code-block:: console

      # curl -X PUT --data-binary ':nxt_ph:`certbot2 <New certificate bundle name in Unit's configuration>`'  \
            --unix-socket :nxt_ph:`/path/to/control.unit.sock <Path to Unit's control socket in your installation>`  \
            'http://localhost/config/listeners/:nxt_hint:`*:443 <Listener's name in Unit's configuration>`/tls/certificate'

   .. note::

      There's no need to shut Unit down; your server can stay online during the
      rollover.

#. Delete the expired bundle:

   .. code-block:: console

      # curl -X DELETE --unix-socket :nxt_ph:`/path/to/control.unit.sock <Path to Unit's control socket in your installation>`  \
            'http://localhost/certificates/:nxt_ph:`certbot1 <Old certificate bundle name in Unit's configuration>`'

            {
                "success": "Certificate deleted."
            }

#. You can also make use of Unit's :ref:`SNI <configuration-listeners>` support
   by configuring several certificate bundles for a listener.

   Suppose you've successfully used Certbot to obtain Let's Encrypt
   certificates for two domains, **www.example.com** and
   **cdn.example.com**.  First, upload them to Unit using the same steps as
   earlier:

   .. code-block:: console

      # cat /etc/letsencrypt/live/cdn.example.com/fullchain.pem  \
            /etc/letsencrypt/live/cdn.example.com/privkey.pem > :nxt_hint:`cdn.example.com.pem <Arbitrary certificate bundle's filename>`

   .. code-block:: console

      # cat /etc/letsencrypt/live/www.example.com/fullchain.pem  \
            /etc/letsencrypt/live/www.example.com/privkey.pem > :nxt_hint:`www.example.com.pem <Arbitrary certificate bundle's filename>`

   .. code-block:: console

      # curl -X PUT --data-binary @:nxt_hint:`cdn.example.com.pem <Certificate bundle's filename>`  \
             --unix-socket :nxt_ph:`/path/to/control.unit.sock <Path to Unit's control socket in your installation>`  \
             http://localhost/certificates/:nxt_hint:`cdn.example.com <Certificate bundle name in Unit's configuration>`

             {
                 "success": "Certificate chain uploaded."
             }

   .. code-block:: console

      # curl -X PUT --data-binary @:nxt_hint:`www.example.com.pem <Certificate bundle's filename>`  \
             --unix-socket :nxt_ph:`/path/to/control.unit.sock <Path to Unit's control socket in your installation>`  \
             http://localhost/certificates/:nxt_hint:`www.example.com <Certificate bundle name in Unit's configuration>`

             {
                 "success": "Certificate chain uploaded."
             }

   Next, configure the listener, supplying both bundles as an array value for
   the **tls/certificate** option:

   .. code-block:: console

      # curl -X PUT --data-binary '{"certificate": :nxt_hint:`["cdn.example.com", "www.example.com"] <Certificate bundle names in Unit's configuration>`}'  \
            --unix-socket :nxt_ph:`/path/to/control.unit.sock <Path to Unit's control socket in your installation>`  \
            'http://localhost/config/listeners/:nxt_hint:`*:443 <Listener's name in Unit's configuration>`/tls'

   Unit does the rest of the job, automatically figuring out which bundle to
   produce for each incoming connection to both domain names.

.. note::

   Currently, Certbot doesn't have `installer plugins
   <https://eff-certbot.readthedocs.io/en/stable/using.html#getting-certificates-and-choosing-plugins>`_
   that enable automatic certificate rollover in Unit.  However, you can set up
   Certbot's `hooks
   <https://eff-certbot.readthedocs.io/en/stable/using.html#renewing-certificates>`_
   using the commands listed here to the same effect.
