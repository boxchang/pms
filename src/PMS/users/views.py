import datetime
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect

from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.urls import reverse
from django.utils import translation


from projects.models import Project
from bases.views import index
from users.forms import CurrentCustomUserForm, CustomUser


def register(request):
    '''
    Register a new user
    '''
    template = 'registration/register.html'
    if request.method == 'GET':
        return render(request, template, {'userForm': CurrentCustomUserForm()})

    # POST
    userForm = CurrentCustomUserForm(request.POST)
    if not userForm.is_valid():
        return render(request, template, {'userForm': userForm})

    userForm.save()
    messages.success(request, '歡迎註冊')
    return redirect('register')


def login(request):
    if 'username' in request.COOKIES:
        cookies_username = request.COOKIES['username']

    if 'password' in request.COOKIES:
        cookies_password = request.COOKIES['password']

    '''
    Login an existing user
    '''
    template = 'registration/login.html'
    if request.method == 'GET':
        next = request.GET.get('next')
        return render(request, template, locals())

    if request.method == 'POST':
        next_page = request.POST.get('next')
        if request.user.is_authenticated:
            if next_page != 'None':
                return HttpResponseRedirect(next_page)
            else:
                return index(request)
        else:
            # POST
            username = request.POST.get('username')
            password = request.POST.get('password')
            if not username or not password:    # Server-side validation
                messages.error(request, '使用者名稱或密碼未填寫！')
                return render(request, template)

            user = authenticate(username=username, password=password)
            if not user:    # authentication fails
                messages.error(request, '使用者名稱或密碼不正確！')
                return render(request, template)

            response = redirect(reverse('assets_main'))
            if request.POST.get('remember') == "on":
                response.set_cookie("username", username, expires=timezone.now()+datetime.timedelta(days=30))
                response.set_cookie("password", password, expires=timezone.now()+datetime.timedelta(days=30))
            else:
                response.delete_cookie("username")
                response.delete_cookie("password")
            # login success
            auth_login(request, user)

            # messages.success(request, '登入成功')

            return response


def logout(request):
    '''
    Logout the user
    '''
    auth_logout(request)
    messages.success(request, '歡迎再度光臨')
    return redirect('login')
