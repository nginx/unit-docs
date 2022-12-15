 .. meta::
   :og:description: Upload SSL/TLS certificates to NGINX Unit to use
                    them with your listeners.

.. include:: include/replace.rst

.. _configuration-ssl:

####################
SSL/TLS Certificates
####################

The :samp:`/certificates` section of the :ref:`control API <configuration-api>`
handles TLS certificates that are used with Unit's :ref:`listeners
<configuration-listeners>`.

To set up SSL/TLS for a listener, upload a :file:`.pem` file with your
certificate chain and private key to Unit and name the uploaded bundle in the
listener's configuration; next, the listener can be accessed via SSL/TLS.

.. note::

   For the details of certificate issuance and renewal in Unit, see an
   example in :doc:`howto/certbot`.

First, create a :file:`.pem` file with your certificate chain and private key:

.. code-block:: console

   $ cat :nxt_ph:`cert.pem <Leaf certificate file>` :nxt_ph:`ca.pem <CA certificate file>` :nxt_ph:`key.pem <Private key file>` > :nxt_ph:`bundle.pem <Arbitrary certificate bundle's filename>`

Usually, your website's certificate (optionally followed by the intermediate CA
certificate) is enough to build a certificate chain.  If you add more
certificates to your chain, order them leaf to root.

Upload the resulting bundle file to Unit's certificate storage under a suitable
name (in this case, :samp:`bundle`):

.. code-block:: console

   # curl -X PUT --data-binary @:nxt_ph:`bundle.pem <Certificate bundle's filename>` --unix-socket \
          :nxt_ph:`/path/to/control.unit.sock <Path to Unit's control socket in your installation>` http://localhost/certificates/:nxt_ph:`bundle <Certificate bundle name in Unit's configuration>`

       {
           "success": "Certificate chain uploaded."
       }

.. warning::

   Don't use :option:`!-d` for file upload with :program:`curl`; this option
   damages :file:`.pem` files.  Use the :option:`!--data-binary` option when
   uploading file-based data to avoid data corruption.

Internally, Unit stores the uploaded certificate bundles along with other
configuration data in its :file:`state` subdirectory; the control API exposes
some of their properties as :samp:`GET`-table JSON via :samp:`/certificates`:

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
                           "since": "Sep 18 19:46:19 2018 GMT",
                           "until": "Jun 15 19:46:19 2021 GMT"
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
                           "since": "Feb 22 22:45:55 2016 GMT",
                           "until": "Feb 21 22:45:55 2019 GMT"
                       }
                   }
               ]
           }
       }
   }

.. note::

   Access array items, such as individual certificates in a chain, and their
   properties by indexing:

   .. code-block:: console

      # curl -X GET --unix-socket :nxt_ph:`/path/to/control.unit.sock <Path to Unit's control socket in your installation>` \
             http://localhost/certificates/:nxt_hint:`bundle <Certificate bundle name>`/chain/0/
      # curl -X GET --unix-socket :nxt_ph:`/path/to/control.unit.sock <Path to Unit's control socket in your installation>` \
             http://localhost/certificates/:nxt_hint:`bundle <Certificate bundle name>`/chain/0/subject/alt_names/0/

Next, add the uploaded bundle to a :ref:`listener <configuration-listeners>`;
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

Now you're solid; the application is accessible via SSL/TLS:

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

Finally, you can :samp:`DELETE` a certificate bundle that you don't need
anymore from the storage:

.. code-block:: console

   # curl -X DELETE --unix-socket :nxt_ph:`/path/to/control.unit.sock <Path to Unit's control socket in your installation>` \
          http://localhost/certificates/:nxt_hint:`bundle <Certificate bundle name>`

       {
           "success": "Certificate deleted."
       }

.. note::

   You can't delete certificate bundles still referenced in your
   configuration, overwrite existing bundles using :samp:`PUT`, or (obviously)
   delete non-existent ones.


