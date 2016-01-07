from django.core.urlresolvers import resolve
from django.test import TestCase

from courses.views import teacher_page, student_page, create_course, edit_course, edit_participants, view_scores
from courses.views import view_course

class CoursesViewsTest(TestCase):

	def test_url_resolves_to_teacher_page(self):
		found = resolve('/courses/')
		self.assertEqual(found.func, teacher_page)

	def test_url_resolves_to_course_creation(self):
		found = resolve('/courses/create')
		self.assertEqual(found.func, create_course)

	def test_url_resolves_to_course_edit(self):
		found = resolve('/courses/8')
		self.assertEqual(found.func, edit_course)

	def test_url_resolves_to_participants_edit(self):
		found = resolve('/courses/8/participants')
		self.assertEqual(found.func, edit_participants)

	def test_url_resolves_to_score_viewing(self):
		found = resolve('/courses/8/scores')
		self.assertEqual(found.func, view_scores)

	def test_url_resolves_to_student_page(self):
		found = resolve('/courses/s')
		self.assertEqual(found.func, student_page)

	def test_url_resolves_to_course_view(self):
		found = resolve('/courses/8/s')
		self.assertEqual(found.func, view_course)