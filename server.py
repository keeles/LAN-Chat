from lib.helpers import get_local_ip, handle_receive, handle_send
from lib.discovery_server import start_discovery_server
import socket
import threading

start_discovery_server()

HOST = get_local_ip()
PORT = 5000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((HOST, PORT))

server_socket.listen(1)
print(f"Server listening on {HOST}:{PORT}")

conn, addr = server_socket.accept()
print(f"Connect by {addr}")

recv_thread = threading.Thread(target=handle_receive, args=(conn,))
send_thread = threading.Thread(target=handle_send, args=(conn,))

recv_thread.start()
send_thread.start()

recv_thread.join()
send_thread.join()

print("Chat ended.")
server_socket.close()