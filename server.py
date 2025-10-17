from lib.helpers import get_local_ip, handle_receive, handle_send
from lib.discovery_server import start_discovery_server
import socket
import threading

start_discovery_server()

HOST = get_local_ip()
PORT = 5000

your_name = input("Enter your username: ")

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((HOST, PORT))

server_socket.listen(1)
print(f"Server listening on {HOST}:{PORT}")

conn, addr = server_socket.accept()
print(f"Connect by {addr}")

client_name = conn.recv(1024).decode()
conn.sendall(your_name.encode())

print(f"Connected with {client_name}")

recv_thread = threading.Thread(target=handle_receive, args=(conn, client_name))
send_thread = threading.Thread(target=handle_send, args=(conn, your_name))

recv_thread.start()
send_thread.start()

recv_thread.join()
send_thread.join()

print("Chat ended.")
server_socket.close()