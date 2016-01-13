from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase

from users.models import User
from users.forms import AuthenticationForm, RegistrationForm
from users.views import home_page, login, signup, confirm


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_uses_correct_template(self):
        request = HttpRequest()
        response_home = home_page(request)
        self.assertTemplateUsed('home.html')


class SignupTest(TestCase):

    def test_signup_response(self):
        response = self.client.get('/signup')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Sign up')
        response = self.client.post('/signup', {'username': 'test',
            'password': 'test'})
        self.assertEqual(response.status_code, 200)

    def test_url_resolves_to_signup_page(self):
        found = resolve('/signup')
        self.assertEqual(found.func, signup)

    def test_signup_correct_template(self):
        request = HttpRequest()
        response_signup = signup(request)
        self.assertTemplateUsed('signup.html')

    def test_signup_registration_form(self):
        response = self.client.get('/signup')
        self.assertIsInstance(response.context['form'], RegistrationForm)


class LoginTest(TestCase):

    def test_login_response(self):
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Log in')
        response = self.client.post('/login', {'username': 'test',
            'password': 'test'})
        self.assertEqual(response.status_code, 200)

    def test_url_resolves_to_login_page(self):
        found = resolve('/login')
        self.assertEqual(found.func, login)

    def test_login_correct_template(self):
        request = HttpRequest()
        response_login = login(request)
        self.assertTemplateUsed('login.html')

    def test_login_authentication_form(self):
        response = self.client.get('/login')
        self.assertIsInstance(response.context['form'], AuthenticationForm)


class ConfirmTest(TestCase):

    def test_confirm_response_fails(self):
        response = self.client.get('/confirm?q=example')
        self.assertEqual(response.status_code, 404)