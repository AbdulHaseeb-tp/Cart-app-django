from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Customer

# Create your views here.

def show_account(request):
    context={}
    if request.POST and 'register' in request.POST:
        context['register']=True
        try:
            username=request.POST.get('username')
            password=request.POST.get('password')
            email=request.POST.get('email')
            address=request.POST.get('address')
            phone=request.POST.get('phone')

            # create user accounts
            user=User.objects.create_user(
                username=username,
                password=password,
                email=email
            )

            # create customer account
            customer=Customer.objects.create(
                user=user,
                address=address,
                phone=phone
            )
            success_message="User registered successfully"
            messages.success(request,success_message)
        except Exception as e:
            error_message="Dupicate username or invalid inputs"
            messages.error(request,error_message)

    # login check...
    if request.POST and 'login' in request.POST:
        context['register']=False
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(username=username,password=password)        
        if user:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'You entered a invalid user credentials')        
    return render(request, 'account.html', context)


# logOut function
def logoutt(request):
    logout(request)
    return redirect('home')