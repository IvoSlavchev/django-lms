from django.core.urlresolvers import resolve
from django.test import TestCase

from courses.views import teacher_page, student_page, create_course, edit_course, view_course

class TeacherDashboardTest(TestCase):

	def test_url_resolves_to_teacher_page(self):
		found = resolve('/courses/teacher/')
		self.assertEqual(found.func, teacher_page)

	def test_url_resolves_to_course_creation(self):
		found = resolve('/courses/teacher/create/')
		self.assertEqual(found.func, create_course)

	def test_url_resolves_to_course_edit(self):
		found = resolve('/courses/teacher/1/')
		self.assertEqual(found.func, edit_course)

	def test_url_resolves_to_student_page(self):
		found = resolve('/courses/student/')
		self.assertEqual(found.func, student_page)

	def test_url_resolves_to_course_view(self):
		found = resolve('/courses/student/1/')
		self.assertEqual(found.func, view_course)