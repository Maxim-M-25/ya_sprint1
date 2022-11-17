import sqlite3

import psycopg2
import pytest
from sqlite_to_postgres.postgres_saver import PostgresSaver
from sqlite_to_postgres.sqlite_extractor import SQLiteExtractor
from psycopg2.extras import DictCursor


def test_data():
    dsl = {'dbname': 'movies_database', 'user': 'app', 'password': '123qwe', 'host': '127.0.0.1', 'port': 5432}
    with sqlite3.connect('db.sqlite') as sqlite_conn, psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn:
        sqlite_extractor = SQLiteExtractor(sqlite_conn)
        sql_data = sqlite_extractor.extract_movies()
        pg_curs = pg_conn.cursor()

        movies = sql_data['movies']
        persons = sql_data['persons']
        genres = sql_data['genres']
        persons_film_works = sql_data['relations']['persons_film_works']
        genres_film_works = sql_data['relations']['genres_film_works']

        custom_data_array = {
            'film_work': movies,
            'person': persons,
            'genre': genres,
            'person_film_work': persons_film_works,
            'genre_film_work': genres_film_works
        }

        for table_name, data_item in custom_data_array.items():
            for item in data_item:
                item_id = item.id
                print('table: {table_name} | uuid: {uuid}'.format(table_name=table_name, uuid=item_id))
                sql = "SELECT * FROM {table_name} WHERE id = '{uuid}'".format(table_name=table_name, uuid=item_id)
                pg_curs.execute(sql)
                result = pg_curs.fetchall()
                assert len(result) == 1
                assert result[0][0] == item_id
