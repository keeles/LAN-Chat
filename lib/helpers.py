import socket

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # No packets are actually sent
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

def handle_receive(conn):
    while True:
        try:
            data = conn.recv(1024)
            if not data:
                print("Disconnected")
                break
            message = data.decode().strip()
            print(f"\nFriend: {message}")
            print("You: ", end="", flush=True)
        except ConnectionResetError:
            print("\nConnection closed.")
            break
        except Exception as e:
            print(f"\nError: {e}")
            break

def handle_send(conn):
    while True:
        try:
            message = input("You: ")
            if message.lower().strip() == "quit":
                print("You: Disconnected")
                conn.close()
                break
            conn.sendall(message.encode())
        except (BrokenPipeError, OSError):
            print("Connection closed.")
            break