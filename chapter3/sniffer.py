# use: ping an address in another terminal
# eg: ping www.google.com

import socket
import os

# DHCP address always changes, be sure to run ifconfig, look for inet
# host to listen on
host = "xxx.xx.xxx.xxx"

# create a raw socket and bind it to the public interface
if os.name == "nt":
    socket_protocol = socket.IPPROTO_IP  # windows allows all sniffing

else:
    socket_protocol = socket.IPPROTO_ICMP  # linux requires icmp

sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)  #AF_INET = IPV4 address
sniffer.bind((host, 0)) # local port open, binds here

# we want the IP headers included in the capture
sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1) # ip headers and captured packets

# if we're using Windows, we need to send an IOCTL
# to set up promiscuous mode
if os.name == "nt":
    sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON) # determine if win or linux

# read in a single packet
print sniffer.recvfrom(65565)

# if we're using windows, turn off promiscuous mode
if os.name == "nt":
    sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
