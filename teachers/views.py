from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext

from teachers.forms import CreateForm
from teachers.models import Course

def teacher_check(user):
    return user.is_teacher

@user_passes_test(teacher_check, login_url='/login')
def dashboard(request):
	courses = Course.objects.filter(owner=request.user)
	return render_to_response('teacher_dashboard.html', {'courses': courses}, context_instance=RequestContext(request))

def create(request):
	if request.method == 'POST':		
		form = CreateForm(data=request.POST)
		form.instance.owner = request.user
		if form.is_valid():
			form.save()
			messages.add_message(request, messages.INFO, 'Course created successfully.')
			return redirect('/teachers')
	else:
		form = CreateForm()
	return render_to_response('create.html', {'form': form,}, context_instance=RequestContext(request))