from lib.helpers import handle_receive, handle_send
from lib.discovery_client import discover_servers
import socket
import threading

your_name = input("Enter your username: ")

servers = discover_servers()

if not servers:
    print("No servers found on the network.")
    exit()

SERVER_IP = servers[0]["ip"]
PORT = int(servers[0]["port"])

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, PORT))

client_socket.sendall(your_name.encode())
server_name = client_socket.recv(1024).decode()
print(f"Connected to {server_name}")


recv_thread = threading.Thread(target=handle_receive, args=(client_socket, server_name))
send_thread = threading.Thread(target=handle_send, args=(client_socket, your_name))

recv_thread.start()
send_thread.start()

recv_thread.join()
send_thread.join()

print("Chat ended.")
client_socket.close()