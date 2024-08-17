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
        'get_avatar',
        'bio',
        'party',
        'get_photo',
    )
    list_display_links = ('id', 'email',)
    search_fields = ('first_name', 'last_name', 'email', 'phone')
    filter_horizontal = ()
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'role')
    ordering = ('-date_joined',)
    fieldsets = (
        (None, {'fields': ('email', 'phone', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'bio', 'party', 'photo')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    readonly_fields = (
        'get_full_name',
        'date_joined',
        'last_login',
        'get_avatar',
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'phone',
                'password1',
                'password2',
                'bio',
                'party',
                'photo',
            ),
        }),
    )

    @admin.display(description=_('Аватарка'))
    def get_avatar(self, user):
        if user.avatar:
            return mark_safe(f'<img src="{user.avatar.url}" alt="{user.get_full_name}" width="100px" />')
        return '-'

    @admin.display(description=_('Фотография'))
    def get_photo(self, user):
        if user.photo:
            return mark_safe(f'<img src="{user.photo.url}" alt="{user.get_full_name}" width="100px" />')
        return '-'

    @admin.display(description=_('Полное имя'))
    def get_full_name(self, user):
        return user.get_full_name()
