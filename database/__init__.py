from orator import DatabaseManager, Schema

databases = {
    'postgres': {
        'driver': 'postgres',
        'host': 'localhost',
        'database': 'yandex',
        'user': 'sasha',
        'password': '123',
        'prefix': '',
        'log_queries': True
    }
}

db = DatabaseManager(databases)
schema = Schema(db)

import logging

logger = logging.getLogger('orator.connection.queries')
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    'It took %(elapsed_time)sms to execute the query %(query)s'
)

handler = logging.StreamHandler()
handler.setFormatter(formatter)

logger.addHandler(handler)