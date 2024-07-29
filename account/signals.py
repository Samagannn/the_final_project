from django.db.models.signals import pre_save
from django.dispatch import receiver

from account.models import User


@receiver(pre_save, sender=User)
def pre_save_user(instance: User, *args, **kwargs):
    if instance.role == User.ADMIN or instance.is_superuser:
        instance.role = User.ADMIN
        instance.is_staff = True
        instance.is_superuser = True

    return instance