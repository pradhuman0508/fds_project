from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin

from .models import Device


# class DeviceAdmin(UserAdmin):
#     model = Device
#     list_display = ('serial_number', 'is_staff', 'is_active',)
#     list_filter = ('serial_number', 'is_staff', 'is_active',)
#     fieldsets = (
#         (None, {'fields': ('serial_number', 'password','qr_code_token','private_key','verification_code')}),
#         ('Permissions', {'fields': ('is_staff', 'is_active')}),
#     )
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('serial_number', 'password1', 'password2', 'is_staff', 'is_active')}
#         ),
#     )
#     search_fields = ('serial_number',)
#     ordering = ('serial_number',)

admin.site.register(Device)


