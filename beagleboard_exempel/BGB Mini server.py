import socket, threading
 
def handle_client(conn, addr):
    with conn:
        print("Connected by", addr)
        conn.sendall(b"hello from BBG #1\n")
        while True:
            data = conn.recv(1024)
            if not data:
                print("Client disconnected:", addr)
                break
            print("Client said:", data.decode().strip())
            conn.sendall(data)
 
HOST = ""
PORT = 5000
 
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen()
    print(f"Server listening on port {PORT}")
 
    while True:
        conn, addr = s.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

--------------------------------------------------------------------------------------

# client.py
import socket
HOST = "10.3.20.101"  # <-- replace with BBG #1 IP
PORT = 5000
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print(s.recv(1024))     # prints hello from server
    s.sendall(b"hi from BBG #2\n")
