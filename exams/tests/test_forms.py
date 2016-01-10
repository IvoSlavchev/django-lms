from django.test import TestCase

from exams.forms import ExamForm


class ExamFormTest(TestCase):

    def test_if_valid_on_all_fields(self):
        form_data = {'name': 'Example name',
            'description': 'Example description', 'password': 'example',
            'time_limit': '00:10', 'active_from': '01/01/2016 10:00',
            'active_to': '10/10/2016 22:00'}
        form = ExamForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_if_valid_on_empty_description_and_password(self):
        form_data = {'name': 'Example name', 'description': '',
            'password': '', 'time_limit': '00:10',
            'active_from': '01/01/2016 10:00',
            'active_to': '10/10/2016 22:00'}
        form = ExamForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_if_not_valid_on_empty_name(self):
        form_data = {'name': '', 'description': '', 'password': 'example',
            'time_limit': '00:10', 'active_from': '01/01/2016 10:00',
            'active_to': '10/10/2016 22:00'}
        form = ExamForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_if_not_valid_on_empty_limit_and_dates(self):
        form_data = {'name': 'Example name', 'description': '',
            'password': 'example', 'time_limit': '', 'active_from': '',
            'active_to': ''}
        form = ExamForm(data=form_data)
        self.assertFalse(form.is_valid())