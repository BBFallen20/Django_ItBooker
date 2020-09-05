from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from django.contrib import admin


# Название приложения
app_name = 'blog'

urlpatterns = [
    # Главная страница
    url(r'^$', views.MainView.as_view(), name='index'),
    # Ссылка на список книг
    url(r'^books/$', views.BookList.as_view(), name='books'),
    # Ссылка на страницу поиска
    url(r'^search/$', views.SearchView.as_view(), name='search'),
    # Ссылка на страницу подробной информации о книге
    url(r'^book/(?P<slug>[-\w]+)$', views.BookDetail.as_view(), name='book-detail'),
    # Ссылка на страницу подробной информации о авторе
    url(r'^author/(?P<pk>\d+)$', views.AuthorDetail.as_view(), name='author-detail'),
    # Список книг по жанру
    url(r'^books/(?P<name>[-\w]+)$', views.BookList.as_view(), name='books'),
    # Ссылка на аккаунт пользователя
    url(r'^account/', include('django.contrib.auth.urls'), name='account'),
    # Регистрация пользователя
    url(r'^account/register/$', views.RegisterFormView.as_view(), name='register'),
    url(r'^account/profile/(?P<user>[-\w]+)$', views.UserProfileView.as_view(), name='profile'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
