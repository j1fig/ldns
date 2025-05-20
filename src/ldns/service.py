from itertools import chain
from typing import List
from dnslib import DNSRecord

from ldns import cache, domain
from ldns.util import log


def get_full_hit_or_miss(conn, req: DNSRecord) -> List[domain.Record]:
    # checks for any cache miss.
    # if there is a miss returns an empty list.
    question_names = set([str(q.qname) for q in req.questions])
    
    log(f"searching cache for {', '.join(question_names)}")
    cache_records = chain.from_iterable([
        r
        for n in question_names
        for r in cache.get(conn, n)
    ])
    
    cached_name_type = set([(r.name, r.type) for r in cache_records])
    for q in req.questions:
        question_name_type = (str(q.qname), str(q.qtype))
        if question_name_type not in cached_name_type:
            return []

    return cache_records
