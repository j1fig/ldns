from time import time
from typing import List
import sqlite3

from ldns import config, record


SCHEMA_STATEMENT = """
    CREATE TABLE IF NOT EXISTS record(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        type TEXT,
        data TEXT,
        expiry FLOAT
    );
    CREATE INDEX IF NOT EXISTS ix_record_name ON record(name);
"""

INSERT_STATEMENT = """
    INSERT INTO record(name, type, data, expiry) VALUES (?, ?, ?, ?);
"""

SELECT_STATEMENT = """
    SELECT name, type, data, expiry FROM record WHERE name  = ? AND expiry > ?;
"""


def conn(db=config.get_db_path()) -> sqlite3.Connection:
    return sqlite3.connect(
        database=db,
        # will need to explicitly commit/rollback per transaction.
        # https://docs.python.org/3/library/sqlite3.html#transaction-control-via-the-autocommit-attribute
        autocommit=False,
        # safe for threadsafety=3 (current case).
        # https://docs.python.org/3/library/sqlite3.html#sqlite3.threadsafety
        check_same_thread=False,  
    )


def init(conn: sqlite3.Connection):
    with conn:
        # Ensures schema
        try:
            conn.executescript(SCHEMA_STATEMENT)
            conn.commit()
        except Exception:
            conn.rollback()
            raise


def set(conn: sqlite3.Connection, r: record.Record):
    with conn:
        try:
            conn.execute(INSERT_STATEMENT, (r.name, r.type, r.data, r.expiry,))
            conn.commit()
        except Exception:
            conn.rollback()
            raise


def get(conn: sqlite3.Connection, name: str) -> List[record.Record]:
    with conn:
        now = time()
        try:
            rows = conn.execute(SELECT_STATEMENT, (name, now,))
            return [
                record.Record(
                    name=r[0],
                    type=r[1],
                    data=r[2],
                    expiry=r[3],
                )
                for r in rows
            ]
        except Exception:
            conn.rollback()
            raise
