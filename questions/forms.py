from django import forms

from questions.models import Question, Choice


class QuestionForm(forms.ModelForm):

	name = forms.CharField(label="Question title", max_length=30)
	question_text = forms.Textarea()

	class Meta:
		model = Question
		fields = ['name', 'question_text']

	def __init__(self, instance=None, *args, **kwargs):
		super().__init__(*args, **kwargs)
		if instance:
			self.instance.question = instance
			self.initial['name'] = instance.name
			self.initial['question_text'] = instance.question_text


class ChoiceForm(forms.ModelForm):

	choice_text = forms.CharField(max_length=30)
	correct = forms.BooleanField(required=False)

	class Meta:
		model = Choice
		fields = ['choice_text', 'correct']

	def __init__(self, instance=None, *args, **kwargs):
		super().__init__(*args, **kwargs)
		if instance:
			self.instance.choice = instance
			self.initial['choice_text'] = instance.choice_text
			self.initial['correct'] = instance.correct