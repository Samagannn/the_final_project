from rest_framework import serializers
from election.models import Election, Candidate, Vote, Voter
from account.models import User


class ElectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Election
        fields = '__all__'


class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = '__all__'


class VoteSerializer(serializers.ModelSerializer):
    candidate = CandidateSerializer()  # To include candidate details
    voter = serializers.PrimaryKeyRelatedField(queryset=Voter.objects.all())  # Only include voter ID

    class Meta:
        model = Vote
        fields = ['id', 'candidate', 'voter', 'timestamp']


class SortedVotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ['id', 'candidate', 'timestamp']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'role', 'date_of_birth', 'phone', 'bio', 'party', 'photo']

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            role=validated_data['role'],
            date_of_birth=validated_data['date_of_birth'],
            phone=validated_data['phone'],
            password=validated_data['password'],
            bio=validated_data.get('bio', None),
            party=validated_data.get('party', None),
            photo=validated_data.get('photo', None),
        )
        return user


class VoterSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())  # Включаем только ID пользователя

    class Meta:
        model = Voter
        fields = ['id', 'address', 'has_voted', 'user']
