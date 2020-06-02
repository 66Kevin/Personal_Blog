from django.contrib import admin
from .models import *


# Register your models here.

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'desc', 'column', 'author')
    list_filter = ('author', 'column', 'created_time', 'tag')
    fieldsets = (
        (None, {
            'fields': ('title', 'desc', 'content', 'column', 'author')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('tag',),
        }),
    )


# admin.site.register(Profile)
admin.site.register(Tag)
admin.site.register(Category)
# admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment)
admin.site.register(Links)
admin.site.register(Advertising)
