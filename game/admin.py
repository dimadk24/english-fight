from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import Group

from game.models import AppUser, AppGroup

admin.site.register(AppUser, UserAdmin)

# Move Group to the same app as User
admin.site.unregister(Group)
admin.site.register(AppGroup, GroupAdmin)
