from django.contrib import admin

from .models import Cuisine, MealType, Unit

for m in (Cuisine, MealType, Unit):
    admin.site.register(m)
