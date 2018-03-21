from django.contrib import admin
from .models import User, UserType

class UserAdmin(admin.ModelAdmin):
    list_display = ['name','user_type','user_address','contact_details_1','contact_details_2','email','rating']
    list_filter = ['name','user_type','rating']
    search_fields = ['name','user_type','rating']

class UserTypeAdmin(admin.ModelAdmin):
    list_display = ['user_type']

admin.site.register(User, UserAdmin)
admin.site.register(UserType, UserTypeAdmin)