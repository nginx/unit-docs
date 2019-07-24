# keep our base image as small as possible
FROM nginx/unit:1.9.0-minimal

# port used by the listener in config.json
EXPOSE 8080

# add Perl language and corresponding language module
RUN apt update                                                             \
    && apt install -y apt-transport-https gnupg1                           \
    && curl https://nginx.org/keys/nginx_signing.key | apt-key add -       \
    && echo "deb https://packages.nginx.org/unit/debian/ stretch unit"     \
         > /etc/apt/sources.list.d/unit.list                               \
    && echo "deb-src https://packages.nginx.org/unit/debian/ stretch unit" \
         >> /etc/apt/sources.list.d/unit.list                              \
    && apt update                                                          \
    && apt install -y unit-perl                                            \
# final cleanup
    && apt remove -y apt-transport-https gnupg1                            \
    && apt autoremove --purge -y                                           \
    && rm -rf /var/lib/apt/lists/* /etc/apt/sources.list.d/*.list

#application setup
RUN mkdir /www/ && echo '#!/usr/bin/env perl                             \n\
    use strict;                                                            \
    use warnings;                                                          \
    my $app = sub {                                                        \
      return [                                                             \
        "200",                                                             \
        [ "Content-Type" => "text/plain" ],                                \
        [ "Hello, Unit!" ],                                                \
      ];                                                                   \
    };' > /www/app.psgi                                                    \
# launch Unit
    && unitd --control unix:/var/run/control.unit.sock                     \
# upload the app config to Unit
    && curl -X PUT --data-binary '{                                        \
    "listeners": {                                                         \
        "*:8080": {                                                        \
            "pass": "applications/perl_app"                                \
        }                                                                  \
    },                                                                     \
    "applications": {                                                      \
        "perl_app": {                                                      \
            "type": "perl",                                                \
            "working_directory": "/www/",                                  \
            "script": "/www/app.psgi"                                      \
        }                                                                  \
    }                                                                      \
    }' --unix-socket /var/run/control.unit.sock http://localhost/config/

