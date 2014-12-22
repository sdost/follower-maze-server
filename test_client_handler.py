import threading
import socket
import time
from client_handler import ClientHandler
from client_handler import ClientServer
from event_router import EventRouter

class MockRouter(EventRouter):

    def __init__(self):
        self.users = {}
        self.followers = {}
        self.test_user_ids = []
        self.test_event = None
        self.test_registered_user = None
        self.test_unregistered_user = None

    def register_user(self, user_id, user_wfile):
        self.test_registered_user = user_id

    def unregister_user(self, user_id):
        self.test_unregistered_user = user_id

def client(ip, port, message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    try:
        sock.sendall(message)
    finally:
        sock.close()

def test_client_register():
    router = MockRouter()
    server = ClientServer(("localhost", 9099), ClientHandler, router)
    ip, port = server.server_address

    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()

    client(ip, port, "230\r\n")

    time.sleep(0.5)

    server.shutdown()

    assert router.test_registered_user == '230'
    assert router.test_unregistered_user == '230'
