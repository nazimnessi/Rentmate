from django.contrib import admin
from .models import Documents, Address, User


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'phone_number')
    search_fields = ['id', 'name', 'email']

    def api_name(self, obj):
        return obj.user.name


# Register your models here.
admin.site.register(Documents)
admin.site.register(Address)
admin.site.register(User, UserAdmin)
