from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    path('ads/', include('adlist.urls')),
    path('faq/', include('faq.urls')),
]
