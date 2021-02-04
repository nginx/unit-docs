.. |app| replace:: Grafana
.. |mod| replace:: Go

#######
Grafana
#######

Here, we install |app| from `sources
<https://grafana.com/docs/project/building_from_source/#building-grafana-from-source>`_
so we can :ref:`configure it <configuration-external-go>` to run in Unit.

#. .. include:: ../include/howto_install_unit.rst

   Also, make sure Unit's Go module is available at :samp:`$GOPATH`.

#. Download |app|'s source files:

   .. code-block:: console

      $ go get github.com/grafana/grafana
      $ cd $GOPATH/src/github.com/grafana/grafana # This is the /path/to/app/

#. Update the code, adding Unit to |app|'s protocol list.  You can either
   apply a patch (:download:`grafana.patch <../downloads/grafana.patch>`):

   .. code-block:: console

      $ cd /path/to/app/
      $ curl -O https://unit.nginx.org/_downloads/grafana.patch
      $ patch -p1 < grafana.patch

   Or update the sources manually.  In :file:`conf/defaults.ini`:

   .. code-block:: ini
      :emphasize-lines: 4

      #################################### Server ##############################
      [server]
      # Protocol (http, https, socket, unit)
      protocol = unit

   In :file:`pkg/api/http_server.go`:

   .. code-block:: go
      :emphasize-lines: 4, 27-33

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

      case setting.HTTP, setting.HTTPS, setting.HTTP2:
          var err error
          listener, err = net.Listen("tcp", hs.httpSrv.Addr)
          if err != nil {
              return errutil.Wrapf(err, "failed to open listener on address %s", hs.httpSrv.Addr)
          }
      case setting.SOCKET:
          var err error
          listener, err = net.ListenUnix("unix", &net.UnixAddr{Name: setting.SocketPath, Net: "unix"})
          if err != nil {
              return errutil.Wrapf(err, "failed to open listener for socket %s", setting.SocketPath)
          }
      case setting.UNIT:
          var err error
          err = unit.ListenAndServe(hs.httpSrv.Addr, hs.macaron)
          if err == http.ErrServerClosed {
              hs.log.Debug("server was shutdown gracefully")
              return nil
          }

   In :file:`pkg/setting/setting.go`:

   .. code-block:: go
      :emphasize-lines: 5, 28-30

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
       if protocolStr == "https" {
           Protocol = HTTPS
           CertFile = server.Key("cert_file").String()
           KeyFile = server.Key("cert_key").String()
       }
       if protocolStr == "h2" {
           Protocol = HTTP2
           CertFile = server.Key("cert_file").String()
           KeyFile = server.Key("cert_key").String()
       }
       if protocolStr == "socket" {
           Protocol = SOCKET
           SocketPath = server.Key("socket").String()
       }
       if protocolStr == "unit" {
           Protocol = UNIT
       }

#. Build |app|:

   .. code-block:: console

      $ cd /path/to/app/
      $ go get ./...                  # install dependencies
      $ go run build.go setup
      $ go run build.go build
      $ yarn install --pure-lockfile
      $ yarn start

   Note the directory where the newly-built :file:`grafana-server` is placed,
   usually :file:`$GOPATH/bin/`; it's used by the :samp:`executable` option in
   Unit configuration.

#. .. include:: ../include/howto_change_ownership.rst

#. Next, :ref:`prepare <configuration-php>` the |app| configuration for
   Unit (use real values for :samp:`executable` and :samp:`working_directory`):

   .. code-block:: json

      {
          "listeners": {
              "*:3000": {
                  "pass": "applications/grafana"
              }
          },

          "applications": {
              "grafana": {
                  "executable": ":nxt_term:`/path/to/go/bin/dir/grafana-server <Path to the grafana-server binary>`",
                  "type": "external",
                  "working_directory": ":nxt_term:`/path/to/app/ <Path to frontend files, usually the installation path>`"
              }
          }
      }

   See :ref:`Go application options <configuration-external>` and the |app|
   `docs
   <https://grafana.com/docs/grafana/latest/installation/configuration/#static-root-path>`_
   for details.

#. .. include:: ../include/howto_upload_config.rst

   After a successful update, |app| should be available on the listener's IP
   and port:

   .. image:: ../images/grafana.png
      :width: 100%
      :alt: Grafana in Unit - Setup Screen
