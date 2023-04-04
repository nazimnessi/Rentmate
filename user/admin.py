from django.contrib import admin
from .models import Documents, Address, User


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'phone_number')
    search_fields = ['id', 'name', 'email']

    def api_name(self, obj):
        return obj.user.name


class AddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'address1', 'address2', 'city', 'state', 'postal_code')
    search_fields = ['id', 'address1', 'address2', 'city', 'state', 'postal_code']
    list_filter = ('state', 'city')

    def api_name(self, obj):
        return obj.user.address1


# Register your models here.
admin.site.register(Documents)
admin.site.register(Address, AddressAdmin)
admin.site.register(User, UserAdmin)
