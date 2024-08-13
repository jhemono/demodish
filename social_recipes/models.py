from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


class Profile(models.Model):
    """Model for user profiles."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    handle = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=150)
    bio = models.TextField()

    def __str__(self):
        return f"@{self.handle}"


class Recipe(models.Model):
    """Model for cooking recipes."""

    profile = models.ForeignKey(Profile, on_delete=models.RESTRICT)
    title = models.CharField(max_length=150)
    slug = models.SlugField()
    description = models.TextField(blank=True)
    meal_types = models.ManyToManyField("MealType")
    cuisines = models.ManyToManyField("Cuisine")
    servings = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            "social_recipes:show_recipe",
            kwargs={"handle": self.profile.handle, "slug": self.slug},
        )

    def save(self, **kwargs):
        self.slug = slugify(self.title)
        if (
            update_fields := kwargs.get("update_fields")
        ) is not None and "title" in update_fields:
            update_fields = {"slug"}.union(update_fields)
        super().save(**kwargs)


class RecipeStep(models.Model):
    """Model for instruction steps of recipes."""

    class Meta:
        order_with_respect_to = "recipe"

    recipe = models.ForeignKey(Recipe, related_name="steps", on_delete=models.CASCADE)
    description = models.TextField()


class RecipeIngredient(models.Model):
    """Model for ingredients and quantities used in recipes."""

    class Meta:
        order_with_respect_to = "step"

    step = models.ForeignKey(
        RecipeStep, related_name="ingredients", on_delete=models.CASCADE
    )
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

    def __str__(self):
        return self.name


class Tag(models.Model):
    """Abtract model for anything that categories recipes."""

    class Meta:
        abstract = True

    name = models.CharField(max_length=150)
    slug = models.SlugField()
    description = models.TextField(blank=True)
    icon_image = models.ImageField(_("icon"), blank=True)
    banner_image = models.ImageField(_("banner"), blank=True)

    def __str__(self):
        return self.name


class Food(Tag):
    """Model for foods (flour, tomato...)."""

    pass


class MealType(Tag):
    """Model for meal types (starter, desert...)."""

    pass


class Cuisine(Tag):
    """Model for cuisines (French, Italian...)."""

    pass
