# The major problem with this is that the current structure does not let the queue persist between reboots,
# so there needs to be more logic to account for that
import time
import threading
import queue

from .models import Server

# Timeout in seconds
TIMEOUT = 120

work_queue = queue.Queue()

def add_timeout(id: int):
    work_queue.put([id, time.time()])

def timeout():
    while True:
        task = work_queue.get()
        print(task)
        time.sleep((task[1] + TIMEOUT) - time.time())
        try:
            server = Server.objects.get(id=task[0], is_on=None)
            server.is_on = False
            server.save()
        except Server.DoesNotExist:
            print(f"Server '{task[0]}' not found, or already on")

def start_timeout():
    threading.Thread(
        target=timeout,
        name="wake-change-timeout",
        daemon=True,
    ).start()