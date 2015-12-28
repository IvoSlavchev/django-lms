from django import forms

from exams.models import Exam

class ExamForm(forms.ModelForm):

	name = forms.CharField(label="Exam name", max_length=30)
	description = forms.Textarea()
	date_to_be_taken = forms.DateTimeField()

	class Meta:
		model = Exam
		fields = ['name', 'description', 'date_to_be_taken']

	def __init__(self, instance=None, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.instance.exam = instance