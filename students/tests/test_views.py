from django.core.urlresolvers import resolve
from django.test import TestCase

from students.views import dashboard

class StudentDashboardTest(TestCase):

	def test_url_resolves_to_student_dashboard(self):
		found = resolve('/students/')
		self.assertEqual(found.func, dashboard)