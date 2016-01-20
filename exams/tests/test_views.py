from django.core.urlresolvers import resolve, reverse
from django.test import TestCase
from django.utils import timezone

from courses.models import Course
from exams.models import Exam
from exams.views import create_exam, edit_exam, list_exams, view_scores
from exams.views import view_assigned, view_exam, take_exam, view_questions

class ExamsViewsTest(TestCase):

    def test_url_resolves_to_exam_creation(self):
        found = resolve('/courses/1/exams/create')
        self.assertEqual(found.func, create_exam)

    def test_create_exam_correct_arguments_and_template(self):
        course = Course.objects.create(name='Example name')
        url = reverse('create_exam', args=[course.id])
        self.assertEqual(url, '/courses/1/exams/create')
        self.assertTemplateUsed('create_exam.html')

    def test_url_resolves_to_exam_edit(self):
        found = resolve('/courses/8/exams/10')
        self.assertEqual(found.func, edit_exam)

    def test_edit_exam_correct_arguments_and_template(self):
        course = Course.objects.create(name='Example name')
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
        course = Course.objects.create(name='Example name')
        url = reverse('list_exams', args=[course.id])
        self.assertEqual(url, '/courses/1/exams/')
        self.assertTemplateUsed('list_exams.html')

    def test_url_resolves_to_score_viewing(self):
        found = resolve('/courses/1/exams/1/scores')
        self.assertEqual(found.func, view_scores)

    def test_view_scores_correct_arguments_and_template(self):
        course = Course.objects.create(name='Example name')
        exam = Exam.objects.create(name='Example', time_limit='00:10',
            course=course, active_from=timezone.now(),
            active_to=timezone.now(), question_count=2)
        url = reverse('view_scores', args=[course.id, exam.id])
        self.assertEqual(url, '/courses/1/exams/1/scores')
        self.assertTemplateUsed('view_scores.html')

    def test_url_resolves_to_viewing_assigned_questions(self):
        found = resolve('/courses/1/exams/1/questions')
        self.assertEqual(found.func, view_assigned)

    def test_view_assigned_correct_arguments_and_template(self):
        course = Course.objects.create(name='Example name')
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
        course = Course.objects.create(name='Example name')
        exam = Exam.objects.create(name='Example', time_limit='00:10',
            course=course, active_from=timezone.now(),
            active_to=timezone.now(), question_count=2)
        url = reverse('view_exam', args=[course.id, exam.id])
        self.assertEqual(url, '/courses/1/exams/1/s')
        self.assertTemplateUsed('view_exam.html')

    def test_url_resolves_to_take_exam(self):
        found = resolve('/courses/1/exams/1/take')
        self.assertEqual(found.func, take_exam)

    def test_take_exam_correct_arguments_and_template(self):
        course = Course.objects.create(name='Example name')
        exam = Exam.objects.create(name='Example', time_limit='00:10',
            course=course, active_from=timezone.now(),
            active_to=timezone.now(), question_count=2)
        url = reverse('take_exam', args=[course.id, exam.id])
        self.assertEqual(url, '/courses/1/exams/1/take')
        self.assertTemplateUsed('take_exam.html')

    def test_url_resolves_to_view_result(self):
        found = resolve('/courses/1/exams/1/questions/s')
        self.assertEqual(found.func, view_questions)
   
    def test_view_exam_result_correct_arguments_and_template(self):
        course = Course.objects.create(name='Example name')
        exam = Exam.objects.create(name='Example', time_limit='00:10',
            course=course, active_from=timezone.now(),
            active_to=timezone.now(), question_count=2)
        url = reverse('view_questions', args=[course.id, exam.id])
        self.assertEqual(url, '/courses/1/exams/1/questions/s')
        self.assertTemplateUsed('view_questions.html')