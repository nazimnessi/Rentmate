from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.


class Job_List(models.Model):
    JOB_TYPES = (
        ('Management', 'Management'),
        ('Sales', 'Sales'),
        ('Developer', 'Developer'),
        ('Marketing', 'Marketing'),
    )
    job_type = models.CharField(max_length=100, choices=JOB_TYPES, default='Developer')
    name = models.CharField(max_length=200)
    small_description = models.CharField(max_length=1000)
    characteristics = models.JSONField(max_length=100)
    created_date = models.DateTimeField('job created date', auto_now_add=True)
    updated_date = models.DateTimeField('job Updated date', auto_now=True)

    def __str__(self):
        return f'{self.name}'


class Job_Application(models.Model):
    full_name = models.CharField(max_length=100, unique=True)
    Job_List = models.ForeignKey(Job_List, on_delete=models.SET_NULL, blank=True, null=True, related_name='Job_list')
    email = models.CharField(max_length=50, unique=True)
    phone_number = models.CharField(max_length=100, unique=True)
    linkedIn = models.CharField(max_length=300, blank=True, null=True, unique=True)
    github = models.CharField(max_length=300, blank=True, null=True, unique=True)
    website = models.CharField(max_length=300, blank=True, null=True, unique=True)
    total_experience = models.IntegerField()
    question1 = models.TextField(max_length=1000, help_text="How did you hear about this position?:")
    question2 = models.TextField(max_length=1000, help_text="Why are you interested in joining the Rentmate team?:")
    question3 = models.TextField(max_length=1000, blank=True, null=True, help_text="ny additional information you'd like to share:")
    resume = models.CharField(max_length=200)
    cover_letter = models.CharField(max_length=200, blank=True, null=True)
    created_date = models.DateTimeField('job created date', auto_now_add=True)
    updated_date = models.DateTimeField('job Updated date', auto_now=True)

    def __str__(self):
        return f'{self.full_name}'

    def clean(self):
        if self.linkedIn and Job_Application.objects.exclude(id=self.id).filter(linkedIn=self.linkedIn).exists():
            raise ValidationError('LinkedIn URL must be unique.')

        if self.github and Job_Application.objects.exclude(id=self.id).filter(github=self.github).exists():
            raise ValidationError('GitHub URL must be unique.')

        if self.website and Job_Application.objects.exclude(id=self.id).filter(website=self.website).exists():
            raise ValidationError('Website URL must be unique.')
