#! /usr/bin/python3
#Amr Hammam - 23180137
import socket
import time
import sys

class cpu():
    def __init__(self, host, port, time_remove):
        self.host = host
        self.port = int(port)
        self.time_remove = time_remove

    def listen(self):

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind((self.host, self.port))
            sock.listen()

            print('Listening on %s:%s' % (self.host, self.port))

            conn, addr = sock.accept()

            with conn:
                print('Connection from:', addr)

                while True:
                    data = conn.recv(1024)

                    if not data:
                        break
                    else:
                        data = data.decode().split(',')
                        index = len(data) - 1
                        value = int(data[index])

                        if self.time_remove == 0:
                            amount = value
                        else:
                            amount = self.time_remove
                            self.time_remove += 2

                        value -= amount
                        value = str(value)
                        data[index] = value
                        data = ','.join(data)
                        conn.send(data.encode('utf-8'))

                print('Connection closed to:', addr)


if __name__ == '__main__':

    host = '127.0.0.1'
    port = 9000

    if len(sys.argv) < 2:
        time_remove = 0
    else:
        if len(sys.argv) < 3:
            if(sys.argv[1].isdigit()):
                time_remove = int(sys.argv[1])
                print("Time Quantum: " + str(time_remove))
            else:
                time_remove = 0

    if time_remove < 0:
        print("Invalid argument.\n")
        sys.exit(0)

    cpu = cpu(host, port, time_remove)
    cpu.listen() 