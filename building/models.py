from django.db import models
from django.core.exceptions import ValidationError
from user.models import User, Address


class Request(models.Model):
    action_choice = (
        ('Accepted', 'Accepted'),
        ('Pending', 'Pending'),
        ('Rejected', 'Rejected')
    )
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_requests')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_requests')
    action = models.CharField(max_length=10, choices=action_choice, default='Pending')
    text = models.CharField(max_length=100, blank=True)
    created_date = models.DateTimeField('Request created date', auto_now_add=True)
    updated_date = models.DateTimeField('Request Updated date', auto_now=True)
    accepted = models.BooleanField(default=False)
    room = models.ForeignKey('Room', on_delete=models.CASCADE, related_name='sent_requests')

    def __str__(self):
        return str(self.id)


class Building(models.Model):
    building_choice = (
        ('House', 'House'),
        ('Apartments', 'Apartments'),
        ('Others', 'Others'),
    )
    name = models.CharField(max_length=100)
    address = models.ForeignKey(
        Address, on_delete=models.CASCADE, null=True, blank=True)
    building_type = models.CharField(
        max_length=10, choices=building_choice, default='House', db_column='building_type')
    house_number = models.CharField(max_length=20, unique=True)
    created_date = models.DateTimeField('Building created date', auto_now_add=True)
    updated_date = models.DateTimeField('Building Updated date', auto_now=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, default=None, related_name='building')
    building_photo_url = models.URLField(max_length=300, blank=True, null=True)
    building_document_url = models.JSONField(blank=True, null=True)

    def __str__(self):
        return self.name


class Room(models.Model):
    criteria_choice = (
        ('Fully Furnished', 'Fully Furnished'),
        ('Semi Furnished', 'Semi Furnished'),
        ('Not Furnished', 'Not Furnished'),
    )
    room_choice = (
        ('3BHK', '3BHK'),
        ('2BHK', '2BHK'),
        ('1BHK', '1BHK'),
        ('business', 'business'),
        ('Studio', 'Studio'),
        ('Others', 'Others'),
    )

    def default_amenities():
        return {"parking": True, "pet_friendly": True, "swimming_pool": False}

    room_no = models.CharField(max_length=100)
    criteria = models.CharField(
        max_length=15, choices=criteria_choice, default='Fully Furnished')
    amenities = models.JSONField(default=default_amenities)
    building = models.ForeignKey(
        Building, on_delete=models.CASCADE, default=None, related_name='rooms')
    renter = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, default=None, related_name='renter')
    rent_amount = models.CharField(max_length=10)
    advance = models.CharField(max_length=10, null=True, blank=True)
    room_type = models.CharField(
        max_length=10, choices=room_choice, default='Studio', db_column='room_type')
    rent_period_start = models.DateField('rent period start', help_text=("Rent period contract start date"), null=True, blank=True)
    rent_period_end = models.DateField('rent period end', help_text=("Rent period contract end date"), null=True, blank=True)
    rent_payment_date = models.DateField('rent payment date', blank=True, null=True, help_text=("Date from which the payment of a month start"))
    rent_payment_interval = models.IntegerField(blank=True, null=True, help_text=("No of days a renter can have before the payment is due"))
    created_date = models.DateTimeField('Room created date', auto_now_add=True)
    updated_date = models.DateTimeField('Room Updated date', auto_now=True)
    description = models.CharField(max_length=100, null=True, blank=True)
    area_in_square_feet = models.CharField(max_length=100, null=True, blank=True)
    floor = models.CharField(max_length=100, null=True, blank=True, help_text="Value will be no.of floors if building type is house else room is in which floor.")
    bedroom_count = models.IntegerField(null=True, blank=True)
    bathroom_count = models.IntegerField(null=True, blank=True)
    garage_count = models.IntegerField(null=True, blank=True)
    room_photo_url = models.URLField(max_length=300, blank=True, null=True)
    room_document_url = models.JSONField(blank=True, null=True)

    def clean(self):
        if self.renter == self.building.owner:
            raise ValidationError("Owner of the building cannot be the renter of a room.")

    def save(self, *args, **kwargs):
        if not self.room_no:
            self.room_no = self.building.House_No
        super().save(*args, **kwargs)

    def __str__(self):
        return self.room_no


class Utility(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=350, null=True, blank=True)
    latest_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    unit = models.CharField(max_length=50, blank=True, null=True)
    enabled = models.BooleanField(default=True)
    meter_reading = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    bill_image_url = models.URLField(max_length=300, blank=True, null=True)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.name


class Lease(models.Model):
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, blank=True, null=True)
    status = models.BooleanField(default=True)
    documents = models.JSONField(blank=True, null=True)
    rent_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    advance = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    rent_period_start = models.DateField('rent period start', help_text=("Rent period contract start date"), null=True, blank=True)
    rent_period_end = models.DateField('rent period end', help_text=("Rent period contract end date"), null=True, blank=True)
    rent_payment_date = models.DateField('rent payment date', blank=True, null=True, help_text=("Date from which the payment of a month start"))
    rent_payment_interval = models.IntegerField(blank=True, null=True, help_text=("No of days a renter can have before the payment is due"))
