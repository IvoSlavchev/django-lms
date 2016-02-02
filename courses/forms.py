from django import forms

from courses.models import Course, Participation
from users.models import User


class CourseForm(forms.ModelForm):

    name = forms.CharField(label="Course name", max_length=30)
    description = forms.Textarea()

    class Meta:
        model = Course
        fields = ['name', 'description']

    def __init__(self, instance=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if instance:
            self.instance.course = instance
            self.initial['name'] = instance.name
            self.initial['description'] = instance.description


class ParticipantsAssetMultiField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return '{} {}'.format(obj, obj.email)


class ParticipantsForm(forms.ModelForm):

    participants = ParticipantsAssetMultiField(label="", required=False,
        queryset=User.objects.filter(is_teacher=False, is_active=True,
        is_superuser=False), widget=forms.CheckboxSelectMultiple())

    class Meta:
        model = Course
        fields = ['participants']

    def __init__(self, instance=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if instance:
            self.instance.course = instance
            self.initial['participants'] = [participant.user for participant in
                Participation.objects.filter(course=instance)]