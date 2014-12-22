Follower Maze Server Test
=========================

##Dependencies
  - Python 2.7
  - pytest (for unit testing)

##Purpose
  This program is intended to solve the problem put forth in the document 'Back-end Developer Challenge: Follower Maze'. Given the input validation program, connect an event stream and 100 clients and properly route events to connected user clients.

##Usage
  ./start_server.sh

##Testing
  The unit tests are setup to use py.test.

##Process
  The application creates two threaded socket server instances, one to listen on 9090 for the event stream and one to listen on 9099 for client connections. The event server allows an event client to connect and then processes events as they are sent. The events are stocked in a priority queue so that order is preserved.

  The client server allows multiple clients to connect and creates a thread for each client connection. Once the user is registered, events coming in are routed to the appropriate clients based on the rules set forth in the specification.

##Methodology
  This application uses the SocketServer library from the Python 2.7 standard libraries to eliminate the need for boilerplate networking code as well as the heapq library from the Python 2.7 standard libraries for processing the event stream using a priority queue implemented as a binary heap.

##Performance
  The event stream processing should take O(n).  Processing each event should be either constant-time or O(n) depending on the event type.
