from django.shortcuts import get_object_or_404, render, redirect
from .models import *
from .forms import *

# Create your views here.
def student_list_view(request):
    if request.method == 'GET':
        students = Student.objects.all()
        context = {
            "students" : students
        }
        return render(request,"student/user-list.html", context)    
    else:
        keyword = request.POST.get('keyword')
        students = Student.objects.filter(fullname__contains=keyword)
        if len(students) == 0:
            students = Student.objects.filter(code__contains=keyword)
        context = {
            "students" : students
        }
        return render(request,"student/user-list.html", context)    
        
def delete_view(request, id):
    student = get_object_or_404(Student, id=id)
    if request.method == 'POST':
        student.delete()
        return redirect('/students')
    context = {'student': student}
    return render(request, "student/delete.html", context)

def update_view(request, id):
    student = get_object_or_404(Student,id=id)
    form = StudentForm(request.POST or None, request.FILES or None, instance=student)
    if form.is_valid():
        form.save()
        return redirect('/students')
    context = {'form': form}
    return render(request, 'student/create.html', context)

def create_view(request):
    form = StudentForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('/students')
    context = {'form': form}
    return render(request, 'student/create.html', context)
