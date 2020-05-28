# keep our base image as small as possible
FROM nginx/unit:1.18.0-python3.7

# port used by the listener in config.json
EXPOSE 8080

# application setup
RUN mkdir /www/ && echo '                                                \n\
def application(environ, start_response):                                \n\
    start_response("200 OK", [("Content-Type", "text/plain")])           \n\
    return (b"Hello, Unit!")                                               \
    ' > /www/wsgi.py                                                       \
# prepare the app config for Unit
    && echo '{                                                             \
    "listeners": {                                                         \
        "*:8080": {                                                        \
            "pass": "applications/python_app"                              \
        }                                                                  \
    },                                                                     \
    "applications": {                                                      \
        "python_app": {                                                    \
            "type": "python",                                              \
            "path": "/www/",                                               \
            "module": "wsgi"                                               \
        }                                                                  \
    }                                                                      \
    }' > /docker-entrypoint.d/config.json
