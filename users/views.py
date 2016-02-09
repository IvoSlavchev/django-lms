import datetime
import hashlib

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login as django_login, authenticate
from django.contrib.auth import logout as django_logout
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from users.models import UserProfile
from users.forms import AuthenticationForm, RegistrationForm


def send_email(user, profile):
    email_subject = 'Your new Django-LMS account confirmation'
    email_body = "Hello, %s,\n\n\
        Thank you for signing up for Django-LMS! To activate your account, \
        click this link within 24 hours:\n\
        http://localhost:8000/confirm?q=%s" % (
            user.username, profile.activation_key)
    send_mail(email_subject, email_body, settings.EMAIL_HOST, [user.email])


def home(request):
    if not request.user.is_authenticated():
        form = AuthenticationForm()
        if request.method == 'POST':
            form = AuthenticationForm(data=request.POST)
            if form.is_valid():
                user = authenticate(username=request.POST['username'],
                    password=request.POST['password'])
                if user is not None:
                    if user.is_active:
                        django_login(request, user)
                        if user.is_teacher:
                            return redirect('/courses/')
                        else:
                            return redirect('/courses/s')
        return render(request, 'home.html', {'form': form})
    if request.user.is_teacher:
        return redirect('/courses/')
    return redirect('/courses/s')


def signup(request):
    if not request.user.is_authenticated():
        form = RegistrationForm() 
        if request.method == 'POST':
            form = RegistrationForm(data=request.POST)
            if form.is_valid():
                user = form.save()
                activation_key = (hashlib.sha224(user.username.encode('utf-8'))
                    .hexdigest())
                key_expires = timezone.now() + datetime.timedelta(1)
                profile = UserProfile(user=user, activation_key=activation_key,
                    key_expires=key_expires)
                profile.save()
                send_email(user, profile)
                messages.info(request, 'Check email for a confirmation link!')
                return redirect('/')          
        return render(request, 'signup.html', {'form': form})
    if request.user.is_teacher:
        return redirect('/courses/')
    return redirect('/courses/s')


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
    messages.success(request, 'Logged out!')
    return redirect('/')