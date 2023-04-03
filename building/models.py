from django.db import models
from django.core.validators import FileExtensionValidator
from user.models import User

# Create your models here.


class Documents(models.Model):
    name = models.CharField(max_length=100)
    file = models.FileField(
        upload_to='files/', validators=[FileExtensionValidator(['pdf', 'jpg', 'jpeg', 'png'])])

    def __str__(self):
        return self.name


class building_photos(models.Model):
    name = models.CharField(max_length=100)
    file = models.FileField(
        upload_to='files/', validators=[FileExtensionValidator(['pdf', 'jpg', 'jpeg', 'png'])])

    def __str__(self):
        return self.name


class Address(models.Model):
    address1 = models.CharField(max_length=100)
    address2 = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.address1}, {self.address2}, {self.city}, {self.state} {self.postal_code}'


class Building(models.Model):
    name = models.CharField(max_length=100)
    address = models.ForeignKey(
        Address, on_delete=models.CASCADE, null=True, blank=True)
    photo = models.ImageField(
        upload_to='images/', default='media/Default_user.png')
    House_No = models.CharField(max_length=20, unique=True)
    documents = models.ManyToManyField(Documents, blank=True)
    created_date = models.DateTimeField('User created date', auto_now_add=True)
    updated_date = models.DateTimeField('User Updated date', auto_now=True)
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
    appliences = models.CharField(max_length=100)
    building = models.ForeignKey(
        Building, on_delete=models.CASCADE, default=None, related_name='rooms')
    renter = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, default=None)
    rent_amount = models.CharField(max_length=10)
    advance = models.CharField(max_length=10)
    room_type = models.CharField(
        max_length=1, choices=room_choice, default='H')
    additional_photo = models.ManyToManyField(Documents, blank=True)
    rent_period_start = models.DateField()
    rent_period_end = models.DateField()
    description = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    floor = models.CharField(max_length=100)
    max_capacity = models.CharField(max_length=2)
    bathroom_count = models.CharField(max_length=2)
    kitchen_count = models.CharField(max_length=2)
    is_parking_available = models.CharField(max_length=2)

    def save(self, *args, **kwargs):
        if not self.room_no:
            self.room_no = self.building.House_No
        super().save(*args, **kwargs)

    def __str__(self):
        return self.room_no
