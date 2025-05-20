import pytest

from ldns import cache, domain


TEST_DB = ":memory:"


@pytest.fixture
def conn():
    conn = cache.conn(TEST_DB)
    try:
        cache.init(conn)
        yield conn
    finally:
        conn.close()


def test_set_record(conn):
    r = domain.Record('google.com.', 'A', '64.233.185.102')
    cache.set(conn, r)

    entries = cache.get(conn, "google.com.")
    assert len(entries) == 1
    assert entries[0].data == '64.233.185.102'


def test_gets_no_records(conn):
    entries = cache.get(conn, "google.com.")
    assert len(entries) == 0


def test_gets_records(conn):
    r1 = domain.Record('google.com.', 'A',      '64.233.185.102')
    r2 = domain.Record('google.com.', 'A',      '142.250.201.78')
    r3 = domain.Record('google.com.', 'AAAA',   '2a00:1450:4003:808::200e')
    cache.set(conn, r1)
    cache.set(conn, r2)
    cache.set(conn, r3)

    entries = cache.get(conn, "google.com.")
    assert len(entries) == 3


def test_gets_no_stale_records(conn, freezer):
    freezer.move_to('2025-05-21')
    r1 = domain.Record('google.com.', 'A',      '64.233.185.102')
    cache.set(conn, r1)

    freezer.move_to('2025-05-22')
    r2 = domain.Record('google.com.', 'A',      '142.250.201.78')
    r3 = domain.Record('google.com.', 'AAAA',   '2a00:1450:4003:808::200e')
    cache.set(conn, r2)
    cache.set(conn, r3)

    entries = cache.get(conn, "google.com.")
    assert len(entries) == 2
