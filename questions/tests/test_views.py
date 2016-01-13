from django.core.urlresolvers import resolve, reverse
from django.test import TestCase

from courses.models import Course
from questions.models import Question
from questions.views import create_question, edit_question, list_questions


class QuestionsViewsTest(TestCase):

    def test_url_resolves_to_question_creation(self):
        found = resolve('/courses/27/questions/create')
        self.assertEqual(found.func, create_question)

    def test_create_question_correct_arguments_and_template(self):
        course = Course.objects.create(name='Example name')
        url = reverse('create_question', args=[course.id])
        self.assertEqual(url, '/courses/1/questions/create')
        self.assertTemplateUsed('create_question.html')

    def test_url_resolves_to_question_edit(self):
        found = resolve('/courses/27/questions/18')
        self.assertEqual(found.func, edit_question)

    def test_edit_question_correct_arguments_and_template(self):
        course = Course.objects.create(name='Example name')
        question = Question.objects.create(name='Example question',
        	category='Examples', course=course, question_text='Example')
        url = reverse('edit_question', args=[course.id, question.id])
        self.assertEqual(url, '/courses/1/questions/1')
        self.assertTemplateUsed('edit_question.html')

    def test_url_resolves_to_question_listing(self):
        found = resolve('/courses/27/questions/')
        self.assertEqual(found.func, list_questions)

    def test_list_questions_correct_arguments_and_template(self):
        course = Course.objects.create(name='Example name')
        url = reverse('list_questions', args=[course.id])
        self.assertEqual(url, '/courses/1/questions/')
        self.assertTemplateUsed('list_questions.html')