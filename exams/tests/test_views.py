from django.core.urlresolvers import resolve
from django.test import TestCase

from exams.views import create_exam, edit_exam, list_exams, view_scores
from exams.views import view_exam, take_exam, view_result

class ExamsViewsTest(TestCase):

    def test_url_resolves_to_exam_creation(self):
        found = resolve('/courses/8/exams/create')
        self.assertEqual(found.func, create_exam)

    def test_url_resolves_to_exam_edit(self):
        found = resolve('/courses/8/exams/10')
        self.assertEqual(found.func, edit_exam)

    def test_url_resolves_to_exam_listing(self):
        found = resolve('/courses/27/exams/')
        self.assertEqual(found.func, list_exams)

    def test_url_resolves_to_score_viewing(self):
        found = resolve('/courses/27/exams/11/scores')
        self.assertEqual(found.func, view_scores)

    def test_url_resolves_to_exam_view(self):
        found = resolve('/courses/8/exams/10/s')
        self.assertEqual(found.func, view_exam)

    def test_url_resolves_to_take_exam(self):
        found = resolve('/courses/27/exams/11/take')
        self.assertEqual(found.func, take_exam)

    def test_url_resolves_to_view_result(self):
        found = resolve('/courses/27/exams/11/result')
        self.assertEqual(found.func, view_result)