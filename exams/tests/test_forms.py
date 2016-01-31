from django.test import TestCase

from courses.models import Course
from exams.forms import ExamForm
from questions.models import Question
from users.models import User


class ExamFormTest(TestCase):

    def test_if_valid_on_all_fields(self):
        user = User.objects.create(username='Example teacher')
        course = Course.objects.create(name='Example name', owner=user)
        question = Question.objects.create(name='Example name',
            category='Examples', question_text='Example', course=course)
        form_data = {'name': 'Example name',
            'description': 'Example description', 'password': 'example',
            'time_limit': '00:10', 'active_from': '2016/09/09 10:00',
            'active_to': '2016/10/10 22:00', 'category': 'Examples', 
            'question_count': '2'}
        form = ExamForm(data=form_data, course=course)
        self.assertTrue(form.is_valid())

    def test_if_valid_on_empty_description_and_password(self):
        user = User.objects.create(username='Example teacher')
        course = Course.objects.create(name='Example name', owner=user)
        question = Question.objects.create(name='Example name',
            category='Examples', question_text='Example', course=course)
        form_data = {'name': 'Example name', 'description': '',
            'password': '', 'time_limit': '00:10',
            'active_from': '2016/09/09 10:00',
            'active_to': '2016/10/10 22:00', 'category': 'Examples', 
            'question_count': '2'}
        form = ExamForm(data=form_data, course=course)
        self.assertTrue(form.is_valid())

    def test_if_not_valid_on_empty_name(self):
        user = User.objects.create(username='Example teacher')
        course = Course.objects.create(name='Example name', owner=user)
        question = Question.objects.create(name='Example name',
            category='Examples', question_text='Example', course=course)
        form_data = {'name': '', 'description': '', 'password': 'example',
            'time_limit': '00:10', 'active_from': '2016/09/09 10:00',
            'active_to': '2016/10/10 22:00', 'category': 'Examples', 
            'question_count': '2'}
        form = ExamForm(data=form_data, course=course)
        self.assertFalse(form.is_valid())

    def test_if_not_valid_on_empty_limit_and_dates(self):
        user = User.objects.create(username='Example teacher')
        course = Course.objects.create(name='Example name', owner=user)
        question = Question.objects.create(name='Example name',
            category='Examples', question_text='Example', course=course)
        form_data = {'name': 'Example name', 'description': '',
            'password': 'example', 'time_limit': '', 'active_from': '',
            'active_to': '', 'category': 'Examples', 
            'question_count': '2'}
        form = ExamForm(data=form_data, course=course)
        self.assertFalse(form.is_valid())

    def test_if_not_valid_on_empty_category_and_questions(self):
        user = User.objects.create(username='Example teacher')
        course = Course.objects.create(name='Example name', owner=user)
        question = Question.objects.create(name='Example name',
            category='Examples', question_text='Example', course=course)
        form_data = {'name': 'Example name', 'description': '',
            'password': 'example', 'time_limit': '00:10',
            'active_from': '2016/09/09 10:00', 'active_to': '2016/10/10 22:00',
            'category': '', 'question_count': ''}
        form = ExamForm(data=form_data, course=course)
        self.assertFalse(form.is_valid())

    def test_if_not_valid_on_reversed_dates(self):
        user = User.objects.create(username='Example teacher')
        course = Course.objects.create(name='Example name', owner=user)
        question = Question.objects.create(name='Example name',
            category='Examples', question_text='Example', course=course)
        form_data = {'name': 'Example name', 'description': '',
            'password': 'example', 'time_limit': '00:10',
            'active_from': '2016/10/10 10:00', 'active_to': '2016/09/09 22:00',
            'category': '', 'question_count': ''}
        form = ExamForm(data=form_data, course=course)
        self.assertFalse(form.is_valid())