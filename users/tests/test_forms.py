from django.test import TestCase

from users.forms import RegistrationForm, AuthenticationForm


class RegistrationFormTest(TestCase):

    def test_if_valid_on_all_required_fields(self):
        form_data = {'username': 'example', 'email': 'example@example.com',
            'is_teacher': False, 'password1': 'example',
            'password2': 'example'}
        form = RegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_if_not_valid_on_different_passwords(self):
        form_data = {'username': 'example', 'email': 'example@example.com',
            'is_teacher': True, 'password1': 'example',
            'password2': 'example2'}
        form = RegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_if_not_valid_on_empty_field(self):
        form_data = {'username': '', 'email': 'example@example.com',
            'is_teacher': False, 'password1': 'example',
            'password2': 'example'}
        form = RegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())


class AuthenticationFormTest(TestCase):

    def test_if_valid_on_all_fields(self):
        form_data = {'username': 'example', 'is_teacher': True,
            'password': 'example'}
        form = AuthenticationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_if_valid_on_empty_is_teacher(self):
        form_data = {'username': 'example', 'is_teacher': '',
            'password': 'example'}
        form = AuthenticationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_if_not_valid_on_empty_field_except_is_teacher(self):
        form_data = {'username': 'example', 'password': ''}
        form = AuthenticationForm(data=form_data)
        self.assertFalse(form.is_valid())