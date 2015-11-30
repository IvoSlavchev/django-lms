from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

from users.views import home_page, teacher_page, student_page

class HomePageTest(TestCase):

	def test_root_url_resolves_to_home_page_view(self):
		found = resolve('/')
		self.assertEqual(found.func, home_page)

	def test_home_page_returns_correct_html(self):
		request = HttpRequest()
		response = home_page(request)
		expected_html = render_to_string('home.html')
		self.assertEqual(response.content.decode(), expected_html)

class TeacherAndStudentPagesTest(TestCase):

	def test_url_resolves_to_correct_page_view(self):
		teacher = resolve('/users/teacher_page.html')
		self.assertEqual(teacher.func, teacher_page)

		student = resolve('/users/student_page.html')
		self.assertEqual(student.func, student_page)

	def test_pages_return_correct_html(self):
		request = HttpRequest()
		response_teacher = teacher_page(request)
		expected_html = render_to_string('teacher_page.html')
		self.assertEqual(response_teacher.content.decode(), expected_html)

		response_student = student_page(request)
		expected_html = render_to_string('student_page.html')
		self.assertEqual(response_student.content.decode(), expected_html)