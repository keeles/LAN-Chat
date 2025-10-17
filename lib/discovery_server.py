import socket
import threading
from lib.helpers import get_local_ip

BROADCAST_PORT = 37020
CHAT_TCP_PORT = 5000
DISCOVERY_KEY = b"LANCHAT_DISCOVER"

def udp_discovery_server():
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    udp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    udp_sock.bind(("", BROADCAST_PORT))

    server_ip = get_local_ip()
    print(f"🔍 Discovery server running on {server_ip}:{CHAT_TCP_PORT}")

    while True:
        data, addr = udp_sock.recvfrom(1024)
        if data == DISCOVERY_KEY:
            reply = f"{server_ip}, {CHAT_TCP_PORT}".encode()
            udp_sock.sendto(reply, addr)
            print(f"Responded to discovery from addr: {addr[0]}")

def start_discovery_server():
    t = threading.Thread(target=udp_discovery_server, daemon=True)
    t.start()