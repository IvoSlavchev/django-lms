from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect, render

from courses.models import Course
from exams.forms import ExamForm
from exams.models import Exam

def teacher_check(user):
    return user.is_teacher

@user_passes_test(teacher_check)
def create_exam(request, course_id):
	if request.method == 'POST':		
		form = ExamForm(data=request.POST)
		if form.is_valid():			
			exam = Exam.objects.create(owner=request.user, name=form.cleaned_data['name'], 
				description=form.cleaned_data['description'], date_to_be_taken=form.cleaned_data['date_to_be_taken'], 
				course=Course.objects.get(id=course_id))		
			return redirect('/courses/' + course_id + '/')
	else:
		form = ExamForm()
	return render(request, 'create_exam.html', {'form': form})