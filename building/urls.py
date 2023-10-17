from django.urls import path
from .views import PropertyAPI

urlpatterns = [
    path('property-download/', PropertyAPI.as_view({"get": "download"}), name='property-download'),
]
