from django.urls import path

from . import views

app_name = "social_recipes"
urlpatterns = [
    path("", views.index, name="index"),
    path("u/<str:handle>/add_recipe", views.create_recipe, name="add_recipe"),
    path("explore", views.explore, name="explore"),
    path("u/<str:handle>", views.show_profile, name="show_profile"),
]
