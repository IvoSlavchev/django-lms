from django import forms

from exams.models import Exam, ExamQuestion
from questions.models import Question

class ExamForm(forms.ModelForm):

	name = forms.CharField(label="Exam name", max_length=30)
	description = forms.Textarea()
	password = forms.CharField(label="Password (optional)", widget=forms.PasswordInput(), required=False)
	time_limit = forms.TimeField(widget=forms.TimeInput(format='%H:%M'), help_text=("Hours:Minutes"))
	active_from = forms.DateTimeField()
	active_to = forms.DateTimeField()

	class Meta:
		model = Exam
		fields = ['name', 'description', 'password', 'time_limit', 'active_from', 'active_to']

	def __init__(self, instance=None, *args, **kwargs):
		super().__init__(*args, **kwargs)
		if instance:
			self.instance.exam = instance
			self.initial['name'] = instance.name
			self.initial['description'] = instance.description
			self.initial['time_limit'] = instance.time_limit
			self.initial['active_from'] = instance.active_from
			self.initial['active_to'] = instance.active_to

class ExamQuestionForm(forms.ModelForm):

	questions = forms.ModelMultipleChoiceField(required=False, queryset = None, widget=forms.CheckboxSelectMultiple())

	class Meta:
		model = Question
		fields = ['questions']

	def __init__(self, course, instance=None, *args, **kwargs):
		super().__init__(*args, **kwargs)
		if instance:
			self.instance.exam = instance
			self.fields['questions'].queryset = Question.objects.filter(course=course)
			self.initial['questions'] = [question.question for question in ExamQuestion.objects.filter(exam=instance)]