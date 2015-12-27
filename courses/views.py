from itertools import chain

from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect, render

from courses.forms import CourseForm
from courses.models import Course
from courses.models import Participation
from users.models import User

def teacher_check(user):
    return user.is_teacher

def student_check(user):
    return user.is_teacher == False

def update(form, course):
	course.name = form.cleaned_data['name']
	course.description = form.cleaned_data['description']
	course.save()
	Participation.objects.filter(course=course).delete()
	for participant in form.cleaned_data['participants']:  
		part = Participation(user=participant, course=course)
		part.save()

def delete(course):
	course.delete()
	Participation.objects.filter(course=course).delete()

@user_passes_test(teacher_check)
def teacher_page(request):
	courses = Course.objects.filter(owner=request.user).order_by('-updated')
	return render(request, 'teacher_page.html', {'courses': courses})

@user_passes_test(teacher_check)
def create_course(request):
	if request.method == 'POST':		
		form = CourseForm(data=request.POST, instance=None)
		if form.is_valid():							
			course = Course.objects.create(owner=request.user, name=form.cleaned_data['name'], 
				description=form.cleaned_data['description'])
			for participant in form.cleaned_data['participants']:  
				part = Participation(user=participant, course=course)
				part.save()
			messages.add_message(request, messages.INFO, 'Course created successfully.')
			return redirect('/courses/')
	else:
		form = CourseForm(instance=None)
	return render(request, 'create_course.html', {'form': form})

@user_passes_test(teacher_check)
def edit_course(request, course_id):
	course = Course.objects.get(id=course_id)
	if request.user.username == course.owner:
		participants = list(Participation.objects.filter(course=course_id))
		if request.method == 'POST' and 'update' in request.POST:
			form = CourseForm(instance=course, data=request.POST)
			if form.is_valid():
				update(form, course)
				messages.add_message(request, messages.INFO, 'Course updated successfully.')
				return redirect('/courses/')						
		if request.method == 'POST' and 'delete' in request.POST:
			delete(course)		
			messages.add_message(request, messages.INFO, 'Course deleted successfully.')
			return redirect('/courses/')		
		else :
			form = CourseForm(instance=course)
		return render(request, 'edit_course.html', {'form': form, 'course': course, 'participants': participants})
	return redirect('/courses/')

@user_passes_test(student_check)
def student_page(request):
	participants = list(Participation.objects.filter(user=request.user.id))
	courses_unflattened = list()
	for participant in participants:
		courses_unflattened.append(list(Course.objects.filter(id=participant.course.id)))
	courses = list(chain.from_iterable(courses_unflattened))
	courses.sort(key=lambda x: x.updated, reverse=True)
	return render(request, 'student_page.html', {'courses': courses})

@user_passes_test(student_check)
def view_course(request, course_id):
    course = Course.objects.get(id=course_id)
    participants = list(Participation.objects.filter(course=course_id))
    return render(request, 'view_course.html', {'course': course, 'participants': participants})