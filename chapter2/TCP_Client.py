# run $ python TCP_Client.py

# usage: test for services, send data, fuzz etc.
# this is a replacement for something like telnet
# connect to something- is this port open/listening?
# TCP requires handshake, stateful (SYN/ACK)
# eg. TCP - an email. UDP streaming video
import socket
# this lib is all about networking\

target_host = "www.google.com"
target_port = 80

# create a socket object
# address familiy internet, sock stream = tcp connection
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect the client
client.connect((target_host, target_port))
client.send("GET / HTTP/1.1\r\nHost: google.com\r\n\r\n")

# rec data - 4096 is the size of the buffer
response = client.recv(4096)
print response
