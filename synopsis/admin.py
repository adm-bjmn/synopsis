from django.contrib import admin
from .models import Genre, Book

admin.site.register(Genre)


class BookAdmin(admin.ModelAdmin):
    search_fields = ['id']


admin.site.register(Book, BookAdmin)
#
