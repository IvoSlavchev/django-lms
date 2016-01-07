from itertools import chain

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.shortcuts import redirect, render

from courses.forms import CourseForm, ParticipantsForm
from courses.models import Course, Participation
from exams.models import Exam, ExamQuestion, Score
from questions.models import Question, Choice

def teacher_check(user):
    return user.is_teacher

def student_check(user):
    return not user.is_teacher

def update_course(form, course):
	course.name = form.cleaned_data['name']
	course.description = form.cleaned_data['description']
	course.save()

def delete_course(course):
	Participation.objects.filter(course=course).delete()	
	Exam.objects.filter(course=course).delete()
	questions = Question.objects.filter(course=course)	
	for question in questions:
		ExamQuestion.objects.filter(question=question).delete()
		Choice.objects.filter(question=question).delete()
	questions.delete()
	course.delete()

def send_email(student, course):
	email_subject = 'Django-LMS course enrollment'
	email_body = "Hello, %s,\n\n\
		You have been enrolled in the %s course by the course creator %s.\
		You can visit the course page by clicking the link below.\n\
		http://localhost:8000/courses/%d/s" % (student.username, course.name, 
			course.owner, course.id)
	send_mail(email_subject, email_body, settings.EMAIL_HOST, [student.email])

@user_passes_test(teacher_check)
def teacher_page(request):
	courses = Course.objects.filter(owner=request.user).order_by('-updated')
	exams_unflattened = list()
	for course in courses:
		exams_unflattened.append(Exam.objects.filter(course=course))
	exams = list(chain.from_iterable(exams_unflattened))
	exams.sort(key=lambda x: x.active_to)
	return render(request, 'teacher_page.html', {'courses': courses, 'exams': exams})

@user_passes_test(teacher_check)
def create_course(request):
	if request.method == 'POST':		
		form = CourseForm(data=request.POST)
		if form.is_valid():							
			course = form.save(commit=False)
			course.owner = request.user
			course.save()
			messages.add_message(request, messages.INFO, 'Course created successfully.')
			return redirect('/courses/')
	else:
		form = CourseForm()
	return render(request, 'create_course.html', {'form': form})

@user_passes_test(teacher_check)
def edit_course(request, course_id):
	course = Course.objects.get(id=course_id)
	if request.user.username == course.owner:		
		if request.method == 'POST' and 'update' in request.POST:
			form = CourseForm(instance=course, data=request.POST)
			if form.is_valid():
				update_course(form, course)
				messages.add_message(request, messages.INFO, 'Course updated successfully.')
				return redirect('/courses/')						
		if request.method == 'POST' and 'delete' in request.POST:
			delete_course(course)
			messages.add_message(request, messages.INFO, 'Course deleted successfully.')
			return redirect('/courses/')		
		else:
			form = CourseForm(instance=course)
		return render(request, 'edit_course.html', {'form': form, 'course': course})
	return redirect('/courses/')

@user_passes_test(teacher_check)
def edit_participants(request, course_id):
	course = Course.objects.get(id=course_id)	
	if request.user.username == course.owner:
		participants = Participation.objects.filter(course=course_id)
		if request.method == 'POST':
			form = ParticipantsForm(instance=course, data=request.POST)
			if form.is_valid():
				Participation.objects.filter(course=course).delete()
				for participant in form.cleaned_data['participants']:  
					part = Participation(user=participant, course=course)
					part.save()
					send_email(part.user, course)
				messages.add_message(request, messages.INFO, 'Participants updated successfully.')
				return redirect('/courses/' + course_id)
		form = ParticipantsForm(instance=course)
		return render(request, 'edit_participants.html', {'form': form, 'course': course, 'participants': participants})
	else:
		return redirect('/courses/')

@user_passes_test(teacher_check)
def view_scores(request, course_id):
	course = Course.objects.get(id=course_id)
	if request.user.username == course.owner:
		participants = Participation.objects.filter(course=course_id)
		exams = Exam.objects.filter(course=course_id)
		scores  = {}
		for participant in participants:
			scores[participant] = {}
			for exam in exams:
				try:
					questions = ExamQuestion.objects.filter(exam=exam)
					score = Score.objects.get(student=participant.user, exam=exam).score
					percentage = str(float(score)/float(questions.count())*100)+'%'
					scores[participant][exam] = str(score) + '/' + str(questions.count()) + ' ' + percentage
				except ObjectDoesNotExist:
					scores[participant][exam] = "Not taken"
		return render(request, 'view_scores.html', {'course': course, 'exams': exams, 'scores': scores})
	else:
		return redirect('/courses/')

@user_passes_test(student_check)
def student_page(request):
	participants = Participation.objects.filter(user=request.user)
	courses_unflattened = list()
	unfinished_exams = list()
	for participant in participants:
		courses_unflattened.append(Course.objects.filter(id=participant.course.id))
	courses = list(chain.from_iterable(courses_unflattened))
	courses.sort(key=lambda x: x.updated, reverse=True)
	for course in courses:
		exams = Exam.objects.filter(course=course)
		for exam in exams:
			if (exam.activated and not exam.expired and 
				not Score.objects.filter(student=request.user, exam=exam).exists() 
				and ExamQuestion.objects.filter(exam=exam).exists()):
					unfinished_exams.append(exam)
	unfinished_exams.sort(key=lambda x: x.active_to)
	return render(request, 'student_page.html', {'courses': courses, 'exams': unfinished_exams})

@user_passes_test(student_check)
def view_course(request, course_id):
    course = Course.objects.get(id=course_id)
    participants = Participation.objects.filter(course=course_id)
    exams = Exam.objects.filter(course=course_id).order_by('active_to')
    return render(request, 'view_course.html', {'course': course, 'participants': participants, 'exams': exams})