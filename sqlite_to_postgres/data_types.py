"""Описание кастомных типов данных."""

import datetime
import uuid
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Movie:
    """Описание полей объекта Movie."""

    title: str
    description: str
    creation_date: datetime.datetime
    type: str
    created: datetime.datetime
    modified: datetime.datetime
    rating: float = field(default=0.0)
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass(frozen=True)
class Genre:
    """Описание полей объекта Genre."""

    name: str
    description: str
    created: datetime.datetime
    modified: datetime.datetime
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass(frozen=True)
class Person:
    """Описание полей объекта Person."""

    full_name: str
    created: datetime.datetime
    modified: datetime.datetime
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass(frozen=True)
class PersonFilmwork:
    """Описание полей объекта PersonFilmwork."""

    role: str
    created: datetime.datetime
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    person_id: uuid.UUID = field(default_factory=uuid.uuid4)
    film_work_id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass(frozen=True)
class GenreFilmwork:
    """Описание полей объекта GenreFilmwork."""

    created: datetime.datetime
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    genre_id: uuid.UUID = field(default_factory=uuid.uuid4)
    film_work_id: uuid.UUID = field(default_factory=uuid.uuid4)
