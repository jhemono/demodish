from django.shortcuts import render


def index(request):
    return render(request, "social_recipes/timeline.html")


def create_recipe(request, handle: str):
    return render(request, "social_recipes/recipe_form.html")


def explore(request):
    return render(request, "social_recipes/explore.html")


def show_profile(request, handle: str):
    return render(request, "social_recipes/profile.html")
