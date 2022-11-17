"""Экспорт данных из sqlite БД."""

import sqlite3
import traceback
from typing import Generator

from sqlite_to_postgres.data_types import (Genre, GenreFilmwork, Movie, Person,
                                           PersonFilmwork)


class SQLiteExtractor(object):
    """Класс отвечает за выгрузку данных из sqlite."""

    def __init__(self, connection: sqlite3.Connection) -> None:
        """
        Init метод.

        Args:
            connection: соединение с БД
        """
        self.connection = connection
        self.connection.row_factory = sqlite3.Row
        self.curs = self.connection.cursor()

    def _collect_movies(self, generator: Generator) -> list:
        """
        Переделывает ответ от БД в объекты класса Movie и объединяет их в список.

        Args:
            generator: генератор полученный на основе sql запроса

        Returns:
            list: список объектов класса Movie
        """
        movies = []
        for row in generator:
            movie_id = row['id']
            title = row['title']
            description = row['description']
            creation_date = row['creation_date']
            rating = row['rating']
            movie_type = row['type']
            created_at = row['created_at']
            updated_at = row['updated_at']
            movie = Movie(title, description, creation_date, movie_type, created_at, updated_at, rating, movie_id)
            movies.append(movie)
        return movies

    def _collect_genres(self, generator: Generator) -> list:
        """
        Переделывает ответ от БД в объекты класса Genre и объединяет их в список.

        Args:
            generator: генератор полученный на основе sql запроса

        Returns:
            list: список объектов класса Genre
        """
        genres = []
        for row in generator:
            genre_id = row['id']
            name = row['name']
            description = row['description']
            created_at = row['created_at']
            updated_at = row['updated_at']
            genre = Genre(name, description, created_at, updated_at, genre_id)
            genres.append(genre)
        return genres

    def _collect_persons(self, generator: Generator) -> list:
        """
        Переделывает ответ от БД в объекты класса Person и объединяет их в список.

        Args:
            generator: генератор полученный на основе sql запроса

        Returns:
            list: список объектов класса Person
        """
        persons = []
        for row in generator:
            person_id = row['id']
            full_name = row['full_name']
            created_at = row['created_at']
            updated_at = row['updated_at']
            genre = Person(full_name, created_at, updated_at, person_id)
            persons.append(genre)
        return persons

    def _collect_genres_filmworks(self, generator: Generator) -> list:
        """
        Переделывает ответ от БД в объекты класса GenreFilmwork и объединяет их в список.

        Args:
            generator: генератор полученный на основе sql запроса

        Returns:
            list: список объектов класса GenreFilmwork
        """
        genres_filmworks = []
        for row in generator:
            relation_id = row['id']
            genre_id = row['genre_id']
            filmwork_id = row['film_work_id']
            created = row['created_at']
            genre = GenreFilmwork(created, relation_id, genre_id, filmwork_id)
            genres_filmworks.append(genre)
        return genres_filmworks

    def _collect_persons_filmworks(self, generator: Generator) -> list:
        """
        Переделывает ответ от БД в объекты класса PersonFilmwork и объединяет их в список.

        Args:
            generator: генератор полученный на основе sql запроса

        Returns:
            list: список объектов класса PersonFilmwork
        """
        persons_film_works = []
        for row in generator:
            relation_id = row['id']
            person_id = row['person_id']
            film_work_id = row['film_work_id']
            role = row['role']
            created = row['created_at']
            genre = PersonFilmwork(role, created, relation_id, person_id, film_work_id)
            persons_film_works.append(genre)
        return persons_film_works

    def _get_generator(self, query: str) -> Generator:
        """
        Создаёт объект генератора на основе полученного sql запроса.

        Args:
            query: sql запрос

        Return:
            Generator: генератор полученный в результате выполнения sql запроса
        """
        try:
            self.curs.execute(query)
            while data := self.curs.fetchmany(1000):
                for part in data:
                    yield part
        except Exception:
            print('ERROR - {error}'.format(error=traceback.format_exc()))

    def _load_movies(self) -> list:
        """
        Управляет процессом создания списка объектов класса Movie.

        Returns:
            list: список объектов класса Movie
        """
        query = 'SELECT * FROM film_work;'
        gen = self._get_generator(query)
        return self._collect_movies(gen)

    def _load_persons(self) -> list:
        """
        Управляет процессом создания списка объектов класса Person.

        Returns:
            list: список объектов класса Person
        """
        query = 'SELECT * FROM person;'
        gen = self._get_generator(query)
        return self._collect_persons(gen)

    def _load_genres(self) -> list:
        """
        Управляет процессом создания списка объектов класса Genre.

        Returns:
            list: список объектов класса Genre
        """
        query = 'SELECT * FROM genre;'
        gen = self._get_generator(query)
        return self._collect_genres(gen)

    def _load_genres_filmworks(self) -> list:
        """
        Управляет процессом создания списка объектов класса GenreFilmwork.

        Returns:
            list: список объектов класса GenreFilmwork
        """
        query = 'SELECT * FROM genre_film_work;'
        gen = self._get_generator(query)
        return self._collect_genres_filmworks(gen)

    def _load_persons_filmworks(self) -> list:
        """
        Управляет процессом создания списка объектов класса PersonFilmwork.

        Returns:
            list: список объектов класса PersonFilmwork
        """
        query = 'SELECT * FROM person_film_work;'
        gen = self._get_generator(query)
        return self._collect_persons_filmworks(gen)

    def extract_movies(self) -> dict:
        """
        Основной метод выгрузки данных из БД.

        Returns:
            dict: словарь с выгруженными из БД данными
        """
        movies = self._load_movies()
        genres = self._load_genres()
        persons = self._load_persons()
        persons_filmworks = self._load_persons_filmworks()
        genres_filmworks = self._load_genres_filmworks()
        return {
            'movies': movies,
            'persons': persons,
            'genres': genres,
            'relations':
                {
                    'persons_film_works': persons_filmworks,
                    'genres_film_works': genres_filmworks,
                },
        }
