from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect, render

from courses.models import Course
from courses.views import teacher_check, student_check
from exams.forms import ExamForm
from exams.models import Exam

def update(form, exam):
	exam.name = form.cleaned_data['name']
	exam.description = form.cleaned_data['description']
	exam.date_to_be_taken = form.cleaned_data['date_to_be_taken']
	exam.save()

@user_passes_test(teacher_check)
def create_exam(request, course_id):
	course = Course.objects.get(id=course_id)
	if request.method == 'POST':		
		form = ExamForm(data=request.POST)
		if form.is_valid():			
			exam = Exam.objects.create(owner=request.user, name=form.cleaned_data['name'], 
				description=form.cleaned_data['description'], date_to_be_taken=form.cleaned_data['date_to_be_taken'], 
				course=Course.objects.get(id=course_id))
			messages.add_message(request, messages.INFO, 'Exam created successfully.')		
			return redirect('/courses/' + course_id + '/')
	else:
		form = ExamForm()
	return render(request, 'create_exam.html', {'form': form, 'course': course })

@user_passes_test(teacher_check)
def edit_exam(request, course_id, exam_id):
	exam = Exam.objects.get(id=exam_id)
	course = Course.objects.get(id=course_id)
	if request.user.username == exam.owner:
		if request.method == 'POST' and 'update' in request.POST:
			form = ExamForm(instance=exam, data=request.POST)
			if form.is_valid():
				update(form, exam)
				messages.add_message(request, messages.INFO, 'Exam updated successfully.')
				return redirect('/courses/' + course_id + '/')						
		if request.method == 'POST' and 'delete' in request.POST:
			exam.delete()		
			messages.add_message(request, messages.INFO, 'Exam deleted successfully.')
			return redirect('/courses/' + course_id + '/')		
		else :
			form = ExamForm(instance=exam)
		return render(request, 'edit_exam.html', {'form': form, 'course': course, 'exam': exam })
	return redirect('/courses/' + course_id + '/')

@user_passes_test(student_check)
def view_exam(request, course_id, exam_id):
	course = Course.objects.get(id=course_id)
	exam = Exam.objects.get(id=exam_id)
	return render(request, 'view_exam.html', {'course': course, 'exam': exam})