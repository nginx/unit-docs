:orphan:

####################
Unit 1.32.0 Released
####################

Unit 1.31.0 introduced a Technology Preview of a WebAssembly language module and an SDK for C and Rust, helping developers build and run web applications compiled to Wasm. Although effective, we recognized that a custom low-level ABI on the host side and a developer SDK for server-side WebAssembly marked not the conclusion, but a significant milestone in our journey.

Unit 1.32.0 comes with a new language module for WebAssembly that supports the WASI 0.2 HTTP world so that WebAssembly Components implementing this Interface can be hosted on Unit.

Additionally, we are adding the following features:

- Enhanced the NJS experience by making all Unit variables accessible from JavaScript

- Added support for conditional access logging

- Added support for changing Unit's control socket permissions

- Added a new variable **request_id**

...and much more! Keep reading to learn more about what changed since 1.31.1.

**********************
Unit is now on GitHub!
**********************

This release is special! Special for us and the Community! As you may have noticed we have moved more and more of our development and planning workloads from our old systems to GitHub.

GitHub is not a read-only mirror anymore. GitHub is the single source of truth for our source code and tests. Feel free to create Issues, contribute by opening a pull request or be part in our discussions. Many ways to engage with us!

Furthermore we have also migrated the development and maintenance of unit.nginx.org fully to GitHub. We are looking forward for pull requests and issues to make our Documentation better.

************************************************************************
WebAssembly next-level: Support for Wasm components and the WASI 0.2 API
************************************************************************

Since the release of Unit 1.31.0 in August 2023 and the announcement of our technology preview for WebAssembly, a lot has changed an happened in the WebAssembly ecosystem.

So we evolved and with 1.32.0, we are happy to announce the support for the WebAssembly Component Model using the WASI 0.2 APIs. This will open the possibilities to run Wasm Components compatible with the WASI 0.2 APIs on Unit without having a need to rebuild them. This is also the first Language Module for Unit that was driven by the Community. Special thanks to Alex Crichton for the contribution!

You can find out more about this in our Blog post: WebAssembly Next-Level: Support for Wasm Components

*******************************************************************
Enhanced scripting support - Use Unit-variables in NGINX JavaScript
*******************************************************************

Using JavaScript in Unit's configuration unlocks almost endless opportunities. A simple Unit configuration can be used to decide where a request should be routed or rewritten to by creating the values for pass and rewrite dynamically inside a JavaScript function. While writing those functions or policies, not having full access to all Unit variables available for the current request turned out to be an huge issue!

With Unit 1.32.0 we have unlocked full access to all Unit variables from our JavaScript runtime.

**************************
Conditional access logging
**************************

Having access logs is a great way to monitor and analyze traffic sent to Unit. But sometimes there are requests we don't want to see in our logs. Periodic health checks or automated UI-tests are a great way to check the current state of your services or web application, but can increase the overall noise in your access logs.

With conditional access logging, you can define rules to decide if a request should be logged or not.

.. code-block:: json

    {
        "access_log": {
            "if": "`${uri == '/health' ? false : true}`",
            "path": "/var/log/unit/access.log",
            "format": "`${host + ': ' + uri}`"
    }

In this example we don't want to log any health checks sent to Unit. Anything will be logged to the given file in the defined format as usual. As shown in our example, to get the maximum out of the newly added **if** option, you can combine it with our JavaScript scripting feature, but this is not a must.

The **if** option also supports simple string validation to check if a value is present in a request or not.

.. code-block:: json

    {
        "access_log": {
            "if": "$cookie_session",
            "path": "…"
    }

In this example Unit will check the existence of a Cookie named session and only log request including this cookie.

******************************************
Variables: Introducing request_id Variable
******************************************


*************************************
Changes in behavior and other updates
*************************************

- Node JS Language Module enhancements

************
Wall of fame
************

Special Thanks to all external contributors helping us making Unit better! With 1.32.0 we would like to send a shout out to:

- Alejandro Colomar
- Alex Crichton
- Andrei Vasiliu
- Chris Adams
- David Carlier
- Dean Coakley
- rustedsword
- Hippolyte Pello
- Javier Evans