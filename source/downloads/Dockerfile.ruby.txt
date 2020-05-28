# keep our base image as small as possible
FROM nginx/unit:1.18.0-ruby2.5

# port used by the listener in config.json
EXPOSE 8080

# application setup
RUN mkdir /www/ && echo '                                                  \
    app = Proc.new do |env|                                                \
        ["200", {                                                          \
            "Content-Type" => "text/plain",                                \
        }, ["Hello, Unit!"]]                                               \
    end;                                                                   \
    run app                                                                \
    ' > /www/config.ru                                                     \
# prepare the app config for Unit
    && echo '{                                                             \
    "listeners": {                                                         \
        "*:8080": {                                                        \
            "pass": "applications/ruby_app"                                \
        }                                                                  \
    },                                                                     \
    "applications": {                                                      \
        "ruby_app": {                                                      \
            "type": "ruby",                                                \
            "working_directory": "/www/",                                  \
            "script": "config.ru"                                          \
        }                                                                  \
    }                                                                      \
    }' > /docker-entrypoint.d/config.json
