""" Un module pour comparer la performance des jointures 'à la main'
    en Python face à ceux en C bien choisis de SQLite3"""

import sqlite3
import logging
from timeit import timeit
from join_algorithms import join_hash # join_nested_loop, join_hash, join_merge

# mettre level=logging.DEBUG pour avoir plus d'information
logging.basicConfig(level=logging.INFO)

DB_FILE = 'join_algorithms_versus_sqlite3.db'


def join_algorithms_versus_sqlite3(nb_repeat=100):
    """Fonction de comparaison"""
    try:
        connection = sqlite3.connect(DB_FILE)

        # Pour avoir des ditcionnaires et non des tuples dans le résultat
        # see https://docs.python.org/3.6/library/sqlite3.html#sqlite3.Row
        # connection.row_factory = sqlite3.Row

        cursor = connection.cursor()

        logging.debug("You are connected to - %s", DB_FILE)
        cursor.execute("SELECT sqlite_version() as version;")
        record = cursor.fetchone()
        logging.debug(tuple(record))

        def join_and_transfer_python():
            # On récupère tout le contenu de table1
            cursor.execute("SELECT * FROM table1")
            table1 = cursor.fetchall()
            # On récupère tout le contenu de table2
            cursor.execute("SELECT * FROM table2")
            table2 = cursor.fetchall()
            return join_hash(table1, 1, table2, 0)

        def join_and_transfer_sqlite():
            # On récupère tout le contenu de la jointure de table1 et table2
            cursor.execute(
                "SELECT * FROM table1 JOIN table2 ON table1.val == table2.val")
            return cursor.fetchall()

        time_python = timeit(join_and_transfer_python, number=nb_repeat)
        logging.info('Temps de transfert et de jointure côté Python  : %fms',
                     1000*time_python/nb_repeat)

        time_sqlite = timeit(join_and_transfer_sqlite, number=nb_repeat)
        logging.info('Temps de transfert et de jointure côté Sqlite3 : %fms',
                     1000*time_sqlite/nb_repeat)

    except (sqlite3.Error) as error:
        logging.error("Error while connecting to sqlite3: %s", error)
    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            logging.debug("Sqlite3 connection is closed")
