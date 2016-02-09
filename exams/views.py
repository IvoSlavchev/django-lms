from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render

from courses.models import Course, Participation
from courses.views import teacher_check, student_check, format_score
from exams.forms import ExamForm
from exams.models import Exam, ExamQuestion, Score, StudentAnswer
from questions.models import Question, Choice
from users.models import User


def update(form, exam):
    exam.name = form.cleaned_data['name']
    exam.description = form.cleaned_data['description']
    exam.password = form.cleaned_data['password']
    exam.time_limit = form.cleaned_data['time_limit']
    exam.active_from = form.cleaned_data['active_from']
    exam.active_to = form.cleaned_data['active_to']
    exam.category = form.cleaned_data['category']
    exam.question_count = form.cleaned_data['question_count']
    exam.save()
    
def delete(exam):
    Score.objects.filter(exam=exam).delete()
    exam_questions = ExamQuestion.objects.filter(exam=exam)
    for exam_question in exam_questions:
        StudentAnswer.objects.filter(exam_question=exam_question).delete()
    exam_questions.delete()
    exam.delete()

def add_questions(course, exam):
    ExamQuestion.objects.filter(exam=exam).delete()
    questions = (Question.objects.filter(course=course, category=exam.category)
        .order_by('?')[:exam.question_count])
    for question in questions:
        quest = ExamQuestion(question=question, exam=exam)
        quest.save()


@user_passes_test(teacher_check)
def create_exam(request, course_id):
    course = Course.objects.get(id=course_id)
    if Question.objects.filter(course=course).exists():
        form = ExamForm(course=course)
        if request.method == 'POST':
            form = ExamForm(course=course, data=request.POST)
            if form.is_valid():
                exam = form.save(commit=False)
                exam.course = course
                exam.save()
                add_questions(course, exam)
                messages.success(request, 'Exam created successfully!')
                return redirect('/courses/' + course_id + '/exams/')
        return render(request, 'create_exam.html', {'form': form,
            'course': course })
    messages.error(request, 'Course has no questions!')
    return redirect('/courses/' + course_id)


@user_passes_test(teacher_check)
def edit_exam(request, course_id, exam_id):
    course = Course.objects.get(id=course_id)
    exam = Exam.objects.get(id=exam_id) 
    if request.user == course.owner:   
        form = ExamForm(instance=exam)
        if request.method == 'POST' and 'update' in request.POST:
            form = ExamForm(instance=exam, data=request.POST)
            if form.is_valid():
                update(form, exam)
                add_questions(course, exam)
                messages.success(request, 'Exam updated successfully!')
                return redirect('/courses/' + course_id + '/exams/')
        if request.method == 'POST' and 'delete' in request.POST:
            delete(exam)
            messages.success(request, 'Exam deleted successfully!')
            return redirect('/courses/' + course_id + '/exams/')
        return render(request, 'edit_exam.html', {'form': form,
            'course': course, 'exam': exam })
    return redirect('/courses/' + course_id + '/exams/')


@user_passes_test(teacher_check)
def list_exams(request, course_id):
    course = Course.objects.get(id=course_id)
    if request.user == course.owner:
        exams = Exam.objects.filter(course=course_id).order_by('active_to')
        return render(request, 'list_exams.html', {'course': course,
            'exams': exams})
    return redirect('/courses/')


@user_passes_test(teacher_check)
def view_exam_results(request, course_id, exam_id):
    course = Course.objects.get(id=course_id)
    exam = Exam.objects.get(id=exam_id)
    if request.user == course.owner:
        participants = Participation.objects.filter(course=course)
        count = ExamQuestion.objects.filter(exam=exam).count()
        scores = {}     
        for participant in participants:
            try:            
                score = (Score.objects.get(user=participant.user, exam=exam)
                    .score)
                scores[participant] = format_score(score, count)
            except ObjectDoesNotExist:
                scores[participant] = "Not taken"
        return render(request, 'view_exam_results.html', {'course': course,
            'exam': exam, 'scores': scores})
    return redirect('/courses/')


@user_passes_test(teacher_check)
def view_participant_result(request, course_id, exam_id, student_id):
    course = Course.objects.get(id=course_id)
    exam = Exam.objects.get(id=exam_id)
    if request.user == course.owner:
        student = User.objects.get(id=student_id)
        exam = Exam.objects.get(id=exam_id)
        exam_questions = ExamQuestion.objects.filter(exam=exam)
        score = Score.objects.get(user=student, exam=exam).score
        result = format_score(score, exam_questions.count())
        answers = {}
        for exam_question in exam_questions:
            answers[exam_question] = StudentAnswer.objects.get(user=
                student, exam_question=exam_question).answer
        return render(request, 'view_result.html', {'course': course,
            'exam': exam, 'exam_questions': exam_questions, 'result': result,
            'answers': answers, 'student': student})
    return redirect('/courses/')


