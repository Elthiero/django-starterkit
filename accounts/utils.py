import threading
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

class EmailThread(threading.Thread):
    """
    A separate thread that handles the actual sending of the email 
    so the main Django process doesn't get blocked.
    """
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send(fail_silently=True)

def send_html_email(subject, template_name, context, recipient_list):
    """Renders an HTML template and sends a multipart email asynchronously."""
    context['site_url'] = getattr(settings, 'SITE_URL', 'http://127.0.0.1:8000') 
    
    html_message = render_to_string(template_name, context)
    plain_message = strip_tags(html_message)
    
    email = EmailMultiAlternatives(
        subject=subject,
        body=plain_message,
        from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@yourdomain.com'),
        to=recipient_list
    )
    email.attach_alternative(html_message, "text/html")
    
    # Hand the email object to the thread and start it immediately
    EmailThread(email).start()