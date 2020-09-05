from autoslug import AutoSlugField
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Author(models.Model):
    """Автор книги. Имеет фото, имя, фамилию, дату рождения и смерти, описание."""
    image = models.ImageField(verbose_name='Фото автора', upload_to='images/', null=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    date_of_birth = models.DateField(verbose_name='Дата рождения', null=True, blank=True)
    date_of_death = models.DateField(verbose_name='Дата Смерти', null=True, blank=True)
    description = models.TextField(max_length=1000)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_absolute_url(self):
        """Ссылка на страницу с подробной информацией."""
        return reverse('blog:author-detail', args=[str(self.id)])

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'


class Genre(models.Model):
    """Жанр книги."""
    name = models.CharField(max_length=15, help_text='Жанр')

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Book(models.Model):
    """Модель книги. Имеет картинку, автора, название, описание, дату публикации, ссылку на скачивание, жанр"""
    image = models.ImageField(verbose_name='Картинка', upload_to='images/', null=True)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=40, verbose_name='Название')
    description = models.TextField(max_length=2000, verbose_name='Описание')
    pubdate = models.DateTimeField(auto_now_add=True)
    link = models.URLField(verbose_name='Ссылка на скачивание')
    genre = models.ManyToManyField(Genre, help_text='Жанр книги')
    slug = AutoSlugField(populate_from='title', unique=True, unique_with=('pubdate', 'description'), db_index=True,
                         editable=True, blank=True)
    count = models.PositiveIntegerField('Просмотры', default=0, editable=False)

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'
        # Сортировка по дате публикации
        ordering = ['-pubdate']

    def __str__(self):
        return f"{self.title}"

    def get_absolute_url(self):
        """Ссылка на страницу с подробной информацией."""
        return reverse('blog:book-detail', args=[str(self.slug)])

    def display_genre(self):
        """Функция отображения жанра книги. Поле ManyToMany не позволяет напрямую передавать данные."""
        return [genre.name for genre in self.genre.all()[:3]]
    display_genre.short_description = 'Genre'

    def get_short_description(self):
        """Краткое описание книги(очень краткое...)"""
        return ''.join(self.description[:25])+'...'


class Comment(models.Model):
    """Комментарии к книгам"""
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='book_comments')
    pubdate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.book} | {self.author} | {self.text}'

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-pubdate']
