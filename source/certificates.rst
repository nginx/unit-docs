 .. meta::
   :og:description: Upload SSL/TLS certificates to NGINX Unit to use
                    them with your listeners.

.. include:: include/replace.rst

.. _configuration-ssl:

####################
SSL/TLS certificates
####################

The **/certificates** section of the
:ref:`control API <configuration-api>`
handles TLS certificates that are used with Unit's
:ref:`listeners <configuration-listeners>`.

To set up SSL/TLS for a listener,
upload a **.pem** file with your certificate chain and private key to Unit,
and name the uploaded bundle in the listener's configuration;
next, the listener can be accessed via SSL/TLS.

.. note::

   For the details of certificate issuance and renewal in Unit,
   see an example in :doc:`howto/certbot`.

First, create a **.pem** file with your certificate chain and private key:

.. code-block:: console

   $ cat :nxt_ph:`cert.pem <Leaf certificate file>` :nxt_ph:`ca.pem <CA certificate file>` :nxt_ph:`key.pem <Private key file>` > :nxt_ph:`bundle.pem <Arbitrary certificate bundle's filename>`

Usually, your website's certificate
(optionally followed by the intermediate CA certificate)
is enough to build a certificate chain.
If you add more certificates to your chain,
order them leaf to root.

Upload the resulting bundle file to Unit's certificate storage
under a suitable name
(in this case, **bundle**):

.. code-block:: console

   # curl -X PUT --data-binary @:nxt_ph:`bundle.pem <Certificate bundle's filename>` --unix-socket \
          :nxt_ph:`/path/to/control.unit.sock <Path to Unit's control socket in your installation>` http://localhost/certificates/:nxt_ph:`bundle <Certificate bundle name in Unit's configuration>`

       {
           "success": "Certificate chain uploaded."
       }

.. warning::

   Don't use **-d** for file upload with :program:`curl`;
   this option damages **.pem** files.
   Use the **--data-binary** option
   when uploading file-based data
   to avoid data corruption.

Internally, Unit stores the uploaded certificate bundles
along with other configuration data
in its **state** subdirectory;
the
:ref:`control API <configuration-api>`
exposes some of their properties
as **GET**-table JSON using **/certificates**:

.. code-block:: json

   {
       "certificates": {
           ":nxt_ph:`bundle <Certificate bundle name>`": {
               "key": "RSA (4096 bits)",
               "chain": [
                   {
                       "subject": {
                           "common_name": "example.com",
                           "alt_names": [
                               "example.com",
                               "www.example.com"
                           ],

                           "country": "US",
                           "state_or_province": "CA",
                           "organization": "Acme, Inc."
                       },

                       "issuer": {
                           "common_name": "intermediate.ca.example.com",
                           "country": "US",
                           "state_or_province": "CA",
                           "organization": "Acme Certification Authority"
                       },

                       "validity": {
                           "since": "Sep 18 19:46:19 2022 GMT",
                           "until": "Jun 15 19:46:19 2025 GMT"
                       }
                   },
                   {
                       "subject": {
                           "common_name": "intermediate.ca.example.com",
                           "country": "US",
                           "state_or_province": "CA",
                           "organization": "Acme Certification Authority"
                       },

                       "issuer": {
                           "common_name": "root.ca.example.com",
                           "country": "US",
                           "state_or_province": "CA",
                           "organization": "Acme Root Certification Authority"
                       },

                       "validity": {
                           "since": "Feb 22 22:45:55 2023 GMT",
                           "until": "Feb 21 22:45:55 2026 GMT"
                       }
                   }
               ]
           }
       }
   }

.. note::

   Access array items,
   such as individual certificates in a chain,
   and their properties by indexing:

   .. code-block:: console

      # curl -X GET --unix-socket :nxt_ph:`/path/to/control.unit.sock <Path to Unit's control socket in your installation>` \
             http://localhost/certificates/:nxt_hint:`bundle <Certificate bundle name>`/chain/0/

   .. code-block:: console

      # curl -X GET --unix-socket :nxt_ph:`/path/to/control.unit.sock <Path to Unit's control socket in your installation>` \
             http://localhost/certificates/:nxt_hint:`bundle <Certificate bundle name>`/chain/0/subject/alt_names/0/

Next, add the uploaded bundle to a
:ref:`listener <configuration-listeners>`;
the resulting control API configuration may look like this:

.. code-block:: json

   {
       "certificates": {
           ":nxt_ph:`bundle <Certificate bundle name>`": {
               "key": "<key type>",
               "chain": [
                   "<certificate chain, omitted for brevity>"
               ]
           }
       },

       "config": {
           "listeners": {
               "*:443": {
                   "pass": "applications/wsgi-app",
                   "tls": {
                       "certificate": ":nxt_ph:`bundle <Certificate bundle name>`"
                   }
               }
           },

           "applications": {
               "wsgi-app": {
                   "type": "python",
                   "module": "wsgi",
                   "path": "/usr/www/wsgi-app/"
               }
           }
       }
   }

All done;
the application is now accessible via SSL/TLS:

.. code-block:: console

   $ curl -v :nxt_hint:`https://127.0.0.1 <Port 443 is conventionally used for HTTPS connections>`
       ...
       * TLSv1.2 (OUT), TLS handshake, Client hello (1):
       * TLSv1.2 (IN), TLS handshake, Server hello (2):
       * TLSv1.2 (IN), TLS handshake, Certificate (11):
       * TLSv1.2 (IN), TLS handshake, Server finished (14):
       * TLSv1.2 (OUT), TLS handshake, Client key exchange (16):
       * TLSv1.2 (OUT), TLS change cipher, Client hello (1):
       * TLSv1.2 (OUT), TLS handshake, Finished (20):
       * TLSv1.2 (IN), TLS change cipher, Client hello (1):
       * TLSv1.2 (IN), TLS handshake, Finished (20):
       * SSL connection using TLSv1.2 / AES256-GCM-SHA384
       ...

Finally, you can delete a certificate bundle
that you don't need anymore
from the storage:

.. code-block:: console

   # curl -X DELETE --unix-socket :nxt_ph:`/path/to/control.unit.sock <Path to Unit's control socket in your installation>` \
          http://localhost/certificates/:nxt_hint:`bundle <Certificate bundle name>`

       {
           "success": "Certificate deleted."
       }

.. note::

   You can't delete certificate bundles still referenced in your
   configuration, overwrite existing bundles using **put**, or delete non-existent ones.
