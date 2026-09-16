import time
import threading

from .models import Server

# Timeout in seconds
TIMEOUT = 120

def timeout(name: str):
    time.sleep(120)
    try:
        server = Server.objects.get(name=name)
        if server.is_on == None:
            server.is_on == False
            server.save()
    except Server.DoesNotExist:
        print(f"Server '{name}' not found")

def start_timeout(name: str):
    threading.Thread(
        target=timeout(name),
        name="wake-change-listener",
        daemon=True,
    ).start()