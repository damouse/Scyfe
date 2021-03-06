Scyfe is an overlay, peer-to-peer network with multicast elements that replaces the trusted-server
in traditional client-server architecture with a plurality voting scheme. 

This project is meant to be used as a library. In that light, any interaction with the "main" application
occurs through an interface on the Client and Server object. 

All functionality is executed from the Scyfe.py top level script. It should take a runtype and an IP
address (most likely for the server) and run from there. 

All imports are relative to the project root (this directory.)

Do not use print(). Use Utils.log(). The first argument is the name of the class logging, the second
is the contents of the log message. It will make things a lot easier later. 

## Structure
Each folder in this directory contains a different module. Each module should be mostly
self-dependant, but this may not be true (and is certainly not true in the case of the Client and Server
objects.) 


### Server
In progress. 


### Client
In progress.


### Administration
High level protocol decisions. 

Defines an interface that maps to a set of protocol directives. These actions include joining groups, kicking
clients, reinforcing groups, and more. 


### Notary
Application global state changing and validation. 

Defines state variables that should be mutable and the permisable mutations on those variables. 

### Chlorine
Implementation dependant multitasking. 

Maintains a pool of working threads and accepts processing tasks, 
sending them to their prescribed locations after processing. 

Since Python does not allow for true multithreading, Stackless Python will most likely be used as the 
implementation here. 


### Relay
Low level networking implementations. 

Creates connections to the server or other clients as directed. Buffers incoming and outgoing packets. 
Decides what to do with incoming packets-- consider moving this off to its own module. 


### Dispatch
Overlay routing.

Maintains routing tables, resolves clients to IP addresses, and makes packet forwarding
decisions. 


### Slander
Gossip-based threat detection.

Maintains a threat predictor for clients based on their past performance. Inspects packet loss rates, 
incorrect validations, and other network-related hints that can be used to determine the honesty of clients. 
As this predictor rises, informs clients or server and possibly acts. 


### Utils
Contains utility functions potentially used by all objects in the project. 
