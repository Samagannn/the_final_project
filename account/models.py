from django.db import models
from django.contrib.auth.models import AbstractUser
from django_resized import ResizedImageField
from phonenumber_field.modelfields import PhoneNumberField
from account.managers import UserManager


class User(AbstractUser):
    CLIENT = 'client'
    CANDIDATE = 'canditat'
    ADMIN = 'admin'

    ROLE = (
        (CLIENT, 'Админ'),
        (CANDIDATE, 'Кандидат'),
        (ADMIN, 'Избиратель')
    )

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
        ordering = ('-date_joined',)

    username = None
    avatar = ResizedImageField(size=[500, 500], crop=['middle', 'center'],
                               upload_to='avatars/', force_format='WEBP', quality=90, verbose_name='аватарка',
                               null=True, blank=True)
    phone = PhoneNumberField(max_length=100, unique=True, verbose_name='номер телефона')
    email = models.EmailField(null=True, verbose_name='электронная почта', unique=True)
    role = models.CharField('роль', choices=ROLE, max_length=15)

    objects = UserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['email']

    @property
    def get_full_name(self):
        return f'{self.last_name} {self.first_name}'

    get_full_name.fget.short_description = 'полное имя'

    def __str__(self):
        return f'{self.get_full_name or str(self.phone)}'

    def set_candidate(self):
        self.role = self.CANDIDATE
        self.save()

    def set_admin(self):
        self.role = self.ADMIN
        self.save()


def check_three_and_two(arr):
    for i in arr:
        if not 2 <= arr.count(i) <= 3:
            return False
    return True


