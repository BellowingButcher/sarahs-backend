from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    ...
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('is_teamleader', 'is_teammember')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('is_teamleader', 'is_teammember')}),
    )


# Now register the new UserAdmin...
admin.site.register(CustomUser, CustomUserAdmin)
