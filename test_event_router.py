from event_router import EventProcessor
from event_router import EventRouter

class MockRouter(EventRouter):
    def __init__(self):
        self.user_keys = ['10', '20', '30', '40']
        self.followers = {}
        self.processor = EventProcessor(self)
        self.test_user_ids = []
        self.test_event = None

    def send_event_to_users(self, user_ids, event):
        self.test_user_ids = user_ids
        self.test_event = event

def test_processor_follow():
    router = MockRouter()
    router.processor.process('1|F|10|20')
    assert len(router.test_user_ids) == 1
    assert router.test_user_ids[0] == '20'
    assert router.test_event == '1|F|10|20'

def test_processor_unfollow():
    router = MockRouter()
    router.processor.process('1|U|10|20')
    assert len(router.test_user_ids) == 0
    assert router.test_event == None

def test_processor_follow_unfollow():
    router = MockRouter()
    router.processor.process('1|F|10|20')
    assert router.followers.has_key('20')
    assert len(router.followers['20']) == 1
    assert list(router.followers['20'])[0] == '10'
    router.processor.process('1|U|10|20')
    assert len(router.followers['20']) == 0

def test_processor_broadcast():
    router = MockRouter()
    router.processor.process('1|B')
    assert len(router.test_user_ids) == 4
    assert router.test_event == '1|B'

def test_processor_private_msg():
    router = MockRouter()
    router.processor.process('1|P|20|40')
    assert len(router.test_user_ids) == 1
    assert router.test_user_ids[0] == '40'
    assert router.test_event == '1|P|20|40'

def test_processor_private_msg():
    router = MockRouter()
    router.processor.process('1|P|20|40')
    assert len(router.test_user_ids) == 1
    assert router.test_user_ids[0] == '40'
    assert router.test_event == '1|P|20|40'

def test_processor_private_msg():
    router = MockRouter()
    router.processor.process('1|P|20|40')
    assert len(router.test_user_ids) == 1
    assert router.test_user_ids[0] == '40'
    assert router.test_event == '1|P|20|40'

def test_processor_status_upd():
    router = MockRouter()
    router.processor.process('1|F|20|40')
    router.processor.process('1|S|40')
    assert len(router.test_user_ids) == 1
    assert router.test_user_ids[0] == '20'
    assert router.test_event == '1|S|40'
