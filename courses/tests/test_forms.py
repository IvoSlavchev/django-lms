from django.test import TestCase

from courses.forms import CourseForm, ParticipantsForm

class CourseFormTest(TestCase):

    def test_if_valid_on_all_required_fields(self):
        form_data = {'name': 'Example name', 
            'description': 'Example description'}
        form = CourseForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_if_valid_on_empty_description(self):
        form_data = {'name': 'Example name', 'description': ''}
        form = CourseForm(data=form_data)
        self.assertTrue(form.is_valid())
        
    def test_if_not_valid_on_empty_name(self):
        form_data = {'name': '', 'description': ''}
        form = CourseForm(data=form_data)
        self.assertFalse(form.is_valid())


class ParticipantsFormTest(TestCase):
    
    def test_if_not_valid_on_only_participants(self):
        form_data = {'participants': '1'}
        form = ParticipantsForm(data=form_data)
        self.assertFalse(form.is_valid())