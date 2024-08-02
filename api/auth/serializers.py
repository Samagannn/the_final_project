from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from django.contrib.auth import get_user_model
from election.models import Candidate, Election

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'role', 'date_of_birth', 'phone', 'avatar', 'employee_id',
                  'department', 'full_name', 'bio', 'party', 'photo']

    def get_full_name(self, obj):
        return obj.get_full_name()

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        if instance.role != User.CANDIDATE:
            representation.pop('photo', None)
            representation.pop('bio', None)
            representation.pop('party', None)

        return representation


class CandidateSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Candidate
        fields = ['id', 'bio', 'party', 'photo', 'votes_per_month', 'user', 'election']

    def get_user(self, obj):
        user = obj.user
        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'phone': user.phone,
            'email': user.email
        }


class CreatUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirmation = serializers.CharField(write_only=True)
    party = serializers.CharField(write_only=True, required=False, allow_blank=True)  # Необязательное поле
    photo = serializers.ImageField(write_only=True, required=False, allow_null=True)
    bio = serializers.CharField(write_only=True, required=False, allow_blank=True)
    election = serializers.PrimaryKeyRelatedField(queryset=Election.objects.all(), required=False, allow_null=True)
    last_name = serializers.CharField(write_only=True, required=False, allow_blank=True)
    first_name = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = User
        fields = (
            'id', 'phone', 'password', 'password_confirmation', 'email', 'role', 'party',
            'photo', 'bio', 'election', 'last_name', 'first_name'
        )

    def validate(self, data):
        # Ваши проверки валидности
        if data['password'] != data['password_confirmation']:
            raise serializers.ValidationError({"password_confirmation": "Passwords must match"})
        if not data.get('email'):
            raise serializers.ValidationError({"email": "Email is required"})

        role = data.get('role')
        if role == User.CANDIDATE:
            # Проверка поля party и bio
            if not data.get('party'):
                print("Party field is blank or not provided")
            if not data.get('bio'):
                print("Bio field is blank or not provided")

        return data

    def create(self, validated_data):
        validated_data.pop('password_confirmation')

        phone = validated_data['phone']

        if User.objects.filter(phone=phone).exists():
            raise serializers.ValidationError({"phone": "A user with this phone number already exists."})

        user = User.objects.create_user(
            phone=validated_data['phone'],
            password=validated_data['password'],
            email=validated_data['email'],
            role=validated_data['role'],
            last_name=validated_data.get('last_name'),
            first_name=validated_data.get('first_name'),
        )

        if user.role == User.CANDIDATE:
            party = validated_data.get('party')
            photo = validated_data.get('photo')
            bio = validated_data.get('bio')
            election = validated_data.get('election')

            Candidate.objects.create(
                user=user,
                party=party,
                photo=photo,
                bio=bio,
                election=election
            )

        return user


class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField(write_only=True)


class ReadUserSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(write_only=True, required=False)
    new_password = serializers.CharField(write_only=True, required=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ('id', 'phone', 'email', 'first_name', 'last_name', 'old_password', 'new_password')

    def validate(self, data):
        old_password = data.get('old_password')
        new_password = data.get('new_password')
        user = self.instance

        if old_password and not user.check_password(old_password):
            raise serializers.ValidationError({'old_password': 'Неправильный текущий пароль'})

        if new_password:
            validate_password(new_password)

        return data

    def update(self, instance, validated_data):
        old_password = validated_data.pop('old_password', None)
        new_password = validated_data.pop('new_password', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if new_password:
            instance.set_password(new_password)

        instance.save()
        return instance
