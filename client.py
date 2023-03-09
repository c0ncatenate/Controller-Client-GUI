import socket

class Client():
    def __init__(self):
        self.host = None
        self.port = None
        self.sock = socket.socket()

    def connect(self):
        try:
            self.host = input("Enter your controller ip: ")
            self.port = 9999
            self.sock.connect((self.host, self.port))
            print(f"Connected to {self.host} on port {self.port}.")
        except ConnectionRefusedError:
            print("\nThe connection was refused. Please try again.")
            quit()

    def communicate(self):
        try:
            while True:
                data = self.sock.recv(1024).decode()
                if data == "hello":
                    self.sock.send("hi!".encode())
                elif data == "bye":
                    self.sock.close()
                else:
                    self.sock.send(data.encode())
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            self.sock.close()
        except ConnectionResetError:
            print("\n\nServer has disconnected. Goodbye!")
            self.sock.close()
            quit()
        except OSError as e:
            if e.errno == 9:
                print("\nServer has disconnected. Goodbye!")

def main():
    client = Client()
    client.connect()
    client.communicate()

if __name__ == '__main__':
    main()
