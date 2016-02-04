from django import forms
from django.utils import timezone

from exams.models import Exam, ExamQuestion
from questions.models import Question

FORMAT = '%Y/%m/%d %H:%M'

class ExamForm(forms.ModelForm):

    name = forms.CharField(label="Exam name", max_length=30)
    description = forms.Textarea()
    password = forms.CharField(label="Password (optional)",
        widget=forms.PasswordInput(render_value=True), required=False)
    time_limit = forms.TimeField(widget=forms.TimeInput(format='%H:%M'),
        help_text=("Hours:Minutes"))
    active_from = forms.DateTimeField(widget=forms.DateTimeInput(format=FORMAT),
        input_formats=[FORMAT])
    active_to = forms.DateTimeField(widget=forms.DateTimeInput(format=FORMAT),
        input_formats=[FORMAT])
    category = forms.ChoiceField()
    question_count = forms.IntegerField(label="Number of questions")

    class Meta:
        model = Exam
        fields = ['name', 'description', 'password', 'time_limit',
            'active_from', 'active_to', 'category', 'question_count']

    def clean(self):
        cleaned_data = super(ExamForm, self).clean()
        if ('active_from' in self.cleaned_data and 
            'active_to' in self.cleaned_data):
            if (self.cleaned_data['active_from'] >= 
                self.cleaned_data['active_to'] and 
                self.cleaned_data['active_to'] > timezone.now()):
                raise forms.ValidationError("Please enter a valid active \
                    time frame")
        return self.cleaned_data

    def __init__(self, instance=None, course=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if instance:
            self.instance.exam = instance
            self.initial['name'] = instance.name
            self.initial['description'] = instance.description
            self.initial['password'] = instance.password
            self.initial['time_limit'] = instance.time_limit
            self.initial['active_from'] = instance.active_from
            self.initial['active_to'] = instance.active_to
            self.initial['category'] = instance.category
            self.initial['question_count'] = instance.question_count
            question_course = instance.course
        elif course:
            question_course = course
        self.fields['category'].choices = [(x, x) for x in 
            Question.objects.filter(course=question_course)
            .values_list('category',flat=True).distinct()]