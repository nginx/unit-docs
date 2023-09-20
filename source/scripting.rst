#########
Scripting
#########

NGINX Unit's :doc:`control API <controlapi>` supports
JavaScript expressions,
including function calls,
in the form of
`template literals
<https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Template_literals>`__
written in the
:program:`njs`
`dialect <https://nginx.org/en/docs/njs/>`__
of JavaScript.
They can be used
with these
:doc:`configuration <configuration>`
options:

- :samp:`pass` in
  :ref:`listeners <configuration-listeners>`
  and
  :ref:`actions <configuration-routes-action>`
  to choose between routes, applications, app targets, or upstreams.

- :samp:`response_headers` values in
  :ref:`actions <configuration-routes-action>`
  to manipulate response header fields.

- :samp:`rewrite` in
  :ref:`actions <configuration-routes-action>`
  to enable :ref:`URI rewriting <configuration-rewrite>`.

- :samp:`share` and :samp:`chroot` in
  :ref:`actions <configuration-routes-action>`
  to control
  :ref:`static content serving <configuration-static>`.

- :samp:`location` in :samp:`return`
  :ref:`actions <configuration-return>`
  to enable HTTP redirects.

- :samp:`format` in the
  :ref:`access log <configuration-access-log>`
  to customize Unit's log output.


As its JavaScript engine,
Unit uses the :program:`njs` library,
shipped with the
:ref:`official packages <installation-precomp-pkgs>`
or
:ref:`built from source <source-njs>`.

.. warning::

   Unit 1.31+ doesn't support
   pre-0.8 :program:`njs`
   `versions <https://nginx.org/en/docs/njs/changes.html>`__;
   please update.

Some request properties
are exposed as :program:`njs` objects or scalars:

.. list-table::
   :header-rows: 1

   * - Name
     - Type
     - Description

   * - :samp:`args`
     - Object
     - Query string arguments;
       :samp:`Color=Blue` is :samp:`args.Color`;
       can be used with :samp:`Object.keys()`.

   * - :samp:`cookies`
     - Object
     - Request cookies;
       an :samp:`authID` cookie is :samp:`cookies.authID`;
       can be used with :samp:`Object.keys()`.

   * - :samp:`headers`
     - Object
     - Request header fields;
       :samp:`Accept` is :samp:`headers.Accept`,
       :samp:`Content-Encoding` is :samp:`headers['Content-Encoding']`
       (hyphen requires an array property accessor);
       can be used with :samp:`Object.keys()`.

   * - :samp:`host`
     - Scalar
     - :samp:`Host`
       `header field
       <https://datatracker.ietf.org/doc/html/rfc7230#section-5.4>`__,
       converted to lower case and normalized
       by removing the port number and the trailing period (if any).

   * - :samp:`remoteAddr`
     - Scalar
     - Remote IP address of the request.

   * - :samp:`uri`
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

Template lterals are wrapped in backticks.
To use a literal backtick in a string,
escape it: :samp:`\\\\\\\\``
(escaping backslashes
is a
`JSON requirement
<https://www.json.org/json-en.html>`_).
The :program:`njs` snippets
should be enclosed in curly brackets:
:samp:`$\\{...\\}`.

Next, you can upload and use custom JavaScript modules
with your configuration.
Consider this :file:`http.js` script
that distinguishes requests
by their :samp:`Authorization` header field values:

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
as :samp:`http`:

.. code-block:: console

   # curl -X PUT --data-binary @http.js --unix-socket :nxt_ph:`/path/to/control.unit.sock <Path to the remote control socket>` \
         http://localhost/js_modules/:nxt_ph:`http <Module name in Unit's configuration>`

Unit doesn't enable the uploaded modules by default,
so add the module's name to :samp:`settings/js_module`:

.. code-block:: console

   # curl -X PUT -d '":nxt_ph:`http <Module name to be enabled>`"' :nxt_ph:`/path/to/control.unit.sock <Path to the remote control socket>` \
         http://localhost/config/settings/js_module

.. note::

   Mind that the :samp:`js_module` option
   can be a string or an array,
   so choose the appropriate HTTP method.

Now, the :samp:`http.route()` function can be used
with Unit-supplied header field values:

.. code-block:: json

   {
       "routes": {
           "entry": [
               {
                   "action": {
                       "pass": "routes/`${http.route(headers)}`"
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
from the :samp:`User-Agent` header field
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


This uses a series of transformations
to log the request's
date, IP, URI,
and all its headers:

.. code-block:: json

   {
       "path": "/var/log/unit/access_kv.log",
       "format": "`@timestamp=${new Date().toISOString()} ip=${remoteAddr} uri=${uri} ${Object.keys(headers).map(k => 'req.' + k + '=\"' + headers[k] + '\"').join(' ')}\n`"
   }

For further reference,
see the :program:`njs`
`documentation <https://nginx.org/en/docs/njs/>`__.
