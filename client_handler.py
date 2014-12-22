import SocketServer

class ClientHandler(SocketServer.StreamRequestHandler):

    """Spawned by the SocketServer base class
        - Registers the user_id in the EventRouter"""

    # Override
    def setup(self):
        SocketServer.StreamRequestHandler.setup(self)
        self.user_id = None

    # Override
    def handle(self):
        while True:
            user_id = self.rfile.readline().strip()
            if not user_id: break
            self.user_id = user_id
            self.server.event_router.register_user(self.user_id, self.wfile)

    #Override
    def finish(self):
        SocketServer.StreamRequestHandler.finish(self)
        if not self.user_id is None:
            self.server.event_router.unregister_user(self.user_id)

class ClientServer(SocketServer.ThreadingTCPServer):

    """Extends from SocketServer.ThreadingTCPServer to automatically spawn handler threads for each new connection"""

    @staticmethod
    def create(server_address, event_router):
        return ClientServer(server_address, ClientHandler, event_router)

    # Override
    def __init__(self, server_address, BaseRequestHandler, event_router):
        self.daemon_threads = True
        self.allow_reuse_address = True
        self.event_router = event_router
        SocketServer.ThreadingTCPServer.__init__(self, server_address, BaseRequestHandler)
