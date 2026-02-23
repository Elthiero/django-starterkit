from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    PasswordChangeForm as DjangoPasswordChangeForm,
)
from .models import User

class BootstrapFormMixin:
    """Automatically injects Bootstrap 5 CSS classes into form fields."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs['class'] = 'form-select'
            else:
                field.widget.attrs['class'] = 'form-control'


class RegistrationForm(BootstrapFormMixin, UserCreationForm):
    """Used on the public /register/ page."""
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder": "you@example.com"}),
    )
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].help_text = "At least 8 characters. Cannot be entirely numeric."
        self.fields["password2"].help_text = "Enter the same password again."


class AdminUserManagementForm(BootstrapFormMixin, forms.ModelForm):
    """Used by admins to edit users (and create users via the manual password logic in views)."""
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "phone", "role", "is_active"]
        widgets = {
            "phone": forms.TextInput(attrs={"placeholder": "+250 780000000"}),
        }


class UserProfileForm(BootstrapFormMixin, forms.ModelForm):
    """Used by authenticated users to edit their own profile (excludes role/status)."""
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "phone"]
        widgets = {
            "phone": forms.TextInput(attrs={"placeholder": "+250 780000000"}),
        }


class PasswordChangeForm(BootstrapFormMixin, DjangoPasswordChangeForm):
    """Thin subclass to ensure Bootstrap styling applies to password changes."""
    pass