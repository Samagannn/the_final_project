from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate
from rest_framework import status, permissions, generics
from rest_framework.viewsets import ViewSet
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from rest_framework.request import Request

from api.auth.serializers import LoginSerializer, ReadUserSerializer, CreatUserSerializer


class RegisterAPIView(generics.CreateAPIView):
    serializer_class = CreatUserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        read_serializer = ReadUserSerializer(user, context={'request': request})
        data = {**read_serializer.data, 'token': token.key}
        return Response(data, status=status.HTTP_201_CREATED)


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data.get('phone')
        password = serializer.validated_data.get('password')

        user = authenticate(phone=phone, password=password)

        if user:
            token, created = Token.objects.get_or_create(user=user)
            read_serializer = ReadUserSerializer(user, context={'request': request})
            data = {**read_serializer.data, 'token': token.key}
            return Response(data)

        return Response(
            {'detail': 'Не существует пользователя или неверный пароль.'}, status=status.HTTP_401_UNAUTHORIZED)


User = get_user_model()


#
# class BaseAPIView:
#     pass


class RedactorProfileApiView(ViewSet, GenericAPIView):
    queryset = User.objects.all()
    serializer_class = CreatUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data)

    def post(self, request):
        return self._update(request)

    def put(self, request):
        return self._update(request)

    def patch(self, request):
        return self._update(request, partial=True)

    def _update(self, request, partial=False):
        instance = request.user
        serializer = self.serializer_class(instance=instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
