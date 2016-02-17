from django import forms

from markitup.widgets import MarkItUpWidget

from questions.models import Question, Choice


class QuestionForm(forms.ModelForm):

    name = forms.CharField(label="Question title", max_length=30)
    category = forms.CharField(max_length=30)
    question_text = forms.CharField(widget=MarkItUpWidget())

    class Meta:
        model = Question
        fields = ['name', 'category', 'question_text']

    def __init__(self, instance=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if instance:
            self.instance.question = instance
            self.initial['name'] = instance.name
            self.initial['category'] = instance.category
            self.initial['question_text'] = instance.question_text


class ChoiceForm(forms.ModelForm):

    choice_text = forms.CharField(max_length=30)
    correct = forms.BooleanField(label='', required=False,
        widget=forms.RadioSelect(choices=[(True, 'Correct')]))

    class Meta:
        model = Choice
        fields = ['choice_text', 'correct']

    def __init__(self, instance=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if instance:
            self.instance.choice = instance
            self.initial['choice_text'] = instance.choice_text
            self.initial['correct'] = instance.correct