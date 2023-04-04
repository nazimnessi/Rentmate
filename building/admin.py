from django.contrib import admin
from .models import Documents, building_photos, Building, Room
# Register your models here.


class BuildingAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'house_number', 'owner')
    list_filter = ('name', 'owner')
    search_fields = ['id', 'name', 'house_number']

    def api_name(self, obj):
        return obj.user.name


class RoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'room_no', 'building', 'renter')
    list_filter = ('criteria', 'room_type')
    search_fields = ['id', 'room_no', 'building', 'renter']

    def api_name(self, obj):
        return obj.user.room_no


admin.site.register(Documents)
admin.site.register(building_photos)
admin.site.register(Building, BuildingAdmin)
admin.site.register(Room, RoomAdmin)
