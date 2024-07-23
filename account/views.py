from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.http import HttpResponse
from .models import User
from account.forms import ConfirmPasswordForm


@login_required
def become_candidate(request):
    user = request.user
    if user.role != User.CANDIDATE:
        user.set_candidate()
        return HttpResponse("Вы стали кандидатом")
    else:
        return HttpResponse("Вы уже являетесь кандидатом")


@login_required
def become_admin(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        user = authenticate(username=request.user.phone, password=password)
        if user is not None:
            user.set_admin()
            return HttpResponse("Вы стали администратором")
        else:
            return HttpResponse("Неверный пароль")
    else:
        return HttpResponse("Метод POST ожидается для этого действия")
