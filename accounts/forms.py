from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    PasswordResetForm,
    PasswordChangeForm as DjangoPasswordChangeForm,
)
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
import threading
from .models import User


class BootstrapFormMixin:
    """Automatically injects Bootstrap 5 CSS classes into form fields."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs["class"] = "form-check-input"
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs["class"] = "form-select"
            else:
                field.widget.attrs["class"] = "form-control"


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
        self.fields["password1"].help_text = (
            "At least 8 characters. Cannot be entirely numeric."
        )
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


class AsyncPasswordResetForm(BootstrapFormMixin, PasswordResetForm):
    """
    Overrides Django's default PasswordResetForm to send the
    reset email in a background thread, preventing server timeouts.
    """

    def send_mail(
        self,
        subject_template_name,
        email_template_name,
        context,
        from_email,
        to_email,
        html_email_template_name=None,
    ):

        # 1. Render the subject and body
        subject = render_to_string(subject_template_name, context)
        subject = "".join(subject.splitlines())  # Remove newlines from subject
        body = render_to_string(email_template_name, context)

        # 2. Build the email message
        email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
        if html_email_template_name is not None:
            html_email = render_to_string(html_email_template_name, context)
            email_message.attach_alternative(html_email, "text/html")

        # 3. Send it in a background thread
        class EmailThread(threading.Thread):
            def __init__(self, email):
                self.email = email
                threading.Thread.__init__(self)

            def run(self):
                try:
                    # CHANGED: fail_silently is now False so it raises the error
                    self.email.send(fail_silently=False)
                    print(f"SUCCESS: Email sent to {self.email.to}")
                except Exception as e:
                    # This will print the exact reason it failed to your Render logs!
                    print(f"EMAIL FAILED: {str(e)}")

        EmailThread(email_message).start()
