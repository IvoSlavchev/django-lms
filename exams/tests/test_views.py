from django.core.urlresolvers import resolve
from django.test import TestCase

from exams.views import create_exam, edit_exam, view_exam

class ExamsViewsTest(TestCase):

	def test_url_resolves_to_exam_creation(self):
		found = resolve('/courses/7/exams/create')
		self.assertEqual(found.func, create_exam)

	def test_url_resolves_to_exam_edit(self):
		found = resolve('/courses/7/exams/1')
		self.assertEqual(found.func, edit_exam)

	def test_url_resolves_to_exam_view(self):
		found = resolve('/courses/7/exams/1/s')
		self.assertEqual(found.func, view_exam)