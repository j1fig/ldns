import os

from platformdirs import user_data_dir


DB_FILENAME = 'ldns.db'
APP_NAME = 'ldns'
PUBLIC_RESOLVERS = [
    '1.1.1.1',  # cloudflare
    '8.8.8.8',  # google
]


def get_db_path():
    base_dir = user_data_dir(APP_NAME)
    return os.path.join(base_dir, DB_FILENAME)
