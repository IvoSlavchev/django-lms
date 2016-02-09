from itertools import chain

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render

from courses.forms import CourseForm, ParticipantsForm
from courses.models import Course, Participation
from exams.models import Exam, ExamQuestion, Score, StudentAnswer
from questions.models import Question, Choice


def teacher_check(user):
    if user.is_anonymous():
        return False
    return user.is_teacher

def student_check(user):
    if user.is_anonymous():
        return False
    return not user.is_teacher


def delete_course(course):
    Participation.objects.filter(course=course).delete()
    questions = Question.objects.filter(course=course)
    exams = Exam.objects.filter(course=course)
    for question in questions:
        exam_questions = ExamQuestion.objects.filter(question=question)
        for exam_question in exam_questions:
            StudentAnswer.objects.filter(exam_question=exam_question).delete()
        Choice.objects.filter(question=question).delete()
        exam_questions.delete()
    for exam in exams:
        Score.objects.filter(exam=exam)
    questions.delete()
    exams.delete()
    course.delete()


def format_score(score, count):
    percentage = str(float(score) / float(count) * 100) + '%'
    return str(score) + '/' + str(count) + ' ' + percentage


@user_passes_test(teacher_check)
def teacher_courses(request):
    courses = Course.objects.filter(owner=request.user).order_by('-updated')
    exams_unflattened = list()
    for course in courses:
        exams_unflattened.append(Exam.objects.filter(course=course))
    exams = list(chain.from_iterable(exams_unflattened))
    exams.sort(key=lambda x: x.active_to)
    return render(request, 'teacher_courses.html', {'courses': courses,
        'exams': exams})


@user_passes_test(teacher_check)
def create_course(request):
    form = CourseForm()
    if request.method == 'POST':
        form = CourseForm(data=request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.owner = request.user
            course.save()
            messages.success(request, 'Course created successfully!')
            return redirect('/courses/')
    return render(request, 'create_course.html', {'form': form})


@user_passes_test(teacher_check)
def edit_course(request, course_id):
    course = Course.objects.get(id=course_id)
    if request.user == course.owner:
        form = CourseForm(instance=course)
        if request.method == 'POST' and 'update' in request.POST:
            form = CourseForm(instance=course, data=request.POST)
            if form.is_valid():
                course.name = form.cleaned_data['name']
                course.description = form.cleaned_data['description']
                course.save()
                messages.success(request, 'Course updated successfully!')
                return redirect('/courses/')
        if request.method == 'POST' and 'delete' in request.POST:
            delete_course(course)
            messages.success(request, 'Course deleted successfully!')
            return redirect('/courses/')
        return render(request, 'edit_course.html', {'form': form,
            'course': course})
    return redirect('/courses/')


@user_passes_test(teacher_check)
def edit_participants(request, course_id):
    course = Course.objects.get(id=course_id)
    if request.user == course.owner:
        participants = Participation.objects.filter(course=course_id)
        form = ParticipantsForm(instance=course)
        if request.method == 'POST':
            form = ParticipantsForm(instance=course, data=request.POST)
            if form.is_valid():
                Participation.objects.filter(course=course).delete()
                for participant in form.cleaned_data['participants']:
                    part = Participation(user=participant, course=course)
                    part.save()
                messages.success(request, 'Participants updated successfully!')
                return redirect('/courses/' + course_id) 
        return render(request, 'edit_participants.html', {'form': form,
            'course': course, 'participants': participants})
    return redirect('/courses/')


@user_passes_test(teacher_check)
def view_course_results(request, course_id):
    course = Course.objects.get(id=course_id)
    if request.user == course.owner:
        participants = Participation.objects.filter(course=course_id)
        exams = Exam.objects.filter(course=course_id)
        scores = {}
        for participant in participants:
            scores[participant] = {}
            for exam in exams:
                try:
                    count = ExamQuestion.objects.filter(exam=exam).count()
                    score = Score.objects.get(user=participant.user,
                        exam=exam).score
                    scores[participant][exam] = format_score(score, count)
                except ObjectDoesNotExist:
                    scores[participant][exam] = "Not taken"
        return render(request, 'view_course_results.html', {'course': course,
            'exams': exams, 'scores': scores})
    return redirect('/courses/')


@user_passes_test(student_check)
def student_courses(request):
    participants = Participation.objects.filter(user=request.user)
    courses = list()
    unfinished = list()
    for participant in participants:
        courses.append(Course.objects.filter(id=participant.course.id))
    courses = list(chain.from_iterable(courses))
    courses.sort(key=lambda x: x.updated, reverse=True)
    for course in courses:
        exams = Exam.objects.filter(course=course)
        for exam in exams:
            if (exam.active and not Score.objects.filter(user=request.user,
                exam=exam).exists() and ExamQuestion.objects.filter(exam=exam)
                .exists()):
                    unfinished.append(exam)
    unfinished.sort(key=lambda x: x.active_to)
    return render(request, 'student_courses.html', {'courses': courses,
        'exams': unfinished})


@user_passes_test(student_check)
def view_course(request, course_id):
    if (Participation.objects.filter(user=request.user, course=course_id)
        .exists()):
        course = Course.objects.get(id=course_id)
        scores = {}
        exams = Exam.objects.filter(course=course_id).order_by('active_to')
        participants = Participation.objects.filter(course=course_id)
        for exam in exams:
                try:
                    count = ExamQuestion.objects.filter(exam=exam).count()
                    score = Score.objects.get(user=request.user,
                        exam=exam).score
                    scores[exam] = format_score(score, count)
                except ObjectDoesNotExist:
                    scores[exam] = "Not taken"
        return render(request, 'view_course.html', {'course': course,
            'participants': participants, 'exams': exams, 'scores': scores})
    return redirect('/courses/s')