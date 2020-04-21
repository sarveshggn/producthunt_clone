from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
# Create your views here.

def signup(request):
    if request.method == 'POST':
        #user has info and wants account
        if request.POST['Password1'] == request.POST['Password2']:
            try:
                user = User.objects.get(username=request.POST['Username'])
                return render(request, 'accounts/signup.html', {'error':'Username already taken'})
            except User.DoesNotExist:
                user = User.objects.create_user(request.POST['Username'], password=request.POST['Password1'])
                auth.login(request,user)
                return redirect('home')
        else:
            return render(request, 'accounts/signup.html', {'error':'Passwords must match'})
    else:
        #user does not have info
        return render(request, 'accounts/signup.html') 

def login(request):
    if request.method == 'POST':
        user = auth.authenticate(username=request.POST['Username'], password=request.POST['Password'])
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            return render(request, 'accounts/login.html', {'error':'Username or Password are not correct'})
    else:
        return render(request, 'accounts/login.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('home')
    # ### Return this to home page ###
    # return render(request, 'accounts/signup.html')