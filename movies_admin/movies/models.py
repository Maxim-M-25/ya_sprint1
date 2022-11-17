"""Модели приложения movies."""

import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedMixin(models.Model):
    """Миксина для добавления полей created и modified."""

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        """Настройки класса миксины."""

        abstract = True


class UUIDMixin(models.Model):
    """Миксина для добавления поля id."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        """Настройки класса миксины."""

        abstract = True


class Genre(TimeStampedMixin, UUIDMixin):
    """Описывает модель Filmwork."""

    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        """Настройки модели."""

        db_table = "content\".\"genre"
        verbose_name = _('Genre')
        verbose_name_plural = _('Genres')

    def __str__(self) -> name:
        """
        Возвращает строковое представление объекта модели.

        Returns:
            name: Строковое представление
        """
        return self.name


class FilmType(models.TextChoices):
    """Описывает варианты выбора типа кинопроизведения."""

    tv_show = 'tv_show', _('TV Show')
    movie = 'movies', _('Movies')


class Filmwork(TimeStampedMixin, UUIDMixin):
    """Описывает модель Filmwork."""

    title = models.TextField(_('title'))
    description = models.TextField(_('description'), blank=True)
    creation_date = models.DateField(_('creation date'))
    rating = models.FloatField(
        _('rating'),
        blank=True,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100),
        ],
    )
    type = models.CharField(
        _('types'),
        choices=FilmType.choices,
        max_length=32,
    )
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    genres = models.ManyToManyField(Genre, through='GenreFilmwork')
    persons = models.ManyToManyField('Person', through='PersonFilmwork')

    class Meta:
        """Настройки модели."""

        db_table = "content\".\"film_work"
        verbose_name = _('Filmwork')
        verbose_name_plural = _('Filmworks')

    def __str__(self):
        """
        Возвращает строковое представление объекта модели.

        Returns:
            name: Строковое представление
        """
        return self.title


class Person(UUIDMixin, TimeStampedMixin):
    """Описывает модель Person."""

    full_name = models.TextField(_('full name'))

    class Meta:
        """Настройки модели."""

        db_table = "content\".\"person"
        verbose_name = _('Person')
        verbose_name_plural = _('Persons')

    def __str__(self):
        """
        Возвращает строковое представление объекта модели.

        Returns:
            name: Строковое представление
        """
        return self.full_name


class GenreFilmwork(UUIDMixin):
    """Описывает связующую таблицу для моделей Genre и Filmwork."""

    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE, verbose_name=_('Filmwork'))
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE, verbose_name=_('Genre'))
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Дополнительные настройки."""

        db_table = "content\".\"genre_film_work"
        verbose_name = _('Filmwork genre')
        verbose_name_plural = _('Filmwork genres')


class PersonFilmwork(UUIDMixin):
    """Описывает связующую таблицу для моделей Person и Filmwork."""

    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE, verbose_name=_('Filmwork'))
    person = models.ForeignKey('Person', on_delete=models.CASCADE, verbose_name=_('Person'))
    role = models.TextField(_('role'), null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Дополнительные настройки."""

        db_table = "content\".\"person_film_work"
        verbose_name = _('Filmwork person')
        verbose_name_plural = _('Filmwork persons')
