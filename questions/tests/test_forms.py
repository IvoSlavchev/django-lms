from django.test import TestCase

from questions.forms import QuestionForm, ChoiceForm


class QuestionFormTest(TestCase):

    def test_if_valid_on_all_required_fields(self):
        form_data = {'name': 'Example name', 'category': 'Examples',
            'question_text': 'Example question text'}
        form = QuestionForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_if_not_valid_on_empty_name(self):
        form_data = {'name': '', 'category': 'Examples',
            'question_text': 'Example question text'}
        form = QuestionForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_if_not_valid_on_empty_category(self):
        form_data = {'name': 'Example name', 'category': '',
            'question_text': 'Example question text'}
        form = QuestionForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_if_not_valid_on_empty_question_text(self):
        form_data = {'name': 'Example name', 'category': 'Examples',
            'question_text': ''}
        form = QuestionForm(data=form_data)
        self.assertFalse(form.is_valid())

class ChoiceFormTest(TestCase):

    def test_if_valid_on_all_fields(self):
        form_data = {'choice_text': 'Example choice text', 'correct': True}
        form = ChoiceForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_if_valid_on_empty_correct(self):
        form_data = {'choice_text': 'Example choice text', 'correct': ''}
        form = ChoiceForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_if_not_valid_on_empty_choice_text(self):
        form_data = {'choice_text': '', 'correct': ''}
        form = ChoiceForm(data=form_data)
        self.assertFalse(form.is_valid())