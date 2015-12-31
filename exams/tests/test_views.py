from django.core.urlresolvers import resolve
from django.test import TestCase

from exams.views import create_exam, edit_exam, edit_questions, list_exams, view_exam

class ExamsViewsTest(TestCase):

	def test_url_resolves_to_exam_creation(self):
		found = resolve('/courses/8/exams/create')
		self.assertEqual(found.func, create_exam)

	def test_url_resolves_to_exam_edit(self):
		found = resolve('/courses/8/exams/10')
		self.assertEqual(found.func, edit_exam)

	def test_url_resolves_to_edit_questions(self):
		found = resolve('/courses/27/exams/11/questions')
		self.assertEqual(found.func, edit_questions)

	def test_url_resolves_to_exam_view(self):
		found = resolve('/courses/8/exams/10/s')
		self.assertEqual(found.func, view_exam)

	def test_url_resolves_to_exam_listing(self):
		found = resolve('/courses/27/exams/')
		self.assertEqual(found.func, list_exams)