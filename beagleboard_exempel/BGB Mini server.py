# client.py
import socket
HOST = "10.3.20.101"  # <-- replace with BBG #1 IP
PORT = 5000
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print(s.recv(1024))     # prints hello from server
    s.sendall(b"hi from BBG #2\n")
