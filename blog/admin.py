from django.contrib import admin
from .models import Category, Tag, Article


# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'publish_time', 'author', 'category', 'cover']


admin.site.register(Category)
admin.site.register(Article, PostAdmin)
admin.site.register(Tag)