@user_passes_test(teacher_check)
def view_assigned(request, course_id, exam_id):
    course = Course.objects.get(id=course_id)
    exam = Exam.objects.get(id=exam_id)
    if request.user == course.owner:
        exam_questions = ExamQuestion.objects.filter(exam=exam)
        return render(request, 'view_questions.html', {'course': course,
            'exam': exam, 'exam_questions': exam_questions})
    return redirect('/courses/')


@user_passes_test(student_check)
def view_exam(request, course_id, exam_id):
    if (Participation.objects.filter(user=request.user, course=course_id)
        .exists()):
        course = Course.objects.get(id=course_id)
        exam = Exam.objects.get(id=exam_id)
        exam_questions = ExamQuestion.objects.filter(exam=exam)
        try:
            score = (Score.objects.get(user=request.user, exam=exam)
                .score)
            result = format_score(score, exam_questions.count())
        except ObjectDoesNotExist:
            result = "Exam not yet taken."
        return render(request, 'view_exam.html', {'course': course,
            'exam': exam, 'exam_questions': exam_questions, 'result': result})
    return redirect('/courses/s')


@user_passes_test(student_check)
def input_password(request, course_id, exam_id):
    course = Course.objects.get(id=course_id)
    exam = Exam.objects.get(id=exam_id)
    if request.method == 'POST':
        entered = request.POST.get('input')
        if entered == exam.password:
            return redirect('/courses/' +  course_id + '/exams/' +
                    exam_id + '/t')
    return render(request, 'input_password.html', {'course': course,
        'exam': exam})

@user_passes_test(student_check)
def take_exam(request, course_id, exam_id):
    exam = Exam.objects.get(id=exam_id)
    try:
        referer = request.META['HTTP_REFERER']
        if ((reverse('input_password', args=[course_id, exam_id]) in
            referer) or
            (reverse('take_exam', args=[course_id, exam_id]) in
            referer) or
            not exam.password):
            if (Participation.objects.filter(user=request.user, course=course_id)
                .exists()):
                course = Course.objects.get(id=course_id)
                exam_questions = ExamQuestion.objects.filter(exam=exam)
                if exam.active:
                    if Score.objects.filter(user=request.user, exam=exam).exists():
                        messages.error(request, 'Exam already taken!')
                        return redirect('/courses/' +  course_id + '/exams/' +
                            exam_id + '/s')
                    if request.method == 'POST':
                        correct = 0
                        for exam_quest in exam_questions:
                            try:
                                st_answer = StudentAnswer.objects.create(
                                    user=request.user, exam_question=exam_quest,
                                    answer=request.POST.get(str(exam_quest.question.id)))
                                if (st_answer.exam_question.question.choice_set.get(id=
                                    st_answer.answer).correct):
                                    correct += 1
                            except ObjectDoesNotExist:
                                continue;
                        score = Score.objects.create(user=request.user,
                            exam=exam, score=correct)
                        messages.success(request, 'Exam finished with ' +
                            str(correct) + ' correct answers!')
                        return redirect('/courses/' +  course_id + '/exams/' +
                            exam_id + '/s')
                    return render(request, 'take_exam.html', {'course': course,
                        'exam': exam, 'exam_questions': exam_questions})
                messages.error(request, 'Exam inactive!')
                return redirect('/courses/' +  course_id + '/exams/' + exam_id + '/s')
            return redirect('/courses/s')
        return redirect('/courses/' +  course_id + '/exams/' +
            exam_id + '/p')
    except KeyError:
        return redirect('/courses/' +  course_id + '/exams/' +
            exam_id + '/p')


@user_passes_test(student_check)
def view_result(request, course_id, exam_id):
    if (Participation.objects.filter(user=request.user, course=course_id)
        .exists() and Score.objects.filter(user=request.user, exam=exam_id)
        .exists()):
        course = Course.objects.get(id=course_id)
        exam = Exam.objects.get(id=exam_id)
        exam_questions = ExamQuestion.objects.filter(exam=exam)
        score = Score.objects.get(user=request.user, exam=exam).score
        result = format_score(score, exam_questions.count())
        answers = {}
        for exam_question in exam_questions:
            answers[exam_question] = StudentAnswer.objects.get(user=
                request.user, exam_question=exam_question).answer
        return render(request, 'view_result.html', {'course': course,
            'exam': exam, 'exam_questions': exam_questions, 'result': result,
            'answers': answers})
    return redirect('/courses/s')