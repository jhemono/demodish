from django import forms
from django.utils.translation import gettext_lazy as _

from .models import CookingProcedure, Recipe, RecipeIngredient, RecipeStep
from .utils.forms import is_empty_form, is_form_persisted


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ["title", "description", "meal_types", "cuisines", "servings"]


RecipeIngredientFormset = forms.inlineformset_factory(
    RecipeStep,
    RecipeIngredient,
    fields=(
        "food",
        "quantity",
        "unit",
        "is_optionnal",
    ),
    extra=1,
)

CookingProcedureFormset = forms.inlineformset_factory(
    RecipeStep, CookingProcedure, fields=("method", "temperature", "duration"), extra=1
)


class BaseExtendedRecipeStepFormset(forms.BaseInlineFormSet):
    """
    The base formset for editing RecipeSteps belonging to a Recipe, and the
    RecipeIngredients and CookingProcedures belonging to those Steps.
    """

    def add_fields(self, form, index):
        super().add_fields(form, index)

        form.nested_ingredient_formset = RecipeIngredientFormset(
            instance=form.instance,
            data=form.data if form.is_bound else None,
            files=form.files if form.is_bound else None,
            prefix=f"{form.prefix}-{RecipeIngredientFormset.get_default_prefix()}",
        )
        form.nested_cooking_formset = CookingProcedureFormset(
            instance=form.instance,
            data=form.data if form.is_bound else None,
            files=form.files if form.is_bound else None,
            prefix=f"{form.prefix}-{CookingProcedureFormset.get_default_prefix()}",
        )
        # Save a list of both formsets to process them in batch
        self.nested_list = [form.nested_ingredient_formset, form.nested_cooking_formset]

    def is_valid(self):
        """
        Also validate the nested formsets.
        """
        result = super().is_valid()

        if self.is_bound:
            for form in self.forms:
                if hasattr(form, "nested_list"):
                    result = result and all(
                        nested.is_valid() for nested in form.nested_list
                    )

        return result

    def clean(self):
        """
        If a parent form has no data, but its nested forms do, we should
        return an error, because we can't save the parent.
        For example, if the Book form is empty, but there are Images.
        """
        super().clean()

        for form in self.forms:
            if not hasattr(form, "nested_list") or self._should_delete_form(form):
                continue

            if self._is_adding_nested_inlines_to_empty_form(form):
                form.add_error(
                    field=None,
                    error=_(
                        "You are trying to add ingredients or cooking information "
                        "to a recipe step which does not yet exist. Please add "
                        "a description to the step and add information again."
                    ),
                )

    def save(self, commit=True):
        """
        Also save the nested formsets.
        """
        result = super().save(commit=commit)

        for form in self.forms:
            if hasattr(form, "nested_list"):
                if not self._should_delete_form(form):
                    for nested in form.nested_list:
                        nested.save(commit=commit)

        return result

    def _is_adding_nested_inlines_to_empty_form(self, form):
        """
        Are we trying to add data in nested inlines to a form that has no data?
        e.g. Adding Images to a new Book whose data we haven't entered?
        """
        if not hasattr(form, "nested_list"):
            # A basic form; it has no nested forms to check.
            return False

        if is_form_persisted(form):
            # We're editing (not adding) an existing model.
            return False

        if not is_empty_form(form):
            # The form has errors, or it contains valid data.
            return False

        # All the inline forms that aren't being deleted:
        non_deleted_forms = set(
            form for nested in form.nested_list for form in nested.forms
        ).difference(
            set(form for nested in form.nested_list for form in nested.deleted_forms)
        )

        # At this point we know that the "form" is empty.
        # In all the inline forms that aren't being deleted, are there any that
        # contain data? Return True if so.
        return any(not is_empty_form(nested_form) for nested_form in non_deleted_forms)


ExtendedRecipeStepFormset = forms.inlineformset_factory(
    Recipe,
    RecipeStep,
    formset=BaseExtendedRecipeStepFormset,
    fields=("description",),
    extra=1,
)
