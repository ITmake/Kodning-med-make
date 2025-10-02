# chat_client.py
import socket, threading, sys
 
SERVER_HOST = "10.3.20.101"   # <-- change to server's IP
SERVER_PORT = 5000
 
def recv_loop(sock: socket.socket):
    try:
        buf = b""
        while True:
            data = sock.recv(1024)
            if not data:
                print("\n[server closed]")
                break
            buf += data
            while b"\n" in buf:
                line, buf = buf.split(b"\n", 1)
                print(line.decode("utf-8", "ignore"))
    except Exception:
        pass
    finally:
        try: sock.close()
        except: pass
 
def send_loop(sock: socket.socket):
    try:
        for line in sys.stdin:
            line = line.rstrip("\n")
            sock.sendall((line + "\n").encode("utf-8", "ignore"))
            if line == "/quit":
                break
    except Exception:
        pass
    finally:
        try: sock.close()
        except: pass
 
def main():
    username = input("Choose a username: ").strip() or "user"
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((SERVER_HOST, SERVER_PORT))
 
    # Expect "ENTER_USERNAME"
    banner = s.recv(1024).decode("utf-8", "ignore")
    if "ENTER_USERNAME" not in banner:
        print("[unexpected server response]")
    s.sendall((username + "\n").encode("utf-8", "ignore"))
 
    # Start threads
    t_r = threading.Thread(target=recv_loop, args=(s,), daemon=True)
    t_r.start()
    print("Connected. Type messages and press Enter. Use /quit to exit.")
    send_loop(s)
 
if __name__ == "__main__":
    main()