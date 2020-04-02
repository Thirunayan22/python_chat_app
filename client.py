import socket
import select
import errno
import sys

HEADER_LENGTH = 10
IP = "127.0.0.1"
PORT = 1234
my_username = input("Username: ")
client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client_socket.connect((IP,PORT))
client_socket.setblocking(False)

username = my_username.encode('utf-8')
username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
client_socket.send(username_header + username)

while True:
    message = input(f'{my_username} > ')
    if message :
        message = message.encode('utf-8')
        message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
        client_socket.send(message_header + message)
    try:
        while True:
            #recieving data
            username_header = client_socket.recv(HEADER_LENGTH)
            if not len(username_header):
                print("connection closed by the server")
                sys.exit()
            username_lenght = int(username_header.decode('utf-8').strip())
            username = client_socket.recv(username_lenght).decode()

            message_header = client_socket.recv(HEADER_LENGTH)
            message_lenght = int(message_header.decode('utf-8').strip())
            message = client_socket.recv(message_lenght).decode('utf-8')

            print(f"{username}>{message}")

    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print("Reading error {}".format(str(e)))
            sys.exit()
        continue

    except Exception as e:
        print("General Error")
        pass
