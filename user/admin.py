from django.contrib import admin
from .models import Documents, Address, User

# Register your models here.
admin.site.register(Documents)
admin.site.register(Address)
admin.site.register(User)
