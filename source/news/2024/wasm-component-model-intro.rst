:orphan:

############################################################
The WebAssembly Component Model - The Why, How and What
############################################################

Would you like to get started with the WebAssembly Component Model and all the things,
but you're lost in the ecosystem and don't know where to start? If yes, then keep reading!
In this blog post we want to share some of the lessons we learned and aha-moments we picked up in
adding support for the WebAssembly Component Model to NGINX Unit thanks to some help from the strong 
and active community!

If you're already familiar with the Wasm ecosystem or just would like to start with code, feel free to
jump to the
:ref:`code samples in our tutorial. <tutorial-rust-based-wasm-component>`

************************************************************************
The WebAssembly Component Model and NGINX Unit
************************************************************************
A lot happened since we shipped the first version of our Wasm Language Module for Unit. 
Back in September 2023 we said: ::

   We introduce WebAssembly support as a Technology Preview - we expect to replace it with WASI-HTTP
   support as soon as that is possible.

With Unit 1.32.0 we did just that. This release supports Wasm Components using the WASI 0.2 proxy world as its main interface. 

Let's pause here for a second. If the last sentence is full of unknown vocabulary, no problem! We will use this blog post to explain
the concept of the Component Model for Wasm and what role WASI plays in this game. Not to mention the importance of the 
"WebAssembly Interface Types".

As you can read in our first `Wasm Blog Post <https://www.nginx.com/blog/server-side-webassembly-nginx-unit/>`__ , the Wasm Runtime shares 
data with the Wasm Module as raw bytes over shared memory. To make sense of this bytestream, the Host as well as the Wasm 
module must speak about the same things or technically speaking implementing the same interfaces. It is a core concept of NGINX 
Unit to create an application specific context of an incoming HTTP request and shares this set of bytes in memory with the runtime. 
This is exactly what we did with **unit-wasm** and it was an interesting and necessary learning to add Wasm support to Unit. 
However, this is far away from implementing or using a standard. This is where the Wasm Component Model comes into play.

The Wasm Component Model describes how different Wasm modules or components can communicate with each other as well as the runtime. 
It defines contracts that must be fulfilled to guarantee that code that is compiled to a Wasm component can be hosted a compatible 
runtime and can natively share data with another Wasm Component at runtime. To give this theoretical context some color we look to 
the implementation in NGINX Unit as a textbook example.

The two essential parts of the Wasm Component Model are the WebAssembly System Interface (WASI) and WebAssembly Interface Types (WIT). 
Let's have a closer look on the two standards.

************************************************************************
WASI and WIT
************************************************************************
WASI is short for "WebAssembly System Interface" and was initiated by wastime project and was designed from the ground up for Wasm. 
WASI can be described as a portable System Interface for Wasm and provides access to several operating-system-like features, including 
files and filesystem, sockets, clocks, random numbers and more. But why is that necessary? 

As we are creating Wasm components for server-side runtimes we cannot target the browser based Wasm runtimes anymore where Web APIs or 
JavaScript is used to provide this functionality. Code, that is outside of the browser needs a way to talk to the underlaying system. 
To better understand where WASI comes into play we think about a very simple program, written in Rust that will print out “Hello World”. 


The code needed can be compiled into an executable binary and after launching it we will see “Hello World” printed on the command line. 
The magic behind this is a standard called POSIX or system calls. They work differently on different operating systems. 

WASI provides an abstraction layer for those syscalls, that can be targeted from the Code that will be compiled to Wasm. 
A WASI compatible runtime will that be able to handle the execution of that code. We will see this in action in our Rust tutorial further 
down in this blog post. Since Preview2 of the WASI proposal - `the WASI-APIs are defined in WIT-files <https://bytecodealliance.org/articles/webassembly-the-updated-roadmap-for-developers#webassembly-system-interface-wasi>`__.

WIT (Wasm Interface Types) is a descriptive `interface description language (IDL) <https://en.wikipedia.org/wiki/IDL_(programming_language)>`__ to define interfaces. It isn't a general-purpose 
coding language. The written WIT-files don't contain any business logic they are pure definitions of contracts. Multiple interfaces 
can be further combined into worlds. As it is not required to deeply understand the way you can create your own WIT-files, it 
will help to track down issues or trouble shoot them while building components. To learn more about the WIT programming language 
see the official `documentation. <https://component-model.bytecodealliance.org/design/wit.html#structure-of-a-wit-file>`__

The WIT-files used by the Wasm Component Model and the **wasi:http/proxy** world in specific are created and maintained by the 
Bytecode alliance. By the time of writing this blog post, the best way to make use of them are the wasmtime GitHub repository and a 
manual pull.

One of interesting facts about WIT-files are the versioning system. As the host implementing the Wasm runtime as well 
as the component we are about to build are creating bindings for the contracts defined by the WIT-files it is important to target 
the exact same version of those contracts or choose a runtime that supports multiple versions of those WIT-files. But this is worth 
another blog post. For now, we should focus on the latest stable release which it was published in February 2024 and is labeled as WASI 0.2. 
This release included **wasi:cli** and the **wasi:http** worlds.

In the Wasm ecosystem these contracts are called worlds. So, we will do from now on. For the use cases of NGINX Unit it was pretty 
clear we will targeting the **wasi/http:proxy** world. You can think of the **wasi:http/proxy** world as the set of interfaces describing 
how a HTTP request and response will look like including all its data (HTTP Method, Headers, Body, etc.). If you are an old school web 
developer, this might remind you of CGI.

************************************************************************
Unit, Wasmtime and Rust - A runtime implementation
************************************************************************

After a short time of investigation, we found out, that the WASI / WIT couple we already heard of plays a crucial role for the support 
of the Component Model. Unit as a Host must implement the WASI http proxy interfaces defined by WIT files to fulfill the contract. This 
is not new - we are already aware about this fact. As we are using Wasmtime as the Wasm runtime this task can be deferred to the 
runtime, can't it?! Yes, it can! BUT there was a little but important detail. Our implementation at this time was purely in C using the 
Wasmtime C-APIs. These APIs missed the necessary functions to implement support for the Component Model.

As mentioned at the beginning, each challenge no matter of its complexity can be solved with the right people and community sharing the same mindset. 
A strong and important partner for us was, and still is, Fermyon. After a late-night Slack and Zoom Session, we found it too complex to add native support 
for the Component Model to the wasmtime C-API. Additionally, implementing the interfaces manually with WIT files without help from automation tools like 
**bindgen** would cause a huge task of constant maintenance.

While explaining how the internals of NGINX Unit and the current C-based Language Module work to Fermyon they shared a prototype of a 
Rust based Unit Language Module targeting the Rust-API of Wasmtime. Not the C-API anymore.

This was the moment we added Rust to the core of NGINX Unit. With all this knowledge we are now ready to write some code.

************************************************************************
Tutorial - A Rust based Wasm Component
************************************************************************
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