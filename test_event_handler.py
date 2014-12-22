import threading
import socket
from event_handler import EventHandler
from event_handler import EventServer
from event_router import EventRouter
from event_router import EventProcessor

class MockEventHandler(EventHandler):
    pass

class MockEventServer(EventServer):
    pass

class MockRouter(EventRouter):

    def __init__(self):
        self.user_keys = ['10', '20', '30', '40']
        self.followers = {}
        self.processor = EventProcessor(self)
        self.test_user_ids = []
        self.test_event = None
        self.events = []

    def process_event(self, event):
        self.events.append(event)

def client(ip, port, message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    try:
        sock.sendall(message)
    finally:
        sock.close()

def test_event_order():
    router = MockRouter()
    server = MockEventServer(("localhost", 9090), MockEventHandler, router)
    ip, port = server.server_address

    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()

    client(ip, port, "2|F|10|20\r\n3|U|10|20\r\n1|B|20\r\n")

    server.shutdown()

    assert router.events[0].rstrip() == '1|B|20'
    assert router.events[1].rstrip() == '2|F|10|20'
    assert router.events[2].rstrip() == '3|U|10|20'
