from django.core.urlresolvers import resolve, reverse
from django.test import TestCase

from courses.models import Course
from questions.forms import QuestionForm
from questions.models import Question
from questions.views import create_question, edit_question, list_questions
from users.models import User


class QuestionsViewsTest(TestCase):

    def test_url_resolves_to_question_creation(self):
        found = resolve('/courses/1/questions/create')
        self.assertEqual(found.func, create_question)

    def test_create_question_correct_arguments_and_template(self):
        user = User.objects.create(username='Example teacher')
        course = Course.objects.create(name='Example name', owner=user)
        url = reverse('create_question', args=[course.id])
        self.assertEqual(url, '/courses/1/questions/create')
        self.assertTemplateUsed('create_question.html')

    def test_valid_question_form(self):
        data = {
            'name': 'Example name',
            'category': 'Examples',
            'question_text': 'Example text'
        }
        form = QuestionForm(data=data)
        self.assertTrue(form.is_valid())

    def test_question_creation_on_POST(self):
        user = User.objects.create(username='Example teacher')
        course = Course.objects.create(name='Example name', owner=user)
        data = {
            'name': 'Example name',
            'category': 'Examples',
            'question_text': 'Example text'
        }
        form = QuestionForm(data=data)
        question = form.save(commit=False)
        question.course = course
        question.save()
        self.assertEqual(Question.objects.count(), 1)

    def test_url_resolves_to_question_edit(self):
        found = resolve('/courses/1/questions/1')
        self.assertEqual(found.func, edit_question)

    def test_edit_question_correct_arguments_and_template(self):
        user = User.objects.create(username='Example teacher')
        course = Course.objects.create(name='Example name', owner=user)
        question = Question.objects.create(name='Example question',
        	category='Examples', course=course, question_text='Example')
        url = reverse('edit_question', args=[course.id, question.id])
        self.assertEqual(url, '/courses/1/questions/1')
        self.assertTemplateUsed('edit_question.html')

    def test_url_resolves_to_question_listing(self):
        found = resolve('/courses/1/questions/')
        self.assertEqual(found.func, list_questions)

    def test_list_questions_correct_arguments_and_template(self):
        user = User.objects.create(username='Example teacher')
        course = Course.objects.create(name='Example name', owner=user)
        url = reverse('list_questions', args=[course.id])
        self.assertEqual(url, '/courses/1/questions/')
        self.assertTemplateUsed('list_questions.html')