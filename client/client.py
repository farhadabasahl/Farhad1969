import socket
import threading

SERVER_IP = '127.0.0.1'
SERVER_PORT = 12345
BUFFER_SIZE = 1024

def receive_messages(sock):
    while True:
        try:
            message, _ = sock.recvfrom(BUFFER_SIZE)
            print(f'\n{message.decode()}')
        except:
            print("An error occurred.")
            sock.close()
            break

def main():
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    threading.Thread(target=receive_messages, args=(client_sock,)).start()

    while True:
        message = input()
        if message.lower() == 'exit':
            break
        client_sock.sendto(message.encode(), (SERVER_IP, SERVER_PORT))

    client_sock.close()

if __name__ == "__main__":
    main()
