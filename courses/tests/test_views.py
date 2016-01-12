from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase, RequestFactory

from courses.forms import CourseForm, ParticipantsForm
from courses.models import Course
from courses.views import teacher_page, student_page, create_course
from courses.views import edit_course, edit_participants, view_scores
from courses.views import view_course
from users.models import User


class CoursesTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_url_resolves_to_teacher_page(self):
        found = resolve('/courses/')
        self.assertEqual(found.func, teacher_page)

    def test_teacher_page_correct_template(self):
        request = HttpRequest()
        request.user = User.objects.create(is_teacher=True)
        response_teacher_page = teacher_page(request)
        with self.assertTemplateUsed('teacher_page.html'):
            render_to_string('teacher_page.html')

    def test_anonymous_doesnt_pass_teacher_test(self):
        with self.assertRaises(AttributeError):
            self.client.get('/courses/')

    def test_teacher_passes_test(self): 
        request = self.factory.get('/courses/')
        request.user = User.objects.create(is_teacher=True)
        response = teacher_page(request)
        self.assertEqual(response.status_code, 200)

    def test_student_doesnt_pass_teacher_test(self): 
        request = self.factory.get('/courses/')
        request.user = User.objects.create(is_teacher=False)
        response = teacher_page(request)
        self.assertEqual(response.status_code, 302)

    def test_url_resolves_to_course_creation(self):
        found = resolve('/courses/create')
        self.assertEqual(found.func, create_course)

    def test_create_course_correct_template(self):
        request = HttpRequest()
        request.user = User.objects.create(is_teacher=True)
        response_create_course = create_course(request)
        with self.assertTemplateUsed('create_course.html'):
            render_to_string('create_course.html')

    def test_url_resolves_to_course_edit(self):
        found = resolve('/courses/8')
        self.assertEqual(found.func, edit_course)

    def test_url_resolves_to_participants_edit(self):
        found = resolve('/courses/8/participants')
        self.assertEqual(found.func, edit_participants)

    def test_url_resolves_to_score_viewing(self):
        found = resolve('/courses/8/scores')
        self.assertEqual(found.func, view_scores)

    def test_url_resolves_to_student_page(self):
        found = resolve('/courses/s')
        self.assertEqual(found.func, student_page)

    def test_student_page_correct_template(self):
        request = HttpRequest()
        request.user = User.objects.create(is_teacher=False)
        response_student_page = student_page(request)
        with self.assertTemplateUsed('student_page.html'):
            render_to_string('student_page.html')

    def test_anonymous_doesnt_pass_student_test(self):
        with self.assertRaises(AttributeError):
            self.client.get('/courses/s')

    def test_student_passes_test(self): 
        request = self.factory.get('/courses/s')
        request.user = User.objects.create(is_teacher=False)
        response = student_page(request)
        self.assertEqual(response.status_code, 200)

    def test_teacher_doesnt_pass_student_test(self): 
        request = self.factory.get('/courses/s')
        request.user = User.objects.create(is_teacher=True)
        response = student_page(request)
        self.assertEqual(response.status_code, 302)

    def test_url_resolves_to_course_view(self):
        found = resolve('/courses/8/s')
        self.assertEqual(found.func, view_course)