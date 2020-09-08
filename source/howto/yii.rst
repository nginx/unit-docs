###
Yii
###

To run apps based on the `Yii <https://www.yiiframework.com>`_ framework
versions 1.1 or 2.0 using Unit:

.. tabs::
   :prefix: yii

   .. tab:: Yii 2.0

      #. Install :ref:`Unit <installation-precomp-pkgs>` with a PHP language
         module.

      #. Next, `install
         <https://www.yiiframework.com/doc/guide/2.0/en/start-installation>`__
         Yii and create or deploy your app.

         Here, we use Yii's `basic project template
         <https://www.yiiframework.com/doc/guide/2.0/en/start-installation#installing-from-composer>`__
         and Composer:

         .. code-block:: console

            $ cd /path/to/
            $ composer create-project --prefer-dist yiisoft/yii2-app-basic app

         This creates the app's directory tree at :file:`/path/to/app/`.
         Its :file:`web/` subdirectory contains both the root
         :file:`index.php` and the static files; if your app requires
         additional :file:`.php` scripts, also store them here.

      #. Prepare and upload the app :ref:`configuration
         <configuration-php>` to Unit (note the use of :samp:`uri`,
         :samp:`share`, and :samp:`fallback`):

         .. code-block:: json

            {
                "listeners": {
                    "*:80": {
                        "pass": "routes/yii"
                    }
                },

                "routes": {
                    "yii": [
                        {
                            "match": {
                                "uri": [
                                    "!/assets/*",
                                    "*.php",
                                    "*.php/*"
                                ]
                            },

                            "action": {
                                "pass": "applications/yii/direct"
                            }
                        },
                        {
                            "action": {
                                "share": "/path/to/app/web/",
                                "fallback": {
                                    "pass": "applications/yii/index"
                                }
                            }
                        }
                    ]
                },

                "applications": {
                    "yii": {
                        "type": "php",
                        "user": "www-data",
                        "targets": {
                            "direct": {
                                "root": "/path/to/app/web/"
                            },
          
                            "index": {
                                "root": "/path/to/app/web/",
                                "script": "index.php"
                            }
                        }
                    }
                }
            }

         For a detailed discussion, see `Configuring Web Servers
         <https://www.yiiframework.com/doc/guide/2.0/en/start-installation#configuring-web-servers>`_
         and `Running Applications
         <https://www.yiiframework.com/doc/guide/2.0/en/start-workflow>`_ in
         Yii 2.0 docs.

         .. note::

            The difference between the :samp:`pass` targets is their usage of
            the :samp:`script` :ref:`setting <configuration-php>`:

            - The :samp:`direct` target runs the :samp:`.php` script from the
              URI or :samp:`index.php` if the URI omits it.
            - The :samp:`index` target specifies the :samp:`script` that Unit
              runs for *any* URIs the target receives.

      #. Upload the configuration to Unit.  Assuming the config above is saved
         as :file:`yii.json`:

         .. code-block:: console

            # curl -X PUT --data-binary @yii.json --unix-socket \
                   :nxt_term:`/path/to/control.unit.sock <Path to Unit control socket in your installation>` http://localhost/config

      #. Finally, browse to http://localhost:80 to check out your app locally:

         .. image:: ../images/yii2.png
            :width: 100%
            :alt: Yii Basic Template App on Unit

   .. tab:: Yii 1.1

      #. Install :ref:`Unit <installation-precomp-pkgs>` with a PHP language
         module.

      #. Next, `install
         <https://www.yiiframework.com/doc/guide/1.1/en/quickstart.installation>`__
         Yii and create or deploy your app.

         Here, we use Yii's `basic project template
         <https://www.yiiframework.com/doc/guide/1.1/en/quickstart.first-app>`__
         and :program:`yiic`:

         .. code-block:: console

            $ git clone git@github.com:yiisoft/yii.git /path/to/yii1.1/
            $ /path/to/yii1.1/framework/yiic webapp /path/to/app

         This creates the app's directory tree at :file:`/path/to/app/`.

      #. Prepare and upload the app :ref:`configuration
         <configuration-php>` to Unit (note the use of :samp:`uri`,
         :samp:`share`, and :samp:`fallback`):

         .. code-block:: json

            {
                "listeners": {
                    "*:80": {
                        "pass": "routes/yii"
                    }
                },

                "routes": {
                    "yii": [
                        {
                            "match": {
                                "uri": [
                                    "!/assets/*",
                                    "!/protected/*",
                                    "!/themes/*",
                                    "*.php",
                                    "*.php/*"
                                ]
                            },

                            "action": {
                                "pass": "applications/yii/direct"
                            }
                        },
                        {
                            "action": {
                                "share": "/path/to/app/",
                                "fallback": {
                                    "pass": "applications/yii/index"
                                }
                            }
                        }
                    ]
                },

                "applications": {
                    "yii": {
                        "type": "php",
                        "user": "www-data",
                        "targets": {
                            "direct": {
                                "root": "/path/to/app/"
                            },
                            "index": {
                                "root": "/path/to/app/",
                                "script": "index.php"
                            }
                        }
                    }
                }
            }

         For a detailed discussion, see Yii 1.1 `docs
         <https://www.yiiframework.com/doc/guide/1.1/en/quickstart.first-app>`_.

         .. note::

            The difference between the :samp:`pass` targets is their usage of
            the :samp:`script` :ref:`setting <configuration-php>`:

            - The :samp:`direct` target runs the :samp:`.php` script from the
              URI or :samp:`index.php` if the URI omits it.
            - The :samp:`index` target specifies the :samp:`script` that Unit
              runs for *any* URIs the target receives.

      #. Upload the configuration to Unit.  Assuming the config above is saved
         as :file:`yii.json`:

         .. code-block:: console

            # curl -X PUT --data-binary @yii.json --unix-socket \
                   :nxt_term:`/path/to/control.unit.sock <Path to Unit control socket in your installation>` http://localhost/config

      #. Finally, browse to http://localhost:80 to check out your app locally:

         .. image:: ../images/yii1.1.png
            :width: 100%
            :alt: Yii Basic Template App on Unit
