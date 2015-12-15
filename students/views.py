from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render

def student_check(user):
    return user.is_teacher == False

@user_passes_test(student_check, login_url='/login')
def dashboard(request):
    return render(request, 'student_dashboard.html')