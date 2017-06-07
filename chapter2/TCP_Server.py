'''
Example for use is:
testing a TCP Client, fuzz a client

if you're testing a client,
send malicous data in and watch for response in server
did it filter content? etc.

How to use:
$ python TCP_Server.py
Remember to check the ports on the client / server and that they match
'''

import socket
import threading

bind_ip = "0.0.0.0"
bind_port = 9999  # don't need to be sudo, non priv IP (less 1024)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((bind_ip, bind_port))

server.listen(5)

print "[*] Listening on %s:%d" % (bind_ip, bind_port)

# this is our client handling thread
def handle_client(client_socket):

    # send data
    client_socket.send("Connection established")

    # print out what the client sends
    request = client_socket.recv(1024)
    print "[*] Received: %s" % request

    # send back a packet
    client_socket.send("ACK!")
    client_socket.close()


while True:

    client, addr = server.accept()
    print "[*] Accepted connection from: %s:%d" % (addr[0], addr[1])

    # spin up our client thread to handle incoming data
    client_handler = threading.Thread(target=handle_client, args=(client,))
    client_handler.start()

