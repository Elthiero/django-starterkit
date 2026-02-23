from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.utils import timezone
from .utils import send_html_email 

@receiver(user_logged_in)
def send_login_alert(sender, user, request, **kwargs):
    # Fetch device and location info from the request headers
    user_agent = request.META.get('HTTP_USER_AGENT', 'Unknown device')
    ip_address = request.META.get('REMOTE_ADDR', 'Unknown')
    
    send_html_email(
        subject="New sign-in to your Starter Kit account",
        template_name="emails/new_login_alert.html",
        context={
            "user": user,
            "ip_address": ip_address,
            "user_agent": user_agent,
            "time": timezone.now()
        },
        recipient_list=[user.email]
    )