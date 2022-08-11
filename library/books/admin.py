from django.contrib import admin

# Models
from .models import Book, BookItem

admin.site.register(Book)
admin.site.register(BookItem)