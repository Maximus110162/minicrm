from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .models import Complaint
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role','image')}),
    )
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Complaint)
