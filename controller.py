import socket
import threading

host = input("Enter your hostname: ")
port = 9999
sock = socket.socket()
sock.bind((host, port))

def handle_client(conn, addr):
    print(f"Connection has been established from: {addr}")
    while True:
        command = conn.recv(1024).decode()
        if command.lower() == 'bye':
            conn.send(command.encode())
            conn.close()
            print(f"Client {addr} has disconnected. Goodbye!")
            break
        else:
            print(f"Client {addr} sent command: {command}")
            conn.send(command.encode())

def listen():
    sock.listen()
    print(f"Server is listening on {host}:{port}")
    while True:
        conn, addr = sock.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

def main():
    listen()

if __name__ == '__main__':
    main()
