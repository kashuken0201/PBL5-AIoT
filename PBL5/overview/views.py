from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from .models import Account
import zlib

# Create your views here.
def overview_view(request):
    if request.session.get('user_id') is None:
        return redirect('/')
    else:
        return render(request, "overview/overview.html")

def change_password_view(request):
    return render(request,"overview/change-password.html")

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        password = zlib.crc32(password.encode())
        if Account.objects.filter(email=email, password=password).exists():
            user_id = Account.objects.get(email=email, password=password).id
            request.session['user_id'] = user_id
            return redirect('/overview')
        else:
            context = {'error': 'Wrong password'}
            return render(request, "overview/login.html", context) 
    else:
        return render(request,"overview/login.html")

def introduction_view(request):
    return render(request, "overview/introduction.html")

def registration_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        fullname = request.POST.get('full_name')
        password = request.POST.get('password')
        re_password = request.POST.get('re_password')
        if password == re_password and password !="" and fullname != "" and email != "":
            if not Account.objects.filter(email=email).exists():
                Account.objects.create(fullname=fullname, email=email, password=zlib.crc32(password.encode()))   
                return redirect('/')
            else:
                context = {'error': 'This account already exist'}
        else :
            context = {'error': 'Password and re-password dissimilarity'}
        return render(request, "overview/registration.html", context)
    else:
        return render(request, 'overview/registration.html')
        
def logout_view(request):
    if request.session.get('user_id') is None:
        return redirect('/')
    else:
        del request.session['user_id']
        return redirect('/')

