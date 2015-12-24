from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect, render, render_to_response
from django.template import RequestContext

from teachers.forms import CourseForm
from teachers.models import Course
from teachers.models import Participation
from users.models import User

def teacher_check(user):
    return user.is_teacher

@user_passes_test(teacher_check)
def dashboard(request):
	courses = Course.objects.filter(owner=request.user).order_by('-created')
	return render_to_response('teacher_dashboard.html', {'courses': courses}, context_instance=RequestContext(request))

@user_passes_test(teacher_check)
def create(request):
	if request.method == 'POST':		
		form = CourseForm(data=request.POST, for_course=None)
		if form.is_valid():							
			course = Course.objects.create(owner=request.user, name=form.cleaned_data['name'], 
				description=form.cleaned_data['description'])
			for participant in form.cleaned_data['participants']:  
				part = Participation(user=participant, course=course)
				part.save()
			messages.add_message(request, messages.INFO, 'Course created successfully.')
			return redirect('/teachers')
	else:
		form = CourseForm(for_course=None)
	return render_to_response('create.html', {'form': form}, context_instance=RequestContext(request))

@user_passes_test(teacher_check)
def edit_course(request, course_id):
	course = Course.objects.get(id=course_id)
	if request.user.username == course.owner:
		participants = list(Participation.objects.filter(course=course_id))
		form = CourseForm(for_course=course)
		if request.method == 'POST':
			form = CourseForm(for_course=course, data=request.POST)
			if form.is_valid():
				course.save()
				form.save(commit=False)
				for participant in form.cleaned_data['participants']:  
					if participant not in participants:
						part = Participation(user=participant, course=course)
						part.save()
				messages.add_message(request, messages.INFO, 'Course updated successfully.')
				return redirect('/teachers')
		return render(request, 'edit_course.html', {'form': form, 'course': course, 'participants': participants})
	return redirect('/teachers')