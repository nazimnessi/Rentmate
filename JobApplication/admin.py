from django.contrib import admin
from JobApplication.models import Job_List, Job_Application, Job_Types

# Register your models here.


class Job_ListAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "jobTypes")
    search_fields = ["id", "name"]
    list_filter = ("jobTypes",)


class Job_ApplicationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "full_name",
        "Job_List",
        "email",
        "total_experience",
        "phone_number",
    )
    search_fields = (
        "id",
        "full_name",
        "Job_List",
        "email",
        "total_experience",
        "phone_number",
    )


admin.site.register(Job_List, Job_ListAdmin)
admin.site.register(Job_Types)
admin.site.register(Job_Application, Job_ApplicationAdmin)
