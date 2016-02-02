from django.contrib.auth.models import AnonymousUser
from django.core.urlresolvers import resolve, reverse
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase, RequestFactory

from courses.models import Course
from courses.views import teacher_courses, student_courses, create_course
from courses.views import edit_course, edit_participants, view_course_results
from courses.views import view_course
from users.models import User


class CoursesTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_url_resolves_to_teacher_courses(self):
        found = resolve('/courses/')
        self.assertEqual(found.func, teacher_courses)

    def test_teacher_courses_correct_template(self):
        request = HttpRequest()
        request.user = User.objects.create(is_teacher=True)
        response_teacher_courses = teacher_courses(request)
        render_to_string('teacher_courses.html')

    def test_anonymous_doesnt_pass_teacher_test(self): 
        request = self.factory.get('/courses/')
        request.user = AnonymousUser()
        response = teacher_courses(request)
        self.assertEqual(response.status_code, 302)

    def test_teacher_passes_test(self): 
        request = self.factory.get('/courses/')
        request.user = User.objects.create(is_teacher=True)
        response = teacher_courses(request)
        self.assertEqual(response.status_code, 200)

    def test_student_doesnt_pass_teacher_test(self): 
        request = self.factory.get('/courses/')
        request.user = User.objects.create(is_teacher=False)
        response = teacher_courses(request)
        self.assertEqual(response.status_code, 302)

    def test_url_resolves_to_course_creation(self):
        found = resolve('/courses/create')
        self.assertEqual(found.func, create_course)

    def test_create_course_correct_template(self):
        request = HttpRequest()
        request.user = User.objects.create(is_teacher=True)
        response_create_course = create_course(request)
        self.assertTemplateUsed('create_course.html')

    def test_url_resolves_to_course_edit(self):
        found = resolve('/courses/8')
        self.assertEqual(found.func, edit_course)

    def test_edit_course_correct_arguments_and_template(self):
        user = User.objects.create(username='Example teacher')
        course = Course.objects.create(name='Example name', owner=user)
        url = reverse('edit_course', args=[course.id])
        self.assertEqual(url, '/courses/1')
        self.assertTemplateUsed('edit_course.html')

    def test_url_resolves_to_participants_edit(self):
        found = resolve('/courses/1/participants')
        self.assertEqual(found.func, edit_participants)

    def test_edit_participants_correct_arguments_and_template(self):
        user = User.objects.create(username='Example teacher')
        course = Course.objects.create(name='Example name', owner=user)
        url = reverse('edit_participants', args=[course.id])
        self.assertEqual(url, '/courses/1/participants')
        self.assertTemplateUsed('edit_course.html')

    def test_url_resolves_to_course_results_viewing(self):
        found = resolve('/courses/1/results')
        self.assertEqual(found.func, view_course_results)

    def test_results_viewing_correct_arguments_and_template(self):
        user = User.objects.create(username='Example teacher')
        course = Course.objects.create(name='Example name', owner=user)
        url = reverse('view_course_results', args=[course.id])
        self.assertEqual(url, '/courses/1/results')
        self.assertTemplateUsed('view_course_results.html')

    def test_url_resolves_to_student_courses(self):
        found = resolve('/courses/s')
        self.assertEqual(found.func, student_courses)

    def test_student_courses_correct_template(self):
        request = HttpRequest()
        user = User.objects.create(username='Example teacher')
        course = Course.objects.create(name='Example name', owner=user)
        request.user = User.objects.create(is_teacher=False)
        response_student_courses = student_courses(request)
        self.assertTemplateUsed('student_courses.html')

    def test_anonymous_doesnt_pass_student_test(self):
        request = self.factory.get('/courses/s')
        request.user = AnonymousUser()
        response = student_courses(request)
        self.assertEqual(response.status_code, 302)

    def test_student_passes_test(self): 
        request = self.factory.get('/courses/s')
        request.user = User.objects.create(is_teacher=False)
        response = student_courses(request)
        self.assertEqual(response.status_code, 200)

    def test_teacher_doesnt_pass_student_test(self): 
        request = self.factory.get('/courses/s')
        request.user = User.objects.create(is_teacher=True)
        response = student_courses(request)
        self.assertEqual(response.status_code, 302)

    def test_url_resolves_to_course_view(self):
        found = resolve('/courses/1/s')
        self.assertEqual(found.func, view_course)

    def test_course_viewing_correct_arguments_and_template(self):
        user = User.objects.create(username='Example teacher')
        course = Course.objects.create(name='Example name', owner=user)
        url = reverse('view_course', args=[course.id])
        self.assertEqual(url, '/courses/1/s')
        self.assertTemplateUsed('view_course.html')