# keep our base image as small as possible
FROM nginx/unit:1.18.0-perl5.28

# port used by the listener in config.json
EXPOSE 8080

#application setup
RUN mkdir /www/ && echo '                                                  \
    my $app = sub {                                                        \
        return [                                                           \
            "200",                                                         \
            [ "Content-Type" => "text/plain" ],                            \
            [ "Hello, Unit!" ],                                            \
        ]                                                                  \
    };                                                                     \
    ' > /www/app.psgi                                                      \
# prepare the app config for Unit
    && echo '{                                                             \
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
    }' > /docker-entrypoint.d/config.json
