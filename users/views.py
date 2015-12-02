from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth import login as django_login, authenticate, logout as django_logout
from django.contrib.auth.decorators import login_required, user_passes_test

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
            user = form.save()
            return redirect('/')
    else:
        form = RegistrationForm()
    return render_to_response('signup.html', {'form': form,}, context_instance=RequestContext(request))

def logout(request):
    django_logout(request)
    return redirect('/login')