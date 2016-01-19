import datetime

from django.test import TestCase
from django.utils import timezone

from courses.models import Course
from exams.models import Exam


class ExamModelTest(TestCase):

	def test_active_in_range(self):
		course = Course.objects.create(name='Example name')
		exam = Exam.objects.create(name='Example', time_limit='00:10',
			course=course, active_from=timezone.now(),
			active_to=timezone.now()+datetime.timedelta(1), question_count=2)
		self.assertTrue(exam.active)

	def test_inactive_outside_range(self):
		course = Course.objects.create(name='Example name')
		exam = Exam.objects.create(name='Example', time_limit='00:10',
			course=course, active_from=timezone.now()-datetime.timedelta(1),
			active_to=timezone.now(), question_count=2)
		self.assertFalse(exam.active)