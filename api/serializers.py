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
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'role', 'date_of_birth', 'phone', 'employee_id',
                  'department', 'password']

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
            employee_id=validated_data.get('employee_id', None),
            department=validated_data.get('department', None)
        )
        return user


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
