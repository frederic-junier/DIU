""" Un module pour comparer la performance des jointures 'à la main'
    en Python face à ceux en C bien choisis de SQLite3"""

import sqlite3
import logging
from timeit import timeit
from join_algorithms import join_nested_loop, join_hash, join_merge

logging.basicConfig(level=logging.INFO)

DB_FILE = 'join_algorithms_versus_sqlite3.db'

def join_algorithms_versus_sqlite3():
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

        def join_python():
            #UNCOMMENT pass
            #BEGIN CUT
            # On récupère tout le contenu de table1
            cursor.execute("SELECT * FROM table1")
            table1 = cursor.fetchall()
            # On récupère tout le contenu de table2
            cursor.execute("SELECT * FROM table2")
            table2 = cursor.fetchall()
            return join_hash(table1, 1, table2, 0)
            #END CUT

        def join_sqlite():
            #UNCOMMENT pass
            #BEGIN CUT
            # On récupère tout le contenu de table1
            cursor.execute("SELECT * FROM table1 JOIN table2 ON table1.val == table2.val")
            return cursor.fetchall()
            #END CUT

        time_join_python = timeit(join_python, number=100)
        logging.info('Temps pour une jointure côté Python : %f', time_join_python)

        time_join_sqlite = timeit(join_sqlite, number=100)
        logging.info('Temps pour une jointure côté Sqlite3 : %f', time_join_sqlite)

    except (sqlite3.Error) as error:
        logging.error("Error while connecting to sqlite3: %s", error)
    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            logging.debug("Sqlite3 connection is closed")
