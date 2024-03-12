:orphan:

************************************************************************
The WebAssembly Component Model - The Why, How and What - Part 2
************************************************************************
This is Part 2 of our Blog series about the Wasm Component Model, it's ecosytem and how to use Wasm Components with NGINX Unit.
In `Part 1 </news/2024/wasm-component-model-part-1>`__ we have covered all the conceptional parts. In this Part we will focus on
the process of creating a Wasm Component.

==========================================================================
Tutorial - A Rust based Wasm Component
==========================================================================
Rust is the premier language of WebAssembly development and the most mature in terms of support. In the example we will use Rust and its ecosystem to 
create a Wasm Component that can be hosted on directly on NGINX Unit.

This tutorial targets Linux based operating systems and macOS. If you are on Windows, we recommend using WSL2 (Windows Subsystem for Linux) 
to follow along. If you haven't already installed NGINX Unit alongside with the WebAssembly language module, please refer to the `docs <https://unit.nginx.org/installation/#official-packages>`__ on how to do it 
or use the official `Docker Image <https://unit.nginx.org/installation/#docker-images>`__ **unit:wasm**.

==========================================================================
Rust Development Setup
==========================================================================
Let's start off by installing the Rust ecosystem if not already done. At the time of writing Rust 1.76 was the latest stable version. 
To install Rust, see the instructions on their `website <https://www.rust-lang.org/tools/install>`__.

After the installation was successful you can check the current version of Rust by issuing:

.. code-block:: bash

   $ rustc -V
   rustc 1.76.0 (07dca489a 2024-02-04)

To work with Wasm Components, we need some additional tooling. This is a one-time setup for your machine to be able to write Rust source 
code and compile it to a WebAssembly Component.

==========================================================================
Add the wasm32-wasi compiler target
==========================================================================
This target will bring general Wasm support to your rustc installation. Add the target by issuing:

.. code-block:: bash

   $ rustup target add wasm32-wasi

==========================================================================
Install cargo-component
==========================================================================
**cargo-component** will add a cargo subcommand to build Wasm Components without any intermediate steps from our Rust project. 
To install the latest version issue:

.. code-block:: bash

   $ cargo install cargo-component

==========================================================================
Install wasmtime runtime and CLI for testing
==========================================================================
The wasmtime-cli will be used to test and play around with the Wasm component. At the time of writing, we are using wasmtime 18. 
To install the latest version of wasmtime run:

.. code-block:: bash

   $ curl https://wasmtime.dev/install.sh -sSf | bash

For more information about wasmtime and installing it, see their `Github repository <https://github.com/bytecodealliance/wasmtime/>`__

Now, as we have all the tooling in place, we can create the Rust projects.

.. _tutorial-rust-based-wasm-component:
==========================================================================
Using the **wasi** Rust library
==========================================================================
The official WASI Rust library was a very interesting and exciting test for us! The component build time was fascinating and it 
comes with a low dependency footprint. But at some costs in terms of developer experience. But see for yourselves.

Start by creating a new Wasm Component using cargo component:

.. code-block:: bash

   $ cargo component new --lib test-wasi-component

At the time of writing, the wasi create (Version 0.12.1) available on `crates.io <https://crates.io/crates/wasi>`__ didn't include the latest version available on 
GitHub. As we are making use of an Macro in Rust, we will have to clone the `repository <https://github.com/bytecodealliance/wasi>`__ and reference it from our new Wasm Component 
project.

Clone the bytecodealliances wasi repository

.. code-block:: bash

   $ git clone https://github.com/bytecodealliance/wasi

You should now have a directory structure like this:

.. code-block:: bash

   $ ls -lah
   ../
   ./
   wasi
   test-wasi-component

Navigate into the **test-wasi-component** directory and modify the **Cargo.toml** file with an editor of your choice. We will 
add the wasi crate to the dependencies section and the **proxy = true** configuration to the **[package.metadata.component]** 
section. After applying the changes, your **Cargo.toml** should look like this:

.. code-block:: toml

   [package]
   name = "test-wasi-component"
   version = "0.1.0"
   edition = "2021"

   [dependencies]
   bitflags = "2.4.2"
   wit-bindgen-rt = "0.21.0"
   wasi = { path = "../wasi" }

   [lib]
   crate-type = ["cdylib"]

   [package.metadata.component]
   package = "component:test-wasi-component"
   proxy = true

   [package.metadata.component.dependencies]

The actual code from **src/lib.rs** will be like this:

