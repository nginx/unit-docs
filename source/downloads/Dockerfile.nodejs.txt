# keep our base image as small as possible
FROM nginx/unit:1.18.0-minimal

# port used by the listener in config.json
EXPOSE 8080

# add Node.js repo and install unit-dev module required to build unit-http
RUN apt update                                                             \
    && apt install -y apt-transport-https gnupg1                           \
    && curl https://nginx.org/keys/nginx_signing.key | apt-key add -       \
    && echo "deb https://packages.nginx.org/unit/debian/ buster unit"      \
         > /etc/apt/sources.list.d/unit.list                               \
    && curl https://deb.nodesource.com/setup_12.x | bash -                 \
    && apt update                                                          \
    && apt install --no-install-recommends --no-install-suggests -y        \
           libpython2.7-stdlib build-essential nodejs unit-dev             \
    && npm install -g --unsafe-perm unit-http                              \
# final cleanup
    && apt remove -y build-essential unit-dev apt-transport-https gnupg1   \
    && apt autoremove --purge -y                                           \
    && rm -rf /var/lib/apt/lists/* /etc/apt/sources.list.d/*.list

#application setup
RUN mkdir /www/ && echo '#!/usr/bin/env node                             \n\
    require("unit-http").createServer(function (req, res) {                \
        res.writeHead(200, {"Content-Type": "text/plain"});                \
        res.end("Hello, Unit!")                                            \
    }).listen()                                                            \
    ' > /www/app.js                                                        \
# make app.js executable; link unit-http locally
    && cd /www && chmod +x app.js                                          \
    && npm link unit-http                                                  \
# prepare the app config for Unit
    && echo '{                                                             \
    "listeners": {                                                         \
        "*:8080": {                                                        \
            "pass": "applications/node_app"                                \
        }                                                                  \
    },                                                                     \
    "applications": {                                                      \
        "node_app": {                                                      \
            "type": "external",                                            \
            "working_directory": "/www/",                                  \
            "executable": "app.js"                                         \
        }                                                                  \
    }                                                                      \
    }' > /docker-entrypoint.d/config.json
