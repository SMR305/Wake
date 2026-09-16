# This currently listens on a different port for messages to make changes to the server.
# For now it is in the same thread as the rest of the webapp for the purposes of having 
# the same memory for properly giving the live updates, but I'll be looking into the
# channels-redis package to potentially set up a better solution for that
import socket
import threading

from .models import Server


HOST = "0.0.0.0"
PORT = 5000


def listen_for_changes():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listener:
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((HOST, PORT))
        listener.listen()
        print(f"Listening for connections on port {PORT}...")

        while True:
            connection, _ = listener.accept()
            with connection:
                message = connection.recv(1024).decode("utf-8")
                message = message.split(":")
                print(message)
                if message[0] == "shutdown":                
                    server = Server.objects.get(name=message[1])
                    server.is_on = False
                    server.save()
                elif message[0] == "reboot":
                    server = Server.objects.get(name=message[1])
                    server.is_on = True
                    server.save()



def start_listener():
    threading.Thread(
        target=listen_for_changes,
        name="wake-change-listener",
        daemon=True,
    ).start()