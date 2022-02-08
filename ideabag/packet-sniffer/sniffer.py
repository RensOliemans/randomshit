import socket
import sys
from struct import unpack

# doesn't show data on ipv6 packets

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
except (socket.error):
    print("Socket could not be created, are you root?")
    print(sys.exc_info()[0])
    sys.exit()

while True:
    packet = s.recvfrom(65565)

    packet = packet[0]

    ip_header = packet[0:20]

    iph = unpack("!BBHHHBBH4s4s", ip_header)

    version_ihl = iph[0]
    version = version_ihl >> 4
    ihl = version_ihl & 0xF

    iph_length = ihl * 4

    ttl = iph[5]
    protocol = iph[6]
    s_addr = socket.inet_ntoa(iph[8])
    d_addr = socket.inet_ntoa(iph[9])

    print(
        "Version: {0}, length: {1}, TTL: {2}, Protocol: {3}, "
        "Source address: {4}, Destination address: {5}".format(
            version, ihl, ttl, protocol, s_addr, d_addr
        )
    )

    tcp_header = packet[iph_length : iph_length + 20]

    tcph = unpack("!HHLLBBHHH", tcp_header)

    source_port = tcph[0]
    dest_port = tcph[1]
    sequence = tcph[2]
    ack = tcph[3]
    data_offset = tcph[4]
    tcph_length = data_offset >> 4

    print(
        "Source port: {0}, Destination port: {1}, Sequence number: {2}, "
        "Ack: {3}, size: {4}".format(source_port, dest_port, sequence, ack, tcph_length)
    )

    h_size = iph_length + tcph_length * 4
    data_size = len(packet) - h_size

    data = packet[h_size:]

    print("Data: {0}\n".format(data))
