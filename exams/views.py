from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render

def teacher_check(user):
    return user.is_teacher

@user_passes_test(teacher_check)
def create_exam(request, course_id):
	return render(request, "create_exam.html")