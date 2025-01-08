#########
Scripting
#########

NGINX Unit's :doc:`control API <controlapi>` supports
JavaScript expressions, including function calls, in the form of
`template literals
<https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Template_literals>`__
written in
`NGINX JavaScript <https://nginx.org/en/docs/njs/>`__ ( :program:`njs` ).
They can be used with these :doc:`configuration <configuration/index>` options:

- **pass** in
  :ref:`listeners <configuration-listeners>`
  and
  :ref:`actions <configuration-routes-action>`
  to choose between routes, applications, app targets, or upstreams.

- **response_headers** values in
  :ref:`actions <configuration-routes-action>`
  to manipulate response header fields.

- **rewrite** in
  :ref:`actions <configuration-routes-action>`
  to enable :ref:`URI rewriting <configuration-rewrite>`.

- **share** and **chroot** in
  :ref:`actions <configuration-routes-action>`
  to control
  :ref:`static content serving <configuration-static>`.

- **location** in **return**
  :ref:`actions <configuration-return>`
  to enable HTTP redirects.

- **format** in the
  :ref:`access log <custom-log-format>`
  to customize Unit's log output.

- **if** in the
  :ref:`access log <conditional-access-log>`
  to dynamically turn Unit's logging on and off.

As its JavaScript engine,
Unit uses the :program:`njs` library,
shipped with the
:ref:`official packages <installation-precomp-pkgs>`
or
:ref:`built from source <source-njs>`.

.. warning::

   Unit 1.32.0 and later require
   `njs 0.8.2 <https://nginx.org/en/docs/njs/changes.html>`__.

Some request properties
are exposed as :program:`njs` objects or scalars:

.. list-table::
   :header-rows: 1

   * - Name
     - Type
     - Description

   * - **args**
     - Object
     - Query string arguments;
       **Color=Blue** is **args.Color**;
       can be used with **Object.keys()**.

   * - **cookies**
     - Object
     - Request cookies;
       an **authID** cookie is **cookies.authID**;
       can be used with **Object.keys()**.

   * - **headers**
     - Object
     - Request header fields;
       **Accept** is **headers.Accept**,
       **Content-Encoding** is **headers['Content-Encoding']**
       (hyphen requires an array property accessor);
       can be used with **Object.keys()**.

   * - **host**
     - Scalar
     - **Host**
       `header field
       <https://datatracker.ietf.org/doc/html/rfc7230#section-5.4>`__,
       converted to lower case and normalized
       by removing the port number and the trailing period (if any).

   * - **remoteAddr**
     - Scalar
     - Remote IP address of the request.

   * - **uri**
     - Scalar
     - `Request target
       <https://datatracker.ietf.org/doc/html/rfc7230#section-5.3>`__,
       `percent decoded
       <https://datatracker.ietf.org/doc/html/rfc3986#section-2.1>`__
       and normalized by removing the
       `query string
       <https://datatracker.ietf.org/doc/html/rfc3986#section-3.4>`__
       and resolving
       `relative references
       <https://datatracker.ietf.org/doc/html/rfc3986#section-4.2>`__
       ("." and "..", "//").

   * - **vars**
     - Object
     - Unit :ref:`variables <configuration-variables>`; vars.method is **$method**.

Template literals are wrapped in backticks.
To use a literal backtick in a string,
escape it: **\\\\`**
(escaping backslashes
is a
`JSON requirement
<https://www.json.org/json-en.html>`_).
The :program:`njs` snippets
should be enclosed in curly brackets:
**${...}**.

Next, you can upload and use custom JavaScript modules
with your configuration.
Consider this **http.js** script
that distinguishes requests
by their **Authorization** header field values:

.. code-block:: javascript

   var http = {}

   http.route = function(headers) {
       var authorization = headers['Authorization'];
       if (authorization) {
           var user = atob(authorization.split(' ')[1]);
           if (String(user) == 'user:password') {
               return 'accept';
           }

           return 'forbidden';
       }

       return 'unauthorized';
   }

   export default http

To upload it to Unit's JavaScript module storage
as **http**:

.. code-block:: console

   # curl -X PUT --data-binary @http.js --unix-socket :nxt_ph:`/path/to/control.unit.sock <Path to the remote control socket>` \
         http://localhost/js_modules/:nxt_ph:`http <Module name in Unit's configuration>`

Unit doesn't enable the uploaded modules by default,
so add the module's name to **settings/js_module**:

.. code-block:: console

   # curl -X PUT -d '":nxt_ph:`http <Module name to be enabled>`"' :nxt_ph:`/path/to/control.unit.sock <Path to the remote control socket>` \
         http://localhost/config/settings/js_module

.. note::

   Please note that the **js_module** option
   can be a string or an array; choose the appropriate HTTP method.

Now, the **http.route()** function can be used
with Unit-supplied header field values:

.. code-block:: json

   {
       "routes": {
           "entry": [
               {
                   "action": {
                       "pass": "`routes/${http.route(headers)}`"
                   }
               }
           ],

           "unauthorized": [
               {
                   "action": {
                       "return": 401
                   }
               }
           ],

           "forbidden": [
               {
                   "action": {
                       "return": 403
                   }
               }
           ],

           "accept": [
               {
                   "action": {
                       "return": 204
                   }
               }
           ]
       }
   }

.. _njs-examples:

********
Examples
********

This example adds simple routing logic
that extracts the agent name
from the **User-Agent** header field
to reject requests
issued by :program:`curl`:

.. code-block:: json

   "routes": {
       "parse": [
           {
               "action": {
                   "pass": "`routes/${ headers['User-Agent'].split('/')[0] == 'curl' ? 'reject' : 'default' }`"
               }
           }
       ],

       "reject": [
           {
               "action": {
                   "return": 400
               }
           }
       ],

       "default": [
           {
               "action": {
                   "return": 204
               }
           }
       ]
   }


This example uses a series of transformations
to log the request's
date, IP, URI,
and all its headers:

.. code-block:: json

   {
       "path": "/var/log/unit/access_kv.log",
       "format": "`@timestamp=${new Date().toISOString()} ip=${remoteAddr} uri=${uri} ${Object.keys(headers).map(k => 'req.' + k + '=\"' + headers[k] + '\"').join(' ')}\n`"
   }

The next example will add the **Cache-Control** Header based on the HTTP Request method:

.. code-block:: json

   {
       "action": {
         "pass": "applications/my_app",
         "response_headers": {
            "Cache-Control": "`${vars.method.startsWith('P') ? 'no-cache' : 'max-age=3600'}`"
         }
       }
   }


For further reference,
see the `njs documentation <https://nginx.org/en/docs/njs/>`__.