from django.contrib import admin
from .models import Book, Author, Genre, Comment


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """Административная панель книги"""
    list_display = ['title', 'author', 'pubdate', 'display_genre', "slug"]
    search_fields = ['title', 'author', 'display_genre']


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """Административная панель автора"""
    list_display = ['first_name', 'last_name', 'date_of_birth', 'date_of_death', ]
    fields = ['image', 'first_name', 'last_name', 'description', ('date_of_birth', 'date_of_death')]


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Административная панель жанра"""
    list_display = ['name']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'book', 'text']
