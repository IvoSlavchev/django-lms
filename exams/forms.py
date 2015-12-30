from django import forms

from exams.models import Exam, ExamQuestion
from questions.models import Question

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
		self.initial['name'] = instance.name
		self.initial['description'] = instance.description
		self.initial['date_to_be_taken'] = instance.date_to_be_taken

class ExamQuestionForm(forms.ModelForm):

	questions = forms.ModelMultipleChoiceField(required=False, queryset = None, widget=forms.CheckboxSelectMultiple())

	class Meta:
		model = Question
		fields = ['questions']

	def __init__(self, course, instance=None, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.instance.exam = instance
		self.fields['questions'].queryset = Question.objects.filter(course=course)
		self.initial['questions'] = [question.question for question in ExamQuestion.objects.filter(exam=instance)]