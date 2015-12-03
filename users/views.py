from django.shortcuts import render, render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.contrib.auth import login as django_login, authenticate, logout as django_logout
from django.contrib.auth.decorators import login_required, user_passes_test
import datetime
from django.contrib.auth.hashers import PBKDF2PasswordHasher
from django.core.mail import send_mail
from django.conf import settings

from users.models import UserProfile
from users.forms import AuthenticationForm, RegistrationForm

def teacher_check(user):
    return user.is_teacher

def student_check(user):
    return user.is_teacher == False

def home_page(request):
    return render(request, 'home.html')

@user_passes_test(teacher_check)
def teacher_page(request):
    return render(request, 'teacher.html')

@user_passes_test(student_check)
def student_page(request):
    return render(request, 'student.html')

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = authenticate(username=request.POST['username'], is_teacher=request.POST.get('is_teacher', False), 
                                password=request.POST['password'])
            if user is not None:
                if user.is_active:
                    django_login(request, user)
                    if user.is_teacher:
                        return redirect('/teacher')
                    else:
                        return redirect('/student')
    else:
        form = AuthenticationForm()
    return render_to_response('login.html', {'form': form,}, context_instance=RequestContext(request))

def signup(request):
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            hasher = PBKDF2PasswordHasher()
            user = form.save()
            activation_key = hasher.encode(password=user.username, salt='salt', iterations=10).replace('+', 's')
            key_expires = datetime.datetime.today() + datetime.timedelta(1)
            profile = UserProfile(user=user, activation_key=activation_key, key_expires=key_expires)
            profile.save()
            email_subject = 'Your new Django-LMS account confirmation'
            email_body = "Hello, %s, and thanks for signing up for an Django-LMS account!\n\n \
                To activate your account, click this link within 24 hours:\n\n \
                http://localhost:8000/confirm/?key=%s" % (
                user.username,
                profile.activation_key)
            send_mail(email_subject, email_body, settings.EMAIL_HOST, [user.email], fail_silently=False)
            return redirect('/')
    else:
        form = RegistrationForm()
    return render_to_response('signup.html', {'form': form,}, context_instance=RequestContext(request))

def confirm(request):
    activation_key = request.GET.get('key', '')
    profile = get_object_or_404(UserProfile, activation_key=activation_key)
    tz_info = profile.key_expires.tzinfo
    if profile.key_expires < datetime.datetime.now(tz_info):
        return render_to_response('confirm.html', {'expired': True})
    user = profile.user
    user.is_active = True
    user.save()
    return render_to_response('confirm.html', {'success': True})

def logout(request):
    django_logout(request)
    return redirect('/login')