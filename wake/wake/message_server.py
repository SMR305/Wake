from .models import Server
import socket

from dotenv import load_dotenv
import os

load_dotenv()

TEST_IP = os.getenv("TEST_IP")
PORT = 6000

def message_server(server: Server, request: str):
    # Create a TCP/IP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.settimeout(30.0)

    try:
        # Connect to the server
        server_address = ("127.0.0.1", PORT)
        client_socket.connect(server_address)
        message = f"{request}:{server.name}" # May want to make a more intelligent way to convey the message
        bytes_sent = client_socket.send(message.encode())
        print(f"Sent {bytes_sent} bytes to the server.")
    except (ConnectionRefusedError, socket.timeout):
        print(f"Connection to {TEST_IP}:{PORT} failed.")
        return 1
    finally:
        client_socket.close()
    return 0