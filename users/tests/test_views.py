from django.core.urlresolvers import resolve, reverse
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase

from django.http import Http404

from users.models import User
from users.views import home_page, teacher_page, student_page, login, signup, confirm

User = User()

class HomePageTest(TestCase):

	def test_root_url_resolves_to_home_page_view(self):
		found = resolve('/')
		self.assertEqual(found.func, home_page)

	def test_home_page_returns_correct_html(self):
		request = HttpRequest()
		response = home_page(request)
		expected_html = render_to_string('home.html')
		self.assertEqual(response.content.decode(), expected_html)

class TeacherAndStudentPageTest(TestCase):

	def test_pages_raise_error_on_anonymous_user(self):
		request = HttpRequest()	
		with self.assertRaises(AttributeError):
			response_teacher = teacher_page(request)

		request = HttpRequest()
		with self.assertRaises(AttributeError):
			response_student = student_page(request)

class LoginAndSignup(TestCase):

	def test_signup_and_login_use_correct_template(self):
		request = HttpRequest()
		response_signup = signup(request)
		with self.assertTemplateUsed('signup.html'):
			render_to_string('signup.html')

		request = HttpRequest()
		response_login = login(request)
		with self.assertTemplateUsed('login.html'):
			render_to_string('login.html')

	def test_confirm_raises_404_error(self):
		request = HttpRequest()
		with self.assertRaises(Http404):
			response_confirm = confirm(request)