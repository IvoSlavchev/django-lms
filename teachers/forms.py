from django import forms
from django.core.exceptions import ValidationError

from teachers.models import Course
from users.models import User

class CourseForm(forms.ModelForm):

	name = forms.CharField(label="Title")
	description = forms.Textarea()
	participants = forms.ModelMultipleChoiceField(required=False, queryset=User.objects.filter(is_teacher=False), 
		widget=forms.CheckboxSelectMultiple())

	class Meta:
		model = Course
		fields = ['name', 'description', 'participants']

	def __init__(self, for_course, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.instance.course = for_course