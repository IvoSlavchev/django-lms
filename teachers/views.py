from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect, render, render_to_response
from django.template import RequestContext

from teachers.forms import CreateForm, ExistingCourseForm
from teachers.models import Course
from users.models import User

def teacher_check(user):
    return user.is_teacher

@user_passes_test(teacher_check, login_url='/login')
def dashboard(request):
	courses = Course.objects.filter(owner=request.user).order_by('-created')
	students = User.objects.filter(is_teacher=False)
	return render_to_response('teacher_dashboard.html', {'courses': courses, 'students': students}, 
		context_instance=RequestContext(request))

def create(request):
	if request.method == 'POST':		
		form = CreateForm(data=request.POST)
		form.instance.owner = request.user
		if form.is_valid():
			form.save()
			messages.add_message(request, messages.INFO, 'Course created successfully.')
			return redirect('/teachers')
	else:
		form = CreateForm()
	return render_to_response('create.html', {'form': form,}, context_instance=RequestContext(request))

def view_course(request, course_id):
    course = Course.objects.get(id=course_id)
    form = ExistingCourseForm(for_course=course)
    if request.method == 'POST':
        form = ExistingCourseForm(for_course=course, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(course)
    return render(request, 'course.html', {'course': course})