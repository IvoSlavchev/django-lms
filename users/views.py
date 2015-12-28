import datetime
import hashlib

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login as django_login, authenticate, logout as django_logout
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from users.models import UserProfile
from users.forms import AuthenticationForm, RegistrationForm

def home_page(request):
    return render(request, 'home.html')

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = authenticate(username=request.POST['username'], password=request.POST['password'])
            if user is not None:
                if user.is_active:
                    django_login(request, user)
                    if user.is_teacher:
                        return redirect('/courses/')
                    else:
                        return redirect('/courses/s')
        messages.add_message(request, messages.ERROR, 'Please try again.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form,})

def signup(request):
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            activation_key = hashlib.sha224(user.username.encode('utf-8')).hexdigest()
            key_expires = timezone.now() + datetime.timedelta(1)
            profile = UserProfile(user=user, activation_key=activation_key, key_expires=key_expires)
            profile.save()
            email_subject = 'Your new Django-LMS account confirmation'
            email_body = "Hello, %s, and thanks for signing up for an Django-LMS account!\n\n \
                To activate your account, click this link within 24 hours:\n\n \
                http://localhost:8000/confirm?q=%s" % (user.username, profile.activation_key)
            send_mail(email_subject, email_body, settings.EMAIL_HOST, [user.email], fail_silently=False)
            messages.add_message(request, messages.INFO, 'Success. Check email for a confirmation link.')
            return redirect('/')
        messages.add_message(request, messages.ERROR, 'Please try again.')
    else:
        form = RegistrationForm()        
    return render(request, 'signup.html', {'form': form,})

def confirm(request):
    activation_key = request.GET.get('q', '')
    profile = get_object_or_404(UserProfile, activation_key=activation_key)
    if profile.key_expires < timezone.now():
        return render(request, 'confirm.html', {'success': False})
    user = profile.user
    user.is_active = True
    user.save()
    return render(request, 'confirm.html', {'success': True})

def logout(request):
    django_logout(request)
    messages.add_message(request, messages.INFO, 'Success.')
    return redirect('/login')