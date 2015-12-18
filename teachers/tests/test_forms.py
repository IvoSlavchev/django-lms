import unittest

from django.test import TestCase

from teachers.forms import CourseForm

class CourseFormTest(TestCase):

	def test_if_valid_on_all_required_fields(self):
		form_data = {'name': 'Example name', 'description': 'Example description'}
		form = CourseForm(data=form_data, instance=None)
		self.assertTrue(form.is_valid())

	def test_if_valid_on_empty_description(self):
		form_data = {'name': 'Example name', 'description': ''}
		form = CreateForm(data=form_data, instance=None)
		self.assertTrue(form.is_valid())	

	def test_if_not_valid_on_empty_name(self):
		form_data = {'name': '', 'description': ''}
		form = CreateForm(data=form_data, instance=None)
		self.assertFalse(form.is_valid())	