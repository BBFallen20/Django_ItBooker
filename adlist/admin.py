from django.contrib import admin
from .models import Ad, Source, Category


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    """Административная панель статей."""
    list_display = ['image', 'title', 'description', 'display_category', 'sour', 'author']


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    """Административная панель источников статей."""
    list_display = ['title', 'url']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Административная панель категорий статей."""
    list_display = ['name']
