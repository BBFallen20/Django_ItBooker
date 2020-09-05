from blog.views import RegisterFormView
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from . import views


# Название приложения для ссылок на него
app_name = 'adlist'

urlpatterns = [
    # Ссылка на список статей
    url(r'^$', views.AdListView.as_view(), name='ad-list'),
    # Ссылка на список статей по категории
    url(r'^(?P<name>[-\w]+)$', views.AdListView.as_view(), name='ad-list'),
    # Страница поиска
    url(r'^search/$', views.SearchView.as_view(), name='search'),
    # Подробная информация о статье
    url(r'^ad/(?P<slug>[-\w]+)$', views.AdDetailView.as_view(), name='ad-detail'),
    # Ссылка на аккаунт пользователя
    url(r'^account/', include('django.contrib.auth.urls'), name='account'),
    # Ссылка на регистрацию пользователя
    url(r'^account/register', RegisterFormView.as_view(), name='register'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
