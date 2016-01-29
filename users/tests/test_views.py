from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase

from users.models import User
from users.forms import AuthenticationForm, RegistrationForm
from users.views import home, signup, confirm


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home)

    def test_home_uses_correct_template(self):
        request = HttpRequest()
        request.user = User.objects.create(is_teacher=True)
        response_home = home(request)
        self.assertTemplateUsed('home.html')

    def test_home_response(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Log in')
        response = self.client.post('/', {'username': 'test',
            'password': 'test'})
        self.assertEqual(response.status_code, 200)
        response = self.client.post('/', {'username': 'test@test.bg',
            'password': 'test'})
        self.assertEqual(response.status_code, 200)

    def test_home_authentication_form(self):
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], AuthenticationForm)


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
        request.user = User.objects.create(is_teacher=True)
        response_signup = signup(request)
        self.assertTemplateUsed('signup.html')

    def test_signup_registration_form(self):
        response = self.client.get('/signup')
        self.assertIsInstance(response.context['form'], RegistrationForm)


class ConfirmTest(TestCase):

    def test_confirm_response_fails(self):
        response = self.client.get('/confirm?q=example')
        self.assertEqual(response.status_code, 404)