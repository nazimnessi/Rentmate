from django.contrib import admin
from .models import Documents, building_photos, Address, Building, Room
# Register your models here.


class BuildingAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'House_No', 'owner')
    list_filter = ('name', 'owner')

    def api_name(self, obj):
        return obj.user.name


class RoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'room_no', 'building', 'renter')
    list_filter = ('criteria', 'room_type')

    def api_name(self, obj):
        return obj.user.room_no


admin.site.register(Documents)
admin.site.register(Address)
admin.site.register(building_photos)
admin.site.register(Building, BuildingAdmin)
admin.site.register(Room, RoomAdmin)
