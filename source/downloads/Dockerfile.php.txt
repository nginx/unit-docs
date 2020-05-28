# keep our base image as small as possible
FROM nginx/unit:1.18.0-php7.3

# port used by the listener in config.json
EXPOSE 8080

# application setup
RUN mkdir /www/ && echo '<?php echo "Hello, Unit!"; ?>' > /www/index.php   \
# prepare the app config for Unit
    && echo '{                                                             \
    "listeners": {                                                         \
        "*:8080": {                                                        \
            "pass": "applications/php_app"                                 \
        }                                                                  \
    },                                                                     \
    "applications": {                                                      \
        "php_app": {                                                       \
            "type": "php",                                                 \
            "root": "/www/"                                                \
        }                                                                  \
    }                                                                      \
    }' > /docker-entrypoint.d/config.json
