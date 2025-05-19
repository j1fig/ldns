import socket

from dnslib import (
    DNSRecord,
    DNSHeader,
    RR,
    A,
    QTYPE
)

from ldns.util import log, config, cache


UDP_RCV_BUFFER_SIZE = 1024
UDP_RCV_ADDR = ('0.0.0.0', 53)  # default DNS port 53


def bind_and_receive():
    log("starting server...")
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_sock, cache.conn() as conn:
        udp_sock.bind(UDP_RCV_ADDR)
        log("server running on port 53.")
        log(f"local cache")

        while True:
            packet, addr = udp_sock.recvfrom(UDP_RCV_BUFFER_SIZE)

            # TODO distinguish upstream replies from downstream requests
            # match addr:
            #     case addr[0] in config.PUBLIC_RESOLVERS:
            #         # TODO store resolver answers in cache.
            #         # TODO reply to waiting requests.
            
            req = DNSRecord.parse(packet)
            log(f"lookup request from {addr[0]}:{addr[1]}\n{req.header}")

            resp = DNSRecord(
                header=DNSHeader(id=req.header.id, qr=1, aa=1, ra=1),
                q=req.q,
            )

            question_names = set([q.qname for q in req.questions])

            log(f"searching cache for {', '.join(question_names)}")
            cache_records = [
                r
                for r in cache.get(conn, n)
                for n in question_names
            ]

            # TODO match entries to name/type questions
            # hits = [
            #     r
            #     for r in cache_records
            #     if r.name
            # ]
            # TODO if all questions cached reply to downstream
            # TODO if any leftover unanswered questions we forward all questions to public resolvers
