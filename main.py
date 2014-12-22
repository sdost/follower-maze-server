import sys
import threading
import SocketServer
from event_router import EventRouter

"""Entry point for the application.
    - Starts the EventRouter
    - Wait for keyboard input
    - Stops the EventRouter"""

router = EventRouter()
router.start()

raw_input('Press enter to stop servers.\n')

router.stop()
