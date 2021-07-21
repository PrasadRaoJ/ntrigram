from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from college.models import CollegeData
from django.contrib import messages

# Create your views here.
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required


def register_view(request):
    if request.method =='POST':
        username = request.POST.get('name')
       
        email = request.POST.get('email')
        pwd_1 = request.POST.get('pwd')
        pwd_2 = request.POST.get('cpwd')

        #print(username,email,pwd_1,pwd_2,10*'---')

        if pwd_1 == pwd_2:
            if User.objects.filter(username=email).exists():
                messages.error(request,'Email already registered..!')
                return redirect('home')
            else:
                user = User.objects.create_user(username=email,first_name=username,last_name=username,email=email,password=pwd_1)
                user.save()
                login(request,user)
                messages.success(request,'Your account has been registered successfully..!')
                return redirect('userform')
                #print('Registered successfully...!')
        else:
            messages.error(request,"Passwords didn't matched..!")
            return redirect('home')



    return render(request,'index.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        pwd = request.POST.get('pwd') 
        user = authenticate(username=email, password=pwd)

        if user is not None:
            login(request,user)
            messages.success(request,'Your are login successful')
            return redirect('userform')
        else:
            messages.info(request,'Your password or email invalid..!')
            return redirect('home')

    return render(request,'index.html')


@login_required(login_url='login',redirect_field_name='dashboard')
def recover(request):
    return render(request,'index.html')


def logout_view(request):
    logout(request)
    messages.success(request,'Your are logout successfully.')
    return redirect('home')