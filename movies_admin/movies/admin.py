"""Настройки админки для приложения movies."""

from django.contrib import admin
from movies.models import (Filmwork, Genre, GenreFilmwork, Person,
                           PersonFilmwork)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Настройки для модели Genre."""

    list_display = ('name', 'description', 'created', 'modified')
    list_filter = ('name',)
    search_fields = ('name', 'description', 'id')


class GenreFilmworkInline(admin.TabularInline):
    """Создаёт поля ввода жанра при редактировании кинопроизведения."""

    model = GenreFilmwork


class PersonFilmworkInline(admin.TabularInline):
    """Создаёт поля ввода актёра при редактировании кинопроизведения."""

    model = PersonFilmwork
    autocomplete_fields = ('person', )


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    """Настройки для модели Filmwork."""

    inlines = (GenreFilmworkInline, PersonFilmworkInline)
    list_display = (
        'title',
        'type',
        'creation_date',
        'rating',
        'created',
        'modified',
    )
    list_filter = ('type', 'rating')
    search_fields = ('title', 'description', 'id')


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    """Настройки для модели Person."""

    list_display = ('full_name', 'modified')
    list_filter = ('full_name',)
    search_fields = ('full_name', 'id')
