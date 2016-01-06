from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.shortcuts import redirect, render

from courses.models import Course, Participation
from courses.views import teacher_check, student_check
from exams.forms import ExamForm, ExamQuestionForm
from exams.models import Exam, ExamQuestion, Score
from questions.models import Question, Choice

def update(form, exam):
	exam.name = form.cleaned_data['name']
	exam.description = form.cleaned_data['description']
	exam.password = form.cleaned_data['password']
	exam.time_limit = form.cleaned_data['time_limit']
	exam.active_from = form.cleaned_data['active_from']
	exam.active_to = form.cleaned_data['active_to']
	exam.save()

def send_email(student, course, exam):
	email_subject = 'Django-LMS new exam added'
	email_body = "Hello, %s,\n\n\
		Exam %s has been added for the %s course and will be active from %s.\
		You can view the exam by clicking the link below.\n\
		http://localhost:8000/courses/%d/exams/%d/s" % (student.username, exam.name, 
			course.name, exam.active_from, course.id, exam.id)
	send_mail(email_subject, email_body, settings.EMAIL_HOST, [student.email])

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
			participants = Participation.objects.filter(course=course_id)
			for participant in participants:
				send_email(participant.user, course, exam)
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
	questions = Question.objects.filter(course=course)
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
	exams = Exam.objects.filter(course=course_id).order_by('active_to')
	if request.user.username == course.owner:
		return render(request, 'list_exams.html', {'course': course, 'exams': exams})
	else:
		return redirect('/courses/')

@user_passes_test(student_check)
def view_exam(request, course_id, exam_id):
	course = Course.objects.get(id=course_id)
	exam = Exam.objects.get(id=exam_id)
	questions = ExamQuestion.objects.filter(exam=exam)
	if questions:
		try:
			score = Score.objects.get(student=request.user, exam=exam).score
			precentage = str(float(score)/float(questions.count())*100)+'%'
			result = precentage + ' '+ str(score) +'/' + str(questions.count())
		except ObjectDoesNotExist:
			result = "Exam not yet taken."
	else:
		result = "Exam has no assigned questions."
	return render(request, 'view_exam.html', {'course': course, 'exam': exam, 'questions': questions, 
		'result': result})

@user_passes_test(student_check)
def take_exam(request, course_id, exam_id):
	course = Course.objects.get(id=course_id)
	exam = Exam.objects.get(id=exam_id)
	questions = Question.objects.filter(exam=exam)
	if exam.activated and not exam.expired:
		try:
			score = Score.objects.get(student=request.user, exam=exam)
			messages.add_message(request, messages.INFO, 'Exam already taken')
			return redirect('/courses/' +  course_id + '/exams/' + exam_id + '/s')
		except ObjectDoesNotExist:
			if request.method == 'POST':
				answered = 0
				for question in questions:
					try:
						selected_answer = question.choice_set.get(id=request.POST.get(str(question.id)))
						if selected_answer.correct:
							answered += 1
					except ObjectDoesNotExist:
						continue;
				score = Score.objects.create(student=request.user, exam=exam, score=answered)
				messages.add_message(request, messages.INFO, 'Exam finished with ' + str(answered) + ' correct answers')
				return redirect('/courses/' +  course_id + '/exams/' + exam_id + '/s')
			return render(request, 'take_exam.html', {'course': course, 'exam': exam, 'questions': questions})
	messages.add_message(request, messages.INFO, 'Exam closed.')
	return redirect('/courses/' +  course_id + '/exams/' + exam_id + '/s')