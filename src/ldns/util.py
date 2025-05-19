from datetime import datetime, UTC
import sys


TIMESTAMP_FORMAT = '%Y-%m-%dT%H:%M:%S.%f'


def log(msg):
    now = datetime.now(UTC)
    ts = now.strftime(TIMESTAMP_FORMAT)
    print(f"[{ts}] {msg}", file=sys.stderr)
