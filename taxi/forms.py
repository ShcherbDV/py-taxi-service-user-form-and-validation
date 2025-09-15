from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from taxi.models import Driver, Car


class DriverCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "license_number",
            "first_name",
            "last_name",
        )

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        license_verification(license_number)
        return license_number


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"


class DriverLicenseUpdateForm(forms.ModelForm):

    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        license_verification(license_number)
        return license_number


def license_verification(license_number):
    min_license_length = 8

    if len(license_number) != min_license_length:
        raise forms.ValidationError("License number must have 8 symbols ")
    elif not all(ch.isupper() for ch in license_number[:3]):
        raise forms.ValidationError(
            "License number must starts with 3 litters in uppercase "
        )
    elif not license_number[3:].isdigit():
        raise forms.ValidationError("License number must ends in 5 digits")
