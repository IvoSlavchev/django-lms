from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect, render

from courses.models import Course
from courses.views import teacher_check, student_check
from exams.forms import ExamForm, ExamQuestionForm
from exams.models import Exam, ExamQuestion
from questions.models import Question

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
			exam = form.save(commit=False)
			exam.owner = request.user
			exam.course = course
			exam.save()
			messages.add_message(request, messages.INFO, 'Exam created successfully.')		
			return redirect('/courses/' + course_id + '/exams/')
	else:
		form = ExamForm()
	return render(request, 'create_exam.html', {'form': form, 'course': course })

@user_passes_test(teacher_check)
def edit_exam(request, course_id, exam_id):
	course = Course.objects.get(id=course_id)
	exam = Exam.objects.get(id=exam_id)	
	if request.user.username == exam.owner:
		if request.method == 'POST' and 'update' in request.POST:
			form = ExamForm(instance=exam, data=request.POST)
			if form.is_valid():
				update(form, exam)
				messages.add_message(request, messages.INFO, 'Exam updated successfully.')
				return redirect('/courses/' + course_id + '/exams/')						
		if request.method == 'POST' and 'delete' in request.POST:
			exam.delete()		
			messages.add_message(request, messages.INFO, 'Exam deleted successfully.')
			return redirect('/courses/' + course_id + '/exams/')		
		else:
			form = ExamForm(instance=exam)
		return render(request, 'edit_exam.html', {'form': form, 'course': course, 'exam': exam })
	return redirect('/courses/' + course_id + '/exams/')

@user_passes_test(teacher_check)
def edit_questions(request, course_id, exam_id):
	course = Course.objects.get(id=course_id)
	exam = Exam.objects.get(id=exam_id)
	#questions = list(ExamQuestion.objects.filter(exam=exam))
	questions = list(Question.objects.filter(course=course))
	if request.user.username == course.owner:
		if request.method == 'POST':
			form = ExamQuestionForm(instance=exam, course=course, data=request.POST)
			if form.is_valid():
				ExamQuestion.objects.filter(exam=exam).delete()
				for question in form.cleaned_data['questions']:  
					quest = ExamQuestion(question=question, exam=exam)
					quest.save()
				messages.add_message(request, messages.INFO, 'Questions updated successfully.')
				return redirect('/courses/' + course_id + '/exams/' + exam_id)
		form = ExamQuestionForm(instance=exam, course=course)
		return render(request, 'edit_questions.html', {'form': form, 'course': course, 'exam': exam, 
			'questions': questions})
	else:
		return redirect('/courses/')

@user_passes_test(teacher_check)
def list_exams(request, course_id):
	course = Course.objects.get(id=course_id)
	exams = Exam.objects.filter(course=course_id)
	if request.user.username == course.owner:
		return render(request, 'list_exams.html', {'course': course, 'exams': exams})
	else:
		return redirect('/courses/')

@user_passes_test(student_check)
def view_exam(request, course_id, exam_id):
	course = Course.objects.get(id=course_id)
	exam = Exam.objects.get(id=exam_id)
	return render(request, 'view_exam.html', {'course': course, 'exam': exam})