.. code-block:: rust

   use wasi::http::types::{
      Fields, IncomingRequest, OutgoingBody, OutgoingResponse, ResponseOutparam,
   };

   wasi::http::proxy::export!(Component);

   struct Component;

   impl wasi::exports::http::incoming_handler::Guest for Component {
      fn handle(_request: IncomingRequest, response_out: ResponseOutparam) {

         let hdrs = Fields::new();
         let mesg = String::from("Hello, This is a Wasm Component using wasi/http:proxy!");
         let _try = hdrs.set(&"Content-Type".to_string(), &[b"plain/text".to_vec()]);
         let _try = hdrs.set(&"Content-Length".to_string(), &[mesg.len().to_string().as_bytes().to_vec()]);

         let resp = OutgoingResponse::new(hdrs);

         // Add the HTTP Response Status Code
         resp.set_status_code(200).unwrap();

         let body = resp.body().unwrap();
         ResponseOutparam::set(response_out, Ok(resp));

         let out = body.write().unwrap();
         out.blocking_write_and_flush(mesg.as_bytes()).unwrap();
         drop(out);

         OutgoingBody::finish(body, None).unwrap();
      }
   }

As you can see, targeting the wasi crate requires some low-level Rust work by us. Not bad at all but something to consider when choosing this 
option. For the **wasi/http:proxy** world there is an interface description available on `Github <https://github.com/WebAssembly/wasi-http/blob/main/proxy.md>`__ 
which will help to write your code.

Let's build the component. Inside of the **test-wasi-component** directory issue:

.. code-block:: bash
   
   $ cargo component build --release

As you will notice, the build shows a very small dependency footprint! So is a major benefit from the wasi crate.

To test the Component, we can use wasmtime serve.

.. code-block:: bash

   $ wasmtime serve target/wasm32-wasi/release/test_wasi_component.wasm

The output should look like:

.. code-block:: bash

   $ wasmtime serve target/wasm32-wasi/release/test_wasi_component.wasm
     Serving HTTP on http://0.0.0.0:8080/

Sending a request to the exposed endpoint will output something like this:

.. code-block:: bash

   $ curl -v localhost:8080
   …
   > GET / HTTP/1.1
   > Host: localhost:8080
   > User-Agent: curl/8.4.0
   > Accept: */*
   >
   < HTTP/1.1 200 OK
   < content-type: plain/text
   < content-length: 54
   < date: Tue, 12 Mar 2024 12:28:56 GMT
   <
   * Connection #0 to host localhost left intact
   Hello, This is a Wasm Component using wasi/http:proxy!


************************************************************************
NGINX Unit for production grade Wasm workloads
************************************************************************

While the **wasmtime-cli** is good for testing Wasm components locally, there are more requirements for production workloads. 

With NGINX Units Wasm runtime, you will be able to run your Wasm workloads next to other host applications on a single host and make 
use of all the other powerful Unit features. Given Units design and as we decoupled the listeners from the application runtime, you 
can make full use of the Unit Router to make routing decisions before sharing a request with your Wasm Component or add HTTPS to 
your stack.

To run the component on NGINX Unit, start Unit and send the initial configuration. Make sure you point to the Wasm component by 
using an absolut path.

Create a **config.json** file:

.. code-block:: json

   {
      "listeners": {
         "127.0.0.1:8085": {
            "pass": "applications/my-wasm-component"
         }
      },
      "applications": {
         "my-wasm-component": {
            "type": "wasm-wasi-component",
            "component": "path/target/wasm32-wasi/release/test_wasi_component.wasm"
         }
      }
   }   

Apply the configuration using **unitc**:

.. code-block:: bash

   unitc config.json /config

Sending a request to the exposed endpoint will create the same output but from a different runtime implemenation:

.. code-block:: bash

   $ curl -v localhost:8085
   …
   < HTTP/1.1 200 OK
   < content-type: plain/text
   < content-length: 54
   < Server: Unit/1.32.0
   < Date: Tue, 12 Mar 2024 15:16:13 GMT
   <
   * Connection #0 to host localhost left intact
   Hello, This is a Wasm Component using wasi/http:proxy!

This is the full power of Wasm Components. Build once - run on every runtime.

************************************************************************
What's next?
************************************************************************
The Wasm ecosystem and all its involved projects are changing very rapidly. For the better! Every week is full of new 
features and things to work on, and NGINX Unit is keeping up! Our commitment to Wasm stays strong and we will keep 
on working on implementing new features to our wasmtime integration and write more technical blog posts about Wasm.

Please share feedback about this blog post using our `GitHub discussions <https://github.com/nginx/unit/discussions>`__ 
and let us know what you think is missing when it comes to the work with Wasm Components.