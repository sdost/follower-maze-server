import heapq
import SocketServer

class EventHandler(SocketServer.StreamRequestHandler):
    """Handles connection from the event stream client
        - Stores events in a priority queue based on sequence number.
        - With each new event read from the stream, attempts to clear the queue while maintaining the sequence
        - Hands off the next event to the EventRouter"""

    # Override
    def setup(self):
        SocketServer.StreamRequestHandler.setup(self)
        self.event_buffer = []
        self.next_event = 1

    #Override
    def handle(self):
        while True:
            # read and store event *as is* for notification
            event = self.rfile.readline()
            if not event: break
            seq_id = int(event.rstrip().split("|")[0])
            self.__add_new_event(seq_id, event)
            self.__consume_events()

    def __add_new_event(self, seq_id, event):
        # push tuple into the heap using the sequence number the sorting value
        heapq.heappush(self.event_buffer, (seq_id, event))

    def __consume_events(self):
        # check top of queue for next event, and pop until we can't find the next event
        while(len(self.event_buffer) > 0 and self.event_buffer[0][0] == self.next_event):
            _, event = heapq.heappop(self.event_buffer)
            self.server.event_router.process_event(event)
            self.next_event += 1

class EventServer(SocketServer.TCPServer):
    """Extends SocketServer.TCPServer to get simple hand off to the handler EventHandler"""

    @staticmethod
    def create(server_address, event_router):
        return EventServer(server_address, EventHandler, event_router)

    def __init__(self, server_address, RequestHandlerClass, event_router):
        self.allow_reuse_address = True
        self.event_router = event_router
        SocketServer.TCPServer.__init__(self, server_address, RequestHandlerClass)
