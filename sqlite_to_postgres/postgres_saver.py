"""Импорт данных из sqlite в postgresql."""

import csv
from traceback import format_exc

from psycopg2.extensions import connection as _connection


class PostgresSaver(object):
    """Класс отвечает за сохранение данных в postgresql."""

    def __init__(self, pg_conn: _connection) -> None:
        """
        init метод.

        Args:
            pg_conn: Соединение с БД

        Returns:
            None
        """
        self.pg_conn = pg_conn
        self.curs = self.pg_conn.cursor()
        self.csv_separator = '|'

    def _run_insert(self) -> None:
        """
        Метод для считывания данных из файла и отправку их в БД.

        Returns:
            None
        """

        relations = {
            'movies': {
                'table_name': 'film_work',
                'table_fields': [
                    'id',
                    'title',
                    'description',
                    'creation_date',
                    'rating',
                    'created',
                    'modified'
                ]
            },
            'persons': {
                'table_name': 'person',
                'table_fields': [
                    'id',
                    'full_name',
                    'created',
                    'modified'
                ]
            },
            'genres': {
                'table_name': 'genre',
                'table_fields': [
                    'id',
                    'name',
                    'description',
                    'created',
                    'modified'
                ]
            },
            'genre_film_work': {
                'table_name': 'genre_film_work',
                'table_fields': [
                    'id',
                    'genre_id',
                    'film_work_id',
                    'created'
                ]
            },
            'person_film_work': {
                'table_name': 'person_film_work',
                'table_fields': [
                    'id',
                    'person_id',
                    'film_work_id',
                    'role',
                    'created'
                ]
            }
        }

        for file_name, table_info in relations.items():
            with open('{file_name}.csv'.format(file_name=file_name), 'r', encoding='utf-8') as file:
                self.curs.execute(
                    'CREATE TEMP TABLE tmp_table (LIKE {table_name} INCLUDING DEFAULTS) ON COMMIT DROP;'.format(
                        table_name=table_info['table_name']))
                sql = "COPY tmp_table FROM STDIN DELIMITER '{sep}' CSV".format(sep=self.csv_separator)
                self.curs.copy_expert(sql, file)
                self.curs.execute('INSERT INTO {table_name} SELECT * FROM tmp_table ON CONFLICT DO NOTHING;'.format(
                    table_name=table_info['table_name']))
                self.pg_conn.commit()

    def save_all_data(self, data: dict) -> None:
        """
        Основной метод класса, отвечает за управление процессом сохранения данных в БД.

        Args:
            data: словарь с извлечёнными данными

        Returns:
            None
        """

        self.movies = data['movies']
        self.persons = data['persons']
        self.genres = data['genres']
        self.persons_film_works = data['relations']['persons_film_works']
        self.genres_film_works = data['relations']['genres_film_works']
        try:
            self._create_files()
            self._run_insert()
        except BaseException:
            print('ERROR:\n{error}'.format(error=format_exc()))
            return

    def _create_files(self) -> None:
        """
        Создаёт файлы с данными для каждой таблицы.

        Returns:
            None
        """

        with open('movies.csv', 'w', encoding='utf-8') as movies_file:
            wr = csv.writer(movies_file, delimiter=self.csv_separator)
            for movie in self.movies:
                wr.writerow(
                    [movie.id, movie.title, movie.description, movie.creation_date, movie.rating, movie.type,
                     movie.created, movie.modified])

        with open('persons.csv', 'w', encoding='utf-8') as persons_file:
            wr = csv.writer(persons_file, delimiter=self.csv_separator)
            for person in self.persons:
                wr.writerow([person.id, person.full_name, person.created, person.modified])

        with open('genres.csv', 'w', encoding='utf-8') as genres_file:
            wr = csv.writer(genres_file, delimiter=self.csv_separator)
            for genre in self.genres:
                wr.writerow([genre.id, genre.name, genre.description, genre.created, genre.modified])

        with open('genre_film_work.csv', 'w', encoding='utf-8') as genre_film_work_file:
            wr = csv.writer(genre_film_work_file, delimiter=self.csv_separator)
            for genre_film_work in self.genres_film_works:
                wr.writerow([genre_film_work.id, genre_film_work.genre_id, genre_film_work.film_work_id,
                             genre_film_work.created])

        with open('person_film_work.csv', 'w', encoding='utf-8') as person_film_work_file:
            wr = csv.writer(person_film_work_file, delimiter=self.csv_separator)
            for person_film_work in self.persons_film_works:
                wr.writerow([person_film_work.id, person_film_work.person_id, person_film_work.film_work_id,
                             person_film_work.role, person_film_work.created])
