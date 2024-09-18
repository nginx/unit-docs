.. include:: ../include/replace.rst
.. |app| replace:: Spring Boot
.. |mod| replace:: Java

###########
Spring Boot
###########

To run apps based on the `Spring Boot
<https://spring.io/projects/spring-boot>`_ frameworks using Unit:

#. .. include:: ../include/howto_install_unit.rst

#. Create your |app| project; we'll use the `quickstart
   <https://spring.io/quickstart>`__ example, creating it at
   https://start.spring.io:

   .. image:: ../images/springboot.png
      :width: 80%
      :alt: Spring Initializr - Project Setup Screen

   .. note::

      Choose the same Java version that your Unit language module has.

   Download and extract the project files where you need them:

   .. code-block:: console

      $ unzip :nxt_hint:`demo.zip <Downloaded project archive>` -d :nxt_ph:`/path/to/app/ <Path to the application directory; use a real path in your configuration>`

   This creates a directory named **/path/to/app/demo/** for you to add
   your app code to; in our `example <https://spring.io/quickstart>`__, it's a
   single file called
   **/path/to/app/demo/src/main/java/com/example/demo/DemoApplication.java**:

   .. code-block:: java

      package com.example.demo;

      import org.springframework.boot.SpringApplication;
      import org.springframework.boot.autoconfigure.SpringBootApplication;
      import org.springframework.web.bind.annotation.GetMapping;
      import org.springframework.web.bind.annotation.RequestParam;
      import org.springframework.web.bind.annotation.RestController;

      @SpringBootApplication
      @RestController
      public class DemoApplication {

        public static void main(String[] args) {
          SpringApplication.run(DemoApplication.class, args);
        }

        @GetMapping("/hello")
        public String hello(@RequestParam(value = "name", defaultValue = "World") String name) {
          return String.format("Hello, %s!", name);
        }
      }

   Finally, assemble a **.war** file.

   If you chose `Gradle <https://gradle.org>`__ as the build tool:

   .. code-block:: console

      $ cd :nxt_ph:`/path/to/app/ <Path to the application directory; use a real path in your configuration>`demo/

   .. code-block:: console

      $ ./gradlew bootWar

   If you chose `Maven <https://maven.apache.org>`__:

   .. code-block:: console

      $ cd :nxt_ph:`/path/to/app/ <Path to the application directory; use a real path in your configuration>`demo/

   .. code-block:: console

      $ ./mvnw package

   .. note::

     By default, Gradle puts the **.war** file in the **build/libs/**
     subdirectory, while Maven uses **target/**; note your path for later
     use in Unit configuration.

#. .. include:: ../include/howto_change_ownership.rst

#. Next, :ref:`put together <configuration-java>` the |app| configuration (use
   a real value for **working_directory**):

   .. code-block:: json

      {
          "listeners": {
              "*:80": {
                  "pass": "applications/bootdemo"
              }
          },

          "applications": {
              "bootdemo": {
                  "type": "java",
                  "webapp": ":nxt_ph:`gradle-or-maven-build-dir/demo.war <Relative pathname of your .war file>`",
                  "working_directory": ":nxt_ph:`/path/to/app/ <Path to the application directory; use a real path in your configuration>`demo/"
              }
          }
      }

#. .. include:: ../include/howto_upload_config.rst

   After a successful update, your app should be available on the listener's IP
   address and port:

   .. code-block:: console

      $ curl http://localhost/hello?name=Unit

            Hello, Unit!
