"""Импорт данных из sqlite в postgresql."""

from psycopg2.extensions import connection as _connection
from psycopg2.extras import execute_values


class PostgresSaver(object):
    """Класс отвечает за сохранение данных в postgresql."""

    def __init__(self, pg_conn: _connection) -> None:
        """
        Init метод.

        Args:
            pg_conn: Соединение с БД
        """
        self.pg_conn = pg_conn
        self.curs = self.pg_conn.cursor()
        self.csv_separator = '|'

    def save_movies(self, movies: list) -> None:
        movies_array = []
        for movie in movies:
            data_tuple = (
                movie.id, movie.title, movie.description, movie.creation_date, movie.rating, movie.type, movie.created,
                movie.modified)
            movies_array.append(data_tuple)
        sql_query = f'INSERT INTO film_work (id, title, description, creation_date, rating, type, created, modified) VALUES %s ON CONFLICT DO NOTHING;'

        self._insert_data(sql_query, movies_array)

    def save_genres(self, genres: list) -> None:
        genres_array = []
        for genre in genres:
            data_tuple = (
                genre.id, genre.name, genre.description, genre.created,
                genre.modified)
            genres_array.append(data_tuple)
        sql_query = f'INSERT INTO genre (id, name, description, created, modified) VALUES %s ON CONFLICT DO NOTHING;'

        self._insert_data(sql_query, genres_array)

    def save_persons(self, persons: list) -> None:
        persons_array = []
        for person in persons:
            data_tuple = (
                person.id, person.full_name, person.created, person.modified)
            persons_array.append(data_tuple)
        sql_query = f'INSERT INTO person (id, full_name, created, modified) VALUES %s ON CONFLICT DO NOTHING;'

        self._insert_data(sql_query, persons_array)

    def save_genres_film_works(self, genres_film_works: list) -> None:
        genres_film_works_array = []
        for genre_film_work in genres_film_works:
            data_tuple = (
                genre_film_work.id, genre_film_work.genre_id, genre_film_work.film_work_id, genre_film_work.created)
            genres_film_works_array.append(data_tuple)
        sql_query = f'INSERT INTO genre_film_work (id, genre_id, film_work_id, created) VALUES %s ON CONFLICT DO NOTHING;'

        self._insert_data(sql_query, genres_film_works_array)

    def save_persons_film_works(self, persons_film_works: list) -> None:
        persons_film_works_array = []
        for person_film_work in persons_film_works:
            data_tuple = (
                person_film_work.id, person_film_work.person_id, person_film_work.film_work_id, person_film_work.role,
                person_film_work.created)
            persons_film_works_array.append(data_tuple)
        sql_query = f'INSERT INTO person_film_work (id, person_id, film_work_id, role, created) VALUES %s ON CONFLICT (id) DO NOTHING;'

        self._insert_data(sql_query, persons_film_works_array)

    def _insert_data(self, query: str, data_list: list) -> None:
        execute_values(
            self.curs, query, data_list, template=None
        )
