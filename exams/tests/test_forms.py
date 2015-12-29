from django.test import TestCase

from exams.forms import ExamForm

class ExamFormTest(TestCase):

	def test_if_valid_on_all_required_fields(self):
		form_data = {'name': 'Example name', 'description': 'Example description', 'date_to_be_taken': '10/10/2016 10:53'}
		form = ExamForm(data=form_data)
		self.assertTrue(form.is_valid())

	def test_if_valid_on_empty_description(self):
		form_data = {'name': 'Example name', 'description': '', 'date_to_be_taken': '10/10/2016 10:53'}
		form = ExamForm(data=form_data)
		self.assertTrue(form.is_valid())	

	def test_if_not_valid_on_empty_name(self):
		form_data = {'name': '', 'description': '', 'date_to_be_taken': '10/10/2016 10:53'}
		form = ExamForm(data=form_data)
		self.assertFalse(form.is_valid())	

	def test_if_not_valid_on_empty_date(self):
		form_data = {'name': 'Example name', 'description': '', 'date_to_be_taken': ''}
		form = ExamForm(data=form_data)
		self.assertFalse(form.is_valid())