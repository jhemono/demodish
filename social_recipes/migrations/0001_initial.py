# Generated by Django 5.0.8 on 2024-08-08 16:25

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Cuisine",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=150)),
                ("slug", models.SlugField()),
                ("description", models.TextField(blank=True)),
                (
                    "icon_image",
                    models.ImageField(blank=True, upload_to="", verbose_name="icon"),
                ),
                (
                    "banner_image",
                    models.ImageField(blank=True, upload_to="", verbose_name="banner"),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Food",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=150)),
                ("slug", models.SlugField()),
                ("description", models.TextField(blank=True)),
                (
                    "icon_image",
                    models.ImageField(blank=True, upload_to="", verbose_name="icon"),
                ),
                (
                    "banner_image",
                    models.ImageField(blank=True, upload_to="", verbose_name="banner"),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="MealType",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=150)),
                ("slug", models.SlugField()),
                ("description", models.TextField(blank=True)),
                (
                    "icon_image",
                    models.ImageField(blank=True, upload_to="", verbose_name="icon"),
                ),
                (
                    "banner_image",
                    models.ImageField(blank=True, upload_to="", verbose_name="banner"),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Unit",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "measure",
                    models.CharField(
                        choices=[("V", "Volume"), ("W", "Weight")], max_length=1
                    ),
                ),
                ("name", models.CharField(max_length=50)),
                ("factor", models.FloatField()),
                ("offset", models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name="Profile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("handle", models.CharField(max_length=50, unique=True)),
                ("name", models.CharField(max_length=150)),
                ("bio", models.TextField()),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Recipe",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=150)),
                ("slug", models.SlugField()),
                ("description", models.TextField(blank=True)),
                ("servings", models.PositiveSmallIntegerField()),
                ("cuisines", models.ManyToManyField(to="social_recipes.cuisine")),
                ("meal_types", models.ManyToManyField(to="social_recipes.mealtype")),
                (
                    "profile",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT,
                        to="social_recipes.profile",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="RecipeStep",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("sequence", models.PositiveIntegerField()),
                ("description", models.TextField()),
                (
                    "recipe",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="steps",
                        to="social_recipes.recipe",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="CookingProcedure",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "method",
                    models.CharField(
                        choices=[("OV", "Oven"), ("ST", "Stove")], max_length=2
                    ),
                ),
                ("temperature", models.FloatField(blank=True, null=True)),
                (
                    "temperature_description",
                    models.CharField(blank=True, max_length=150),
                ),
                ("duration", models.DurationField(blank=True, null=True)),
                ("duration_description", models.CharField(blank=True, max_length=150)),
                (
                    "step",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="cooking_procedures",
                        to="social_recipes.recipestep",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="RecipeIngredient",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("sequence", models.PositiveIntegerField()),
                ("quantity", models.FloatField()),
                ("is_optionnal", models.BooleanField(default=False)),
                (
                    "food",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT,
                        to="social_recipes.food",
                    ),
                ),
                (
                    "step",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="ingredients",
                        to="social_recipes.recipestep",
                    ),
                ),
                (
                    "unit",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT,
                        to="social_recipes.unit",
                    ),
                ),
            ],
        ),
    ]
