"""
Main purpose of this project is to learn multiple client handling
"""
import socket
import select

HEADER_LENGHT = 10
IP = "127.0.0.1"
PORT = 1234

server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1) #Allows to reconnect to the same port without refining the port number each time


server_socket.bind((IP,PORT))
server_socket.listen()



#Storing the list of sockets(Clients)
sockets_list = [server_socket]

clients = {}

print(f'Listening for connections on {IP}:{PORT}...')
def recieve_message(client_socket):


    try:
        message_header = client_socket.recv(HEADER_LENGHT)

        if not len(message_header):
            return False
        message_lenght  = int(message_header.decode('utf-8').strip())
        return {"header " : message_header , "data" : client_socket.recv(message_lenght)}
    except:
        return False

while True :
    read_sockets , _, exception_sockets = select.select(sockets_list,[],sockets_list) #gets read sockets

    for notified_socket in read_sockets:
        if notified_socket == server_socket:
            clients_socket , client_address = server_socket.accept()

            user = recieve_message(clients_socket)
            if user is False:
                continue
            sockets_list.append(clients_socket)

            clients[clients_socket]  = user
            print(f"Accepted new connetion from {client_address[0]}:{client_address[1]} username:{user['data'].decode('utf-8')}")

        else:
            message = recieve_message(notified_socket)
            if message is False:
                print(f"Closed connection from {clients[notified_socket]['data'].decode('utf-8')}")
                sockets_list.remove(notified_socket)
                sockets_list.remove(notified_socket)
                del clients[notified_socket]
                continue

            user  = clients[notified_socket]
            print(f"Received messsage from {user['data'].decode('utf-8')} : {message['data'].decode('utf-8')}")

            for clients_socket in clients:
                if clients_socket != notified_socket:
                    clients_socket.send(user['header'] + user['data'] + message['header'] + message['data'])#Just so other clients can know the username with the message from the sender

        for  notified_socket in exception_sockets:
            sockets_list.remove(notified_socket)
            del clients[notified_socket]
