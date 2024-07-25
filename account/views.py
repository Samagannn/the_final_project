from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.http import HttpResponse
from .models import User
from account.forms import ConfirmPasswordForm
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from api.serializers import UserSerializer


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


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
