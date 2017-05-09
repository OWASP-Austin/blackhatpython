'''
A) check a page is returning (glorified grep)
$ python TCP_Client.py

B) fuzz
Example: use the TCP_Client to test a victim TCP server
use ours to see if it's working

C) Sanity Check, see if both scripts are working:
$ python TCP_Server.py
$ python TCP_Client.py

This is a replacement for something like telnet

connect to something- is this port open/listening?
TCP requires handshake, stateful (SYN/ACK)

eg. TCP - an email. protocols where order/reciepts matter.
'''
import socket # this lib is all about networking, woot!
# A)
# target_host = "www.google.com"
# target_port = 80

# B) fuzz
target_host = "127.0.0.1"  # doesnt work
target_port = 9999

# create a socket object
# address familiy internet, sock stream = tcp connection
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect the client
client.connect((target_host, target_port))
# send some data
client.send("GET / HTTP/1.1\r\nHost: google.com\r\n\r\n")  # you can send malicous data here

# recieve some data - 4096 is the size of the buffer
response = client.recv(4096)
print response

