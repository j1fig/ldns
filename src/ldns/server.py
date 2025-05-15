import socket
import sys


UDP_RCV_BUFFER_SIZE = 1024
UDP_ADDR = ('0.0.0.0', 53)  # UDP port 53


def _log(msg):
    print(f"[ldns] {msg}", file=sys.stderr)


def bind_and_receive():
    _log("starting server...")
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_sock:
        udp_sock.bind(UDP_ADDR)
        _log("server running on port 53.")

        while True:
            data, addr = socket.recvfrom(UDP_RCV_BUFFER_SIZE)
            _log(addr)
            _log(data)
