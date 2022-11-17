"""Тест проверяющий целостность данных после переноса."""

import sqlite3

import psycopg2
from psycopg2.extras import DictCursor

from sqlite_to_postgres.sqlite_extractor import SQLiteExtractor


def test_data() -> None:
    """Проверка целостности данных."""
    dsl = {'dbname': 'movies_database', 'user': 'app', 'password': '123qwe', 'host': '127.0.0.1', 'port': 5432}
    with sqlite3.connect('db.sqlite') as sqlite_conn, psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn:
        sqlite_extractor = SQLiteExtractor(sqlite_conn)
        sql_data = sqlite_extractor.extract_movies()
        pg_curs = pg_conn.cursor()

        custom_data_array = {
            'film_work': sql_data['movies'],
            'person': sql_data['persons'],
            'genre': sql_data['genres'],
            'person_film_work': sql_data['relations']['persons_film_works'],
            'genre_film_work': sql_data['relations']['genres_film_works'],
        }

        for table_name, table_data in custom_data_array.items():
            for data_item in table_data:
                sql = "SELECT * FROM {table_name} WHERE id = '{uuid}'".format(table_name=table_name, uuid=data_item.id)
                pg_curs.execute(sql)
                db_response = pg_curs.fetchall()
                assert len(db_response) == 1
                assert db_response[0][0] == data_item.id
