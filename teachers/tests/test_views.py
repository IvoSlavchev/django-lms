from django.core.urlresolvers import resolve
from django.test import TestCase

from teachers.views import dashboard, create, edit_course

class TeacherDashboardTest(TestCase):

	def test_url_resolves_to_teacher_dashboard(self):
		found = resolve('/teachers/')
		self.assertEqual(found.func, dashboard)

	def test_url_resolves_to_course_creation(self):
		found = resolve('/teachers/create/')
		self.assertEqual(found.func, create)

	def test_url_resolves_to_course_edit(self):
		found = resolve('/teachers/1/')
		self.assertEqual(found.func, edit_course)