import select
import logging
import socket
import hashlib

SERVER_PORT = 5555
SERVER_IP = '0.0.0.0'

logging.basicConfig(level=logging.DEBUG)


def print_client_sockets(client_sockets):
    for i in range(len(client_sockets)):
        logging.debug(client_sockets[i])


def newclient(current_socket, client_sockets):
    connection, client_address = current_socket.accept()
    logging.info("New client joined!")
    client_sockets.append(connection)
    print_client_sockets(client_sockets)


def client_mesege(current_socket, client_sockets, answer, num):
    rsv = current_socket.recv(1024).decode()
    rsv = rsv.split(",")
    if rsv[0] == "request":
        mesege = (current_socket, str(num) + "," + str(answer))
        # logging.error(str(rsv[1]*1000 + num))
        messages_to_send.append(mesege)
        return int(rsv[1]) * 10000

    elif rsv[0] == "answer":
        print(rsv[1])
        for socket in client_sockets:
            socket.close()
        exit()

    elif rsv[0] == "":
        logging.info("Connection closed")
        client_sockets.remove(current_socket)
        current_socket.close()
        print_client_sockets(client_sockets)
        return 0


logging.debug("Setting up server...")
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_IP, SERVER_PORT))
server_socket.listen()
logging.info("Listening for clients...")
client_sockets = []
messages_to_send = []
num = 0
answer = hashlib.md5(str(123456789).encode()).hexdigest().upper()
# answer = "EC9C0F7EDCC18A98B1F31853B1813301"
count = 0.01

while True:
    rlist, wlist, xlist = select.select([server_socket] + client_sockets, client_sockets, [])
    for current_socket in rlist:
        if current_socket is server_socket:
            newclient(current_socket, client_sockets)  # create new client
        else:
            num += client_mesege(current_socket, client_sockets, answer, num)  # messages from client
            # logging.error(num)
            if (float(num / 9999999999)) > count:
                print(str(float(num / 9999999999)))
                count += 0.01

    for message in messages_to_send:
        current_socket, data = message
        if current_socket in wlist:
            current_socket.send(data.encode())
            messages_to_send.remove(message)
