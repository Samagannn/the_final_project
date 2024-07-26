from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        'id',
        'email',
        'phone',
        'first_name',
        'last_name',
        'role',
    )
    list_display_links = ('id', 'email',)
    search_fields = ('first_name', 'last_name', 'email', 'phone')
    filter_horizontal = ()
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'role')
    ordering = ('-date_joined',)
    fieldsets = (
        (None, {'fields': (
            'email',
            'phone',
            'password',
        )}),
        (_('Personal info'), {'fields': (
            'avatar',
            'first_name',
            'last_name',
        )}),
        (_('Permissions'), {'fields': (
            'role',
            'is_active',
            'is_staff',
            'is_superuser',
        )}),
        (_('Important dates'), {'fields': (
            'date_joined',
            'last_login',
        )}),
    )
    readonly_fields = (
        'get_full_name',
        'date_joined',
        'last_login',
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'phone',
                'password1',
                'password2',
            ),
        }),
    )

    @admin.display(description=_('Аватарка'))
    def get_avatar(self, user):
        if user.avatar:
            return mark_safe(
                f'<img src="{user.avatar.url}" alt="{user.get_full_name}" width="100px" />')
        return '-'

    @admin.display(description=_('Полное имя'))
    def get_full_name(self, user):
        return user.get_full_name()

# Register your models here.
