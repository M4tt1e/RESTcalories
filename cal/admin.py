from django.contrib import admin

from .models import Food, Macros, Counter

admin.site.register(Food)
admin.site.register(Macros)
admin.site.register(Counter)
