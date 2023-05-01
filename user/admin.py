from django.contrib import admin
from .models import Documents, Address, User


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'phone_number')
    search_fields = ['id', 'username', 'email']


class AddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'address1', 'address2', 'city', 'state', 'postal_code')
    search_fields = ['id', 'address1', 'address2', 'city', 'state', 'postal_code']
    list_filter = ('state', 'city')


# Register your models here.
admin.site.register(Documents)
admin.site.register(Address, AddressAdmin)
admin.site.register(User, UserAdmin)
