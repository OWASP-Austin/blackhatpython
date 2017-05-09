'''
Example for use is:
testing a UDP Client, fuzz a client

if you're testing a client,
send malicous data in and watch for response in server
did it filter content? etc.

How to use:
$ python UDP_Server.py
Remember to check the ports on the client / server and that they match
'''
import socket

BIND_IP = '0.0.0.0'  # bad practice...or messy
BIND_PORT = 9000


def udp_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind((BIND_IP, BIND_PORT))
    print "Waiting on port: " + str(BIND_PORT)

    while 1:
        data, addr = server.recvfrom(1024)
        print data


udp_server()

