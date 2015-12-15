from django.core.urlresolvers import resolve
from django.test import TestCase

from teachers.views import dashboard

class TeacherDashboardTest(TestCase):

	def test_url_resolves_to_student_dashboard(self):
		found = resolve('/teachers/')
		self.assertEqual(found.func, dashboard)