from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from game.models import AppUser, AppGroup


@admin.register(AppUser)
class AppUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'),
         {'fields': ('first_name', 'last_name', 'email', 'vk_id', 'score')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups',
                       'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    list_display = ('__str__', 'email', 'first_name', 'last_name', 'is_staff')


# Move Group to the same app as User
admin.site.unregister(Group)
admin.site.register(AppGroup, GroupAdmin)
