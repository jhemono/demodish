from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView

from .forms import ExtendedRecipeStepFormset, RecipeForm
from .models import Profile, Recipe


def index(request):
    return render(request, "social_recipes/timeline.html")


def create_recipe(request, handle: str):
    profile = get_object_or_404(Profile, handle=handle)
    if request.method == "POST":
        recipe_form = RecipeForm(request.POST)
        step_formset = ExtendedRecipeStepFormset(request.POST)

        if recipe_form.is_valid() and step_formset.is_valid():
            recipe = recipe_form.save(commit=False)
            recipe.profile = profile
            recipe.save()
            recipe_form.save_m2m()
            steps = step_formset.save(commit=False)
            for step in steps:
                step.recipe = recipe
                step.save()
                step_formset.save_m2m()
            return redirect(recipe.get_absolute_url())
    else:
        recipe_form = RecipeForm()
        step_formset = ExtendedRecipeStepFormset()

    return render(
        request,
        "social_recipes/recipe_form.html",
        {"recipe_form": recipe_form, "step_formset": step_formset},
    )


class RecipeDetailView(DetailView):
    model = Recipe


def explore(request):
    return render(request, "social_recipes/explore.html")


def show_profile(request, handle: str):
    return render(request, "social_recipes/profile.html")
