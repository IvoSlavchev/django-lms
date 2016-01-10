from django.core.urlresolvers import resolve
from django.test import TestCase

from questions.views import create_question, edit_question, list_questions


class QuestionsViewsTest(TestCase):

    def test_url_resolves_to_question_creation(self):
        found = resolve('/courses/27/questions/create')
        self.assertEqual(found.func, create_question)

    def test_url_resolves_to_question_edit(self):
        found = resolve('/courses/27/questions/18')
        self.assertEqual(found.func, edit_question)

    def test_url_resolves_to_question_listing(self):
        found = resolve('/courses/27/questions/')
        self.assertEqual(found.func, list_questions)