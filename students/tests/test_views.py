from django.core.urlresolvers import resolve
from django.test import TestCase

from students.views import dashboard, view_course

class StudentDashboardTest(TestCase):

	def test_url_resolves_to_student_dashboard(self):
		found = resolve('/students/')
		self.assertEqual(found.func, dashboard)

	def test_url_resolves_to_course_view(self):
		found = resolve('/students/1/')
		self.assertEqual(found.func, view_course)