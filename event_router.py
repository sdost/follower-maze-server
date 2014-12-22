import threading
from event_handler import EventServer
from client_handler import ClientServer

class EventProcessor:

    """Simple handler map for routing each event to the right receivers"""

    def __init__(self, router):
        self.router = router
        self.handlers = {
            'F': self.__handle_follow,
            'U': self.__handle_unfollow,
            'B': self.__handle_broadcast,
            'P': self.__handle_private_msg,
            'S': self.__handle_status_upd
        }

    def __handle_follow(self, id, type, from_user, to_user):
        self.router.add_follower(to_user, from_user)
        return [to_user]

    def __handle_unfollow(self, id, type, from_user, to_user):
        self.router.remove_follower(to_user, from_user)
        return []

    def __handle_broadcast(self, id, type):
        return self.router.get_all_users()

    def __handle_private_msg(self, id, type, from_user, to_user):
        return [to_user]

    def __handle_status_upd(self, id, type, from_user):
        return self.router.get_all_followers(from_user)

    def process(self, event):
        event_fields = event.rstrip().split('|')
        notify = self.handlers[event_fields[1]](*event_fields)
        if len(notify) > 0:
            self.router.send_event_to_users(notify, event)

class EventRouter:

    """Main portion of the program
        - Starts SocketServers
        - Maintains a list of connected users
        - Maintains a list of followers for each user
        - Processes incoming events in order"""

    def __init__(self):
        self.client_server = ClientServer.create(('', 9099), self)
        self.event_server = EventServer.create(('', 9090), self)
        self.users = {}
        self.user_keys = self.users.viewkeys() # this is a dynamic view and changes based on the state of self.users
        self.followers = {}
        self.processor = EventProcessor(self)

    def start(self):
        self.client_thread = threading.Thread(target=self.client_server.serve_forever)
        self.client_thread.daemon = True
        self.client_thread.start()

        self.event_thread = threading.Thread(target=self.event_server.serve_forever)
        self.event_thread.daemon = True
        self.event_thread.start()

    def stop(self):
        self.client_server.shutdown()
        self.event_server.shutdown()
        del self.client_server
        del self.event_server

    def register_user(self, user_id, user_wfile):
        self.users[user_id] = user_wfile # store reference to socket "file object" granted by StreamRequestHandler

    def unregister_user(self, user_id):
        del self.users[user_id]

    def process_event(self, event):
        self.processor.process(event)

    def get_all_users(self):
        return list(self.user_keys)

    def get_all_followers(self, user_id):
        if self.followers.has_key(user_id):
            return list(self.followers[user_id])
        else:
            return []

    def send_event_to_users(self, user_ids, event):
        for user_id in user_ids:
            if self.users.has_key(user_id):
                self.users[user_id].write(event)
                self.users[user_id].flush()

    def add_follower(self, user_id, follower_id):
        if not self.followers.has_key(user_id):
            self.followers[user_id] = set() # using a set to ensure uniqueness

        self.followers[user_id].add(follower_id)

    def remove_follower(self, user_id, follower_id):
        if self.followers.has_key(user_id):
            self.followers[user_id].discard(follower_id) # doesn't fail if follower_id doesn't exist in the set
