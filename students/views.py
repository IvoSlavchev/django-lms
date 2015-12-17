from itertools import chain

from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render

from teachers.forms import CreateForm, ExistingCourseForm
from teachers.models import Course
from teachers.models import Participation
from users.models import User

def student_check(user):
    return user.is_teacher == False

@user_passes_test(student_check, login_url='/login')
def dashboard(request):
	participants = list(Participation.objects.filter(user=request.user.id))
	courses_unflattened = list()
	for participant in participants:
		courses_unflattened.append(list(Course.objects.filter(id=participant.course.id)))
	courses = list(chain.from_iterable(courses_unflattened))
	courses.sort(key=lambda x: x.created, reverse=True)
	return render(request, 'student_dashboard.html', {'courses': courses})

@user_passes_test(student_check, login_url='/login')
def view_course(request, course_id):
    course = Course.objects.get(id=course_id)
    participants = list(Participation.objects.filter(course=course_id))
    form = ExistingCourseForm(for_course=course)
    if request.method == 'POST':
        form = ExistingCourseForm(for_course=course, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(course)
    return render(request, 'course.html', {'course': course, 'participants': participants})