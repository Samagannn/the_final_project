from account.models import User
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password


class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField()


# class CreatUserSerializer(serializers.Serializer):
#     first_name = serializers.CharField()
#     last_name = serializers.CharField()
#     username = serializers.CharField()
#     password1 = serializers.CharField()
#     password2 = serializers.CharField()


class ReadUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password', 'user_permissions', 'groups')


class CreatUserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        exclude = ('password', 'user_permissions', 'groups', 'is_staff', 'is_active', 'is_superuser')

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError({'password2': ["Пароли не совпадают."]})
        return data

    # def validate_first_name(self, first_name):
    #     return first_name

    def create(self, validated_data):
        password = validated_data.pop('password1')
        validated_data.pop('password2')
        validated_data['password'] = make_password(password)

        return super().create(validated_data)

    # def update(self, instance, validated_data):
    #     return instance
