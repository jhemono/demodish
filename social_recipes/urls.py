from django.urls import path

from . import views

app_name = "social_recipes"
urlpatterns = [
    path("", views.index, name="index"),
    path(
        "u/<str:handle>/r/<str:slug>",
        views.RecipeDetailView.as_view(),
        name="show_recipe",
    ),
    path("explore", views.explore, name="explore"),
    path("u/<str:handle>", views.show_profile, name="show_profile"),
]
