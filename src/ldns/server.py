import random
import socket

from dnslib import (
    DNSRecord,
    DNSHeader,
    RR,
    A,
    QTYPE
)

from ldns import config, cache, service
from ldns.util import log


UDP_RCV_BUFFER_SIZE = 1024
UDP_RCV_ADDR = ('0.0.0.0', 53)  # default DNS port 53


def bind_and_receive():
    log("starting server...")
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_sock, cache.conn() as conn:
        udp_sock.bind(UDP_RCV_ADDR)
        log("server running on port 53.")

        cache.init(conn)
        log("DNS cache initialized.")

        while True:
            packet, addr = udp_sock.recvfrom(UDP_RCV_BUFFER_SIZE)

            req = DNSRecord.parse(packet)
            log(f"lookup request from {addr[0]}:{addr[1]}\n{req.header}")
            # TODO log request to DB.


            # TODO distinguish upstream replies from downstream requests
            # match addr:
            #     case addr[0] in config.PUBLIC_RESOLVERS:
            #         # TODO store resolver answers in cache.
            #         # TODO reply to waiting requests.

            # a single cache miss will return an empty list here.
            # we take a pessimistic approach here, in that if there
            # is a single miss, we refresh the whole cache for the
            # affected names/types.
            hits = service.get_full_hit_or_miss(conn, req)

            match hits:
                case [_, *_]:
                    # TODO if all questions cached reply to downstream
                    resp = DNSRecord(
                        header=DNSHeader(id=req.header.id, qr=1, aa=1, ra=1),
                        q=req.q,
                    )
                case []:
                    # we forward the full downstream request to a public resolver
                    resolver_host = random.choice(config.PUBLIC_RESOLVERS)
                    resolver_port = 53
                    resolver_addr = (resolver_host, resolver_port)
                    udp_sock.sendto(req.pack(), resolver_addr)
