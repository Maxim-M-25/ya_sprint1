"""Перенос данных из SQLite в Postgres."""

import sqlite3

import psycopg2
from postgres_saver import PostgresSaver
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor
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

    sqlite_data = sqlite_extractor.extract_movies()
    postgres_saver.save_all_data(sqlite_data)


if __name__ == '__main__':
    dsl = {'dbname': 'movies_database', 'user': 'app', 'password': '123qwe', 'host': '127.0.0.1', 'port': 5432}
    with sqlite3.connect('db.sqlite') as sqlite_conn, psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)
