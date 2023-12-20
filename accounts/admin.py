from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import AccountUser

class AccountUserAdmin(UserAdmin):
    list_display = ('id', 'email', 'phone_number', 'is_active', 'role', 'is_superuser')
    search_fields = ('email', 'phone_number')
    
    # Specify a valid field for ordering, for example, 'id'

    ordering = ('id',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name' ,'role', 'phone_number', 'image')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
       
    )



# class UserProfileAdmin(admin.ModelAdmin):
#     list_display = ('user', 'address')
#     search_fields = ('user__first_name', 'user__last_name', 'user__email', 'address')


class ChatMessageAdmin(admin.ModelAdmin):
    list_editable = ["is_read"]
    list_display = ["sender","receiver","message","is_read"]

admin.site.register(AccountUser,AccountUserAdmin)





