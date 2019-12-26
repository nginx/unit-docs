:orphan:

#######
Grafana
#######

Here, we install Grafana from `sources
<https://grafana.com/docs/project/building_from_source/#building-grafana-from-source>`_
so we can :ref:`configure it <configuration-external-go>` to run in Unit.

#. Install :ref:`Unit with Go support <installation-precomp-pkgs>`,
   making sure Unit's Go modules are available at :samp:`$GOPATH`.

#. Download Grafana files:

   .. code-block:: console

      $ go get github.com/grafana/grafana
      $ cd $GOPATH/src/github.com/grafana/grafana # path to Grafana

#. Update the code, adding Unit to the list of supported protocols.  You can
   apply a patch (:download:`grafana.patch <../downloads/grafana.patch>`):

   .. code-block:: console

      $ cd /path/to/grafana
      $ curl -O https://unit.nginx.org/_downloads/grafana.patch
      $ patch -p1 < grafana.patch

   Otherwise, update the sources manually.  In :file:`conf/defaults.ini`:

   .. code-block:: ini

      #################################### Server ##############################
      [server]
      # Protocol (http, https, socket, unit)
      protocol = unit

   In :file:`pkg/api/http_server.go`:

   .. code-block:: go

      import (
          // ...
          "net/http"
          "unit.nginx.org/go"
          "os"
          // ...
      )

      // ...

      switch setting.Protocol {

      // ...

      case setting.UNIT:
          err = unit.ListenAndServe(listenAddr, hs.macaron)
          if err == http.ErrServerClosed {
              hs.log.Debug("server was shutdown gracefully")
              return nil
          }

   In :file:`pkg/setting/setting.go`:

   .. code-block:: go

       const (
           HTTP              Scheme = "http"
           HTTPS             Scheme = "https"
           SOCKET            Scheme = "socket"
           UNIT              Scheme = "unit"
           DEFAULT_HTTP_ADDR string = "0.0.0.0"
       )

       // ...

       Protocol = HTTP
       protocolStr, err := valueAsString(server, "protocol", "http")
       // ...
       if protocolStr == "unit" {
           Protocol = UNIT
       }

#. Build your Grafana app:

   .. code-block:: console

      $ cd /path/to/grafana
      $ go run build.go setup
      $ go run build.go build
      $ yarn install --pure-lockfile
      $ yarn start

   Note the directory where the newly-built :file:`grafana-server` is placed;
   it's needed for Unit configuration.

#. .. include:: ../include/get-config.rst

   This creates a JSON file with Unit's current settings.  In
   :samp:`listeners`, add a :ref:`listener <configuration-listeners>` that
   points to your app in :samp:`applications`; the app must reference
   the path to Grafana and the executable you've built:

   .. code-block:: json

      {
          "listeners": {
              "*:3000": {
                  "pass": "applications/grafana"
              }
          },

          "applications": {
              "grafana": {
                  "executable": "/path/to/grafana/build/dir/grafana-server",
                  "type": "external",
                  "user": "grafanauser",
                  "working_directory": "/path/to/grafana/"
               }
           }
       }

   See :ref:`Go application options <configuration-external>` for details.

#. Upload the updated configuration:

   .. code-block:: console

      # curl -X PUT --data-binary @config.json --unix-socket \
             /path/to/control.unit.sock http://localhost/config

   After a successful update, Grafana should be available on the listener's IP
   and port:

   .. image:: ../images/grafana.png
      :width: 100%
      :alt: Grafana in Unit - Setup Screen
