from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.


class Job_Types(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_date = models.DateTimeField("job type created date", auto_now_add=True)
    updated_date = models.DateTimeField("job type Updated date", auto_now=True)

    def __str__(self):
        return f"{self.name}"


class Job_List(models.Model):
    jobTypes = models.ForeignKey(
        Job_Types, on_delete=models.CASCADE, related_name="Job_type"
    )
    name = models.CharField(max_length=200)
    small_description = models.CharField(max_length=1000)
    characteristics = models.JSONField(max_length=100)
    questions = models.JSONField(blank=True, null=True)
    created_date = models.DateTimeField("job created date", auto_now_add=True)
    updated_date = models.DateTimeField("job Updated date", auto_now=True)

    def __str__(self):
        return f"{self.name}"


class Job_Application(models.Model):
    full_name = models.CharField(max_length=100, unique=False)
    Job_List = models.ForeignKey(
        Job_List,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="Job_list",
    )
    email = models.CharField(max_length=50, unique=True)
    phone_number = models.CharField(max_length=100, unique=True)
    linkedIn = models.CharField(max_length=255, blank=True, null=True, unique=True)
    github = models.CharField(max_length=255, blank=True, null=True, unique=True)
    website = models.CharField(max_length=255, blank=True, null=True, unique=True)
    total_experience = models.IntegerField()
    questions = models.JSONField(blank=True, null=True)
    resume = models.CharField(max_length=200)
    cover_letter = models.CharField(max_length=200, blank=True, null=True)
    photo = models.CharField(max_length=200, blank=True, null=True)
    created_date = models.DateTimeField("job created date", auto_now_add=True)
    updated_date = models.DateTimeField("job Updated date", auto_now=True)

    def __str__(self):
        return f"{self.full_name}"

    def clean(self):
        if (
            self.linkedIn
            and Job_Application.objects.exclude(id=self.id)
            .filter(linkedIn=self.linkedIn)
            .exists()
        ):
            raise ValidationError("LinkedIn URL must be unique.")

        if (
            self.github
            and Job_Application.objects.exclude(id=self.id)
            .filter(github=self.github)
            .exists()
        ):
            raise ValidationError("GitHub URL must be unique.")

        if (
            self.website
            and Job_Application.objects.exclude(id=self.id)
            .filter(website=self.website)
            .exists()
        ):
            raise ValidationError("Website URL must be unique.")
