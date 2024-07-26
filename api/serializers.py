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


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'phone', 'email', 'first_name', 'last_name', 'avatar',
                  'role')


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = '__all__'
        depth = 1
        read_only_fields = ['election']
        write_only_fields = ['election']


class VoterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voter
        fields = '__all__'
        depth = 1
        read_only_fields = ['election']
        write_only_fields = ['election']
