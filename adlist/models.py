from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from autoslug import AutoSlugField


class Category(models.Model):
    """Класс категории статьи"""
    name = models.CharField('Название', max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Source(models.Model):
    """Класс источника статьи, если таков имеется"""
    title = models.CharField('Источник', max_length=100)
    url = models.URLField('Ссылка на источник')

    class Meta:
        verbose_name = 'Источник'
        verbose_name_plural = 'Источники'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """Прямая ссылка на источник"""
        return self.url


class Ad(models.Model):
    """Статья. Имеет картинку, название, описание, дату публикации, отношение к категории(ям), источник"""
    image = models.ImageField(verbose_name='Картинка', upload_to='images/')
    title = models.CharField(verbose_name='Название', max_length=50)
    description = models.TextField(max_length=10000, verbose_name='Описание')
    slug = AutoSlugField(populate_from='title', unique=True, db_index=True, editable=False, blank=True)
    pubdate = models.DateTimeField(verbose_name='Дата публикации', auto_now_add=True)
    sour = models.ForeignKey(Source, on_delete=models.SET_NULL, null=True, verbose_name='Источник')
    category = models.ManyToManyField(Category, help_text='Категории статей')
    count = models.PositiveIntegerField("Просмотры", default=0, editable=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор статьи', null=True,
                               default=User.__name__, editable=True)

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['-pubdate']

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        """Ссылка на подробную информацию о статье"""
        return reverse('adlist:ad-detail', args=[str(self.slug)])

    def get_short_description(self):
        """Короткое описание статьи"""
        return self.description[:12] + '...'

    def display_category(self):
        """Функция отображения категории статьи, нужна потому-что напрямую из типа поля ManyToMany
         невозможно передать данные"""
        return [category.name for category in self.category.all()[:3]]
    display_category.short_description = 'Genre'


class Comment(models.Model):
    """Комментарии к статьям"""
    text = models.TextField('Текст комментария')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ad_comment_author',
                               verbose_name='Автор комментария')
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='ad_comments', verbose_name='Статья комментария')
    pubdate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.ad} | {self.author} | {self.text}'

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-pubdate']
