from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from election.models import Candidate, Election

User = get_user_model()


class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = ['election', 'party', 'photo', 'bio']


class CreatUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirmation = serializers.CharField(write_only=True)
    party = serializers.CharField(write_only=True, required=False)
    photo = serializers.ImageField(write_only=True, required=False)
    bio = serializers.CharField(write_only=True, required=False)
    election = serializers.PrimaryKeyRelatedField(queryset=Election.objects.all(), required=False, allow_null=True)

    class Meta:
        model = User
        fields = (
            'id', 'phone', 'password', 'password_confirmation', 'email', 'role', 'party',
            'photo', 'bio', 'election'
        )

    def validate(self, data):
        if data['password'] != data['password_confirmation']:
            raise serializers.ValidationError({"password_confirmation": "Passwords must match"})
        if not data.get('email'):
            raise serializers.ValidationError({"email": "Email is required"})

        # Проверка обязательных полей в зависимости от роли
        role = data.get('role')
        if role == User.CANDIDATE:
            if not data.get('party'):
                raise serializers.ValidationError({"party": "This field may not be blank."})
            if not data.get('bio'):
                raise serializers.ValidationError({"bio": "This field may not be blank."})
        elif role == User.CLIENT:
            # Не требуется проверка полей для избирателя
            pass
        elif role == User.ADMIN:
            pass

        return data

    def create(self, validated_data):
        validated_data.pop('password_confirmation')

        phone = validated_data['phone']

        # Проверка уникальности номера телефона
        if User.objects.filter(phone=phone).exists():
            raise serializers.ValidationError({"phone": "A user with this phone number already exists."})

        # Создание пользователя
        user = User.objects.create_user(
            phone=validated_data['phone'],
            password=validated_data['password'],
            email=validated_data['email'],
            role=validated_data['role']
        )

        # Если роль — кандидат, создайте профиль кандидата
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

    class Meta:
        model = User
        fields = ('id', 'phone', 'email', 'old_password', 'new_password')

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
