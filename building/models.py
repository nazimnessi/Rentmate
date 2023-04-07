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
        ('A', 'Accepted'),
        ('P', 'Pending'),
        ('R', 'Rejected')
    )
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_requests')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recieved_requests')
    action = models.CharField(max_length=1, choices=action_choice, default='P')
    text = models.CharField(max_length=100, blank=True)
    created_date = models.DateTimeField('Request created date', auto_now_add=True)
    updated_date = models.DateTimeField('Request Updated date', auto_now=True)
    accepted = models.BooleanField(default=False)
    room = models.ForeignKey('Room', on_delete=models.CASCADE, related_name='sent_requests')

    def __str__(self):
        return str(self.id)


class building_photos(models.Model):
    name = models.CharField(max_length=100)
    file = models.FileField(
        upload_to='files/', validators=[FileExtensionValidator(['pdf', 'jpg', 'jpeg', 'png'])])

    def __str__(self):
        return self.name


class Building(models.Model):
    name = models.CharField(max_length=100)
    address = models.ForeignKey(
        Address, on_delete=models.CASCADE, null=True, blank=True)
    photo = models.ImageField(
        upload_to='images/', default='media/Default_user.png')
    house_number = models.CharField(max_length=20, unique=True)
    documents = models.ManyToManyField(Documents, blank=True)
    created_date = models.DateTimeField('Building created date', auto_now_add=True)
    updated_date = models.DateTimeField('Building Updated date', auto_now=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, default=None)

    def __str__(self):
        return self.name


class Room(models.Model):
    criteria_choice = (
        ('F', 'Fully Furnished'),
        ('S', 'Semi Furnished'),
        ('N', 'Not Furnished'),
    )
    room_choice = (
        ('3', '3BHK'),
        ('2', '2BHK'),
        ('1', '1BHK'),
        ('S', 'Studio'),
        ('H', 'House'),
        ('A', 'Appartment'),
        ('O', 'Others'),
    )
    room_no = models.CharField(max_length=10)
    criteria = models.CharField(
        max_length=1, choices=criteria_choice, default='F')
    appliences = models.CharField(max_length=100, blank=True)
    building = models.ForeignKey(
        Building, on_delete=models.CASCADE, default=None, related_name='rooms')
    renter = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, default=None)
    rent_amount = models.CharField(max_length=10)
    advance = models.CharField(max_length=10, null=True, blank=True)
    room_type = models.CharField(
        max_length=1, choices=room_choice, default='H')
    additional_photo = models.ManyToManyField(Documents, blank=True)
    rent_period_start = models.DateField('rent period start')
    rent_period_end = models.DateField('rent period end')
    created_date = models.DateTimeField('Room created date', auto_now_add=True)
    updated_date = models.DateTimeField('Room Updated date', auto_now=True)
    description = models.CharField(max_length=100, null=True, blank=True)
    area = models.CharField(max_length=100, null=True, blank=True)
    floor = models.CharField(max_length=100, null=True, blank=True)
    max_capacity = models.CharField(max_length=2, null=True, blank=True)
    bathroom_count = models.CharField(max_length=2, null=True, blank=True)
    kitchen_count = models.CharField(max_length=2, null=True, blank=True)
    is_parking_available = models.BooleanField(default=True)

    def clean(self):
        if self.renter == self.building.owner:
            raise ValidationError("Owner of the building cannot be the renter of a room.")

    def save(self, *args, **kwargs):
        if not self.room_no:
            self.room_no = self.building.House_No
        super().save(*args, **kwargs)

    def __str__(self):
        return self.room_no