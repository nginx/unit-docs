# keep our base image as small as possible
FROM nginx/unit:1.18.0-go1.11-dev

# port used by the listener in config.json
EXPOSE 8080

# application setup
RUN mkdir /www/ && echo '                                                  \
    package main;                                                          \
    import (                                                               \
        "io";                                                              \
        "net/http";                                                        \
        "unit.nginx.org/go"                                                \
    );                                                                     \
    func main() {                                                          \
        http.HandleFunc("/",func (w http.ResponseWriter, r *http.Request) {\
            io.WriteString(w, "Hello, Unit!")                              \
        });                                                                \
        unit.ListenAndServe(":8080", nil)                                  \
    }                                                                      \
    ' > /www/app.go                                                        \
# install build tools to compile the app
    && apt update && apt install --no-install-recommends                   \
                         --no-install-suggests -y build-essential          \
# make nginx/unit package available at $GOPATH to compile the app
    && cp -r /usr/share/gocode/src/* /usr/lib/go-1.11/src/                 \
    && /usr/lib/go-1.11/bin/go build -o /www/app /www/app.go               \
# final cleanup
    && apt remove -y build-essential                                       \
    && apt autoremove --purge -y                                           \
    && rm -rf /var/lib/apt/lists/* /etc/apt/sources.list.d/*.list          \
    && rm /www/app.go

# prepare the app config for Unit
RUN echo '{                                                                \
    "listeners": {                                                         \
        "*:8080": {                                                        \
            "pass": "applications/go_app"                                  \
        }                                                                  \
    },                                                                     \
    "applications": {                                                      \
        "go_app": {                                                        \
            "type": "external",                                            \
            "working_directory": "/www/",                                  \
            "executable": "/www/app"                                       \
        }                                                                  \
    }                                                                      \
    }' > /docker-entrypoint.d/config.json                                  \
