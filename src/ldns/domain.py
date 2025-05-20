from dataclasses import dataclass, field
from time import time


DEFAULT_RECORD_EXPIRY = 3600
DEFAULT_REQUEST_EXPIRY = 60


def _expiry_factory(exp):
    def _inner():
        return time() + exp
    return _inner


@dataclass
class Record:
    name: str
    type: str
    data: str
    expiry: float = field(
        default_factory=_expiry_factory(DEFAULT_RECORD_EXPIRY)
    )


@dataclass
class Request:
    addr: str
    port: int
    name: str
    type: str
    hit: bool
    timeout: float = field(
        default_factory=_expiry_factory(DEFAULT_REQUEST_EXPIRY)
    )
