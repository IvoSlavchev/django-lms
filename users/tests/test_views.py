from django.core.urlresolvers import resolve, reverse
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from users.views import home_page, login, signup
from users.models import User
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

class LoginAndSignup(TestCase):

	def test_pages_return_correct_html(self):
		request = HttpRequest()
		response_login = login(request)
		expected_html = render_to_string('login.html')
		self.assertEqual(response_login.content.decode(), expected_html)

		response_signup = signup(request)
		expected_html = render_to_string('signup.html')
		self.assertEqual(response_login.content.decode(), expected_html)