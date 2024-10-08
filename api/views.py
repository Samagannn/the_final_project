from datetime import timezone

from httpie import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.utils import json
from rest_framework.viewsets import ModelViewSet
from election.models import Election, Candidate, Vote, Voter
from . import serializers
from .permissions import IsOwnerOrReadOnly, IsAdminOrReadOnly
from .serializers import ElectionSerializer, CandidateSerializer, VoteSerializer, VoterSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import status
from rest_framework import serializers

class ElectionViewSet(viewsets.ModelViewSet):
    queryset = Election.objects.all()
    serializer_class = ElectionSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['start_date', 'end_date']


class CandidateViewSet(viewsets.ModelViewSet):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsOwnerOrReadOnly()]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class VoteViewSet(viewsets.ModelViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [IsAuthenticated]


    def perform_create(self, serializer):
        # Проверяем, зарегистрирован ли пользователь как избиратель
        if not hasattr(self.request.user, 'voter'):
            raise serializers.ValidationError("Вы не зарегистрированы как избиратель.")

        # Проверяем, голосовал ли уже пользователь
        if Vote.objects.filter(voter=self.request.user.voter).exists():
            raise serializers.ValidationError("Вы уже проголосовали.")

        # Сохраняем голос
        serializer.save(voter=self.request.user.voter)


class VoterViewSet(viewsets.ModelViewSet):
    queryset = Voter.objects.all()
    serializer_class = VoterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
