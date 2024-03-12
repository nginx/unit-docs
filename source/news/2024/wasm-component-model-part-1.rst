:orphan:

#################################################################
The WebAssembly Component Model - The Why, How and What - Part 1
#################################################################

Would you like to get started with the WebAssembly Component Model and all the things,
but you're lost in the ecosystem and don't know where to start? If yes, then keep reading!
In this blog post we want to share some of the lessons we learned and aha-moments we picked up in
adding support for the WebAssembly Component Model to NGINX Unit thanks to some help from the strong 
and active community!

If you're already familiar with the Wasm ecosystem or just would like to start with code, feel free to
jump directly to `Part 2 </news/2024/wasm-component-model-part-2>`__ of this blog series.

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

As you can read in our first `Wasm Blog Post <https://www.nginx.com/blog/server-side-webassembly-nginx-unit/>`__ , the Wasm runtime shares 
data with the Wasm Module as raw bytes over shared memory. To make sense of this bytestream, the Host as well as the Wasm 
Module must speak about the same things or technically speaking implementing the same interfaces. It is a core concept of NGINX 
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
A WASI compatible runtime will that be able to handle the execution of that code. We will see this in action in our `Rust tutorial </news/2024/wasm-component-model-part-2>`-- further 
in part 2 of this blog series. Since Preview2 of the WASI proposal - `the WASI-APIs are defined in WIT-files <https://bytecodealliance.org/articles/webassembly-the-updated-roadmap-for-developers#webassembly-system-interface-wasi>`__.

WIT (Wasm Interface Types) is a descriptive `interface description language (IDL) <https://en.wikipedia.org/wiki/IDL_(programming_language)>`__ to define interfaces. It isn't a general-purpose 
coding language. The written WIT-files don't contain any business logic they are pure definitions of contracts. Multiple interfaces 
can be further combined into worlds. As it is not required to deeply understand the way you can create your own WIT-files, it 
will help to track down issues or trouble shoot them while building components. To learn more about the WIT programming language 
see the official `documentation. <https://component-model.bytecodealliance.org/design/wit.html#structure-of-a-wit-file>`__

The WIT-files used by the Wasm Component Model and the **wasi:http/proxy** world in specific are created and maintained by the 
Bytecode Alliance. By the time of writing this blog post, the best way to make use of them are the wasmtime GitHub repository and a 
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
NGINX Unit, Wasmtime and Rust - A runtime implementation
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
What's next?
************************************************************************
In the next part we will covering the process of creating a Wasm Component using Rust and the WASI 0.2 APIs.

`Part 2 </news/2024/wasm-component-model-part-2>`__ 


