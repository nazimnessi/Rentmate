import phonenumbers
from django.db import models
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError

# Create your models here.


class Documents(models.Model):
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


class User(models.Model):
    Role_choice = (
        ('T', 'Tenant'),
        ('O', 'Owner'),
    )
    name = models.CharField(max_length=100)
    address = models.ForeignKey(
        Address, on_delete=models.CASCADE, null=True, blank=True)
    photo = models.ImageField(
        upload_to='images/', default='media/Default_user.png')
    phone_number = models.CharField(max_length=20, unique=True)
    alt_phone_number = models.CharField(max_length=20, blank=True)
    email = models.EmailField(unique=True)
    documents = models.ManyToManyField(Documents, blank=True)
    aadhar = models.CharField(max_length=12, unique=True)
    is_active = models.BooleanField(default=True)
    role = models.CharField(max_length=1, choices=Role_choice, default='O')
    created_date = models.DateTimeField('User created date', auto_now_add=True)
    updated_date = models.DateTimeField('User Updated date', auto_now=True)

    def clean(self):
        try:
            phone_number = phonenumbers.parse(
                self.phone_number, self.get_country_code())
            if not phonenumbers.is_valid_number(phone_number):
                raise ValidationError('Invalid phone number.')
        except phonenumbers.NumberParseException:
            raise ValidationError('Invalid phone number.')

    def get_country_code(self):
        if self.phone_number:
            phone_number = phonenumbers.parse(self.phone_number, None)
            if phone_number.country_code:
                return str(phone_number.country_code)
        return None

    def __str__(self):
        return self.name
