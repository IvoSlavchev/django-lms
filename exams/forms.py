from django import forms

from exams.models import Exam, ExamQuestion
from questions.models import Question


class ExamForm(forms.ModelForm):

    name = forms.CharField(label="Exam name", max_length=30)
    description = forms.Textarea()
    password = forms.CharField(label="Password (optional)",
        widget=forms.PasswordInput(), required=False)
    time_limit = forms.TimeField(widget=forms.TimeInput(format='%H:%M'),
        help_text=("Hours:Minutes"))
    active_from = forms.DateTimeField()
    active_to = forms.DateTimeField()
    category = forms.CharField(max_length=30)
    question_count = forms.IntegerField(label="Number of questions")

    class Meta:
        model = Exam
        fields = ['name', 'description', 'password', 'time_limit',
            'active_from', 'active_to', 'category', 'question_count']

    def __init__(self, instance=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if instance:
            self.instance.exam = instance
            self.initial['name'] = instance.name
            self.initial['description'] = instance.description
            self.initial['time_limit'] = instance.time_limit
            self.initial['active_from'] = instance.active_from
            self.initial['active_to'] = instance.active_to
            self.initial['category'] = instance.category
            self.initial['question_count'] = instance.question_count