from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from .views import MainView
from blog.views import RegisterFormView

app_name = 'faq'

urlpatterns = [
    url(r'^$', MainView.as_view(), name='main'),
    url(r'^account/', include('django.contrib.auth.urls'), name='account'),
    url(r'^account/register', RegisterFormView.as_view(), name='register'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
