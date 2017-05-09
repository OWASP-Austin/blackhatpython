'''
open terminal, run $ python UDP_Client.py
open terminal, run $ python UDP_Server.py

UDP doesn't require handshake:
it's not concerned with packet order or arrival
ex: FTP, video and audio protocols.

this could be used as a fuzzer by playing with sendto() below
'''
import socket

# target_host = "172.16.236.128"
target_host = "127.0.0.1"
target_port = 9000  # was 80 for webserver before
data = "AAABBBCCC"

# create a socket object - DATAGRAM is FOR UDP
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Because UDP is connectionless there is no connect() method needed.
client.sendto(data, (target_host, target_port))

# recieve some data
data, addr = client.recv(4096)
print data, addr

