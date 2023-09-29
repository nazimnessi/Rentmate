from django.db import models
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from user.models import User, Address

# Create your models here.


class Documents(models.Model):
    name = models.CharField(max_length=100)
    file = models.FileField(
        upload_to='files/', validators=[FileExtensionValidator(['pdf', 'jpg', 'jpeg', 'png'])])

    def __str__(self):
        return self.name


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
        ('Apartment', 'Apartment'),
        ('Others', 'Others'),
    )
    name = models.CharField(max_length=100)
    address = models.ForeignKey(
        Address, on_delete=models.CASCADE, null=True, blank=True)
    photo = models.ImageField(
        upload_to='images/', default='Default_user.png')
    building_type = models.CharField(
        max_length=10, choices=building_choice, default='House', db_column='building_type')
    house_number = models.CharField(max_length=20, unique=True)
    documents = models.ManyToManyField(Documents, blank=True)
    created_date = models.DateTimeField('Building created date', auto_now_add=True)
    updated_date = models.DateTimeField('Building Updated date', auto_now=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, default=None, related_name='building')
    building_photo_url = models.CharField(max_length=500, blank=True, null=True)
    building_document_Url = models.JSONField(blank=True, null=True)

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
        ('Studio', 'Studio'),
        ('Others', 'Others'),
    )
    room_no = models.CharField(max_length=100)
    criteria = models.CharField(
        max_length=15, choices=criteria_choice, default='Fully Furnished')
    appliances = models.CharField(max_length=100, blank=True)
    building = models.ForeignKey(
        Building, on_delete=models.CASCADE, default=None, related_name='rooms')
    renter = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, default=None, related_name='renter')
    rent_amount = models.CharField(max_length=10)
    advance = models.CharField(max_length=10, null=True, blank=True)
    room_type = models.CharField(
        max_length=10, choices=room_choice, default='Studio', db_column='room_type')
    additional_photo = models.ManyToManyField(Documents, blank=True)
    rent_period_start = models.DateField('rent period start', help_text=("Rent period contract start date"))
    rent_period_end = models.DateField('rent period end', help_text=("Rent period contract end date"))
    rent_payment_date = models.DateField('rent payment date', blank=True, null=True, help_text=("Date from which the payment of a month start"))
    rent_payment_interval = models.IntegerField(max_length=31, blank=True, null=True, help_text=("No of days a renter can have before the payment is due"))
    created_date = models.DateTimeField('Room created date', auto_now_add=True)
    updated_date = models.DateTimeField('Room Updated date', auto_now=True)
    description = models.CharField(max_length=100, null=True, blank=True)
    area = models.CharField(max_length=100, null=True, blank=True)
    floor = models.CharField(max_length=100, null=True, blank=True)
    max_capacity = models.CharField(max_length=2, null=True, blank=True)
    bathroom_count = models.CharField(max_length=3, null=True, blank=True)
    kitchen_count = models.CharField(max_length=3, null=True, blank=True)
    is_parking_available = models.BooleanField(default=True)
    garage_count = models.CharField(max_length=3, null=True, blank=True)
    room_photo_Url = models.CharField(max_length=900, blank=True, null=True)
    room_document_Url = models.JSONField(blank=True, null=True)

    def clean(self):
        if self.renter == self.building.owner:
            raise ValidationError("Owner of the building cannot be the renter of a room.")

    def save(self, *args, **kwargs):
        if not self.room_no:
            self.room_no = self.building.House_No
        super().save(*args, **kwargs)

    def __str__(self):
        return self.room_no
