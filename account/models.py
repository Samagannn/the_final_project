from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django_resized import ResizedImageField
from phonenumber_field.modelfields import PhoneNumberField

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')

        email = self.normalize_email(email)
        extra_fields.setdefault('username', self.generate_unique_username(email))
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

    def generate_unique_username(self, email):
        base_username = email.split('@')[0]
        username = base_username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}_{counter}"
            counter += 1
        return username

class User(AbstractUser):
    CLIENT = 'client'
    CANDIDATE = 'candidate'
    ADMIN = 'admin'

    ROLE_CHOICES = (
        (CLIENT, 'Избиратель'),
        (CANDIDATE, 'Кандидат'),
        (ADMIN, 'Администратор'),
    )

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True, blank=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    role = models.CharField(max_length=30, choices=ROLE_CHOICES)
    date_of_birth = models.DateField(blank=True, null=True)
    phone = PhoneNumberField(unique=True, blank=True, null=True)
    avatar = ResizedImageField(size=[500, 500], crop=['middle', 'center'],
                               upload_to='avatars/', force_format='WEBP', quality=90, null=True, blank=True)
    employee_id = models.CharField(max_length=30, blank=True, null=True)
    department = models.CharField(max_length=30, blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone']

    def __str__(self):
        return self.email

    @property
    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def set_candidate(self):
        self.role = self.CANDIDATE
        self.save()

    def set_admin(self):
        self.role = self.ADMIN
        self.save()
