from django import forms
from django.core.exceptions import ValidationError

from teachers.models import Course

class CreateForm(forms.ModelForm):

	name = forms.CharField(label="Title")
	description = forms.Textarea()

	class Meta:
		model = Course
		fields = ['name', 'description']
		
class ExistingCourseForm(CreateForm):

    def __init__(self, for_course, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.course = for_course

    def validate_unique(self):
        try:
            self.instance.validate_unique()
        except ValidationError as e:
            e.error_dict = {'name': "A course with this name already exists."}
            self._update_errors(e)