from django import forms

from courses.models import Course
from users.models import User

class CourseForm(forms.ModelForm):

	name = forms.CharField(label="Course name", max_length=30)
	description = forms.Textarea()

	class Meta:
		model = Course
		fields = ['name', 'description']

	def __init__(self, instance=None, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.instance.course = instance

class ParticipantsForm(forms.ModelForm):

	participants = forms.ModelMultipleChoiceField(required=False, queryset=User.objects.filter(is_teacher=False), 
		widget=forms.SelectMultiple())

	class Meta:
		model = Course
		fields = ['participants']

	def __init__(self, instance=None, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.instance.course = instance
