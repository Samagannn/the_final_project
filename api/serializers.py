# serializers.py
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


class VoterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voter
        fields = '__all__'


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
    class Meta:
        model = Voter
        fields = '__all__'
        depth = 1
        read_only_fields = ['election']
        write_only_fields = ['election']
