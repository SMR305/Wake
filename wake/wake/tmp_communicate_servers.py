from .models import Server
import time

def shutdown_server(server: Server):
    time.sleep(2)
    server.is_on = False
    server.save()

def reboot_server(server: Server):
    return