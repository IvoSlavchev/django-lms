from django.core.urlresolvers import resolve, reverse
from django.test import TestCase
from django.utils import timezone

from courses.models import Course
from exams.models import Exam
from exams.views import create_exam, edit_exam, list_exams, view_exam_results
from exams.views import view_participant_result, view_assigned, view_exam
from exams.views import take_exam, view_result, input_password
from users.models import User

class ExamsViewsTest(TestCase):

    def test_url_resolves_to_exam_creation(self):
        found = resolve('/courses/1/exams/create')
        self.assertEqual(found.func, create_exam)

    def test_create_exam_correct_arguments_and_template(self):
        user = User.objects.create(username='Example teacher')
        course = Course.objects.create(name='Example name', owner=user)
        url = reverse('create_exam', args=[course.id])
        self.assertEqual(url, '/courses/1/exams/create')
        self.assertTemplateUsed('create_exam.html')

    def test_url_resolves_to_exam_edit(self):
        found = resolve('/courses/8/exams/10')
        self.assertEqual(found.func, edit_exam)

    def test_edit_exam_correct_arguments_and_template(self):
        user = User.objects.create(username='Example teacher')
        course = Course.objects.create(name='Example name', owner=user)
        exam = Exam.objects.create(name='Example', time_limit='00:10',
            course=course, active_from=timezone.now(),
            active_to=timezone.now(), question_count=2)
        url = reverse('edit_exam', args=[course.id, exam.id])
        self.assertEqual(url, '/courses/1/exams/1')
        self.assertTemplateUsed('edit_exam.html')

    def test_url_resolves_to_exam_listing(self):
        found = resolve('/courses/1/exams/')
        self.assertEqual(found.func, list_exams)

    def test_list_exams_correct_arguments_and_template(self):
        user = User.objects.create(username='Example teacher')
        course = Course.objects.create(name='Example name', owner=user)
        url = reverse('list_exams', args=[course.id])
        self.assertEqual(url, '/courses/1/exams/')
        self.assertTemplateUsed('list_exams.html')

    def test_url_resolves_to__exam_results_viewing(self):
        found = resolve('/courses/1/exams/1/results')
        self.assertEqual(found.func, view_exam_results)

    def test_view_exam_results_correct_arguments_and_template(self):
        user = User.objects.create(username='Example teacher')
        course = Course.objects.create(name='Example name', owner=user)
        exam = Exam.objects.create(name='Example', time_limit='00:10',
            course=course, active_from=timezone.now(),
            active_to=timezone.now(), question_count=2)
        url = reverse('view_exam_results', args=[course.id, exam.id])
        self.assertEqual(url, '/courses/1/exams/1/results')
        self.assertTemplateUsed('view_exam_results.html')

    def test_url_resolves_to_viewing_participant_result(self):
        found = resolve('/courses/1/exams/1/result/1')
        self.assertEqual(found.func, view_participant_result)

    def test_participant_result_correct_arguments_and_template(self):
        user = User.objects.create(username='Example teacher')
        course = Course.objects.create(name='Example name', owner=user)
        exam = Exam.objects.create(name='Example', time_limit='00:10',
            course=course, active_from=timezone.now(),
            active_to=timezone.now(), question_count=2)
        user_student = User.objects.create(username='Example student')
        url = reverse('view_participant_result',
            args=[course.id, exam.id, user.id])
        self.assertEqual(url, '/courses/1/exams/1/result/1')
        self.assertTemplateUsed('view_participant_result.html')

    def test_url_resolves_to_viewing_assigned_questions(self):
        found = resolve('/courses/1/exams/1/questions')
        self.assertEqual(found.func, view_assigned)

    def test_view_assigned_correct_arguments_and_template(self):
        user = User.objects.create(username='Example teacher')
        course = Course.objects.create(name='Example name', owner=user)
        exam = Exam.objects.create(name='Example', time_limit='00:10',
            course=course, active_from=timezone.now(),
            active_to=timezone.now(), question_count=2)
        url = reverse('view_assigned', args=[course.id, exam.id])
        self.assertEqual(url, '/courses/1/exams/1/questions')
        self.assertTemplateUsed('view_questions.html')

    def test_url_resolves_to_exam_view(self):
        found = resolve('/courses/8/exams/10/s')
        self.assertEqual(found.func, view_exam)

    def test_view_exam_correct_arguments_and_template(self):
        user = User.objects.create(username='Example teacher')
        course = Course.objects.create(name='Example name', owner=user)
        exam = Exam.objects.create(name='Example', time_limit='00:10',
            course=course, active_from=timezone.now(),
            active_to=timezone.now(), question_count=2)
        url = reverse('view_exam', args=[course.id, exam.id])
        self.assertEqual(url, '/courses/1/exams/1/s')
        self.assertTemplateUsed('view_exam.html')

    def test_url_resolves_to_exam_password_input(self):
        found = resolve('/courses/1/exams/1/p')
        self.assertEqual(found.func, input_password)

    def test_input_password_correct_arguments_and_template(self):
        user = User.objects.create(username='Example teacher')
        course = Course.objects.create(name='Example name', owner=user)
        exam = Exam.objects.create(name='Example', time_limit='00:10',
            course=course, active_from=timezone.now(), password='test',
            active_to=timezone.now(), question_count=2)
        url = reverse('input_password', args=[course.id, exam.id])
        self.assertEqual(url, '/courses/1/exams/1/p')
        self.assertTemplateUsed('input_password.html')

    def test_url_resolves_to_take_exam(self):
        found = resolve('/courses/1/exams/1/t')
        self.assertEqual(found.func, take_exam)

    def test_take_exam_correct_arguments_and_template(self):
        user = User.objects.create(username='Example teacher')
        course = Course.objects.create(name='Example name', owner=user)
        exam = Exam.objects.create(name='Example', time_limit='00:10',
            course=course, active_from=timezone.now(),
            active_to=timezone.now(), question_count=2)
        url = reverse('take_exam', args=[course.id, exam.id])
        self.assertEqual(url, '/courses/1/exams/1/t')
        self.assertTemplateUsed('take_exam.html')

    def test_url_resolves_to_view_result(self):
        found = resolve('/courses/1/exams/1/result/s')
        self.assertEqual(found.func, view_result)
   
    def test_view_exam_result_correct_arguments_and_template(self):
        user = User.objects.create(username='Example teacher')
        course = Course.objects.create(name='Example name', owner=user)
        exam = Exam.objects.create(name='Example', time_limit='00:10',
            course=course, active_from=timezone.now(),
            active_to=timezone.now(), question_count=2)
        url = reverse('view_result', args=[course.id, exam.id])
        self.assertEqual(url, '/courses/1/exams/1/result/s')
        self.assertTemplateUsed('view_result.html')