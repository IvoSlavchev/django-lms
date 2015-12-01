from django.shortcuts import render

def home_page(request):
	return render(request, 'home.html')

def teacher_page(request):
	return render(request, 'teacher.html')

def student_page(request):
	return render(request, 'student.html')