from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import UserSignUP

class UserAdmin(BaseUserAdmin):
    # Fields to display in the admin user list
    list_display = ('first_name', 'surname', 'phone', 'email', 'role','photo','hostel','address', 'password','is_active', 'is_staff')
    search_fields = ('phone', 'email', 'first_name', 'surname')
    ordering = ('first_name',)

    # Fieldsets for organizing the user detail page
    fieldsets = (
        (None, {'fields': ('phone', 'email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'surname', 'role', 'photo', 'hostel', 'address')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login',)}),
    )

    # Fieldsets for the add user form in admin
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'email', 'password1', 'password2', 'first_name', 'surname', 'role', 'photo'),
        }),
    )

# Register the User model with the custom admin interface
admin.site.register(UserSignUP, UserAdmin)
