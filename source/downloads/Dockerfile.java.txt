# keep our base image as small as possible
FROM nginx/unit:1.18.0-minimal

# port used by the listener in config.json
EXPOSE 8080

# add Java language and corresponding language module
RUN apt update                                                             \
    && apt install -y apt-transport-https gnupg1                           \
    && curl https://nginx.org/keys/nginx_signing.key | apt-key add -       \
    && echo "deb https://packages.nginx.org/unit/debian/ buster unit"      \
         > /etc/apt/sources.list.d/unit.list                               \
    && mkdir -p /usr/share/man/man1/                                       \
    && apt update && apt install --no-install-recommends                   \
       --no-install-suggests -y unit-jsc11                                 \
# final cleanup
    && apt remove -y apt-transport-https gnupg1                            \
    && apt autoremove --purge -y                                           \
    && rm -rf /var/lib/apt/lists/* /etc/apt/sources.list.d/*.list

# application setup
RUN mkdir /www/ && echo                                                    \
    '<%@page language="java" contentType="text/plain"%><%="Hello, Unit!"%>'\
    > /www/index.jsp                                                       \
# prepare the app config for Unit
    && echo '{                                                             \
    "listeners": {                                                         \
        "*:8080": {                                                        \
            "pass": "applications/java_app"                                \
        }                                                                  \
    },                                                                     \
    "applications": {                                                      \
        "java_app": {                                                      \
            "type": "java",                                                \
            "webapp": "/www/"                                              \
        }                                                                  \
    }                                                                      \
    }' > /docker-entrypoint.d/config.json
