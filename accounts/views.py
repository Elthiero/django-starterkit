from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model, login, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.conf import settings
from .utils import send_html_email
from .forms import UserProfileForm, AdminUserManagementForm, RegistrationForm
from .decorators import allowed_users

User = get_user_model()


def register_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Send Welcome Email
            send_html_email(
                subject=f"Welcome to Starter Kit, {user.first_name}!",
                template_name="emails/welcome.html",
                context={"user": user},
                recipient_list=[user.email],
            )
            login(request, user)
            messages.success(request, "Registration successful. Welcome!")
            return redirect("accounts:profile")
    else:
        form = RegistrationForm()

    return render(request, "accounts/register.html", {"form": form})


# --- MANAGE USERS ---
@login_required
@allowed_users(allowed_roles=["ADMIN", "MANAGER"])
def manage_users(request):
    users = User.objects.all().order_by("-date_joined")

    search_query = request.GET.get("q", "").strip()
    if search_query:
        users = users.filter(
            Q(first_name__icontains=search_query)
            | Q(last_name__icontains=search_query)
            | Q(email__icontains=search_query)
        )

    role_filter = request.GET.get("role", "")
    if role_filter:
        users = users.filter(role=role_filter)

    paginator = Paginator(users, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    if request.headers.get("HX-Request"):
        return render(request, "accounts/partials/user_table.html", {"users": page_obj})

    if request.method == "POST":
        form = AdminUserManagementForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            password = request.POST.get("password")
            if password:
                new_user.set_password(password)
            else:
                raise ValueError("Password is required.")
            new_user.save()

            # Send Welcome Email when admin creates user
            send_html_email(
                subject=f"Welcome to Starter Kit, {new_user.first_name}!",
                template_name="emails/welcome.html",
                context={"user": new_user},
                recipient_list=[new_user.email],
            )

            messages.success(request, f"User {new_user.email} created successfully!")
            return redirect("accounts:manage_users")
        else:
            messages.error(request, "Error creating user. Please check the form.")
    else:
        form = AdminUserManagementForm()

    counts = User.objects.aggregate(
        admins=Count("id", filter=Q(role="ADMIN")),
        managers=Count("id", filter=Q(role="MANAGER")),
        default=Count("id", filter=Q(role="DEFAULT")),
    )

    context = {
        "users": page_obj,
        "page_obj": page_obj,
        "form": form,
        "total_users": User.objects.count(),
        "total_admins": counts["admins"],
        "total_managers": counts["managers"],
        "total_default": counts["default"],
        "roles": User.ROLE_CHOICES,
        "search_query": search_query,
        "role_filter": role_filter,
    }
    return render(request, "accounts/manage_users.html", context)


# --- UPDATED EDIT USER (Detects Activation) ---
@login_required
@allowed_users(allowed_roles=["ADMIN", "MANAGER"])
def edit_user(request, user_id):
    user_to_edit = get_object_or_404(User, id=user_id)
    # Check current status before binding form
    was_inactive = not user_to_edit.is_active

    if request.method == "POST":
        form = AdminUserManagementForm(request.POST, instance=user_to_edit)
        if form.is_valid():
            updated_user = form.save()

            # Trigger 'Account Activated' email if status changed to True
            if was_inactive and updated_user.is_active:
                send_html_email(
                    subject="Your account has been approved — Starter Kit",
                    template_name="emails/account_activated.html",
                    context={"user": updated_user},
                    recipient_list=[updated_user.email],
                )

            messages.success(request, "User updated successfully.")
            return redirect("accounts:manage_users")
    else:
        form = AdminUserManagementForm(instance=user_to_edit)

    return render(
        request, "accounts/edit_user.html", {"form": form, "user_to_edit": user_to_edit}
    )


@login_required
@allowed_users(allowed_roles=["ADMIN", "MANAGER"])
def delete_user(request, user_id):
    user_to_delete = get_object_or_404(User, id=user_id)
    if request.method == "POST":
        user_to_delete.delete()
        messages.success(request, "User deleted successfully.")
        return redirect("accounts:manage_users")
    return redirect("accounts:manage_users")


# --- UPDATED PROFILE VIEW (Password Change Email) ---
@login_required
def profile_view(request):
    user = request.user
    profile_form = UserProfileForm(instance=user)
    password_form = PasswordChangeForm(user)

    if request.method == "POST":
        if "update_profile" in request.POST:
            profile_form = UserProfileForm(request.POST, instance=user)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, "Your profile information has been updated.")
                return redirect("accounts:profile")

        elif "change_password" in request.POST:
            password_form = PasswordChangeForm(user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)

                # Send Password Changed Alert
                send_html_email(
                    subject="Your password was changed — Starter Kit",
                    template_name="emails/password_changed.html",
                    context={
                        "user": user,
                        "ip_address": request.META.get("REMOTE_ADDR"),
                    },
                    recipient_list=[user.email],
                )

                messages.success(
                    request, "Your password has been changed successfully."
                )
                return redirect("accounts:profile")
            else:
                messages.error(
                    request, "Please correct the errors in the password form."
                )

    context = {
        "profile_form": profile_form,
        "password_form": password_form,
        "sales_count": 125,
        "years_active": 2,
    }
    return render(request, "accounts/profile.html", context)
