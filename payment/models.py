from django.db import models
from user.models import User
from building.models import Room, Utility
from django.core.exceptions import ValidationError


class Payment(models.Model):
    PAYMENT_STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
        ('Unpaid', 'Unpaid'),
    )
    payer = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="payments_done")
    payee = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="payments_received")
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="payments")
    utility = models.ForeignKey(Utility, on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, null=True, blank=True)
    transaction_id = models.CharField(max_length=80, null=True, blank=True)
    note = models.TextField(max_length=350, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    no_of_days_before_due = models.IntegerField(blank=True, null=True, help_text=("No of days a renter can have before the payment is due"))
    created_date = models.DateTimeField('Payment date', auto_now_add=True)

    def __str__(self):
        return str(f"{self.id}:{self.amount}:{self.room.room_no}:{self.utility.name}" if self.utility else f"{self.id}:{self.amount}:{self.room.room_no}")

    def clean(self):
        if self.payer == self.payee:
            raise ValidationError("Payer cannot be same as payee.")
