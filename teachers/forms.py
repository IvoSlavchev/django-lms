from django import forms

from teachers.models import Course

class CreateForm(forms.ModelForm):

	name = forms.CharField(label="Title")
	description = forms.Textarea()

	class Meta:
		model = Course
		fields = ['name', 'description']