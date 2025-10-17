import socket
import time

BROADCAST_PORT = 37020
DISCOVERY_KEY = b"LANCHAT_DISCOVER"

def discover_servers(timeout=2.0):
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    udp_sock.settimeout(timeout)

    servers = []

    udp_sock.sendto(DISCOVERY_KEY, ("255.255.255.255", BROADCAST_PORT))
    print("Searching for LAN Chat servers")

    start = time.time()
    try:
        while time.time() - start < timeout:
            data, addr = udp_sock.recvfrom(1024)
            decoded = data.decode()
            ip, port = decoded.split(",")
            servers.append({"ip": ip, "port": port})
            print(f"Found server: {ip}:{port}")
    except socket.timeout:
        pass
    finally:
        udp_sock.close()

    if not servers:
        print("No servers found")
    return servers