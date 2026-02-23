from django.shortcuts import render
from django.contrib.auth.decorators import login_required


# Create your views here.
def home(request):
    return render(request, 'public/home.html')

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

def contact(request):
    return render(request, 'public/contact.html')

def privacy(request):
    return render(request, 'public/privacy.html')

def terms(request):
    return render(request, 'public/terms.html')