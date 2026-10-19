from .models import Server
from .message_server import message_server

import threading
import time

POLL_DELAY = 600


def poll_loop():
    while True:
        print("Polling...")
        servers = Server.objects.all()
        for server in servers: 
            poll(server)
        time.sleep(POLL_DELAY)


def poll(server: Server):
    result = message_server(server.ip_address, "check", 0.2, False)
    if result == 1:
        server.is_on = False
    else:
        server.is_on = True
    server.save()


def start_polling():
    threading.Thread(
        target=poll_loop,
        name="wake-change-timeout",
        daemon=True,
    ).start()