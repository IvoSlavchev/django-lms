from django.db import models

from courses.models import Course


class Question(models.Model):

    owner = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    category = models.CharField(max_length=30)
    question_text = models.TextField()
    course = models.ForeignKey(Course)
    
    def __str__(self):
        return self.name


class Choice(models.Model):

    choice_text = models.CharField(max_length=30)
    correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question)

    def __str__(self):
        return self.choice_text