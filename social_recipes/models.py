from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class Profile(models.Model):
    """Model for user profiles."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    handle = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=150)
    bio = models.TextField()


class Recipe(models.Model):
    """Model for cooking recipes."""

    profile = models.ForeignKey(Profile, on_delete=models.RESTRICT)
    title = models.CharField(max_length=150)
    slug = models.SlugField()
    description = models.TextField(blank=True)
    meal_types = models.ManyToManyField("MealType")
    cuisines = models.ManyToManyField("Cuisine")
    servings = models.PositiveSmallIntegerField()


class RecipeStep(models.Model):
    """Model for instruction steps of recipes."""

    recipe = models.ForeignKey(Recipe, related_name="steps", on_delete=models.CASCADE)
    sequence = models.PositiveIntegerField()
    description = models.TextField()


class RecipeIngredient(models.Model):
    """Model for ingredients and quantities used in recipes."""

    step = models.ForeignKey(
        RecipeStep, related_name="ingredients", on_delete=models.CASCADE
    )
    sequence = models.PositiveIntegerField()
    food = models.ForeignKey("Food", on_delete=models.RESTRICT)
    quantity = models.FloatField()
    unit = models.ForeignKey("Unit", on_delete=models.RESTRICT)
    is_optionnal = models.BooleanField(default=False)


class CookingProcedure(models.Model):
    """Model for cooking mean (oven, stove..), temperature and time of recipes."""

    class Method(models.TextChoices):
        OVEN = "OV", _("Oven")
        STOVE = "ST", _("Stove")

    step = models.ForeignKey(
        RecipeStep, related_name="cooking_procedures", on_delete=models.CASCADE
    )
    method = models.CharField(max_length=2, choices=Method)
    temperature = models.FloatField(blank=True, null=True)
    temperature_description = models.CharField(max_length=150, blank=True)
    duration = models.DurationField(blank=True, null=True)
    duration_description = models.CharField(max_length=150, blank=True)


class Unit(models.Model):

    class Measure(models.TextChoices):
        VOLUME = "V", _("Volume")
        WEIGHT = "W", _("Weight")

    measure = models.CharField(max_length=1, choices=Measure)
    name = models.CharField(max_length=50)
    factor = models.FloatField()
    offset = models.FloatField()


class Tag(models.Model):
    """Abtract model for anything that categories recipes."""

    class Meta:
        abstract = True

    name = models.CharField(max_length=150)
    slug = models.SlugField()
    description = models.TextField(blank=True)
    icon_image = models.ImageField(_("icon"), blank=True)
    banner_image = models.ImageField(_("banner"), blank=True)


class Food(Tag):
    """Model for foods (flour, tomato...)."""

    pass


class MealType(Tag):
    """Model for meal types (starter, desert...)."""

    pass


class Cuisine(Tag):
    """Model for cuisines (French, Italian...)."""

    pass
