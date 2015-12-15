import unittest

from django.test import TestCase

from teachers.forms import CreateForm

class CreateFormTest(TestCase):

	def test_if_valid_on_all_required_fields(self):
		form_data = {'name': 'Example name', 'description': 'Example description'}
		form = CreateForm(data=form_data)
		self.assertTrue(form.is_valid())

	def test_if_valid_on_empty_description(self):
		form_data = {'name': 'Example name', 'description': ''}
		form = CreateForm(data=form_data)
		self.assertTrue(form.is_valid())	

	def test_if_not_valid_on_empty_name(self):
		form_data = {'name': '', 'description': ''}
		form = CreateForm(data=form_data)
		self.assertFalse(form.is_valid())	