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
    candidate = CandidateSerializer()
    voter = serializers.PrimaryKeyRelatedField(queryset=Voter.objects.all())

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
        fields = ['id', 'email', 'first_name', 'last_name', 'role', 'phone', 'bio', 'party', 'photo',
                  ]

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    def create(self, validated_data):
        print(f"Валидированные данные: {validated_data}")
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            role=validated_data['role'],
            phone=validated_data['phone'],
            password=validated_data['password'],
            bio=validated_data['bio'],
            party=validated_data['party'],
            photo=validated_data['photo'],
        )
        return user


class VoterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voter
        fields = ['id', 'user', 'election']

    def validate(self, data):
        user = data.get('user')

        if Voter.objects.filter(user=user).exists():
            raise serializers.ValidationError(
                {"user": "Этот пользователь уже зарегистрирован как избиратель для этих выборов."})

        return data
