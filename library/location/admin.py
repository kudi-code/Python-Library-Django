from django.contrib import admin

# Register your models here.

from django.contrib import admin

from .models import Rack, RackBookItem
admin.site.register(Rack)
admin.site.register(RackBookItem)