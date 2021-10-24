import multiprocessing
import sys
import threading
import logging
import hashlib
import socket

logging.basicConfig(level=logging.DEBUG)

logging.debug("client begin")
my_socket = socket.socket()
ip = "127.0.0.1"
port = 5555
my_socket.connect((ip, port))
logging.info("connect to server at {0} with port {1}".format(ip, port))


def findNumber(start, end, answer):
    num = start
    while num <= end:
        result = hashlib.md5(str(num).encode()).hexdigest().upper()
        # print(result)
        # print(num)
        if result == answer:
            logging.info("correct")
            # print(result)
            send = "answer" + "," + str(num)
            my_socket.send(send.encode())
            exit()
            logging.debug("found")
        num += 1


def close():
    logging.error("client close")
    sys.exit()


def main():
    while True:
        data = [0, 0]

        pros = multiprocessing.cpu_count()
        send = "request" + "," + str(pros)
        my_socket.send(send.encode())

        try:
            data = my_socket.recv(1024)
            data = data.decode()
            data = data.split(",")

        except Exception as e:
            close()

        answer = data[1]
        num = int(data[0])

        threads = []
        for core in range(pros):
            t = threading.Thread(target=findNumber, args=(num, num + 10000, str(answer)))
            threads.append(t)
            t.start()
            num += 10000



if __name__ == "__main__":
    main()
