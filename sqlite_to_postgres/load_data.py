"""Перенос данных из SQLite в Postgres."""

import sqlite3

import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor

from postgres_saver import PostgresSaver
from sqlite_extractor import SQLiteExtractor


def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection) -> None:
    """
    Основной метод загрузки данных из SQLite в Postgres.

    Args:
        connection: соединение с SQLite
        pg_conn: соединение с Postgres
    """
    postgres_saver = PostgresSaver(pg_conn)
    sqlite_extractor = SQLiteExtractor(connection)

    postgres_saver.save_movies(sqlite_extractor.get_movies())
    postgres_saver.save_genres(sqlite_extractor.get_genres())
    postgres_saver.save_persons(sqlite_extractor.get_persons())
    postgres_saver.save_genres_film_works(sqlite_extractor.get_genres_film_works())
    postgres_saver.save_persons_film_works(sqlite_extractor.get_persons_film_works())


    # sqlite_data = sqlite_extractor.extract_movies()
    # postgres_saver.save_all_data(sqlite_data)
if __name__ == '__main__':
    dsl = {'dbname': 'movies_database', 'user': 'app', 'password': '123qwe', 'host': '127.0.0.1', 'port': 5432}
    with sqlite3.connect('db.sqlite') as sqlite_conn, psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)
