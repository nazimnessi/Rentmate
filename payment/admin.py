from django.contrib import admin
from .models import Payment


class PaymentAdmin(admin.ModelAdmin):
    list_display = ("__str__", "payee", "payer", "room", "status", "transaction_id")
    search_fields = ["transaction_id"]
    list_filter = ("status",)


admin.site.register(Payment, PaymentAdmin)
