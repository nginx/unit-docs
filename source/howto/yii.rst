.. |app| replace:: Yii
.. |mod| replace:: PHP

###
Yii
###

To run apps based on the `Yii <https://www.yiiframework.com>`_ framework
versions 1.1 or 2.0 using Unit:

.. tabs::
   :prefix: version

   .. tab:: Yii 2.0

      #. .. include:: ../include/howto_install_unit.rst

      #. Next, `install
         <https://www.yiiframework.com/doc/guide/2.0/en/start-installation>`__
         Yii and create or deploy your app.

         Here, we use Yii's `basic project template
         <https://www.yiiframework.com/doc/guide/2.0/en/start-installation#installing-from-composer>`__
         and Composer:

         .. code-block:: console

            $ cd :nxt_ph:`/path/to/ <Partial path to the application directory; use a real path in your configuration>`
            $ composer create-project --prefer-dist yiisoft/yii2-app-basic :nxt_ph:`app <Arbitrary app name>`

         This creates the app's directory tree at :file:`/path/to/app/`.
         Its :file:`web/` subdirectory contains both the root
         :file:`index.php` and the static files; if your app requires
         additional :file:`.php` scripts, also store them here.

      #. .. include:: ../include/howto_change_ownership.rst

      #. Next, :ref:`prepare <configuration-php>` the |app| configuration for
         Unit (use real values for :samp:`share` and :samp:`root`):

         .. code-block:: json

            {
                "listeners": {
                    "*:80": {
                        "pass": "routes"
                    }
                },

                "routes": [
                    {
                        "match": {
                            "uri": [
                                "!:nxt_hint:`/assets/* <This path stores application data that shouldn't be run as code>`",
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
                            ":nxt_hint:`share <Serves static files>`": ":nxt_ph:`/path/to/app/ <Path to the application directory; use a real path in your configuration>`web$uri",
                            "fallback": {
                                "pass": "applications/yii/index"
                            }
                        }
                    }
                ],

                "applications": {
                    "yii": {
                        "type": "php",
                        "targets": {
                            "direct": {
                                "root": ":nxt_ph:`/path/to/app/ <Path to the application directory; use a real path in your configuration>`web/"
                            },

                            "index": {
                                "root": ":nxt_ph:`/path/to/app/ <Path to the application directory; use a real path in your configuration>`web/",
                                "script": ":nxt_hint:`index.php <All requests are handled by a single script>`"
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

      #. .. include:: ../include/howto_upload_config.rst

         After a successful update, your app should be available on the
         listener’s IP address and port:

         .. image:: ../images/yii2.png
            :width: 100%
            :alt: Yii Basic Template App on Unit


   .. tab:: Yii 1.1

      #. .. include:: ../include/howto_install_unit.rst

      #. Next, `install
         <https://www.yiiframework.com/doc/guide/1.1/en/quickstart.installation>`__
         Yii and create or deploy your app.

         Here, we use Yii's `basic project template
         <https://www.yiiframework.com/doc/guide/1.1/en/quickstart.first-app>`__
         and :program:`yiic`:

         .. code-block:: console

            $ git clone git@github.com:yiisoft/yii.git :nxt_ph:`/path/to/yii1.1/ <Arbitrary framework path>`
            $ :nxt_ph:`/path/to/yii1.1/ <Arbitrary framework path>`framework/yiic webapp :nxt_ph:`/path/to/app/ <Path to the application directory; use a real path in your configuration>`

         This creates the app's directory tree at :file:`/path/to/app/`.

      #. Next, :ref:`prepare <configuration-php>` the |app| configuration for
         Unit (use real values for :samp:`share` and :samp:`root`):

         .. code-block:: json

            {
                "listeners": {
                    "*:80": {
                        "pass": "routes"
                    }
                },

                "routes": [
                    {
                        "match": {
                            "uri": [
                                "!:nxt_hint:`/assets/* <This path stores application data that shouldn't be run as code>`",
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
                            ":nxt_hint:`share <Serves static files>`": ":nxt_ph:`/path/to/app <Path to the application directory; use a real path in your configuration>`$uri",
                            "fallback": {
                                "pass": "applications/yii/index"
                            }
                        }
                    }
                ],

                "applications": {
                    "yii": {
                        "type": "php",
                        "targets": {
                            "direct": {
                                "root": ":nxt_ph:`/path/to/app/ <Path to the application directory; use a real path in your configuration>`"
                            },
                            "index": {
                                "root": ":nxt_ph:`/path/to/app/ <Path to the application directory; use a real path in your configuration>`",
                                "script": ":nxt_hint:`index.php <All requests are handled by a single script>`"
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

      #. .. include:: ../include/howto_upload_config.rst

         After a successful update, your app should be available on the
         listener’s IP address and port:

         .. image:: ../images/yii1.1.png
            :width: 100%
            :alt: Yii Basic Template App on Unit
