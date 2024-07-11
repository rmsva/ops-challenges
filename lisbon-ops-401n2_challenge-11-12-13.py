#!/bin/python3

import random
import ipaddress
import os
from scapy.all import sr1, IP, TCP, ICMP

# Scan specified ports for the given host
def tcp_port_scan(host, ports):
    for port in ports:
        src_port = random.randint(1024, 65535)
        pkt = IP(dst=host)/TCP(sport=src_port, dport=port, flags='S')
        response = sr1(pkt, timeout=2, verbose=0)

        if response is None:
            print(f"Port {port}: Filtered (no response)")
        elif response.haslayer(TTCP):
            if response[TCP].flags == 0x12:  # SYN-ACK
                sr1(IP(dst=host)/TCP(sport=src_port, dport=port, flags='R'), timeout=2, verbose=0)
                print(f"Port {port}: Open")
            elif response[TCP].flags == 0x14:  # RST-ACK
                print(f"Port {port}: Closed")
            else:
                print(f"Port {port}: Filtered (unexpected flags {response[TCP].flags})")
        else:
            print(f"Port {port}: Filtered (no TCP layer)")

# Ping the host and scan its ports if it's up
def scan_host(host, ports):
    print(f"Pinging {host} - please wait...")
    response = sr1(IP(dst=str(host)) / ICMP(), timeout=2, verbose=0)

    if response is None:
        print(f"{host} is down or unresponsive.")
    elif response.haslayer(ICMP) and response[ICMP].type == 3 and response[ICMP].code in [1, 2, 3, 9, 10, 13]:
        print(f"{host} is actively blocking ICMP traffic.")
    else:
        print(f"{host} is responding.")
        tcp_port_scan(host, ports)

# Scan all hosts in the given network
def scan_network(network, ports):
    for ip in ipaddress.IPv4Network(network).hosts():
        scan_host(str(ip), ports)

# Parse port input into a list of ports
def get_ports(port_input):
    ports = set()
    for part in port_input.split(','):
        if '-' in part:
            start, end = map(int, part.split('-'))
            ports.update(range(start, end + 1))
        else:
            ports.add(int(part))
    return sorted(ports)

if __name__ == "__main__":
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        scan_type = input("Enter scan type (host/network): ").lower()

        if scan_type == "host":
            host = input("Enter target host address (ex. 1.2.3.4): ")
            ports = get_ports(input("Enter ports (eg., 23,443,25535 or 10-18): "))
            scan_host(host, ports)
            break

        elif scan_type == "network":
            network = input("Enter target network address (eg., 1.2.3.0/24): ")
            ports = get_ports(input("Enter ports (eg., 23,443,25535 or 10-18): "))
            scan_network(network, ports)
            break

        else:
            print("Error! Please enter 'host' or 'network'.")

    print("Done!")
