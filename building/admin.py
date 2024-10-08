from django.contrib import admin
from .models import Building, Room, Request, Utility, Lease

# Register your models here.


class RequestAdmin(admin.ModelAdmin):
    list_display = ("id", "sender", "receiver", "action", "text", "accepted", "room")
    search_fields = ["id", "sender", "receiver", "text", "room"]
    list_filter = ("action", "accepted")


class BuildingAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "house_number", "owner")
    list_filter = ("name", "owner")
    search_fields = ["id", "name", "house_number"]

    def api_name(self, obj):
        return obj.user.name


class RoomAdmin(admin.ModelAdmin):
    list_display = ("id", "room_no", "building", "renter")
    list_filter = ("criteria", "room_type")
    search_fields = ["id", "room_no", "building__name", "renter__username"]

    def api_name(self, obj):
        return obj.user.room_no


class UtilityAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "room")
    search_fields = ["name", "room__room_no"]


class LeaseAdmin(admin.ModelAdmin):
    list_display = ("id", "room", "status", "rent_amount", "advance")
    list_filter = ("status",)


admin.site.register(Building, BuildingAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(Utility, UtilityAdmin)
admin.site.register(Request, RequestAdmin)
admin.site.register(Lease, LeaseAdmin)
