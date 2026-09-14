from .models import Server
import socket

from dotenv import load_dotenv
import os

load_dotenv()

TEST_IP = os.getenv("TEST_IP")
PORT = 6000

def shutdown_server(server: Server):
    # Create a TCP/IP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.settimeout(30.0)

    try:
        # Connect to the server
        server_address = (TEST_IP, PORT)
        client_socket.connect(server_address)
        message = server.name
        bytes_sent = client_socket.send(message.encode()) # Send data as bytes
        print(f"Sent {bytes_sent} bytes to the server.")
    except ConnectionRefusedError:
        print(f"Connection to {TEST_IP}:{PORT} failed.")
        server.is_on = True
        server.save()
    except socket.timeout:
        print(f"Connection to {TEST_IP}:{PORT} Timed Out.")
        server.is_on = True
        server.save()
    finally:
        client_socket.close()
    

def reboot_server(server: Server):
    return