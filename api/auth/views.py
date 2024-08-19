from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework import status, permissions
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from rest_framework.request import Request
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from api.auth.serializers import LoginSerializer, ReadUserSerializer, CreatUserSerializer
from api.serializers import CandidateSerializer, VoterSerializer, UserSerializer, VoteSerializer, SortedVotesSerializer
from election.models import Candidate, Vote, Voter
from drf_yasg import openapi

User = get_user_model()


class RegisterAPIView(APIView):
    serializer_class = CreatUserSerializer
    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'phone': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
                'password_confirmation': openapi.Schema(type=openapi.TYPE_STRING),
                'email': openapi.Schema(type=openapi.TYPE_STRING),
                'first_name': openapi.Schema(type=openapi.TYPE_STRING),
                'last_name': openapi.Schema(type=openapi.TYPE_STRING),
                'role': openapi.Schema(type=openapi.TYPE_STRING, enum=[User.CLIENT, User.CANDIDATE, User.ADMIN]),
                'party': openapi.Schema(type=openapi.TYPE_STRING, description="Party name (for candidates)", blank=True,
                                        null=True),
                'photo': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_BINARY,
                                        description="Candidate photo"),
            }
        )
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            read_serializer = UserSerializer(user, context={'request': request})
            data = {**read_serializer.data, 'token': token.key}
            return Response({"token": token.key, **data},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data.get('phone')
        password = serializer.validated_data.get('password')

        user = authenticate(phone=phone, password=password)

        if user:
            token, created = Token.objects.get_or_create(user=user)
            read_serializer = UserSerializer(user, context={'request': request})
            data = {**read_serializer.data, 'token': token.key}
            return Response(data)

        return Response({'detail': 'Не существует пользователя или неверный пароль.'},
                        status=status.HTTP_401_UNAUTHORIZED)


class UserProfileApiView(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = self.serializer_class(user)
        return Response(serializer.data)

    def put(self, request):
        user = request.user
        serializer = self.serializer_class(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def patch(self, request):
        user = request.user
        serializer = self.serializer_class(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class CandidateListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        candidates = Candidate.objects.all()
        serializer = CandidateSerializer(candidates, many=True)
        return Response(serializer.data)


class SortedVotesView(APIView):

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'voter_id': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID избирателя"),
                'votes': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(type=openapi.TYPE_INTEGER),
                    description="Массив голосов"
                )
            },
            required=['voter_id', 'votes']
        ),
        responses={
            200: openapi.Response(
                description="Sorted votes",
                schema=openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(type=openapi.TYPE_INTEGER),
                    description="Array of sorted vote counts"
                )
            ),
            400: openapi.Response(
                description="Bad request",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING)
                    }
                )
            )
        }
    )
    def post(self, request, *args, **kwargs):
        voter_id = request.data.get('voter_id')
        votes = request.data.get('votes')

        if not voter_id or not votes:
            return Response(
                {'detail': 'Both voter_id and votes are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Ваш код для обработки данных
        sorted_votes = sorted(votes)  # Пример сортировки массива

        return Response(sorted_votes, status=status.HTTP_200_OK)


class VoteCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        if request.user.role != User.CLIENT:
            return Response({"detail": "Только избиратели могут голосовать."}, status=status.HTTP_403_FORBIDDEN)

        voter = Voter.objects.filter(user=request.user).first()
        if not voter:
            return Response({"detail": "Избиратель не найден."}, status=status.HTTP_400_BAD_REQUEST)

        candidate_id = request.data.get('candidate_id')
        candidate = Candidate.objects.filter(id=candidate_id).first()

        if not candidate:
            return Response({"detail": "Кандидат не найден."}, status=status.HTTP_400_BAD_REQUEST)

        # Проверка, что избиратель не голосовал уже
        if Vote.objects.filter(voter=voter).exists():
            return Response({"detail": "Вы уже проголосовали."}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "Голос успешно зарегистрирован"}, status=status.HTTP_201_CREATED)
